import abc
from typing import Optional

from im_library.entities.enums.cloud_provider_type import CloudProviderType


class IMCredentialComponentBase(metaclass=abc.ABCMeta):
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
        return CloudProviderType(self.type)

    def serialize(self) -> str:
        parts = []
        for key, value in self.__dict__.items():
            if value is not None:
                parts.append(f"{key} = {value}")
        return " ; ".join(parts)
