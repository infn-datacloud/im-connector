import dataclasses

from im_library.entities.im_base_requests import Get
from im_library.entities.im_request_parameters import IMPathParametersBase


@dataclasses.dataclass(kw_only=True)
class GetInfrastructureOutputsPathParameters(IMPathParametersBase):
    InfId: str


class GetInfrastructureOutputs(Get):
    def __init__(self, *,
                 path_parameters: GetInfrastructureOutputsPathParameters):
        super().__init__(path_parameters=path_parameters)

    @property
    def _url_template(self) -> str:
        return "/infrastructures/{InfId}/outputs"
