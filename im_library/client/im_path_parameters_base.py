import dataclasses


@dataclasses.dataclass(kw_only=True)
class IMPathParametersBase:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)