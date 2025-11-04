from im_library.client.im_base_requests import Get
from im_library.client.im_query_parameters_base import IMQueryParametersBase


class ExportInfrastructureQueryParameters(IMQueryParametersBase):
    def __init__(self, *, delete: str):
        super().__init__(delete=delete)


class ExportInfrastructure(Get):
    @property
    def _url_template(self) -> str:
        return "/infrastructures/{InfId}/data"
