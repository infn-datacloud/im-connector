import dataclasses

from im_connector.im_library.entities.im_base_requests import Put
from im_connector.im_library.entities.im_request_parameters import IMPathParametersBase


@dataclasses.dataclass(kw_only=True)
class AlterVMPathParameters(IMPathParametersBase):
    InfId: str
    VMId: str


class AlterVM(Put):
    def __init__(self, *,
                 path_parameters: AlterVMPathParameters,
                 body: str):
        super().__init__(path_parameters=path_parameters, body=body)

    @property
    def _url_template(self) -> str:
        return "/infrastructures/{InfId}/vms/{VMId}"
