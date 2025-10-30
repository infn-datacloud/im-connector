from typing import Optional

from im_library.header.im_header_component_base import IMHeaderComponentBase


class InfrastructureManagerHeaderComponent(IMHeaderComponentBase):
    def __init__(self, *,
                 id: str = "im",
                 type: str = "infrastructuremanager",
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
