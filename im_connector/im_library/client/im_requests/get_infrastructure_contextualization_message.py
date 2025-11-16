import dataclasses
from typing import Optional

from im_connector.im_library.entities.im_base_requests import Get
from im_connector.im_library.entities.im_request_parameters import IMQueryParametersBase, IMPathParametersBase


@dataclasses.dataclass(kw_only=True)
class GetInfrastructureContextualizationMessageQueryParameters(IMQueryParametersBase):
    headeronly: str = "false"


@dataclasses.dataclass(kw_only=True)
class GetInfrastructureContextualizationMessagePathParameters(IMPathParametersBase):
    InfId: str


class GetInfrastructureContextualizationMessage(Get):
    def __init__(self, *,
                 path_parameters: GetInfrastructureContextualizationMessagePathParameters,
                 query_parameters: Optional[GetInfrastructureContextualizationMessageQueryParameters] = None):
        super().__init__(path_parameters=path_parameters, query_parameters=query_parameters)

    @property
    def _url_template(self) -> str:
        return "/infrastructures/{InfId}/contmsg"
