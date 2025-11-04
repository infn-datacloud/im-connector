from im_library.client.im_base_requests import Get


class GetInfrastructureOutputs(Get):
    @property
    def _url_template(self) -> str:
        return "/infrastructures/{InfId}/outputs"
