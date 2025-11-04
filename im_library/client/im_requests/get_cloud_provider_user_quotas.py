from im_library.client.im_base_requests import Get
from im_library.client.im_query_parameters_base import IMQueryParametersBase


class GetCloudProviderUserQuotas(Get):
    @property
    def _url_template(self) -> str:
        return "/clouds/{CloudId}/quotas"
