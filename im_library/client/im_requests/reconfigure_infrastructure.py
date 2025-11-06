import dataclasses
from typing import Optional

from im_library.entities.im_base_requests import Put
from im_library.entities.im_request_parameters import IMPathParametersBase, IMQueryParametersBase


@dataclasses.dataclass(kw_only=True)
class ReconfigureInfrastructureQueryParameters(IMQueryParametersBase):
    vm_list: str


@dataclasses.dataclass(kw_only=True)
class ReconfigureInfrastructurePathParameters(IMPathParametersBase):
    InfId: str


class ReconfigureInfrastructure(Put):
    def __init__(self, *,
                 path_parameters: ReconfigureInfrastructurePathParameters,
                 query_parameters: Optional[ReconfigureInfrastructureQueryParameters] = None):
        super().__init__(path_parameters=path_parameters, query_parameters=query_parameters)

    @property
    def _url_template(self) -> str:
        return "/infrastructures/{InfId}/reconfigure"
