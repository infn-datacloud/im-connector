import requests

from im_connector.config import get_settings
from im_connector.im_library.entities.im_base_requests import IMBaseRequest
from im_connector.im_library.header.im_header_composer import IMHeaderComposer
from im_connector.logger import get_logger

settings = get_settings()
logger = get_logger(settings)


class IMClient:
    """InfrastructureManagr client."""

    @classmethod
    def request(cls, request: IMBaseRequest, header: IMHeaderComposer) -> requests.Response:
        """Make an HTTP request to the IM deployment.

        The request is built based on a IMBaseRequest instance (carrying the endpoint's URL, the HTTP verb,
        all query parameters and the request body. In addition, the IMHeaderComposer containing all headers,
        including the authorization header, is passed and invoked to serialize the header data to the dict required by
        the requests library.

        Args:
            request: IMBaseRequest instance (e.g. CreateInfrastructure)

            header:  IMHeaderComposer instance containing all header data. The composer is invoked to serialize the header data.

        Returns:
             requests.Response: the requests.Response object instance as received from the IM deployment.

        """

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
