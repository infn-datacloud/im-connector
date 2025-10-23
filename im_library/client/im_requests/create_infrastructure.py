from typing import Optional

from im_library.client.base_requests import Post


class CreateInfrastructure(Post):
    @property
    def url(self) -> str:
        return f"/infrastructures"
