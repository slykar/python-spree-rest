"""
Pyramid views (controllers in the classical meaning) for traversal resources.

Each class of :class:`spree.rest.traversal.APIResource`
and :class:`spree.rest.traversal.APIAction` defines it's own view.
"""
from marshmallow import ValidationError, MarshalResult

from . import events

from .endpoints import (
    APICollection,
    APIEntity,
    APIAction
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
    :type context: APIEntity|APICollection
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


class TraversalResourceView(object):

    def __init__(self, context, request):
        """
        Create a Traversal REST view.
        :param context: API endpoint context
        :type context: APIEntity|APICollection
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

        # ========== BEFORE EVENTS =========

        self.context.before_create(
            request=self.request,
            deserialized=deserialized
        )
        # noinspection PyCallByClass,PyTypeChecker
        self.request.registry.notify(events.BeforeCreate(
            view=self,
            deserialized=deserialized
        ))

        # ========== CREATE CALL ==========

        created = self.context.create(self.request, deserialized)

        # ========== AFTER EVENTS ==========

        self.context.after_create(
            request=self.request,
            created=created,
            deserialized=deserialized
        )
        # noinspection PyCallByClass,PyTypeChecker
        self.request.registry.notify(events.AfterCreate(
            view=self,
            created=created,
            deserialized=deserialized
        ))

        # ========== SERIALIZE ==========

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

        # ========== BEFORE EVENTS =========

        self.context.before_update(
            request=self.request,
            deserialized=deserialized
        )
        # noinspection PyCallByClass,PyTypeChecker
        self.request.registry.notify(events.BeforeUpdate(
            view=self,
            deserialized=deserialized
        ))

        # ========== UPDATE CALL ==========

        updated = self.context.update(self.request, deserialized)

        # ========== AFTER EVENTS ==========

        self.context.after_update(
            request=self.request,
            updated=updated,
            deserialized=deserialized
        )
        # noinspection PyCallByClass,PyTypeChecker
        self.request.registry.notify(events.AfterUpdate(
            view=self,
            updated=updated,
            deserialized=deserialized
        ))

        # ========== SERIALIZE ==========

        serialized = self.context.serialize(updated)
        return get_serialized_data(serialized)

    def entity_delete(self):
        """
        Process DELETE requests on :class:`APIEntityEndpoint`
        :rtype: dict
        """
        raise NotImplementedError


class TraversalActionView(object):

    def __init__(self, context, request):
        """
        :type context: APIAction
        :type request: pyramid.request.Request
        """
        self.context = context
        self.request = request

    def _method(self, method):
        deserialized = self.context.deserialize(self.request)
        result = getattr(self.context, method)(self.request, deserialized)
        return get_serialized_data(result)

    def get(self):
        result = self.context.get(self.request)
        return get_serialized_data(result)

    def post(self):
        return self._method('post')

    def put(self):
        return self._method('put')

    def delete(self):
        return self._method('delete')


def includeme(config):
    """
    Include traversal view configuration
    :param config:
    """

    # # # # # # # # # # # #
    #     APIResource     #
    # # # # # # # # # # # #

    config.add_view(
        TraversalResourceView, attr='collection_get',
        request_method='GET', context=APICollection,
        renderer='json', permission='view'
    )
    config.add_view(
        TraversalResourceView, attr='collection_post',
        request_method='POST', context=APICollection,
        renderer='json', permission='create'
    )
    config.add_view(
        TraversalResourceView, attr='entity_get',
        request_method='GET', context=APIEntity,
        renderer='json', permission='view'
    )
    config.add_view(
        TraversalResourceView, attr='entity_put',
        request_method='PUT', context=APIEntity,
        renderer='json', permission='update'
    )

    # # # # # # # # # # # #
    #      APIAction      #
    # # # # # # # # # # # #

    config.add_view(
        TraversalActionView, attr='get',
        request_method='GET', context=APIAction,
        renderer='json', permission='view'
    )
    config.add_view(
        TraversalActionView, attr='post',
        request_method='POST', context=APIAction,
        renderer='json', permission='create'
    )
    config.add_view(
        TraversalActionView, attr='put',
        request_method='PUT', context=APIAction,
        renderer='json', permission='update'
    )
    config.add_view(
        TraversalActionView, attr='delete',
        request_method='DELETE', context=APIAction,
        renderer='json', permission='delete'
    )

    # # # # # # # # # # # #
    #   ValidationError   #
    # # # # # # # # # # # #

    config.add_view(
        validation_error_view, context=ValidationError,
        renderer='json'
    )
