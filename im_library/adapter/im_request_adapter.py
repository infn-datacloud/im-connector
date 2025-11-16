from typing import Callable, Optional

from fastapi.requests import Request as FastAPIRequest
from typing_extensions import Any

from im_connector.config import get_settings
from im_library.adapter.im_endpoint_map import IMEndpointMap
from im_library.client.im_requests.add_resources_to_infrastructure import AddResourceToInfrastructurePathParameters, \
    AddResourcesToInfrastructure, AddResourcesToInfrastructureQueryParameters
from im_library.client.im_requests.alter_vm import AlterVMPathParameters, AlterVM
from im_library.client.im_requests.change_infrastructure_authorization_data import \
    ChangeInfrastructureAuthorizationDataPathParameters, ChangeInfrastructureAuthorizationData, \
    ChangeInfrastructureAuthorizationDataQueryParameters
from im_library.client.im_requests.create_disk_snapshot import CreateDiskSnapshot, CreateDiskSnapshotPathParameters, \
    CreateDiskSnapshotQueryParameters
from im_library.client.im_requests.create_infrastructure import CreateInfrastructure, \
    CreateInfrastructureQueryParameters
from im_library.client.im_requests.delete_infrastructure import DeleteInfrastructure, \
    DeleteInfrastructurePathParameters, DeleteInfrastructureQueryParameters
from im_library.client.im_requests.delete_vm import DeleteVM, DeleteVMPathParameters
from im_library.client.im_requests.export_infrastructure import ExportInfrastructure, \
    ExportInfrastructurePathParameters, ExportInfrastructureQueryParameters
from im_library.client.im_requests.get_cloud_provider_available_images_list import GetCloudProviderAvailableImagesList, \
    GetCloudProviderAvailableImagesListPathParameters, GetCloudProviderAvailableImagesListQueryParameters
from im_library.client.im_requests.get_cloud_provider_user_quotas import GetCloudProviderUserQuotas, \
    GetCloudProviderUserQuotasPathParameters
from im_library.client.im_requests.get_im_server_stats import GetIMServerStats, GetIMServerStatsQueryParameters
from im_library.client.im_requests.get_infrastructure_contextualization_message import \
    GetInfrastructureContextualizationMessage, GetInfrastructureContextualizationMessagePathParameters, \
    GetInfrastructureContextualizationMessageQueryParameters
from im_library.client.im_requests.get_infrastructure_creation_radl import GetInfrastructureCreationRadl, \
    GetInfrastructureCreationRadlPathParameters
from im_library.client.im_requests.get_infrastructure_outputs import GetInfrastructureOutputs, \
    GetInfrastructureOutputsPathParameters
from im_library.client.im_requests.get_infrastructure_owners_list import GetInfrastructureOwnersList, \
    GetInfrastructureOwnersListPathParameters
from im_library.client.im_requests.get_infrastructure_state import GetInfrastructureState, \
    GetInfrastructureStatePathParameters
from im_library.client.im_requests.get_infrastructure_tosca_representation import GetInfrastructureToscaRepresentation, \
    GetInfrastructureToscaRepresentationPathParameters
from im_library.client.im_requests.get_oai_pmh_tosca_info import GetOAIPMHToscaInfo
from im_library.client.im_requests.get_vm_contextualization_message import GetVMContextualizationMessage, \
    GetVMContextualizationMessagePathParameters
from im_library.client.im_requests.get_vm_info import GetVMInfo, GetVMInfoPathParameters
from im_library.client.im_requests.get_vm_property import GetVMProperty, GetVMPropertyPathParameters
from im_library.client.im_requests.import_infrastructure import ImportInfrastructure
from im_library.client.im_requests.list_infrastructure_vms import ListInfrastructureVms, \
    ListInfrastructureVmsPathParameters
from im_library.client.im_requests.list_user_infrastructures import ListUserInfrastructures, \
    ListUserInfrastructuresQueryParameters
