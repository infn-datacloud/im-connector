import dataclasses

from im_connector.im_library.entities.im_base_requests import Put
from im_connector.im_library.entities.im_request_parameters import IMQueryParametersBase, IMPathParametersBase


@dataclasses.dataclass(kw_only=True)
class CreateDiskSnapshotQueryParameters(IMQueryParametersBase):
    image_name: str
    auto_delete: str = "false"


@dataclasses.dataclass(kw_only=True)
class CreateDiskSnapshotPathParameters(IMPathParametersBase):
    InfId: str
    VMId: str
    diskNum: str


class CreateDiskSnapshot(Put):
    def __init__(self, *,
                 path_parameters: CreateDiskSnapshotPathParameters,
                 query_parameters: CreateDiskSnapshotQueryParameters):
        super().__init__(path_parameters=path_parameters, query_parameters=query_parameters)

    @property
    def _url_template(self) -> str:
        return "/infrastructures/{InfId}/vms/{VMId}/disks/{diskNum}/snapshot"
