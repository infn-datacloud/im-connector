from typing import Callable, Optional

from fastapi.requests import Request as FastAPIRequest
from typing_extensions import Any

from im_library.adapter.im_endpoint_map import IMEndpointMap
from im_library.client.im_base_requests import IMBaseRequest
from im_library.client.im_path_parameters_base import IMPathParametersBase
from im_library.client.im_query_parameters_base import IMQueryParametersBase
from im_library.client.im_requests.create_infrastructure import CreateInfrastructure
from im_library.client.im_requests.import_infrastructure import ImportInfrastructure
from im_library.client.im_requests.list_user_infrastructures import ListUserInfrastructures
from im_library.entities.enums.cloud_provider_type import CloudProviderType
from im_library.entities.enums.im_request_type import IMRequestType
from im_library.header.components.infrastructure_manager_header import InfrastructureManagerHeaderComponent
from im_library.header.components.kubernetes_header import KubernetesHeaderComponent
from im_library.header.components.openstack_header import OpenStackHeaderComponent
from im_library.header.im_header_component_base import IMHeaderComponentBase
from im_library.header.im_header_composer import IMHeaderComposer


class IMRequestAdapter:
    _headers: dict[CloudProviderType, Callable[..., IMHeaderComponentBase]] = {
        CloudProviderType.INFRASTRUCTUREMANAGER: lambda **kw: InfrastructureManagerHeaderComponent(**kw),
        CloudProviderType.OPENSTACK: lambda **kw: OpenStackHeaderComponent(**kw),
        CloudProviderType.KUBERNETES: lambda **kw: KubernetesHeaderComponent(**kw),
    }

    _im_request_map: dict[IMRequestType, Callable[..., IMBaseRequest]] = {
        IMRequestType.LIST_USER_INFRASTRUCTURES: lambda *a, **kw: ListUserInfrastructures(*a, **kw),
        IMRequestType.CREATE_INFRASTRUCTURE: lambda *a, **kw: CreateInfrastructure(*a, **kw),
        IMRequestType.IMPORT_INFRASTRUCTURE: lambda *a, **kw: ImportInfrastructure(*a, **kw),
    }

    _im_path_parameters_map: dict[IMRequestType, Optional[Callable[..., IMPathParametersBase]]] = {
        IMRequestType.LIST_USER_INFRASTRUCTURES: None,
        IMRequestType.CREATE_INFRASTRUCTURE: None,
        IMRequestType.IMPORT_INFRASTRUCTURE: None,
    }

    def __init__(self, request: FastAPIRequest, request_body: Any):
        self._query_parameters: IMQueryParametersBase = IMQueryParametersBase(**request.query_params)
        self._path_parameters = IMEndpointMap.extract_path_params(request.url.path)
        self._body = request_body
        self._header_composer: IMHeaderComposer = self._populate_header_composer(request.headers)
        self._im_request_type: IMRequestType = IMEndpointMap.identify_request_type(request.url.path, request.method)

    @staticmethod
    def _parse_im_auth_header(header_string: str) -> list[dict[str, str]]:
        lines = [line.strip() for line in header_string.split("\\n") if line.strip()]
        result = []
        for line in lines:
            pairs = [p.strip() for p in line.split(";") if p.strip()]
            entry = {}
            for pair in pairs:
                if " = " in pair:
                    key, val = pair.split(" = ", 1)
                    entry[key.strip()] = val.strip().strip("'\"")
            result.append(entry)
        return result

    def _populate_header_composer(self, headers) -> IMHeaderComposer:
        auth_header_dict: list[dict[str, str]] = self._parse_im_auth_header(headers["Authorization"])
        composer = IMHeaderComposer()
        for cred in auth_header_dict:
            provider_type: CloudProviderType = CloudProviderType(cred["type"])
            header: IMHeaderComponentBase = IMRequestAdapter._headers[provider_type](**cred)
            composer.add_credential(header)
        for header_name, header_value in headers.items():
            if header_name.lower() != "authorization":
                composer.add_header(header_name, header_value)
        return composer

    @property
    def request(self) -> IMBaseRequest:
        path_parameters = IMRequestAdapter._im_path_parameters_map[self._im_request_type]
        if path_parameters is not None:
            path_parameters_dataclass: Optional[IMPathParametersBase] = path_parameters(**self._path_parameters)
        else:
            path_parameters_dataclass : Optional[IMPathParametersBase] = None
        return IMRequestAdapter._im_request_map[self._im_request_type](query_parameters=self._query_parameters,
                                                                       path_parameters=path_parameters_dataclass,
                                                                       body=self._body)

    @property
    def header(self) -> IMHeaderComposer:
        return self._header_composer
