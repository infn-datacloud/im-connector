import dataclasses
from typing import Optional

from im_library.entities.im_base_requests import Get
from im_library.entities.im_request_parameters import IMQueryParametersBase


@dataclasses.dataclass(kw_only=True)
class GetIMServerStatsQueryParameters(IMQueryParametersBase):
    init_date: str
    end_date: str


class GetIMServerStats(Get):
    def __init__(self, *,
                 query_parameters: Optional[GetIMServerStatsQueryParameters] = None):
        super().__init__(query_parameters=query_parameters)

    @property
    def _url_template(self) -> str:
        return "/stats"
