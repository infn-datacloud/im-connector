from im_library.entities.im_base_requests import Put


class ImportInfrastructure(Put):
    def __init__(self, *,
                 body: str):
        super().__init__(body=body)

    @property
    def _url_template(self) -> str:
        return "/infrastructures"
