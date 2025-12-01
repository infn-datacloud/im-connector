import enum


class CloudProviderType(str, enum.Enum):
    """Enumeration representing all the Cloud Providers supported by the IM."""

    INFRASTRUCTUREMANAGER = "InfrastructureManager"
    VMRC = "VMRC"
    OPENNEBULA = "OpenNebula"
    EC2 = "EC2"
    FOGBOW = "FogBow"
    OPENSTACK = "OpenStack"
    OCCI = "OCCI"
    LIBCLOUD = "LibCloud"
    DOCKER = "Docker"
    GCE = "GCE"
    AZURE = "Azure"
    KUBERNETES = "Kubernetes"
    VSPHERE = "vSphere"
    LINODE = "Linode"
    ORANGE = "Orange"
    EGI = "EGI"
    VAULT = "Vault"
    LAMBDA = "Lambda"
