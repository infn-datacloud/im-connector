import enum


class CloudProviderType(str, enum.Enum):
    INFRASTRUCTUREMANAGER = "infrastructuremanager"
    VMRC = "vmrc"
    OPENNEBULA = "opennebula"
    EC2 = "ec2"
    FOGBOW = "fogbow"
    OPENSTACK = "openstack"
    OCCI = "occi"
    LIBCLOUD = "libcloud"
    DOCKER = "docker"
    GCE = "gce"
    AZURE = "azure"
    KUBERNETES = "kubernetes"
    VSPHERE = "vsphere"
    LINODE = "linode"
    ORANGE = "orange"
    EGI = "egi"
    VAULT = "vault"
    LAMBDA = "lambda"
