from typing import Optional

from im_library.client.base_requests import Get


class ListUserInfrastructures(Get):
    def __init__(self, filter: str):
        ...


    @property
    def url(self) -> str:
        # TODO Prendere enum, recuperare url pattern
        # .replace(self._path_parameters.key())
        return f"/infrastructures"
