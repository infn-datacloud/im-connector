import dataclasses
from typing import Optional

from im_library.entities.im_base_requests import Get
from im_library.entities.im_request_parameters import IMPathParametersBase, IMQueryParametersBase


@dataclasses.dataclass(kw_only=True)
class GetCloudProviderAvailableImagesListQueryParameters(IMQueryParametersBase):
    filters: str


@dataclasses.dataclass(kw_only=True)
class GetCloudProviderAvailableImagesListPathParameters(IMPathParametersBase):
    CloudId: str


class GetCloudProviderAvailableImagesList(Get):
    def __init__(self, *,
                 path_parameters: GetCloudProviderAvailableImagesListPathParameters,
                 query_parameters: Optional[GetCloudProviderAvailableImagesListQueryParameters] = None):
        super().__init__(path_parameters=path_parameters, query_parameters=query_parameters)

    @property
    def _url_template(self) -> str:
        return "/clouds/{CloudId}/images"
