import dataclasses

from im_connector.im_library.entities.im_base_requests import Put
from im_connector.im_library.entities.im_request_parameters import IMPathParametersBase


@dataclasses.dataclass(kw_only=True)
class StartInfrastructurePathParameters(IMPathParametersBase):
    InfId: str


class StartInfrastructure(Put):
    def __init__(self, *,
                 path_parameters: StartInfrastructurePathParameters):
        super().__init__(path_parameters=path_parameters)

    @property
    def _url_template(self) -> str:
        return "/infrastructures/{InfId}/start"
