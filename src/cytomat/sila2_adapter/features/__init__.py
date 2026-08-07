from cytomat.sila2_adapter.features.barcode_scanner import (
    BARCODE_SCANNER_FEATURE,
    BarcodeScannerFeature,
)
from cytomat.sila2_adapter.features.plate_handler import (
    PLATE_HANDLER_FEATURE,
    PlateHandlerFeature,
)

FEATURE_BINDINGS = [
    (PLATE_HANDLER_FEATURE, PlateHandlerFeature),
    (BARCODE_SCANNER_FEATURE, BarcodeScannerFeature),
]

__all__ = ["FEATURE_BINDINGS"]
