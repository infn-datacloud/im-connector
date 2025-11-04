import dataclasses
from typing import Optional

from im_library.client.im_base_requests import Delete
from im_library.client.im_path_parameters_base import IMPathParametersBase
from im_library.client.im_query_parameters_base import IMQueryParametersBase


class DeleteInfrastructureQueryParameters(IMQueryParametersBase):
    def __init__(self, *, force: str = "false", async_: str = "false"):
        super().__init__(force=force, async_=async_)


@dataclasses.dataclass(kw_only=True)
class DeleteInfrastructurePathParameters(IMPathParametersBase):
    InfId: str


class DeleteInfrastructure(Delete):
    def __init__(self, *,
                 path_parameters: DeleteInfrastructurePathParameters,
                 body: str,
                 query_parameters: Optional[DeleteInfrastructureQueryParameters] = None):
        super().__init__(path_parameters=path_parameters, body=body, query_parameters=query_parameters)

    @property
    def _url_template(self) -> str:
        return "/infrastructures/{InfId}"
