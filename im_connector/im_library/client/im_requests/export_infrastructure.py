import dataclasses
from typing import Optional

from im_connector.im_library.entities.im_base_requests import Get
from im_connector.im_library.entities.im_request_parameters import IMPathParametersBase, IMQueryParametersBase


@dataclasses.dataclass(kw_only=True)
class ExportInfrastructureQueryParameters(IMQueryParametersBase):
    delete: str = "false"


@dataclasses.dataclass(kw_only=True)
class ExportInfrastructurePathParameters(IMPathParametersBase):
    InfId: str


class ExportInfrastructure(Get):
    def __init__(self, *,
                 path_parameters: ExportInfrastructurePathParameters,
                 body: str,
                 query_parameters: Optional[ExportInfrastructureQueryParameters] = None):
        super().__init__(path_parameters=path_parameters, body=body, query_parameters=query_parameters)

    @property
    def _url_template(self) -> str:
        return "/infrastructures/{InfId}/data"
