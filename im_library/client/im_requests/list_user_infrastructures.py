from typing import Optional

from im_library.client.base_requests import Get
from im_library.client.query_parameters_base import QueryParametersBase
from im_library.entities.enums.im_request_type import IMRequestType


class ListUserInfrastructuresQueryParameters(QueryParametersBase):
    def __init__(self, *, filter: str):
        super().__init__(filter=filter)


class ListUserInfrastructures(Get):
    @property
    def request_type(self) -> IMRequestType:
        return IMRequestType.LIST_USER_INFRASTRUCTURES
