from typing import Optional

from im_library.client.im_base_requests import Post
from im_library.client.im_path_parameters_base import IMPathParametersBase
from im_library.client.im_query_parameters_base import IMQueryParametersBase


class AddResourcesToInfrastructureQueryParameters(IMQueryParametersBase):
    def __init__(self, *, context: str = "true"):
        super().__init__(context=context)


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
