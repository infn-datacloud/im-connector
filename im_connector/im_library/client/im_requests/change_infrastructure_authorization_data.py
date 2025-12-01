import dataclasses
from typing import Optional

from im_connector.im_library.entities.im_base_requests import Post
from im_connector.im_library.entities.im_request_parameters import IMQueryParametersBase, IMPathParametersBase


@dataclasses.dataclass(kw_only=True)
class ChangeInfrastructureAuthorizationDataQueryParameters(IMQueryParametersBase):
    overwrite: str = "false"


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
