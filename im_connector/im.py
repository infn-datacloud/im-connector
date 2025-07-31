import requests
from fastapi import HTTPException, status
from fastapi.responses import Response as FastAPIResponse
from pydantic import AnyHttpUrl

from im_connector.fastapi_response_wrapper import FastAPIResponseMapper


def create_k8s_deployment(*,
                          im_url: AnyHttpUrl,
                          im_access_token: str,
                          iaas_access_token: str,
                          tosca_template: str,
                          provider_name: str,
                          provider_endpoint: AnyHttpUrl,
                          provider_type: str) -> FastAPIResponse:

    header_list: list[str] = [
        f"type = InfrastructureManager; token = {im_access_token}",
        f"id = {provider_name}; type = '{provider_type}'; host = {provider_endpoint}; token = {iaas_access_token}"
    ]

    headers: dict[str, str] = {
        "Content-Type": "text/yaml",
        "Authorization": "\\n".join(header_list)
    }

    try:
        im_backend_response: requests.Response = requests.post(url=str(im_url), data=tosca_template, headers=headers)
    except Exception as e:
        # Relaying the exception to ensure consistency with FastAPI data types
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=e)

    if not im_backend_response.ok:
        raise HTTPException(status_code=im_backend_response.status_code, detail=im_backend_response.reason)

    return FastAPIResponseMapper(im_backend_response)
