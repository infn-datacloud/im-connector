import dataclasses
from typing import Optional

from im_connector.im_library.entities.im_base_requests import Post
from im_connector.im_library.entities.im_request_parameters import IMQueryParametersBase, IMPathParametersBase


@dataclasses.dataclass(kw_only=True)
class AddResourcesToInfrastructureQueryParameters(IMQueryParametersBase):
    context: str = "true"


@dataclasses.dataclass(kw_only=True)
class AddResourceToInfrastructurePathParameters(IMPathParametersBase):
    InfId: str


class AddResourcesToInfrastructure(Post):
    def __init__(self, *,
                 path_parameters: AddResourceToInfrastructurePathParameters,
                 body: str,
                 query_parameters: Optional[AddResourcesToInfrastructureQueryParameters] = None):
        super().__init__(path_parameters=path_parameters, body=body, query_parameters=query_parameters)

    @property
    def _url_template(self) -> str:
        return "/infrastructures/{InfId}"
