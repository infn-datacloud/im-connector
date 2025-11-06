import dataclasses

from im_library.entities.im_base_requests import Put
from im_library.entities.im_request_parameters import IMPathParametersBase


@dataclasses.dataclass(kw_only=True)
class StopVMPathParameters(IMPathParametersBase):
    InfId: str
    VMId: str


class StopVM(Put):
    def __init__(self, *,
                 path_parameters: StopVMPathParameters):
        super().__init__(path_parameters=path_parameters)

    @property
    def _url_template(self) -> str:
        return "/infrastructures/{InfId}/vms/{VMId}/stop"
