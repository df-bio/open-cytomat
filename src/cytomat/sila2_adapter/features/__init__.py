from cytomat.sila2_adapter.features.barcode_scanner import (
    BARCODE_SCANNER_FEATURE,
    BarcodeScannerFeature,
)
from cytomat.sila2_adapter.features.climate_controller import (
    CLIMATE_CONTROLLER_FEATURE,
    ClimateControllerFeature,
)
from cytomat.sila2_adapter.features.maintenance_controller import (
    MAINTENANCE_CONTROLLER_FEATURE,
    MaintenanceControllerFeature,
)
from cytomat.sila2_adapter.features.plate_handler import (
    PLATE_HANDLER_FEATURE,
    PlateHandlerFeature,
)

FEATURE_BINDINGS = [
    (PLATE_HANDLER_FEATURE, PlateHandlerFeature),
    (BARCODE_SCANNER_FEATURE, BarcodeScannerFeature),
    (MAINTENANCE_CONTROLLER_FEATURE, MaintenanceControllerFeature),
    (CLIMATE_CONTROLLER_FEATURE, ClimateControllerFeature),
]

__all__ = ["FEATURE_BINDINGS"]
