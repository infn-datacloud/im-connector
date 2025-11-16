import dataclasses


@dataclasses.dataclass(kw_only=True)
class IMParametersBase:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_dict(self) -> dict[str, str]:
        dataclass_dict = dataclasses.asdict(self)
        stripped_dataclass_dict = {}

        for k, v in dataclass_dict.items():
            key = k.strip("_")
            stripped_dataclass_dict[key] = v

        return stripped_dataclass_dict


@dataclasses.dataclass(kw_only=True)
class IMQueryParametersBase(IMParametersBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@dataclasses.dataclass(kw_only=True)
class IMPathParametersBase(IMParametersBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
