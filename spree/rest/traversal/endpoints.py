import re

from pyramid import httpexceptions


class APIEndpoint(object):
    """
    :cvar endpoints Map of child endpoints
    :type endpoints list[(str, APIEndpoint)]
    """
    endpoints = []
    schema = None

    def __init__(self, parent, ref, *args, **kwargs):
        self.__name__ = ref
        self.__parent__ = parent
        self.ref = ref

    def __getitem__(self, item: str):
        for ep in self.endpoints:
            ep_rex, ep_callable = ep
            # We can match by literal string or regexp pattern
            if re.search(ep_rex, item) is not None:
                return ep_callable(self, item)
        raise KeyError('API Endpoint could not be matched')

    def deserialize(self, request, schema=None):
        """
        :type request: pyramid.request.Request
        :param schema:
        :return:
        """
        if not request.body:
            return None

        if schema is None:
            schema = self.schema

        if schema:
            return schema(strict=True, context={
                'node': self,
                'request': request
            }).load(request.json_body)
        return request.json_body


class APIAction(APIEndpoint):

    def __init__(self, *args, **kwargs):
        super(APIAction, self).__init__(*args, **kwargs)

    def get(self, request):
        raise httpexceptions.HTTPMethodNotAllowed()

    def post(self, request, deserialized):
        raise httpexceptions.HTTPMethodNotAllowed()

    def put(self, request, deserialized):
        raise httpexceptions.HTTPMethodNotAllowed()

    def delete(self, request, deserialized):
        raise httpexceptions.HTTPMethodNotAllowed()


class APIResource(APIEndpoint):

    def retrieve(self, request):
        raise NotImplementedError

    def serialize(self, data):
        if self.schema:
            return self.schema(many=isinstance(data, list)).dump(data)
        return data


class APICollection(APIResource):

    create_schema = None

    def retrieve(self, request):
        raise NotImplementedError

    def create(self, request, deserialized):
        raise NotImplementedError

    def before_create(self, request, deserialized):
        pass

    def after_create(self, request, created, deserialized):
        pass


class APIEntity(APIResource):

    update_schema = None

    def retrieve(self, request):
        raise NotImplementedError

    def update(self, request, deserialized):
        raise NotImplementedError

    def before_update(self, request, deserialized):
        pass

    def after_update(self, request, updated, deserialized):
        pass

    def delete(self, request):
        pass
