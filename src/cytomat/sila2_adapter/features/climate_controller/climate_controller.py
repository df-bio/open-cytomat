from sila2.server import MetadataDict, SilaServer

from cytomat import Cytomat
from cytomat.sila2_adapter.features.common import CytomatFeatureBase, load_feature_xml

CLIMATE_CONTROLLER_FEATURE = load_feature_xml(__file__, "climate_controller.sila.xml")


class ClimateControllerFeature(CytomatFeatureBase):
    def __init__(self, parent_server: SilaServer, cytomat: Cytomat) -> None:
        super().__init__(parent_server, cytomat, feature=CLIMATE_CONTROLLER_FEATURE)

    def Invoke(self, Method: str, ArgumentsJson: str, *, metadata: MetadataDict):
        _ = (Method, ArgumentsJson, metadata)
        with self._error_mapper:
            raise NotImplementedError("ClimateController feature is not implemented yet")
