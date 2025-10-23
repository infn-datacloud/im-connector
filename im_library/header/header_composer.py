import abc

class HeaderComposer(metaclass=abc.ABCMeta):
    def __init__(self):
        self._headers: list[str] = []

    @abc.abstractmethod
    def load_data(self, **kwargs):
        ...

    @abc.abstractmethod
    def get_header(self) -> str:
        ...
