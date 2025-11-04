import abc
from typing import Optional

from im_library.client.im_query_parameters_base import IMQueryParametersBase


class IMBaseRequest(metaclass=abc.ABCMeta):
    def __init__(self, *,
                 path_parameters: Optional[dict] = None,
                 query_parameters: Optional[IMQueryParametersBase] = None,
                 body: str = ""):
        self._path_parameters: dict = {} if path_parameters is None else path_parameters
        self._query_parameters: IMQueryParametersBase = query_parameters
        self._body: str = body

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
        return self._url_template.format(**self._path_parameters)

    @property
    def query_parameters(self) -> dict[str, str]:
        return self._query_parameters

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
