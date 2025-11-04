from im_library.client.im_base_requests import Delete


class DeleteVM(Delete):
    @property
    def _url_template(self) -> str:
        return "/infrastructures/{InfId}/vms/{VMId}"
