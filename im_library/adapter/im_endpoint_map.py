import re

from starlette.datastructures import QueryParams

from im_library.entities.enums.im_request_type import IMRequestType


def swagger_endpoint_to_regex(swagger_path: str) -> re.Pattern:
    """Convert a Swagger-like path (with {param}) into a regex pattern."""
    regex = re.escape(swagger_path)
    regex = regex.replace(r'\{', '{').replace(r'\}', '}')
    regex = re.sub(r'\{[^/}]+\}', r'[^/]+', regex)
    return re.compile(f'^{regex}/?$')  # allow optional trailing slash


class IMEndpointMap:
    _endpoint_patterns = {
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
        "/infrastructures/{InfId}/authorization": IMRequestType.AUTH_CHECK_METHOD,
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

    _compiled_patterns = {swagger_endpoint_to_regex(k): v for k, v in _endpoint_patterns.items()}

    @classmethod
    def identify_request_type(cls, path: str, method: str) -> IMRequestType:
        request_type: IMRequestType = IMRequestType.NONE
        for regex, enum_value in IMEndpointMap._compiled_patterns.items():
            if regex.match(path):
                request_type = enum_value

        if request_type is IMRequestType.INFRASTRUCTURE_CHECK_METHOD:
            if method == "GET":
                request_type = IMRequestType.LIST_USER_INFRASTRUCTURES
            elif method == "POST":
                request_type = IMRequestType.CREATE_INFRASTRUCTURE
            elif method == "PUT":
                request_type = IMRequestType.IMPORT_INFRASTRUCTURE
            else:
                raise ValueError(f"Method {method} not implemented for path {path}")
        elif request_type is IMRequestType.INFID_CHECK_METHOD:
            if method == "GET":
                request_type = IMRequestType.LIST_INFRASTRUCTURE_VMS
            elif method == "POST":
                request_type = IMRequestType.ADD_RESOURCES_TO_INFRASTRUCTURE
            elif method == "DELETE":
                request_type = IMRequestType.DELETE_INFRASTRUCTURE
            else:
                raise ValueError(f"Method {method} not implemented for path {path}")
        elif request_type is IMRequestType.AUTH_CHECK_METHOD:
            if method == "GET":
                request_type = IMRequestType.GET_INFRASTRUCTURE_OWNERS_LIST
            elif method == "POST":
                request_type = IMRequestType.CHANGE_INFRASTRUCTURE_AUTHORIZATION_DATA
            else:
                raise ValueError(f"Method {method} not implemented for path {path}")
        elif request_type is IMRequestType.VMS_CHECK_METHOD:
            if method == "GET":
                request_type = IMRequestType.GET_VM_INFO
            elif method == "PUT":
                request_type = IMRequestType.ALTER_VM
            elif method == "DELETE":
                request_type = IMRequestType.DELETE_VM
            else:
                raise ValueError(f"Method {method} not implemented for path {path}")
        elif request_type is IMRequestType.NONE:
            raise ValueError(f"Unknown request type for path {path}")

        return request_type

    @classmethod
    def extract_path_params(cls, path: str) -> dict:
        for pattern in IMEndpointMap._endpoint_patterns.keys():
            regex_pattern = re.sub(r"\{(\w+)\}", r"(?P<\1>[^/]+)", pattern)
            regex_pattern = f"^{regex_pattern}$"
            match = re.match(regex_pattern, path)
            if match:
                return match.groupdict()  # dict of {param_name: value}
        return {}

    @classmethod
    def sanitize_query_params(cls, query: QueryParams) -> dict:
        sanitized_query_params = {}
        for k, v in query.items():
            if k in {"async"}:
                sanitized_query_params[k + "_"] = v
            else:
                sanitized_query_params[k] = v
        return sanitized_query_params