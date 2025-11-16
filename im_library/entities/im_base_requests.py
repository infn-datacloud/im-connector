import abc
from typing import Optional

from im_connector.config import get_settings
from im_library.entities.im_request_parameters import IMPathParametersBase, IMQueryParametersBase
from im_library.logging.logger import get_logger

settings = get_settings()
logger = get_logger(settings)


class IMBaseRequest(metaclass=abc.ABCMeta):
    def __init__(self, *,
                 path_parameters: Optional[IMPathParametersBase] = None,
                 query_parameters: Optional[IMQueryParametersBase] = None,
                 body: str = ""):
        self._path_parameters: Optional[IMPathParametersBase] = path_parameters
        self._query_parameters: Optional[IMQueryParametersBase] = query_parameters
        self._body: str = body
        logger.info(f"[REQUEST] - Created request  {type(self).__name__}.")

    @property
    @abc.abstractmethod
    def _url_template(self) -> str:
        ...

    @property
    @abc.abstractmethod
    def method(self) -> str:
        ...

    @property
    def url(self) -> str:
        path_parameters = self._path_parameters.to_dict() if self._path_parameters is not None else {}
        rendered_url = self._url_template.format(**path_parameters)
        return rendered_url

    @property
    def query_parameters(self) -> dict[str, str]:
        return self._query_parameters.to_dict() if self._query_parameters is not None else None

    @property
    def body(self) -> str:
        return self._body


class Get(IMBaseRequest, metaclass=abc.ABCMeta):
    @property
    def method(self) -> str:
        return "GET"


class Post(IMBaseRequest, metaclass=abc.ABCMeta):
    @property
    def method(self) -> str:
        return "POST"


class Put(IMBaseRequest, metaclass=abc.ABCMeta):
    @property
    def method(self) -> str:
        return "PUT"


class Patch(IMBaseRequest, metaclass=abc.ABCMeta):
    @property
    def method(self) -> str:
        return "PATCH"


class Delete(IMBaseRequest, metaclass=abc.ABCMeta):
    @property
    def method(self) -> str:
        return "DELETE"
