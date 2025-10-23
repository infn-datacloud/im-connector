from typing import Optional

from im_library.client.base_requests import Get


class ListUserInfrastructures(Get):
    @property
    def url(self) -> str:
        return f"/infrastructures"
