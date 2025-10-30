from typing import Optional

from im_library.client.base_requests import Post
from im_library.client.query_parameters_base import QueryParametersBase
from im_library.entities.enums.im_request_type import IMRequestType


class CreateInfrastructureQueryParameters(QueryParametersBase):
    def __init__(self, *, async_: str = "false", dry_run: str = "false"):
        super().__init__(async_=async_, dry_run=dry_run)


class CreateInfrastructure(Post):
    @property
    def request_type(self) -> IMRequestType:
        return IMRequestType.CREATE_INFRASTRUCTURE
