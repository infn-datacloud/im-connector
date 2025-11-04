from im_library.client.im_base_requests import Get


class GetInfrastructureState(Get):
    @property
    def _url_template(self) -> str:
        return "/infrastructures/{InfId}/state"
