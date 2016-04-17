from marshmallow import ValidationError, MarshalResult

from spree.rest.traversal import (
    APICollectionEndpoint,
    APIEntityEndpoint
)
from pyramid import httpexceptions


def validation_error_view(error, request):
    """
    Return Marshmallow :class:`ValidationError`
    as a JSON response with a proper response code.
    :param error: Marshmallow error instance
    :type error: ValidationError
    :param request: Pyramid request
    :type request: pyramid.request.Request
    :return: Error messages
    :rtype: dict[str,list]
    """
    request.response.status_int = 400
    return error.messages


def get_serialized_data(serialized):
    if isinstance(serialized, MarshalResult):
        return serialized.data
    return serialized


def process_get_request(context, request):
    """
    Process GET requests on either :class:`APICollectionEndpoint`
    or :class:`APIEntityEndpoint`
    :param context: API endpoint context
    :type context: APIEntityEndpoint|APICollectionEndpoint
    :param request: Pyramid request
    :type request: pyramid.request.Request
    :return: Serialization result, most likely a :class:`dict`
    :rtype: dict
    """
    retrieved = context.retrieve(request)

    if retrieved is None:
        raise httpexceptions.HTTPNotFound()

    serialized = context.serialize(retrieved)
    return get_serialized_data(serialized)


class TraversalRESTView(object):

    def __init__(self, context, request):
        """
        Create a Traversal REST view.
        :param context: API endpoint context
        :type context: APIEntityEndpoint|APICollectionEndpoint
        :param request: Pyramid request
        :type request: pyramid.request.Request
        """
        self.request = request
        self.context = context

    def collection_get(self):
        """
        Process GET requests on :class:`APICollectionEndpoint`
        :rtype: dict
        """
        return process_get_request(self.context, self.request)

    def collection_post(self):
        """
        Process POST requests on :class:`APICollectionEndpoint`
        :returns: POST action result
        :rtype: dict
        """
        deserialized = self.context.deserialize(self.request, self.context.create_schema)
        created = self.context.create(self.request, deserialized)
        serialized = self.context.serialize(created)
        return get_serialized_data(serialized)

    def entity_get(self):
        """
        Process GET requests on :class:`APIEntityEndpoint`
        :rtype: dict
        """
        return process_get_request(self.context, self.request)

    def entity_put(self):
        """
        Process PUT requests on :class:`APIEntityEndpoint`
        :rtype: dict
        """
        deserialized = self.context.deserialize(self.request, self.context.update_schema)
        updated = self.context.update(self.request, deserialized)
        serialized = self.context.serialize(updated)
        return get_serialized_data(serialized)

    def entity_delete(self):
        """
        Process DELETE requests on :class:`APIEntityEndpoint`
        :rtype: dict
        """
        raise NotImplementedError


def includeme(config):
    config.add_view(
        TraversalRESTView, attr='collection_get',
        request_method='GET', context=APICollectionEndpoint,
        renderer='json', permission='view'
    )
    config.add_view(
        TraversalRESTView, attr='collection_post',
        request_method='POST', context=APICollectionEndpoint,
        renderer='json', permission='create'
    )
    config.add_view(
        TraversalRESTView, attr='entity_get',
        request_method='GET', context=APIEntityEndpoint,
        renderer='json', permission='view'
    )
    config.add_view(
        TraversalRESTView, attr='entity_put',
        request_method='PUT', context=APIEntityEndpoint,
        renderer='json', permission='view'
    )
    config.add_view(
        validation_error_view, context=ValidationError,
        renderer='json'
    )
