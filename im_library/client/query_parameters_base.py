class QueryParametersBase(dict):
    def __init__(self, **kwargs):
        stripped_kwargs: dict = {}
        for k, v in kwargs:
            key = k.strip("_")
            stripped_kwargs[key] = v
        super().__init__(**stripped_kwargs)
