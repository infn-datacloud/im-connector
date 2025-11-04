from im_library.client.im_base_requests import Put
from im_library.client.im_path_parameters_base import IMPathParametersBase


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
