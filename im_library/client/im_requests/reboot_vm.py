from im_library.client.im_base_requests import Put


class RebootVM(Put):
    @property
    def _url_template(self) -> str:
        return "/infrastructures/{InfId}/vms/{VMId}/reboot"
