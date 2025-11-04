from im_library.client.im_base_requests import Get
from im_library.client.im_query_parameters_base import IMQueryParametersBase


class ListUserInfrastructuresQueryParameters(IMQueryParametersBase):
    def __init__(self, *, filter: str):
        super().__init__(filter=filter)


class ListUserInfrastructures(Get):
    @property
    def _url_template(self) -> str:
        return "/infrastructures"
