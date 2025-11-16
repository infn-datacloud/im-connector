import dataclasses

from im_connector.im_library.entities.im_base_requests import Get
from im_connector.im_library.entities.im_request_parameters import IMPathParametersBase


@dataclasses.dataclass(kw_only=True)
class GetCloudProviderUserQuotasPathParameters(IMPathParametersBase):
    CloudId: str


class GetCloudProviderUserQuotas(Get):
    def __init__(self, *,
                 path_parameters: GetCloudProviderUserQuotasPathParameters):
        super().__init__(path_parameters=path_parameters)

    @property
    def _url_template(self) -> str:
        return "/clouds/{CloudId}/quotas"
