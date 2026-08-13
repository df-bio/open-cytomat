import logging
from types import TracebackType
from typing import Any

from typing_extensions import Literal, Self

from cytomat.cytomat import Cytomat
from cytomat.status import OverviewStatus, PlateShuttleSystemStatus, Status

logger = logging.getLogger(__name__)


class CommandExecutionContext:
    def __init__(
        self,
        *,
        cytomat: Cytomat,
        scope: str = "",
        timeout: float = 60.0,
        poll_interval: float = 0.5,
    ) -> None:
        self._cytomat = cytomat
        self.scope = scope
        self._timeout = timeout
        self._poll_interval = poll_interval
        self._operation = ""
        self._last_status: Status | None = None

    def __call__(self, operation: str) -> Self:
        self._operation = operation
        return self

    @property
    def final_status(self) -> Status:
        if self._last_status is None:
            raise RuntimeError(
                f"{self._log_prefix()} no final status available; "
                "command context did not finish yet"
            )
        return self._last_status

    @property
    def final_status_payload(self) -> dict[str, Any]:
        return self.final_status.model_dump(mode="json", by_alias=True)

    def log_action_status(self, status: PlateShuttleSystemStatus) -> None:
        logger.debug(
            f"{self._log_prefix()} Immediate: {self._format_plate_shuttle(status)}"
        )

    def _log_prefix(self) -> str:
        if self.scope:
            return f"[{self.scope}:{self._operation}]"
        return f"[{self._operation}]"

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
    def _format_plate_shuttle(status: PlateShuttleSystemStatus) -> str:
        active = []
        for key, value in status.model_dump(mode="python").items():
            if value:
                active.append(f"{key}={value}")
        return ", ".join(active)

    @staticmethod
    def _overview_diff(
        previous: OverviewStatus, current: OverviewStatus
    ) -> dict[str, bool]:
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

        changes: list[str] = []
        if action_changed:
            changes.append(f"action={self._format_action(current)}")
        if overview_diff:
            changes.append(f"overview={self._format_diff(overview_diff)}")
        if error_changed:
            changes.append(f"error={current.error.name}")

        logger.debug(f"{self._log_prefix()} Changed: {', '.join(changes)}")

    def __enter__(self) -> Self:
        if not self._operation:
            raise RuntimeError(
                "Operation must be set before entering command execution context"
            )

        self._last_status = None
        logger.debug(f"{self._log_prefix()} begin command execution")
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> Literal[False]:
        del exc_type, tb
        if exc is not None:
            logger.debug(f"{self._log_prefix()} command raised before wait: {exc}")
            return False

        iterator = self._cytomat.iter_overview_status_until_not_busy(
            timeout=self._timeout, poll_interval=self._poll_interval
        )

        current = next(iterator)

        if current.overview.command_in_process:
            logger.debug(
                f"{self._log_prefix()} Waiting: action={self._format_action(current)}, "
                f"overview={self._overview_active(current.overview)}"
            )

        while True:
            try:
                new_status = next(iterator)
            except StopIteration as stop:
                self._last_status = stop.value
                logger.debug(
                    f"{self._log_prefix()} Finished: "
                    f"action={self._format_action(stop.value)}, "
                    f"overview={self._overview_active(stop.value.overview)}"
                )
                return False

            self._log_changed(current, new_status)
            current = new_status
