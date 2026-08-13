from __future__ import annotations

from enum import IntEnum

from pydantic import BaseModel, Field

from cytomat.utils import int_to_bits


class PlateShuttleSystemStatus(BaseModel):
    transfer_station_occupied: bool = Field(serialization_alias="TransferStationOccupied")
    device_door_open: bool = Field(serialization_alias="DeviceDoorOpen")
    transfer_door_open: bool = Field(serialization_alias="TransferDoorOpen")
    shovel_occupied: bool = Field(serialization_alias="ShovelOccupied")
    error: bool = Field(serialization_alias="Error")
    warning: bool = Field(serialization_alias="Warning")
    ready: bool = Field(serialization_alias="Ready")
    busy: bool = Field(serialization_alias="Busy")

    @classmethod
    def from_hex_string(cls, hex_byte: str) -> PlateShuttleSystemStatus:
        """Create an instance from the hex string (e.g. ``'F1'``)."""
        bits = int_to_bits(int(hex_byte, base=16), n_bits=8)
        return cls(
            transfer_station_occupied=bits[0],
            device_door_open=bits[1],
            transfer_door_open=bits[2],
            shovel_occupied=bits[3],
            error=bits[4],
            warning=bits[5],
            ready=bits[6],
            busy=bits[7],
        )


class OverviewStatus(BaseModel):
    command_in_process: bool = Field(serialization_alias="CommandInProcess")
    command_executed_device_busy: bool = Field(serialization_alias="CommandExecutedDeviceBusy")
    warning_pending: bool = Field(serialization_alias="WarningPending")
    error_pending: bool = Field(serialization_alias="ErrorPending")
    shovel_occupied: bool = Field(serialization_alias="ShovelOccupied")
    auto_lift_door_open: bool = Field(serialization_alias="AutoLiftDoorOpen")
    device_door_open: bool = Field(serialization_alias="DeviceDoorOpen")
    transfer_station_occupied: bool = Field(serialization_alias="TransferStationOccupied")

    @classmethod
    def from_hex_string(cls, hex_byte: str) -> OverviewStatus:
        """Create an instance from the hex string (e.g. ``'F1'``)."""
        value = int(hex_byte, base=16)
        return cls(
            command_in_process=bool(value & 0x01),
            command_executed_device_busy=bool(value & 0x02),
            warning_pending=bool(value & 0x04),
            error_pending=bool(value & 0x08),
            shovel_occupied=bool(value & 0x10),
            auto_lift_door_open=bool(value & 0x20),
            device_door_open=bool(value & 0x40),
            transfer_station_occupied=bool(value & 0x80),
        )


class ErrorStatus(IntEnum):
    NoError = 0x00
    MotorCommunicationDisrupted = 0x01
    PlateNotMountedOnShovel = 0x02
    PlateNotDroppedFromShovel = 0x03
    ShovelNotExtended = 0x04
    ProcedureTimeout = 0x05
    TransferDoorNotOpened = 0x06
    TransferDoorNotClosed = 0x07
    ShovelNotRetracted = 0x08
    StepMotorTemperatureTooHigh = 0x0A
    OtherStepMotorError = 0x0B
    TransferStationNotRotated = 0x0C
    HeatingOrCo2CommunicationDisrupted = 0x0D
    ShakerCommunicationDisrupted = 0x0E
    ShakerConfigurationOutOfOrder = 0x0F
    ShakerNotStarted = 0x10
    ShakerClampNotOpen = 0x13
    ShakerClampNotClosed = 0x14
    Critical = 0xFF

    @classmethod
    def from_hex_string(cls, hex_byte: str) -> ErrorStatus:
        """Map a status hex byte (e.g. ``'0A'``) to a typed error status."""
        return cls(int(hex_byte, base=16))


class WarningStatus(IntEnum):
    NoWarning = 0x00
    MotorCommunicationDisrupted = 0x01
    PlateNotMountedOnShovel = 0x02
    PlateNotDroppedFromShovel = 0x03
    ShovelNotExtended = 0x04
    ProcedureTimeout = 0x05
    TransferDoorNotOpened = 0x06
    TransferDoorNotClosed = 0x07
    ShovelNotRetracted = 0x08
    InitialisingDueToOpenedDeviceDoor = 0x09
    TransferStationNotRotated = 0x0C

    @classmethod
    def from_hex_string(cls, hex_byte: str) -> WarningStatus:
        """Map a status hex byte (e.g. ``'09'``) to a typed warning status."""
        return cls(int(hex_byte, base=16))


class ActionType(IntEnum):
    NoAction = 0x00
    MoveHeightBelowSlot = 0x01
    CheckHeightBelowSlot = 0x02
    MoveHeightAboveSlot = 0x03
    CheckHeightAboveSlot = 0x04
    RotateToSlot = 0x05
    CheckRotation = 0x06
    ExtendShovel = 0x07
    CheckExtendedShovel = 0x08
    CheckShovelExtensionSensor = 0x09
    RetractShovel = 0x0A
    CheckRetractedShovel = 0x0B
    CloseTransferDoor = 0x0C
    CheckTransferDoorClosed = 0x0D
    OpenTransferDoor = 0x0E
    CheckTransferDoorOpened = 0x0F
    MoveSwapStationToPos1 = 0x10
    CheckSwapStationAtPos1 = 0x11
    MoveSwapStationToPos2 = 0x12
    CheckSwapStationAtPos2 = 0x13
    CheckPlateOnShovel = 0x14
    CheckPlateOnTransferStation = 0x15
    MoveToBarcodeReader = 0x16
    CheckHandlerAtBarcodeReader = 0x17
    ReadBarcode = 0x18
    UnknownX1b = 0x1B
    UnknownX1c = 0x1C


class ActionTarget(IntEnum):
    InitPosition = 1
    WaitPosition = 2
    Stacker = 3
    TransferStation = 4


class ActionStatus(BaseModel):
    type: ActionType = Field(serialization_alias="Type")
    target: ActionTarget = Field(serialization_alias="Target")

    @classmethod
    def from_hex_string(cls, hex_byte: str) -> ActionStatus:
        """Create an instance from the hex string (e.g. ``'F1'``)."""
        value = int(hex_byte, base=16)
        target = ActionTarget((value & 0b11100000) >> 5)
        action_type = ActionType(value & 0b00011111)
        return cls(type=action_type, target=target)


class SwapStationStatus(BaseModel):
    position1_at_door: bool = Field(serialization_alias="Position1AtDoor")
    occupied_at_door: bool = Field(serialization_alias="OccupiedAtDoor")
    occupied_at_user: bool = Field(serialization_alias="OccupiedAtUser")

    @classmethod
    def from_response_string(cls, response: str) -> SwapStationStatus:
        """Create an instance from the response string (e.g. ``'111'``)."""
        return cls(
            position1_at_door=response[0] == "1",
            occupied_at_door=response[1] == "1",
            occupied_at_user=response[2] == "1",
        )


class Status(BaseModel):
    plate_shuttle_system: PlateShuttleSystemStatus = Field(serialization_alias="PlateShuttleSystem")
    overview: OverviewStatus = Field(serialization_alias="Overview")
    action: ActionStatus = Field(serialization_alias="Action")
    error: ErrorStatus = Field(serialization_alias="Error")
    warning: WarningStatus = Field(serialization_alias="Warning")
