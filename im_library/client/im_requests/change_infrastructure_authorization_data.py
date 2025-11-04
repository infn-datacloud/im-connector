import dataclasses
from typing import Optional

from im_library.client.im_base_requests import Post
from im_library.client.im_path_parameters_base import IMPathParametersBase
from im_library.client.im_query_parameters_base import IMQueryParametersBase


class ChangeInfrastructureAuthorizationDataQueryParameters(IMQueryParametersBase):
    def __init__(self, *, overwrite: str = "false"):
        super().__init__(overwrite=overwrite)


@dataclasses.dataclass(kw_only=True)
class ChangeInfrastructureAuthorizationDataPathParameters(IMPathParametersBase):
    InfId: str


class ChangeInfrastructureAuthorizationData(Post):
    def __init__(self, *,
                 path_parameters: ChangeInfrastructureAuthorizationDataPathParameters,
                 body: str,
                 query_parameters: Optional[ChangeInfrastructureAuthorizationDataQueryParameters] = None):
        super().__init__(path_parameters=path_parameters, body=body, query_parameters=query_parameters)

    @property
    def _url_template(self) -> str:
        return "/infrastructures/{InfId}/authorization"
