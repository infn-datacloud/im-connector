from typing import Optional

from im_connector.im_library.entities.im_credential_component_base import IMCredentialComponentBase


class OpenStackCredentialComponent(IMCredentialComponentBase):
    """Concrete class representing OpenStack credential."""

    def __init__(self, *,
                 id: str = "os",
                 type: str = "OpenStack",
                 username: Optional[str] = None,
                 password: Optional[str] = None,
                 host: Optional[str] = None,
                 token: Optional[str] = None,
                 proxy: Optional[str] = None,
                 tenant: Optional[str] = None,
                 domain: Optional[str] = None,
                 auth_version: Optional[str] = None,
                 api_version: Optional[str] = None,
                 base_url: Optional[str] = None,
                 network_url: Optional[str] = None,
                 image_url: Optional[str] = None,
                 volume_url: Optional[str] = None,
                 service_region: Optional[str] = None,
                 service_name: Optional[str] = None,
                 auth_token: Optional[str] = None,
                 tenant_domain_id: Optional[str] = None,
                 microversion: Optional[str] = None):
        self.id = id
        self.type = type
        self.username = username
        self.password = password
        self.host = host
        self.token = token
        self.proxy = proxy
        self.tenant = tenant
        self.domain = domain
        self.auth_version = auth_version
        self.api_version = api_version
        self.base_url = base_url
        self.network_url = network_url
        self.image_url = image_url
        self.volume_url = volume_url
        self.service_region = service_region
        self.service_name = service_name
        self.auth_token = auth_token
        self.tenant_domain_id = tenant_domain_id
        self.microversion = microversion


