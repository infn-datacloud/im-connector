from im_library.header.header_composer import HeaderComposer


class KubernetesHeaderComposer(HeaderComposer):
    def _compose(self, *,
                 id: str,
                 type: str,
                 host: str,
                 username: str,
                 password: str,
                 proxy: str,
                 token: str,
                 **kwargs):
        pass

    def get_header(self) -> str:
        pass