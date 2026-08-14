from cytomat.sila2_adapter.features.plate_handler import (
    PLATE_HANDLER_FEATURE,
    PlateHandlerFeature,
)
from cytomat.sila2_adapter.features.system_status import (
    SYSTEM_STATUS_FEATURE,
    SystemStatusFeature,
)

FEATURE_BINDINGS = [
    (PLATE_HANDLER_FEATURE, PlateHandlerFeature),
    (SYSTEM_STATUS_FEATURE, SystemStatusFeature),
]

__all__ = ["FEATURE_BINDINGS"]
