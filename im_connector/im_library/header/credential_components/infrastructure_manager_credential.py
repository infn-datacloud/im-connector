from typing import Optional

from im_connector.im_library.header.im_credential_component_base import IMCredentialComponentBase


class InfrastructureManagerCredentialComponent(IMCredentialComponentBase):
    def __init__(self, *,
                 id: str = "im",
                 type: str = "InfrastructureManager",
                 username: Optional[str] = None,
                 password: Optional[str] = None,
                 host: Optional[str] = None,
                 token: Optional[str] = None,
                 proxy: Optional[str] = None):
        self.id = id
        self.type = type
        self.username = username
        self.password = password
        self.host = host
        self.token = token
        self.proxy = proxy
