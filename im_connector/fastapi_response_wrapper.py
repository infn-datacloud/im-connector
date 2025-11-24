import requests
from fastapi.responses import Response as FastAPIResponse


class FastAPIResponseWrapper(FastAPIResponse):
    """Wrap a generic response object of the requests library to a FastAPI Response object.

    Args:
        response: The requests.Response object instance to be wrapped.

    """

    def __init__(self, response: requests.Response):
        super().__init__(content=response.content,
                         status_code=response.status_code,
                         headers={
                             key: value
                             for key, value in response.headers.items()
                             if key.lower() not in {"content-encoding",
                                                    "transfer-encoding",
                                                    "content-length",
                                                    "connection"}
                         },
                         media_type=response.headers.get("content-type"))
