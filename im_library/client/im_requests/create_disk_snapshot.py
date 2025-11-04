from typing import Optional

from im_library.client.im_base_requests import Put
from im_library.client.im_path_parameters_base import IMPathParametersBase
from im_library.client.im_query_parameters_base import IMQueryParametersBase


class CreateDiskSnapshotQueryParameters(IMQueryParametersBase):
    def __init__(self, *, image_name: str, auto_delete: str = "false"):
        super().__init__(image_name=image_name, auto_delete=auto_delete)


class CreateDiskSnapshotPathParameters(IMPathParametersBase):
    InfId: str
    VMId: str
    diskNum: str


class CreateDiskSnapshot(Put):
    def __init__(self, *,
                 path_parameters: CreateDiskSnapshotPathParameters,
                 query_parameters: CreateDiskSnapshotQueryParameters,
                 body: str):
        super().__init__(path_parameters=path_parameters, body=body, query_parameters=query_parameters)

    @property
    def _url_template(self) -> str:
        return "/infrastructures/{InfId}/vms/{VMId}/disks/{diskNum}/snapshot"
