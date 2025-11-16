import dataclasses

from im_connector.im_library.entities.im_base_requests import Get
from im_connector.im_library.entities.im_request_parameters import IMPathParametersBase


@dataclasses.dataclass(kw_only=True)
class GetVMContextualizationMessagePathParameters(IMPathParametersBase):
    InfId: str
    VMId: str


class GetVMContextualizationMessage(Get):
    def __init__(self, *,
                 path_parameters: GetVMContextualizationMessagePathParameters):
        super().__init__(path_parameters=path_parameters)

    @property
    def _url_template(self) -> str:
        return "/infrastructures/{InfId}/vms/{VMId}/contmsg"
