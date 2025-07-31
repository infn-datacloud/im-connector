from pydantic import BaseModel, AnyHttpUrl


class DeploymentCreate(BaseModel):
    im_url: AnyHttpUrl
    im_access_token: str
    iaas_access_token: str
    tosca_template: str
    provider_name: str
    provider_endpoint: AnyHttpUrl
    provider_type: str