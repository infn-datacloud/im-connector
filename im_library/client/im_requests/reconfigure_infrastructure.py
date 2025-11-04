from im_library.client.im_base_requests import Put
from im_library.client.im_query_parameters_base import IMQueryParametersBase


class ReconfigureInfrastructureQueryParameters(IMQueryParametersBase):
    def __init__(self, *, vm_list: str):
        super().__init__(vm_list=vm_list)


class ReconfigureInfrastructure(Put):
    @property
    def _url_template(self) -> str:
        return "/infrastructures/{InfId}/reconfigure"
