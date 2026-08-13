import logging
from types import TracebackType

from typing_extensions import Self

from cytomat.cytomat import Cytomat
from cytomat.status import OverviewStatus, Status

logger = logging.getLogger(__name__)


class CommandExecutionContext:
    def __init__(
        self,
        *,
        cytomat: Cytomat,
        operation: str,
        timeout: float = 60.0,
        poll_interval: float = 0.5,
    ) -> None:
        self._cytomat = cytomat
        self._operation = operation
        self._timeout = timeout
        self._poll_interval = poll_interval

    @staticmethod
    def _format_action(status: Status) -> str:
        return f"{status.action.type.name}@{status.action.target.name}"

    @staticmethod
    def _overview_active(status: OverviewStatus) -> str:
        active = []
        for key, value in status.model_dump(mode="python").items():
            if value:
                active.append(f"{key}={value}")
        return ", ".join(active)

    @staticmethod
    def _overview_diff(previous: OverviewStatus, current: OverviewStatus) -> dict[str, bool]:
        previous_values = previous.model_dump(mode="python")
        current_values = current.model_dump(mode="python")

        diff: dict[str, bool] = {}
        for key, value in current_values.items():
            if previous_values[key] != value:
                diff[key] = value
        return diff

    @staticmethod
    def _format_diff(diff: dict[str, bool]) -> str:
        if not diff:
            return ""
        return ", ".join(f"{key}={value}" for key, value in diff.items())

    def _log_changed(self, previous: Status, current: Status) -> None:
        action_changed = previous.action != current.action
        error_changed = previous.error != current.error
        overview_diff = self._overview_diff(previous.overview, current.overview)

        if not action_changed and not error_changed and not overview_diff:
            return

        action_text = self._format_action(current) if action_changed else ""
        overview_text = self._format_diff(overview_diff)
        error_text = current.error.name if error_changed else ""

        if error_text:
            logger.debug(
                "[%s] Changed: action=%s, overview=%s, error=%s",
                self._operation,
                action_text,
                overview_text,
                error_text,
            )
            return

        logger.debug("[%s] Changed: action=%s, overview=%s", self._operation, action_text, overview_text)

    def __enter__(self) -> Self:
        logger.debug("[%s] begin command execution", self._operation)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> bool:
        del exc_type, tb
        if exc is not None:
            logger.debug("[%s] command raised before wait: %s", self._operation, exc)
            return False

        iterator = self._cytomat.iter_overview_status_until_not_busy(
            timeout=self._timeout, poll_interval=self._poll_interval
        )

        current = next(iterator)

        if current.overview.command_in_process:
            logger.debug(
                "[%s] Waiting: action=%s, overview=%s",
                self._operation,
                self._format_action(current),
                self._overview_active(current.overview),
            )

        while True:
            try:
                new_status = next(iterator)
            except StopIteration as stop:
                final = stop.value
                logger.debug(
                    "[%s] Finished: action=%s, overview=%s",
                    self._operation,
                    self._format_action(final),
                    self._overview_active(final.overview),
                )
                return False

            self._log_changed(current, new_status)
            current = new_status
