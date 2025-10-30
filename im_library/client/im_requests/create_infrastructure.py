from im_library.client.im_base_requests import Post
from im_library.client.im_query_parameters_base import IMQueryParametersBase
from im_library.entities.enums.im_request_type import IMRequestType


class CreateInfrastructureQueryParameters(IMQueryParametersBase):
    def __init__(self, *, async_: str = "false", dry_run: str = "false"):
        super().__init__(async_=async_, dry_run=dry_run)


class CreateInfrastructure(Post):
    @property
    def request_type(self) -> IMRequestType:
        return IMRequestType.CREATE_INFRASTRUCTURE