from im_library.client.im_requests.reboot_vm import RebootVM, RebootVMPathParameters
from im_library.client.im_requests.reconfigure_infrastructure import ReconfigureInfrastructure, \
    ReconfigureInfrastructurePathParameters, ReconfigureInfrastructureQueryParameters
from im_library.client.im_requests.start_infrastructure import StartInfrastructure, StartInfrastructurePathParameters
from im_library.client.im_requests.start_vm import StartVM, StartVMPathParameters
from im_library.client.im_requests.stop_infrastructure import StopInfrastructure, StopInfrastructurePathParameters
from im_library.client.im_requests.stop_vm import StopVM, StopVMPathParameters
from im_library.client.im_requests.version import Version
from im_library.entities.enums.cloud_provider_type import CloudProviderType
from im_library.entities.enums.im_request_type import IMRequestType
from im_library.entities.im_base_requests import IMBaseRequest
from im_library.entities.im_request_parameters import IMPathParametersBase, IMQueryParametersBase
from im_library.header.credential_components.infrastructure_manager_credential import \
    InfrastructureManagerCredentialComponent
from im_library.header.credential_components.kubernetes_credential import KubernetesCredentialComponent
from im_library.header.credential_components.openstack_credential import OpenStackCredentialComponent
from im_library.header.im_credential_component_base import IMCredentialComponentBase
from im_library.header.im_header_composer import IMHeaderComposer
from im_library.logging.logger import get_logger

settings = get_settings()
logger = get_logger(settings)


