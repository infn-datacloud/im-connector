from im_connector.im_library.entities.enums.cloud_provider_type import CloudProviderType
from im_connector.im_library.entities.im_credential_component_base import IMCredentialComponentBase


class IMHeaderComposer:
    """Helper class storing all header data (authorization and other metadata)."""

    def __init__(self):
        self._headers: dict[str,str] = {"content-type": "text/yaml"}
        self._im_auth_credentials: list[IMCredentialComponentBase] = []

    def add_header(self, header_name: str, header_value: str):
        """Add generic header.

        Args:
            header_name: The name of the header entry

            header_value: The value to assign to the specified header name

        """
        self._headers[header_name] = header_value

    def add_credential(self, credential: IMCredentialComponentBase):
        """Add IM credential object to header data.

        An instance of a concrete class inheriting from IMCredentialComponentBase is added to the header data.

        Args:
            credential: instance of a concrete object inheriting from IMCredentialComponentBase.
                        The concrete object represents the target cloud provider.

        """

        self._im_auth_credentials.append(credential)

    def get_header(self) -> dict[str, str]:
        """Create a dict with all stored header data.

        Returns:
            dict[str, str]: the request header represented as a dictionary.

        """

        if not any(h.header_type is CloudProviderType.INFRASTRUCTUREMANAGER for h in self._im_auth_credentials):
            raise AttributeError("Missing credential for IM.")

        serialized_headers = [h.serialize() for h in self._im_auth_credentials]

        header = {
            "authorization": "\\n".join(serialized_headers)
        }

        header.update(self._headers)
        return header
