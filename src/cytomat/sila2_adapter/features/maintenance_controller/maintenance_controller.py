from sila2.server import MetadataDict, SilaServer

from cytomat import Cytomat
from cytomat.sila2_adapter.features.common import CytomatFeatureBase, load_feature_xml

MAINTENANCE_CONTROLLER_FEATURE = load_feature_xml(
    __file__, "maintenance_controller.sila.xml"
)


class MaintenanceControllerFeature(CytomatFeatureBase):
    def __init__(self, parent_server: SilaServer, cytomat: Cytomat) -> None:
        super().__init__(parent_server, cytomat, feature=MAINTENANCE_CONTROLLER_FEATURE)

    def Invoke(self, Method: str, ArgumentsJson: str, *, metadata: MetadataDict):
        _ = (Method, ArgumentsJson, metadata)
        with self._error_mapper:
            raise NotImplementedError(
                "MaintenanceController feature is not implemented yet"
            )
