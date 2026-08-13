from collections.abc import Callable
from typing import Any

from sila2.server import MetadataDict, SilaServer

from cytomat import Cytomat
from cytomat.sila2_adapter.features.common import CytomatFeatureBase, load_feature_xml
from cytomat.status import PlateShuttleSystemStatus

PLATE_HANDLER_FEATURE = load_feature_xml(__file__, "plate_handler.sila.xml")


class PlateHandlerFeature(CytomatFeatureBase):
    def __init__(self, parent_server: SilaServer, cytomat: Cytomat) -> None:
        super().__init__(parent_server, cytomat, feature=PLATE_HANDLER_FEATURE)
        self._cmd_context.scope = "PlateHandler"

    def _run_operation(
        self, fn_name: str, operation: Callable[[], PlateShuttleSystemStatus]
    ) -> dict[str, Any]:
        with self._error_mapper, self._cmd_context(fn_name):
            immediate_status = operation()
            self._cmd_context.log_action_status(immediate_status)
        return self._cmd_context.final_status_payload

    def Initialize(self, *, metadata: MetadataDict):
        _ = metadata
        return self._run_operation("Initialize", self._cytomat.plate_handler.initialize)

    def MovePlateFromTransferStationToSlot(
        self,
        Slot: int,
        *,
        metadata: MetadataDict,
    ):
        _ = metadata
        return self._run_operation(
            "MovePlateFromTransferStationToSlot",
            lambda: (
                self._cytomat.plate_handler.move_plate_from_transfer_station_to_slot(
                    Slot
                )
            ),
        )

    def MovePlateFromSlotToTransferStation(
        self,
        Slot: int,
        *,
        metadata: MetadataDict,
    ):
        _ = metadata
        return self._run_operation(
            "MovePlateFromSlotToTransferStation",
            lambda: (
                self._cytomat.plate_handler.move_plate_from_slot_to_transfer_station(
                    Slot
                )
            ),
        )

    def ExecuteLowLevel(self, Command: str, *, metadata: MetadataDict):
        _ = metadata
        return self._run_operation(
            "ExecuteLowLevel",
            lambda: self._cytomat.plate_handler.execute_low_level(Command),
        )

    def MovePlateFromTransferStationToHandler(self, *, metadata: MetadataDict):
        _ = metadata
        return self._run_operation(
            "MovePlateFromTransferStationToHandler",
            self._cytomat.plate_handler.move_plate_from_transfer_station_to_handler,
        )

    def MovePlateFromHandlerToTransferStation(self, *, metadata: MetadataDict):
        _ = metadata
        return self._run_operation(
            "MovePlateFromHandlerToTransferStation",
            self._cytomat.plate_handler.move_plate_from_handler_to_transfer_station,
        )

    def MovePlateFromExposedPositionToInside(self, *, metadata: MetadataDict):
        _ = metadata
        return self._run_operation(
            "MovePlateFromExposedPositionToInside",
            self._cytomat.plate_handler.move_plate_from_exposed_position_to_inside,
        )

    def MovePlateFromInsideToExposedPosition(self, *, metadata: MetadataDict):
        _ = metadata
        return self._run_operation(
            "MovePlateFromInsideToExposedPosition",
            self._cytomat.plate_handler.move_plate_from_inside_to_exposed_position,
        )

    def MovePlateFromHandlerToSlot(self, Slot: int, *, metadata: MetadataDict):
        _ = metadata
        return self._run_operation(
            "MovePlateFromHandlerToSlot",
            lambda: self._cytomat.plate_handler.move_plate_from_handler_to_slot(Slot),
        )

    def MovePlateFromSlotToHandler(self, Slot: int, *, metadata: MetadataDict):
        _ = metadata
        return self._run_operation(
            "MovePlateFromSlotToHandler",
            lambda: self._cytomat.plate_handler.move_plate_from_slot_to_handler(Slot),
        )

    def MovePlateFromExposedPositionToSlot(
        self,
        Slot: int,
        *,
        metadata: MetadataDict,
    ):
        _ = metadata
        return self._run_operation(
            "MovePlateFromExposedPositionToSlot",
            lambda: (
                self._cytomat.plate_handler.move_plate_from_exposed_position_to_slot(
                    Slot
                )
            ),
        )

    def MovePlateFromSlotToExposedPosition(
        self,
        Slot: int,
        *,
        metadata: MetadataDict,
    ):
        _ = metadata
        return self._run_operation(
            "MovePlateFromSlotToExposedPosition",
            lambda: (
                self._cytomat.plate_handler.move_plate_from_slot_to_exposed_position(
                    Slot
                )
            ),
        )

    def RetractShovel(self, *, metadata: MetadataDict):
        _ = metadata
        return self._run_operation(
            "RetractShovel", self._cytomat.plate_handler.retract_shovel
        )

    def ExtendShovel(self, *, metadata: MetadataDict):
        _ = metadata
        return self._run_operation(
            "ExtendShovel", self._cytomat.plate_handler.extend_shovel
        )

    def CloseTransferDoor(self, *, metadata: MetadataDict):
        _ = metadata
        return self._run_operation(
            "CloseTransferDoor", self._cytomat.plate_handler.close_transfer_door
        )

    def OpenTransferDoor(self, *, metadata: MetadataDict):
        _ = metadata
        return self._run_operation(
            "OpenTransferDoor", self._cytomat.plate_handler.open_transfer_door
        )

    def ResetHandlerPosition(self, *, metadata: MetadataDict):
        _ = metadata
        return self._run_operation(
            "ResetHandlerPosition", self._cytomat.plate_handler.reset_handler_position
        )
