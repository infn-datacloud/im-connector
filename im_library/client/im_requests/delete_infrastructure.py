import dataclasses
from typing import Optional

from im_library.entities.im_base_requests import Delete
from im_library.entities.im_request_parameters import IMPathParametersBase, IMQueryParametersBase


@dataclasses.dataclass(kw_only=True)
class DeleteInfrastructureQueryParameters(IMQueryParametersBase):
    force: str = "false"
    async_: str = "false"


@dataclasses.dataclass(kw_only=True)
class DeleteInfrastructurePathParameters(IMPathParametersBase):
    InfId: str


class DeleteInfrastructure(Delete):
    def __init__(self, *,
                 path_parameters: DeleteInfrastructurePathParameters,
                 query_parameters: Optional[DeleteInfrastructureQueryParameters] = None):
        super().__init__(path_parameters=path_parameters, query_parameters=query_parameters)

    @property
    def _url_template(self) -> str:
        return "/infrastructures/{InfId}"
