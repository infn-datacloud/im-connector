from im_connector.im_library.entities.enums.cloud_provider_type import CloudProviderType
from im_connector.im_library.entities.im_credential_component_base import IMCredentialComponentBase


class IMHeaderComposer:
    def __init__(self):
        self._headers: dict[str,str] = {"content-type": "text/yaml"}
        self._im_auth_credentials: list[IMCredentialComponentBase] = []

    def add_header(self, header_name: str, header_value: str):
        self._headers[header_name] = header_value

    def add_credential(self, credential: IMCredentialComponentBase):
        self._im_auth_credentials.append(credential)

    def get_header(self) -> dict[str, str]:
        if not any(h.header_type is CloudProviderType.INFRASTRUCTUREMANAGER for h in self._im_auth_credentials):
            raise AttributeError("Missing credential for IM.")

        serialized_headers = [h.serialize() for h in self._im_auth_credentials]

        header = {
            "authorization": "\\n".join(serialized_headers)
        }

        header.update(self._headers)
        return header
