import re


class APIEndpoint(dict):
    """
    :cvar endpoints Map of child endpoints
    :type endpoints list[(str, APIEndpoint)]
    """
    endpoints = []

    def __init__(self, parent, ref, *args, **kwargs):
        self.__name__ = ref
        self.__parent__ = parent
        self.ref = ref
        super().__init__(*args, **kwargs)

    def __getitem__(self, item: str):
        for ep in self.endpoints:
            ep_rex, ep_callable = ep
            # We can match by literal string or regexp pattern
            if re.search(ep_rex, item) is not None:
                return ep_callable(self, item)
        raise KeyError('API Endpoint could not be matched')

    def retrieve(self, request):
        raise NotImplementedError


class APICollectionEndpoint(APIEndpoint):
    def retrieve(self, request):
        raise NotImplementedError

    def create(self, request):
        raise NotImplementedError


class APIEntityEndpoint(APIEndpoint):
    def retrieve(self, request):
        raise NotImplementedError

    def update(self, request):
        pass
