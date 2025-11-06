import dataclasses
from typing import Optional

from im_library.entities.im_base_requests import Post
from im_library.entities.im_request_parameters import IMQueryParametersBase


@dataclasses.dataclass(kw_only=True)
class CreateInfrastructureQueryParameters(IMQueryParametersBase):
    async_: str = "false"
    dry_run: str = "false"


class CreateInfrastructure(Post):
    def __init__(self, *,
                 body: str,
                 query_parameters: Optional[CreateInfrastructureQueryParameters] = None):
        super().__init__(body=body, query_parameters=query_parameters)

    @property
    def _url_template(self) -> str:
        return "/infrastructures"
