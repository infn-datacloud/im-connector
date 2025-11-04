from im_library.client.im_base_requests import Get
from im_library.client.im_query_parameters_base import IMQueryParametersBase


class GetInfrastructureContextualizationMessageQueryParameters(IMQueryParametersBase):
    def __init__(self, *, headeronly: str):
        super().__init__(headeronly=headeronly)


class GetInfrastructureContextualizationMessage(Get):
    @property
    def _url_template(self) -> str:
        return "/infrastructures/{InfId}/contmsg"
