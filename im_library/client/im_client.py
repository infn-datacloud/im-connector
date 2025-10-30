import requests

from im_connector.main import settings
from im_library.client.base_requests import IMBaseRequest
from im_library.header.header_composer import HeaderComposer


class IMClient:
    @classmethod
    def request(cls, request: IMBaseRequest, header: HeaderComposer):
        url = f"{settings.IM_HOST}{request.url}"

        backend_response = requests.request(
            method=request.method,
            url=url,
            params=request.parameters,
            data=request.body,
            headers=header.headers,
            timeout=30.0,
        )

        return backend_response