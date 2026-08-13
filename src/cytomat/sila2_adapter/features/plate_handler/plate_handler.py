from sila2.server import MetadataDict, SilaServer

from cytomat import Cytomat
from cytomat.sila2_adapter.features.common import CytomatFeatureBase, load_feature_xml

PLATE_HANDLER_FEATURE = load_feature_xml(__file__, "plate_handler.sila.xml")


class PlateHandlerFeature(CytomatFeatureBase):
    def __init__(self, parent_server: SilaServer, cytomat: Cytomat) -> None:
        super().__init__(parent_server, cytomat, feature=PLATE_HANDLER_FEATURE)

    def Initialize(self, *, metadata: MetadataDict):
        _ = metadata
        fn_name = "Initialize"
        with self._error_mapper, self._command_execution(fn_name):
            return self._cytomat.plate_handler.initialize().model_dump(mode="python", by_alias=True)

    def MovePlateFromTransferStationToSlot(self, Slot: int, *, metadata: MetadataDict):
        _ = metadata
        fn_name = "MovePlateFromTransferStationToSlot"
        with self._error_mapper, self._command_execution(fn_name):
            return self._cytomat.plate_handler.move_plate_from_transfer_station_to_slot(Slot).model_dump(
                mode="python", by_alias=True
            )

    def MovePlateFromSlotToTransferStation(self, Slot: int, *, metadata: MetadataDict):
        _ = metadata
        fn_name = "MovePlateFromSlotToTransferStation"
        with self._error_mapper, self._command_execution(fn_name):
            return self._cytomat.plate_handler.move_plate_from_slot_to_transfer_station(Slot).model_dump(
                mode="python", by_alias=True
            )

    def ExecuteLowLevel(self, Command: str, *, metadata: MetadataDict):
        _ = metadata
        fn_name = "ExecuteLowLevel"
        with self._error_mapper, self._command_execution(fn_name):
            return self._cytomat.plate_handler.execute_low_level(Command).model_dump(mode="python", by_alias=True)

    def MovePlateFromTransferStationToHandler(self, *, metadata: MetadataDict):
        _ = metadata
        fn_name = "MovePlateFromTransferStationToHandler"
        with self._error_mapper, self._command_execution(fn_name):
            return self._cytomat.plate_handler.move_plate_from_transfer_station_to_handler().model_dump(
                mode="python", by_alias=True
            )

    def MovePlateFromHandlerToTransferStation(self, *, metadata: MetadataDict):
        _ = metadata
        fn_name = "MovePlateFromHandlerToTransferStation"
        with self._error_mapper, self._command_execution(fn_name):
            return self._cytomat.plate_handler.move_plate_from_handler_to_transfer_station().model_dump(
                mode="python", by_alias=True
            )

    def MovePlateFromExposedPositionToInside(self, *, metadata: MetadataDict):
        _ = metadata
        fn_name = "MovePlateFromExposedPositionToInside"
        with self._error_mapper, self._command_execution(fn_name):
            return self._cytomat.plate_handler.move_plate_from_exposed_position_to_inside().model_dump(
                mode="python", by_alias=True
            )

    def MovePlateFromInsideToExposedPosition(self, *, metadata: MetadataDict):
        _ = metadata
        fn_name = "MovePlateFromInsideToExposedPosition"
        with self._error_mapper, self._command_execution(fn_name):
            return self._cytomat.plate_handler.move_plate_from_inside_to_exposed_position().model_dump(
                mode="python", by_alias=True
            )

    def MovePlateFromHandlerToSlot(self, Slot: int, *, metadata: MetadataDict):
        _ = metadata
        fn_name = "MovePlateFromHandlerToSlot"
        with self._error_mapper, self._command_execution(fn_name):
            return self._cytomat.plate_handler.move_plate_from_handler_to_slot(Slot).model_dump(
                mode="python", by_alias=True
            )

    def MovePlateFromSlotToHandler(self, Slot: int, *, metadata: MetadataDict):
        _ = metadata
        fn_name = "MovePlateFromSlotToHandler"
        with self._error_mapper, self._command_execution(fn_name):
            return self._cytomat.plate_handler.move_plate_from_slot_to_handler(Slot).model_dump(
                mode="python", by_alias=True
            )

    def MovePlateFromExposedPositionToSlot(self, Slot: int, *, metadata: MetadataDict):
        _ = metadata
        fn_name = "MovePlateFromExposedPositionToSlot"
        with self._error_mapper, self._command_execution(fn_name):
            return self._cytomat.plate_handler.move_plate_from_exposed_position_to_slot(Slot).model_dump(
                mode="python", by_alias=True
            )

    def MovePlateFromSlotToExposedPosition(self, Slot: int, *, metadata: MetadataDict):
        _ = metadata
        fn_name = "MovePlateFromSlotToExposedPosition"
        with self._error_mapper, self._command_execution(fn_name):
            return self._cytomat.plate_handler.move_plate_from_slot_to_exposed_position(Slot).model_dump(
                mode="python", by_alias=True
            )

    def RetractShovel(self, *, metadata: MetadataDict):
        _ = metadata
        fn_name = "RetractShovel"
        with self._error_mapper, self._command_execution(fn_name):
            return self._cytomat.plate_handler.retract_shovel().model_dump(mode="python", by_alias=True)

    def ExtendShovel(self, *, metadata: MetadataDict):
        _ = metadata
        fn_name = "ExtendShovel"
        with self._error_mapper, self._command_execution(fn_name):
            return self._cytomat.plate_handler.extend_shovel().model_dump(mode="python", by_alias=True)

    def CloseTransferDoor(self, *, metadata: MetadataDict):
        _ = metadata
        fn_name = "CloseTransferDoor"
        with self._error_mapper, self._command_execution(fn_name):
            return self._cytomat.plate_handler.close_transfer_door().model_dump(mode="python", by_alias=True)

    def OpenTransferDoor(self, *, metadata: MetadataDict):
        _ = metadata
        fn_name = "OpenTransferDoor"
        with self._error_mapper, self._command_execution(fn_name):
            return self._cytomat.plate_handler.open_transfer_door().model_dump(mode="python", by_alias=True)

    def ResetHandlerPosition(self, *, metadata: MetadataDict):
        _ = metadata
        fn_name = "ResetHandlerPosition"
        with self._error_mapper, self._command_execution(fn_name):
            return self._cytomat.plate_handler.reset_handler_position().model_dump(mode="python", by_alias=True)
