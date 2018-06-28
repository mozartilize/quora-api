class RowProxyMock:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __getitem__(self, k):
        if hasattr(self, k):
            return getattr(self, k)
        else:
            raise AttributeError
