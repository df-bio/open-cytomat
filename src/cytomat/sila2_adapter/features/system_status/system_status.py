from sila2.server import MetadataDict, SilaServer

from cytomat import Cytomat
from cytomat.sila2_adapter.features.common import CytomatFeatureBase, load_feature_xml

SYSTEM_STATUS_FEATURE = load_feature_xml(__file__, "system_status.sila.xml")


class SystemStatusFeature(CytomatFeatureBase):
    def __init__(self, parent_server: SilaServer, cytomat: Cytomat) -> None:
        super().__init__(parent_server, cytomat, feature=SYSTEM_STATUS_FEATURE)

    def GetStatus(self, *, metadata: MetadataDict):
        _ = metadata
        with self._error_mapper:
            return self._cytomat.status.model_dump(mode="json", by_alias=True)

    def GetPlateShuttleSystemStatus(self, *, metadata: MetadataDict):
        _ = metadata
        with self._error_mapper:
            return self._cytomat.status.plate_shuttle_system.model_dump(mode="json", by_alias=True)

    def GetOverviewStatus(self, *, metadata: MetadataDict):
        _ = metadata
        with self._error_mapper:
            return self._cytomat.overview_status.model_dump(mode="json", by_alias=True)

    def GetActionStatus(self, *, metadata: MetadataDict):
        _ = metadata
        with self._error_mapper:
            return self._cytomat.action_status.model_dump(mode="json", by_alias=True)

    def GetErrorStatus(self, *, metadata: MetadataDict):
        _ = metadata
        with self._error_mapper:
            return {"Error": int(self._cytomat.error_status)}

    def GetWarningStatus(self, *, metadata: MetadataDict):
        _ = metadata
        with self._error_mapper:
            return {"Warning": int(self._cytomat.warning_status)}

    def ResetErrorRegister(self, *, metadata: MetadataDict):
        _ = metadata
        with self._error_mapper:
            return self._cytomat.reset_error_register().model_dump(mode="json", by_alias=True)
