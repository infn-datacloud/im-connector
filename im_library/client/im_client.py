import requests

from im_connector.config import get_settings
from im_library.entities.im_base_requests import IMBaseRequest
from im_library.header.im_header_composer import IMHeaderComposer

settings = get_settings()

class IMClient:
    @classmethod
    def request(cls, request: IMBaseRequest, header: IMHeaderComposer):
        url = f"{settings.IM_HOST}{request.url}"

        backend_response = requests.request(
            method=request.method,
            url=url,
            params=request.query_parameters,
            data=request.body,
            headers=header.get_header(),
            timeout=30.0,
        )

        return backend_response