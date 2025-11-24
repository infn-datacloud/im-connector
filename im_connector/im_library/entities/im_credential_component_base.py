import abc
from typing import Optional

from im_connector.im_library.entities.enums.cloud_provider_type import CloudProviderType


class IMCredentialComponentBase(metaclass=abc.ABCMeta):
    """Base abstact class representing an IM credential."""

    @abc.abstractmethod
    def __init__(self, *,
                 id: str,
                 type: str,
                 username: Optional[str] = None,
                 password: Optional[str] = None,
                 host: Optional[str] = None,
                 token: Optional[str] = None,
                 proxy: Optional[str] = None,
                 **kwargs):
        ...

    @property
    def header_type(self) -> CloudProviderType:
        """Credential header type, e.f. InfrastructureManager or Kubernetes.

        Returns:
            CloudProviderType: enum entry representing the cloud provider associated to the credential.

        """

        return CloudProviderType(self.type)

    def serialize(self) -> str:
        """Serialize the credential to a string, as specified by the IM documentation.

        Returns:
            str: the serialized credential header.

        """

        parts = []
        for key, value in self.__dict__.items():
            if value is not None:
                parts.append(f"{key} = {value}")
        return " ; ".join(parts)
