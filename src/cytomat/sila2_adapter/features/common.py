from pathlib import Path
from types import TracebackType

from sila2.framework import DefinedExecutionError, Feature
from sila2.server import FeatureImplementationBase, SilaServer
from typing_extensions import Self

from cytomat import Cytomat
from cytomat.command_execution import CommandExecutionContext


def load_feature_xml(module_file: str, filename: str) -> Feature:
    return Feature(str(Path(module_file).resolve().with_name(filename)))


class ErrorMapper:
    def __init__(
        self, *, feature: Feature, fallback_identifier: str = "CytomatError"
    ) -> None:
        self._feature = feature
        self._fallback_identifier = fallback_identifier

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> bool:
        del exc_type, tb
        if exc is None:
            return False
        raise DefinedExecutionError(
            self._feature.defined_execution_errors[self._fallback_identifier],
            str(exc),
        ) from exc


class CytomatFeatureBase(FeatureImplementationBase):
    def __init__(
        self, parent_server: SilaServer, cytomat: Cytomat, *, feature: Feature
    ) -> None:
        super().__init__(parent_server)
        self._cytomat: Cytomat = cytomat
        self._cmd_context = CommandExecutionContext(cytomat=self._cytomat)
        self._error_mapper = ErrorMapper(feature=feature)
