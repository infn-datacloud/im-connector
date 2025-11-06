from im_library.entities.im_base_requests import Get


class GetOAIPMHToscaInfo(Get):
    @property
    def _url_template(self) -> str:
        return "/oai"
