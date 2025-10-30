import re
from typing import Optional, Callable

from fastapi.requests import Request as FastAPIRequest

from im_library.adapter.im_endpoint_map import IMEndpointMap
from im_library.client.base_requests import IMBaseRequest
from im_library.client.im_requests.create_infrastructure import CreateInfrastructure, \
    CreateInfrastructureQueryParameters
from im_library.client.im_requests.list_user_infrastructures import ListUserInfrastructures, \
    ListUserInfrastructuresQueryParameters
from im_library.client.query_parameters_base import QueryParametersBase
from im_library.entities.enums.cloud_provider_type import CloudProviderType
from im_library.entities.enums.im_request_type import IMRequestType
from im_library.header.IMHeaderComponentBase import IMHeaderComponentBase
from im_library.header.composers.infrastructure_manager_header import InfrastructureManagerHeaderComponent
from im_library.header.composers.kubernetes_header import KubernetesHeaderComponent
from im_library.header.composers.openstack_header import OpenStackHeaderComponent
from im_library.header.header_composer import HeaderComposer




class IMRequestAdapter:
    _headers: dict[CloudProviderType, Callable[..., IMHeaderComponentBase]] = {
        CloudProviderType.INFRASTRUCTUREMANAGER: lambda **kw: InfrastructureManagerHeaderComponent(**kw),
        CloudProviderType.OPENSTACK: lambda **kw: OpenStackHeaderComponent(**kw),
        CloudProviderType.KUBERNETES: lambda **kw: KubernetesHeaderComponent(**kw),
    }

    _im_request_map: dict[IMRequestType, Callable[..., IMBaseRequest]] = {
        IMRequestType.LIST_USER_INFRASTRUCTURES: lambda *a, **kw: ListUserInfrastructures(*a, **kw),
        IMRequestType.CREATE_INFRASTRUCTURE: lambda *a, **kw: CreateInfrastructure(*a, **kw)
    }

    def __init__(self, request: FastAPIRequest):
        self._method = request.method.lower()
        self._query_parameters: QueryParametersBase = QueryParametersBase(**request.query_params)
        self._path_parameters = IMEndpointMap.extract_path_params(request.url.path)
        self._body = self._extract_body(request)
        self._auth_header_dict: list[dict[str, str]] = self._parse_im_auth_header(request.headers["Authorization"])
        self._header_composer: HeaderComposer = self._populate_header_composer()
        self._im_request_type: IMRequestType = IMEndpointMap.identify_request_type(request.url.path, request.method)

    @staticmethod
    async def _extract_body(request: FastAPIRequest):
        return await request.body()

    @staticmethod
    def _parse_im_auth_header(header_string: str) -> list[dict[str, str]]:
        lines = [line.strip() for line in header_string.split("\\n") if line.strip()]
        result = []
        for line in lines:
            pairs = [p.strip() for p in line.split(" ; ") if p.strip()]
            entry = {}
            for pair in pairs:
                if " = " in pair:
                    key, val = pair.split(" = ", 1)
                    entry[key.strip()] = val.strip().strip("'\"")
            result.append(entry)
        return result

    def _populate_header_composer(self) -> HeaderComposer:
        composer = HeaderComposer()
        for cred in self._auth_header_dict:
            provider_type: CloudProviderType = CloudProviderType(cred["type"])
            header: IMHeaderComponentBase = IMRequestAdapter._headers[provider_type](**cred)
            composer.add_credential(header)
        return composer

    @property
    def request(self) -> IMBaseRequest:
        return IMRequestAdapter._im_request_map[self._im_request_type](query_parameters=self._query_parameters,
                                                                       path_parameters=self._path_parameters,
                                                                       body=self._body)

    @property
    def header(self) -> HeaderComposer:
        return self._header_composer
