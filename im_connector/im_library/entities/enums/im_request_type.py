import enum


class IMRequestType(str, enum.Enum):
    """Enumeration representing all operations supported by the IM."""

    ADD_RESOURCES_TO_INFRASTRUCTURE = "add_resources_to_infrastructure"
    ALTER_VM = "alter_vm"
    CHANGE_INFRASTRUCTURE_AUTHORIZATION_DATA = "change_infrastructure_authorization_data"
    CREATE_DISK_SNAPSHOT = "create_disk_snapshot"
    CREATE_INFRASTRUCTURE = "create_infrastructure"
    DELETE_INFRASTRUCTURE = "delete_infrastructure"
    DELETE_VM = "delete_vm"
    EXPORT_INFRASTRUCTURE = "export_infrastructure"
    GET_CLOUD_PROVIDER_AVAILABLE_IMAGES_LIST = "get_cloud_provider_available_images_list"
    GET_CLOUD_PROVIDER_USER_QUOTAS = "get_cloud_provider_user_quotas"
    GET_IM_SERVER_STATS = "get_im_server_stats"
    GET_INFRASTRUCTURE_CONTEXTUALIZATION_MESSAGE = "get_infrastructure_contextualization_message"
    GET_INFRASTRUCTURE_CREATION_RADL = "get_infrastructure_creation_radl"
    GET_INFRASTRUCTURE_OUTPUTS = "get_infrastructure_outputs"
    GET_INFRASTRUCTURE_OWNERS_LIST = "get_infrastructure_owners_list"
    GET_INFRASTRUCTURE_STATE = "get_infrastructure_state"
    GET_INFRASTRUCTURE_TOSCA_REPRESENTATION = "get_infrastructure_tosca_representation"
    GET_OAI_PMH_TOSCA_INFO = "get_oai_pmh_tosca_info"
    GET_VM_CONTEXTUALIZATION_MESSAGE ="get_vm_contextualization_message"
    GET_VM_INFO = "get_vm_info"
    GET_VM_PROPERTY = "get_vm_property"
    IMPORT_INFRASTRUCTURE = "import_infrastructure"
    LIST_INFRASTRUCTURE_VMS = "list_infrastructure_vms"
    LIST_USER_INFRASTRUCTURES = "list_user_infrastructures"
    REBOOT_VM = "reboot_vm"
    RECONFIGURE_INFRASTRUCTURE =  "reconfigure_infrastructure"
    START_INFRASTRUCTURE =  "start_infrastructure"
    START_VM = "start_vm"
    STOP_INFRASTRUCTURE = "stop_infrastructure"
    STOP_VM = "stop_vm"
    VERSION = "version"

    # Some IM REST API endpoints use the same URL and can only be identified by evaluating the used HTTP verb.
    # The following enum entries are meant to identify such cases, which then require further analysis.
    # This is only used by the IMRequestAdapter workflow.

    INFRASTRUCTURE_CHECK_METHOD = "infrastructure_check_method"
    INFID_CHECK_METHOD = "infid_check_method"
    VMS_CHECK_METHOD = "vms_check_method"
    AUTH_CHECK_METHOD = "auth_check_method"

    NONE = "none"
