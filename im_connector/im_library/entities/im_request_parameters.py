import dataclasses


@dataclasses.dataclass(kw_only=True)
class IMParametersBase:
    """Base abstract class wrapping python's builtin dict.

    Dataclass behaviour is added to enforce the required attributes when the concrete objects are created."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_dict(self) -> dict[str, str]:
        """Dict containing key:value pair of query or path parameters. This allows serialization to JSON."""

        dataclass_dict = dataclasses.asdict(self)
        stripped_dataclass_dict = {}

        for k, v in dataclass_dict.items():
            key = k.strip("_")
            stripped_dataclass_dict[key] = v

        return stripped_dataclass_dict


@dataclasses.dataclass(kw_only=True)
class IMQueryParametersBase(IMParametersBase):
    """Intermediate base class serving as base class for all query parameters objects."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@dataclasses.dataclass(kw_only=True)
class IMPathParametersBase(IMParametersBase):
    """Intermediate base class serving as base class for all path parameters objects."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
