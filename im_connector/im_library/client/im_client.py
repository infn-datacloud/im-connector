import requests

from im_connector.config import get_settings
from im_connector.im_library.entities.im_base_requests import IMBaseRequest
from im_connector.im_library.header.im_header_composer import IMHeaderComposer
from im_connector.logger import get_logger

settings = get_settings()
logger = get_logger(settings)


class IMClient:
    @classmethod
    def request(cls, request: IMBaseRequest, header: IMHeaderComposer):
        url = f"{settings.IM_HOST}{request.url}"

        logger.info(f"[CLIENT]: forwarding request to IM at URL: {url}.")

        backend_response = requests.request(
            method=request.method,
            url=url,
            params=request.query_parameters,
            data=request.body,
            headers=header.get_header(),
            timeout=30.0,
        )

        return backend_response
