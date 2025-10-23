import re
from typing import Optional, Callable

from fastapi.requests import Request as FastAPIRequest

from im_library.client.base_requests import IMBaseRequest
from im_library.client.im_requests.create_infrastructure import CreateInfrastructure
from im_library.client.im_requests.list_user_infrastructures import ListUserInfrastructures
from im_library.entities.enums.cloud_provider_type import CloudProviderType
from im_library.entities.enums.im_request_type import IMRequestType
from im_library.header.composers.kubernetes_header_composer import KubernetesHeaderComposer
from im_library.header.composers.openstack_header_composer import OpenStackHeaderComposer
from im_library.header.header_composer import HeaderComposer


def swagger_endpoint_to_regex(swagger_path: str) -> re.Pattern:
    """Convert a Swagger-like path (with {param}) into a regex pattern."""
    regex = re.escape(swagger_path)
    regex = regex.replace(r'\{', '{').replace(r'\}', '}')
    regex = re.sub(r'\{[^/}]+\}', r'[^/]+', regex)
    return re.compile(f'^{regex}/?$')  # allow optional trailing slash

# Define your map from Swagger path → Enum
ENDPOINT_PATTERNS = {
    "/version": IMRequestType.VERSION,
    "/stats": IMRequestType.GET_IM_SERVER_STATS,
    "/infrastructures": IMRequestType.INFRASTRUCTURE_CHECK_METHOD,
    "/infrastructures/{InfId}": IMRequestType.INFID_CHECK_METHOD,
    "/infrastructures/{InfId}/state": IMRequestType.GET_INFRASTRUCTURE_STATE,
    "/infrastructures/{InfId}/outputs": IMRequestType.GET_INFRASTRUCTURE_OUTPUTS,
    "/infrastructures/{InfId}/contmsg": IMRequestType.GET_INFRASTRUCTURE_CONTEXTUALIZATION_MESSAGE,
    "/infrastructures/{InfId}/data": IMRequestType.EXPORT_INFRASTRUCTURE,
    "/infrastructures/{InfId}/radl": IMRequestType.GET_INFRASTRUCTURE_CREATION_RADL,
    "/infrastructures/{InfId}/tosca": IMRequestType.GET_INFRASTRUCTURE_TOSCA_REPRESENTATION,
    "/infrastructures/{InfId}/authorization": IMRequestType.GET_INFRASTRUCTURE_OWNERS_LIST,
    "/infrastructures/{InfId}/stop": IMRequestType.STOP_INFRASTRUCTURE,
    "/infrastructures/{InfId}/start": IMRequestType.START_INFRASTRUCTURE,
    "/infrastructures/{InfId}/reconfigure": IMRequestType.RECONFIGURE_INFRASTRUCTURE,
    "/infrastructures/{InfId}/vms/{VMId}": IMRequestType.VMS_CHECK_METHOD,
    "/infrastructures/{InfId}/vms/{VMId}/contmsg": IMRequestType.GET_VM_CONTEXTUALIZATION_MESSAGE,
    "/infrastructures/{InfId}/vms/{VMId}/{Property}": IMRequestType.GET_VM_PROPERTY,
    "/infrastructures/{InfId}/vms/{VMId}/stop": IMRequestType.STOP_VM,
    "/infrastructures/{InfId}/vms/{VMId}/start": IMRequestType.START_VM,
    "/infrastructures/{InfId}/vms/{VMId}/reboot": IMRequestType.REBOOT_VM,
    "/infrastructures/{InfId}/vms/{VMId}/disks/{diskNum}/snapshot": IMRequestType.CREATE_DISK_SNAPSHOT,
    "/clouds/{CloudId}/images": IMRequestType.GET_CLOUD_PROVIDER_AVAILABLE_IMAGES_LIST,
    "/clouds/{CloudId}/quotas": IMRequestType.GET_CLOUD_PROVIDER_USER_QUOTAS,
    "/oai": IMRequestType.GET_OAI_PMH_TOSCA_INFO
}

# Precompile the regexes once
COMPILED_PATTERNS = {swagger_endpoint_to_regex(k): v for k, v in ENDPOINT_PATTERNS.items()}

