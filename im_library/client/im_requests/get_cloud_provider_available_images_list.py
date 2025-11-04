from im_library.client.im_base_requests import Get
from im_library.client.im_query_parameters_base import IMQueryParametersBase


class GetCloudProviderAvailableImagesListQueryParameters(IMQueryParametersBase):
    def __init__(self, *, filters: str = ""):
        super().__init__(filters=filters)


class GetCloudProviderAvailableImagesList(Get):
    @property
    def _url_template(self) -> str:
        return "/clouds/{CloudId}/images"
