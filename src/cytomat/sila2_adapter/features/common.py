from pathlib import Path
from types import TracebackType
from typing import Any

from sila2.framework import DefinedExecutionError, Feature
from sila2.server import FeatureImplementationBase, SilaServer

from cytomat import Cytomat


def load_feature_xml(module_file: str, filename: str) -> Feature:
    return Feature(str(Path(module_file).resolve().with_name(filename)))


def status_payload(status: Any) -> dict[str, bool]:
    return {
        "TransferStationOccupied": bool(status.transfer_station_occupied),
        "DeviceDoorOpen": bool(status.device_door_open),
        "TransferDoorOpen": bool(status.transfer_door_open),
        "ShovelOccupied": bool(status.shovel_occupied),
        "Error": bool(status.error),
        "Warning": bool(status.warning),
        "Ready": bool(status.ready),
        "Busy": bool(status.busy),
    }


class ErrorMapper:
    def __init__(self, *, feature: Feature, fallback_identifier: str = "CytomatError") -> None:
        self._feature = feature
        self._fallback_identifier = fallback_identifier

    def __enter__(self) -> "ErrorMapper":
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
    def __init__(self, parent_server: SilaServer, cytomat: Cytomat, *, feature: Feature) -> None:
        super().__init__(parent_server)
        self._cytomat: Cytomat = cytomat
        self._error_mapper = ErrorMapper(feature=feature)