class IMRequestAdapter:
    _header_composers: dict[CloudProviderType, HeaderComposer] = {
        CloudProviderType.OPENSTACK: OpenStackHeaderComposer(),
        CloudProviderType.KUBERNETES: KubernetesHeaderComposer(),
    }

    _im_request_map: dict[IMRequestType, Callable[..., IMBaseRequest]] = {
        IMRequestType.LIST_USER_INFRASTRUCTURES: lambda *a, **kw: ListUserInfrastructures(*a, **kw),
        IMRequestType.CREATE_INFRASTRUCTURE: lambda *a, **kw: CreateInfrastructure(*a, **kw)
    }

    def __init__(self, request: FastAPIRequest):
        self._method = request.method.lower()
        self._auth_header_dict: list[dict[str, str]] = self._parse_im_auth_header(request.headers["Authorization"])
        self._query_parameters = request.query_params
        self._body = self._extract_body(request)
        self._im_request_type: IMRequestType = self._identify_request_type(request.url.path)
        self._credentials: Optional[list[HeaderComposer]] = None

    @staticmethod
    async def _extract_body(request: FastAPIRequest):
        return await request.body()

    @staticmethod
    def _parse_im_auth_header(header_string: str) -> list[dict[str, str]]:
        lines = [line.strip() for line in header_string.split("\n") if line.strip()]
        result = []
        for line in lines:
            pairs = [p.strip() for p in line.split(";") if p.strip()]
            entry = {}
            for pair in pairs:
                if "=" in pair:
                    key, val = pair.split("=", 1)
                    entry[key.strip()] = val.strip().strip("'\"")
            result.append(entry)
        return result

    @property
    def credentials(self) -> list[HeaderComposer]:
        if self._credentials is None:
            for cred in self._auth_header_dict:
                provider_type: CloudProviderType = CloudProviderType(cred["type"].lower())
                composer: HeaderComposer = IMRequestAdapter._header_composers[provider_type]
                composer.load_data(**cred)

    def compose_headers(self, cp_type: CloudProviderType, **kwargs) -> str:
        composer: HeaderComposer = IMRequestAdapter._header_composers[cp_type]
        composer.compose(**kwargs)
        return composer.get_header()

    def _identify_request_type(self, path: str) -> IMRequestType:
        request_type: IMRequestType = IMRequestType.NONE
        for regex, enum_value in COMPILED_PATTERNS.items():
            if regex.match(path):
                request_type = enum_value

        if request_type is IMRequestType.INFRASTRUCTURE_CHECK_METHOD:
            if self._method == "get":
                request_type = IMRequestType.LIST_USER_INFRASTRUCTURES
            elif self._method == "post":
                request_type = IMRequestType.CREATE_INFRASTRUCTURE
            elif self._method == "put":
                request_type = IMRequestType.IMPORT_INFRASTRUCTURE
            else:
                raise ValueError(f"Method {self._method} not implemented for path {path}")
        elif request_type is IMRequestType.INFID_CHECK_METHOD:
            if self._method == "get":
                request_type = IMRequestType.LIST_INFRASTRUCTURE_VMS
            elif self._method == "post":
                request_type = IMRequestType.ADD_RESOURCES_TO_INFRASTRUCTURE
            elif self._method == "delete":
                request_type = IMRequestType.DELETE_INFRASTRUCTURE
            else:
                raise ValueError(f"Method {self._method} not implemented for path {path}")
        elif request_type is IMRequestType.VMS_CHECK_METHOD:
            if self._method == "get":
                request_type = IMRequestType.GET_VM_INFO
            elif self._method == "put":
                request_type = IMRequestType.ALTER_VM
            elif self._method == "delete":
                request_type = IMRequestType.DELETE_VM
            else:
                raise ValueError(f"Method {self._method} not implemented for path {path}")
        else:
            raise ValueError(f"Unkown request type for path {path}")

        return request_type

    @property
    def request(self) -> IMBaseRequest:
        return IMRequestAdapter._im_request_map[self._im_request_type](query_parameters=self._query_parameters,
                                                                       body=self._body)

    @property
    def header(self) -> HeaderComposer:
        return OpenStackHeaderComposer()
