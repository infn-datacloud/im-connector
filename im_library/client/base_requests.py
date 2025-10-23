import abc
from typing import Optional


class IMBaseRequest(metaclass=abc.ABCMeta):
    def __init__(self, *, query_parameters: Optional[dict] = None, body: str = "",
                 path_parameters: Optional[dict] = None):
        self._parameters: Optional[dict] = query_parameters
        self._body: str = body
        self._path_parameters: Optional[dict] = path_parameters

    @property
    @abc.abstractmethod
    def method(self) -> str:
        ...

    @property
    @abc.abstractmethod
    def url(self) -> str:
        ...

    @property
    def parameters(self) -> dict[str, str]:
        return self._parameters

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
