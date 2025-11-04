from im_library.entities.enums.cloud_provider_type import CloudProviderType
from im_library.header.im_header_component_base import IMHeaderComponentBase


class IMHeaderComposer:
    def __init__(self):
        self._headers: dict[str,str] = {"Content-Type": "text/yaml"}
        self._im_auth_credentials: list[IMHeaderComponentBase] = []

    def add_header(self, header_name: str, header_value: str):
        self._headers[header_name] = header_value

    def add_credential(self, credential: IMHeaderComponentBase):
        self._im_auth_credentials.append(credential)

    def get_header(self) -> dict[str, str]:
        if not any(h.header_type is CloudProviderType.INFRASTRUCTUREMANAGER for h in self._im_auth_credentials):
            raise AttributeError("Missing credential for IM.")

        serialized_headers = [h.serialize() for h in self._im_auth_credentials]

        header = {
            "Authorization": "\\n".join(serialized_headers)
        }

        header.update(self._headers)
        return header
