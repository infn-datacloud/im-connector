from typing import Optional

from im_connector.im_library.entities.im_credential_component_base import IMCredentialComponentBase


class KubernetesCredentialComponent(IMCredentialComponentBase):
    def __init__(self, *,
                 id: str = "kub",
                 type: str = "Kubernetes",
                 username: Optional[str] = None,
                 password: Optional[str] = None,
                 host: Optional[str] = None,
                 token: Optional[str] = None,
                 proxy: Optional[str] = None,
                 namespace: Optional[str] = None,
                 apps_dns: Optional[str] = None):
        self.id = id
        self.type = type
        self.username = username
        self.password = password
        self.host = host
        self.token = token
        self.proxy = proxy
        self.namespace = namespace
        self.apps_dns = apps_dns
