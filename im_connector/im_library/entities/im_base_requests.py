import abc
from typing import Optional

from im_connector.config import get_settings
from im_connector.im_library.entities.im_request_parameters import IMPathParametersBase, IMQueryParametersBase
from im_connector.logger import get_logger

settings = get_settings()
logger = get_logger(settings)


class IMBaseRequest(metaclass=abc.ABCMeta):
    """Base abstract class representing the generic HTTP request format.

    This class defines the handling of the body and query/path parameters.

    """

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
        """The URL template, e.g. /infrastructures/{InfId}/authorization. Where the templated path parameter is enclosed between {}.
        The path parameter is later replaced by the actual value. The parameter name is case-sensitive.

        Returns:
            str: the URL template, e.g. "/infrastructures/{InfId}/authorization".

        """
        ...

    @property
    @abc.abstractmethod
    def method(self) -> str:
        """The HTTP verb to be used for the request.

        Returns:
            str: the HTTP verb, e.g. "POST".

        """
        ...

    @property
    def url(self) -> str:
        """The formatted URL. The URL templated path parameters are replaced with corresponding values.

        Returns:
            str: the complete endpoint URL, with path parameters added as specified by the URL template.

        """
        path_parameters = self._path_parameters.to_dict() if self._path_parameters is not None else {}
        rendered_url = self._url_template.format(**path_parameters)
        return rendered_url

    @property
    def query_parameters(self) -> dict[str, str]:
        """Dict containing all query parameters supported by the concrete request.

        Returns:
            dict[str, str]: Dict of all query parameter names with the correspoinding values.

        """

        return self._query_parameters.to_dict() if self._query_parameters is not None else None

    @property
    def body(self) -> str:
        """The request body represented as a string.

        Returns:
            str: the request body represented as a string.

        """

        return self._body


class Get(IMBaseRequest, metaclass=abc.ABCMeta):
    """Intermediate base class to build requests using the GET verb."""

    @property
    def method(self) -> str:
        return "GET"


class Post(IMBaseRequest, metaclass=abc.ABCMeta):
    """Intermediate base class to build requests using the POST verb."""

    @property
    def method(self) -> str:
        return "POST"


class Put(IMBaseRequest, metaclass=abc.ABCMeta):
    """Intermediate base class to build requests using the PUT verb."""

    @property
    def method(self) -> str:
        return "PUT"


class Patch(IMBaseRequest, metaclass=abc.ABCMeta):
    """Intermediate base class to build requests using the PATCH verb."""

    @property
    def method(self) -> str:
        return "PATCH"


class Delete(IMBaseRequest, metaclass=abc.ABCMeta):
    """Intermediate base class to build requests using the DELETE verb."""

    @property
    def method(self) -> str:
        return "DELETE"
