from im_library.client.im_base_requests import Post
from im_library.client.im_query_parameters_base import IMQueryParametersBase


class CreateInfrastructureQueryParameters(IMQueryParametersBase):
    def __init__(self, *, async_: str = "false", dry_run: str = "false"):
        super().__init__(async_=async_, dry_run=dry_run)


class CreateInfrastructure(Post):
    @property
    def _url_template(self) -> str:
        return "/infrastructures"