class IMRequestAdapter:
    _headers: dict[CloudProviderType, Callable[..., IMCredentialComponentBase]] = {
        CloudProviderType.INFRASTRUCTUREMANAGER: lambda **kw: InfrastructureManagerCredentialComponent(**kw),
        CloudProviderType.OPENSTACK: lambda **kw: OpenStackCredentialComponent(**kw),
        CloudProviderType.KUBERNETES: lambda **kw: KubernetesCredentialComponent(**kw),
    }

    _im_request_map: dict[IMRequestType, Callable[..., IMBaseRequest]] = {
        IMRequestType.ADD_RESOURCES_TO_INFRASTRUCTURE: lambda **kw: AddResourcesToInfrastructure(**kw),
        IMRequestType.ALTER_VM: lambda **kw: AlterVM(**kw),
        IMRequestType.CHANGE_INFRASTRUCTURE_AUTHORIZATION_DATA: lambda **kw: ChangeInfrastructureAuthorizationData(
            **kw),
        IMRequestType.CREATE_DISK_SNAPSHOT: lambda **kw: CreateDiskSnapshot(**kw),
        IMRequestType.CREATE_INFRASTRUCTURE: lambda **kw: CreateInfrastructure(**kw),
        IMRequestType.DELETE_INFRASTRUCTURE: lambda **kw: DeleteInfrastructure(**kw),
        IMRequestType.DELETE_VM: lambda **kw: DeleteVM(**kw),
        IMRequestType.EXPORT_INFRASTRUCTURE: lambda **kw: ExportInfrastructure(**kw),
        IMRequestType.GET_CLOUD_PROVIDER_AVAILABLE_IMAGES_LIST: lambda **kw: GetCloudProviderAvailableImagesList(**kw),
        IMRequestType.GET_CLOUD_PROVIDER_USER_QUOTAS: lambda **kw: GetCloudProviderUserQuotas(**kw),
        IMRequestType.GET_IM_SERVER_STATS: lambda **kw: GetIMServerStats(**kw),
        IMRequestType.GET_INFRASTRUCTURE_CONTEXTUALIZATION_MESSAGE: lambda
            **kw: GetInfrastructureContextualizationMessage(**kw),
        IMRequestType.GET_INFRASTRUCTURE_CREATION_RADL: lambda **kw: GetInfrastructureCreationRadl(**kw),
        IMRequestType.GET_INFRASTRUCTURE_OUTPUTS: lambda **kw: GetInfrastructureOutputs(**kw),
        IMRequestType.GET_INFRASTRUCTURE_OWNERS_LIST: lambda **kw: GetInfrastructureOwnersList(**kw),
        IMRequestType.GET_INFRASTRUCTURE_STATE: lambda **kw: GetInfrastructureState(**kw),
        IMRequestType.GET_INFRASTRUCTURE_TOSCA_REPRESENTATION: lambda **kw: GetInfrastructureToscaRepresentation(**kw),
        IMRequestType.GET_OAI_PMH_TOSCA_INFO: lambda **kw: GetOAIPMHToscaInfo(**kw),
        IMRequestType.GET_VM_CONTEXTUALIZATION_MESSAGE: lambda **kw: GetVMContextualizationMessage(**kw),
        IMRequestType.GET_VM_INFO: lambda **kw: GetVMInfo(**kw),
        IMRequestType.GET_VM_PROPERTY: lambda **kw: GetVMProperty(**kw),
        IMRequestType.IMPORT_INFRASTRUCTURE: lambda **kw: ImportInfrastructure(**kw),
        IMRequestType.LIST_INFRASTRUCTURE_VMS: lambda **kw: ListInfrastructureVms(**kw),
        IMRequestType.LIST_USER_INFRASTRUCTURES: lambda **kw: ListUserInfrastructures(**kw),
        IMRequestType.REBOOT_VM: lambda **kw: RebootVM(**kw),
        IMRequestType.RECONFIGURE_INFRASTRUCTURE: lambda **kw: ReconfigureInfrastructure(**kw),
        IMRequestType.START_INFRASTRUCTURE: lambda **kw: StartInfrastructure(**kw),
        IMRequestType.START_VM: lambda **kw: StartVM(**kw),
        IMRequestType.STOP_INFRASTRUCTURE: lambda **kw: StopInfrastructure(**kw),
        IMRequestType.STOP_VM: lambda **kw: StopVM(**kw),
        IMRequestType.VERSION: lambda **kw: Version(**kw)
    }

    _im_path_parameters_map: dict[IMRequestType, Optional[Callable[..., IMPathParametersBase]]] = {
        IMRequestType.ADD_RESOURCES_TO_INFRASTRUCTURE: lambda **kw: AddResourceToInfrastructurePathParameters(**kw),
        IMRequestType.ALTER_VM: lambda **kw: AlterVMPathParameters(**kw),
        IMRequestType.CHANGE_INFRASTRUCTURE_AUTHORIZATION_DATA: lambda
            **kw: ChangeInfrastructureAuthorizationDataPathParameters(**kw),
        IMRequestType.CREATE_DISK_SNAPSHOT: lambda **kw: CreateDiskSnapshotPathParameters(**kw),
        IMRequestType.CREATE_INFRASTRUCTURE: None,
        IMRequestType.DELETE_INFRASTRUCTURE: lambda **kw: DeleteInfrastructurePathParameters(**kw),
        IMRequestType.DELETE_VM: lambda **kw: DeleteVMPathParameters(**kw),
        IMRequestType.EXPORT_INFRASTRUCTURE: lambda **kw: ExportInfrastructurePathParameters(**kw),
        IMRequestType.GET_CLOUD_PROVIDER_AVAILABLE_IMAGES_LIST: lambda
            **kw: GetCloudProviderAvailableImagesListPathParameters(**kw),
        IMRequestType.GET_CLOUD_PROVIDER_USER_QUOTAS: lambda **kw: GetCloudProviderUserQuotasPathParameters(**kw),
        IMRequestType.GET_IM_SERVER_STATS: None,
        IMRequestType.GET_INFRASTRUCTURE_CONTEXTUALIZATION_MESSAGE: lambda
            **kw: GetInfrastructureContextualizationMessagePathParameters(**kw),
        IMRequestType.GET_INFRASTRUCTURE_CREATION_RADL: lambda **kw: GetInfrastructureCreationRadlPathParameters(**kw),
        IMRequestType.GET_INFRASTRUCTURE_OUTPUTS: lambda **kw: GetInfrastructureOutputsPathParameters(**kw),
        IMRequestType.GET_INFRASTRUCTURE_OWNERS_LIST: lambda **kw: GetInfrastructureOwnersListPathParameters(**kw),
        IMRequestType.GET_INFRASTRUCTURE_STATE: lambda **kw: GetInfrastructureStatePathParameters(**kw),
        IMRequestType.GET_INFRASTRUCTURE_TOSCA_REPRESENTATION: lambda
            **kw: GetInfrastructureToscaRepresentationPathParameters(**kw),
        IMRequestType.GET_OAI_PMH_TOSCA_INFO: None,
        IMRequestType.GET_VM_CONTEXTUALIZATION_MESSAGE: lambda **kw: GetVMContextualizationMessagePathParameters(**kw),
        IMRequestType.GET_VM_INFO: lambda **kw: GetVMInfoPathParameters(**kw),
        IMRequestType.GET_VM_PROPERTY: lambda **kw: GetVMPropertyPathParameters(**kw),
        IMRequestType.IMPORT_INFRASTRUCTURE: None,
        IMRequestType.LIST_INFRASTRUCTURE_VMS: lambda **kw: ListInfrastructureVmsPathParameters(**kw),
        IMRequestType.LIST_USER_INFRASTRUCTURES: None,
        IMRequestType.REBOOT_VM: lambda **kw: RebootVMPathParameters(**kw),
        IMRequestType.RECONFIGURE_INFRASTRUCTURE: lambda **kw: ReconfigureInfrastructurePathParameters(**kw),
        IMRequestType.START_INFRASTRUCTURE: lambda **kw: StartInfrastructurePathParameters(**kw),
        IMRequestType.START_VM: lambda **kw: StartVMPathParameters(**kw),
        IMRequestType.STOP_INFRASTRUCTURE: lambda **kw: StopInfrastructurePathParameters(**kw),
        IMRequestType.STOP_VM: lambda **kw: StopVMPathParameters(**kw),
        IMRequestType.VERSION: None
    }

    _im_query_parameters_map: dict[IMRequestType, Optional[Callable[..., IMQueryParametersBase]]] = {
        IMRequestType.ADD_RESOURCES_TO_INFRASTRUCTURE: lambda **kw: AddResourcesToInfrastructureQueryParameters(**kw),
        IMRequestType.ALTER_VM: None,
        IMRequestType.CHANGE_INFRASTRUCTURE_AUTHORIZATION_DATA: lambda
            **kw: ChangeInfrastructureAuthorizationDataQueryParameters(**kw),
        IMRequestType.CREATE_DISK_SNAPSHOT: lambda **kw: CreateDiskSnapshotQueryParameters(**kw),
        IMRequestType.CREATE_INFRASTRUCTURE: lambda **kw: CreateInfrastructureQueryParameters(**kw),
        IMRequestType.DELETE_INFRASTRUCTURE: lambda **kw: DeleteInfrastructureQueryParameters(**kw),
        IMRequestType.DELETE_VM: None,
        IMRequestType.EXPORT_INFRASTRUCTURE: lambda **kw: ExportInfrastructureQueryParameters(**kw),
        IMRequestType.GET_CLOUD_PROVIDER_AVAILABLE_IMAGES_LIST: lambda
            **kw: GetCloudProviderAvailableImagesListQueryParameters(**kw),
        IMRequestType.GET_CLOUD_PROVIDER_USER_QUOTAS: None,
        IMRequestType.GET_IM_SERVER_STATS: lambda **kw: GetIMServerStatsQueryParameters(**kw),
        IMRequestType.GET_INFRASTRUCTURE_CONTEXTUALIZATION_MESSAGE: lambda
            **kw: GetInfrastructureContextualizationMessageQueryParameters(**kw),
        IMRequestType.GET_INFRASTRUCTURE_CREATION_RADL: None,
        IMRequestType.GET_INFRASTRUCTURE_OUTPUTS: None,
        IMRequestType.GET_INFRASTRUCTURE_OWNERS_LIST: None,
        IMRequestType.GET_INFRASTRUCTURE_STATE: None,
        IMRequestType.GET_INFRASTRUCTURE_TOSCA_REPRESENTATION: None,
        IMRequestType.GET_OAI_PMH_TOSCA_INFO: None,
        IMRequestType.GET_VM_CONTEXTUALIZATION_MESSAGE: None,
        IMRequestType.GET_VM_INFO: None,
        IMRequestType.GET_VM_PROPERTY: None,
        IMRequestType.IMPORT_INFRASTRUCTURE: None,
        IMRequestType.LIST_INFRASTRUCTURE_VMS: None,
        IMRequestType.LIST_USER_INFRASTRUCTURES: lambda **kw: ListUserInfrastructuresQueryParameters(**kw),
        IMRequestType.REBOOT_VM: None,
        IMRequestType.RECONFIGURE_INFRASTRUCTURE: lambda **kw: ReconfigureInfrastructureQueryParameters(**kw),
        IMRequestType.START_INFRASTRUCTURE: None,
        IMRequestType.START_VM: None,
        IMRequestType.STOP_INFRASTRUCTURE: None,
        IMRequestType.STOP_VM: None,
        IMRequestType.VERSION: None
    }

    def __init__(self, request: FastAPIRequest, request_body: Any):
        self._im_request_type: IMRequestType = IMEndpointMap.identify_request_type(request.url.path, request.method)
        self._query_parameters = IMEndpointMap.sanitize_query_params(request.query_params)
        self._path_parameters = IMEndpointMap.extract_path_params(request.url.path)
        self._body = request_body
        self._header_composer: IMHeaderComposer = self._populate_header_composer(request.headers)

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
        logger.info(f"[ADAPTER]: identified credentials for {[x["type"] for x in result]}.")
        return result

    def _populate_header_composer(self, headers) -> IMHeaderComposer:
        auth_header_dict: list[dict[str, str]] = self._parse_im_auth_header(headers["Authorization"])
        composer = IMHeaderComposer()
        for cred in auth_header_dict:
            provider_type: CloudProviderType = CloudProviderType(cred["type"])
            header: IMCredentialComponentBase = IMRequestAdapter._headers[provider_type](**cred)
            composer.add_credential(header)
        for header_name, header_value in headers.items():
            if header_name.lower() != "authorization":
                composer.add_header(header_name, header_value)
        return composer

    @property
    def request(self) -> IMBaseRequest:
        request_args = {}

        path_parameters = IMRequestAdapter._im_path_parameters_map[self._im_request_type]
        if path_parameters is not None:
            path_parameters_dataclass: Optional[IMPathParametersBase] = path_parameters(**self._path_parameters)
            request_args["path_parameters"] = path_parameters_dataclass

        if len(self._body) > 0:
            request_args["body"] = self._body

        query_parameters = IMRequestAdapter._im_query_parameters_map[self._im_request_type]
        if query_parameters is not None:
            query_parameters_dataclass: Optional[IMQueryParametersBase] = query_parameters(**self._query_parameters)
            request_args["query_parameters"] = query_parameters_dataclass

        logger.info(
            f"[ADAPTER]: request type {self._im_request_type} requirese these arguments: {request_args.keys()}.")
        return IMRequestAdapter._im_request_map[self._im_request_type](**request_args)

    @property
    def header(self) -> IMHeaderComposer:
        return self._header_composer
