from __future__ import annotations

from sila2.server import MetadataDict, SilaServer

from cytomat import Cytomat
from cytomat.sila2_adapter.features.common import CytomatFeatureBase, load_feature_xml

SHAKER_CONTROLLER_FEATURE = load_feature_xml(__file__, "shaker_controller.sila.xml")


class ShakerControllerFeature(CytomatFeatureBase):
    def __init__(self, parent_server: SilaServer, cytomat: Cytomat) -> None:
        super().__init__(parent_server, cytomat, feature=SHAKER_CONTROLLER_FEATURE)

    def Invoke(self, Method: str, ArgumentsJson: str, *, metadata: MetadataDict):
        _ = (Method, ArgumentsJson, metadata)
        with self._error_mapper:
            raise NotImplementedError("ShakerController feature is not implemented yet")
