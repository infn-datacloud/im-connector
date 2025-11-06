import dataclasses
from typing import Optional

from im_library.entities.im_base_requests import Get
from im_library.entities.im_request_parameters import IMQueryParametersBase


@dataclasses.dataclass()
class ListUserInfrastructuresQueryParameters(IMQueryParametersBase):
    filter: str = ""


class ListUserInfrastructures(Get):
    def __init__(self, *,
                 query_parameters: Optional[ListUserInfrastructuresQueryParameters] = None):
        super().__init__(query_parameters=query_parameters)

    @property
    def _url_template(self) -> str:
        return "/infrastructures"
