import dataclasses

from im_connector.im_library.entities.im_base_requests import Put
from im_connector.im_library.entities.im_request_parameters import IMPathParametersBase


@dataclasses.dataclass(kw_only=True)
class RebootVMPathParameters(IMPathParametersBase):
    InfId: str
    VMId: str


class RebootVM(Put):
    def __init__(self, *,
                 path_parameters: RebootVMPathParameters):
        super().__init__(path_parameters=path_parameters)

    @property
    def _url_template(self) -> str:
        return "/infrastructures/{InfId}/vms/{VMId}/reboot"
