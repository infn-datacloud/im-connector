from im_connector.im_library.entities.im_base_requests import Get


class Version(Get):
    @property
    def _url_template(self) -> str:
        return "/version"
