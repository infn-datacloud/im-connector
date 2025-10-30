from im_library.entities.enums.cloud_provider_type import CloudProviderType
from im_library.header.IMHeaderComponentBase import IMHeaderComponentBase


class HeaderComposer:
    def __init__(self):
        self._headers: list[IMHeaderComponentBase] = []

    def add_credential(self, credential: IMHeaderComponentBase):
        self._headers.append(credential)

    def get_header(self) -> dict[str, str]:
        if not any(h.header_type is CloudProviderType.INFRASTRUCTUREMANAGER for h in self._headers):
            raise AttributeError("Missing credential for IM.")

        serialized_headers = [h.serialize() for h in self._headers]
        return {
            "Content-Type": "text/yaml",
            "Authorization": "\\n".join(serialized_headers)
        }
