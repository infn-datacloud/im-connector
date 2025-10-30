class IMQueryParametersBase(dict):
    def __init__(self, **kwargs):
        stripped_kwargs: dict = {}
        for k, v in kwargs.items():
            key = k.strip("_")
            stripped_kwargs[key] = v
        super().__init__(**stripped_kwargs)
