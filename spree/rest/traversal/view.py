from spree.rest.traversal import (
    APICollectionEndpoint,
    APIEntityEndpoint
)
from pyramid import httpexceptions, view


def process_get_request(context, request):
    if hasattr(context, 'retrieve'):
        retrieve_result = context.retrieve(request)
    else:
        retrieve_result = None

    if retrieve_result is None:
        raise httpexceptions.HTTPNotFound()

    if hasattr(context, 'serialize'):
        retrieve_result = context.serialize(retrieve_result)

    return retrieve_result


class TraversalRESTView(object):

    def __init__(self, context, request):
        self.request = request
        self.context = context

    def collection_get(self):
        return process_get_request(self.context, self.request)

    def entity_get(self):
        return process_get_request(self.context, self.request)


def includeme(config):
    config.add_view(
        TraversalRESTView, attr='collection_get',
        request_method='GET', context=APICollectionEndpoint,
        renderer='json', permission='view'
    )
    config.add_view(
        TraversalRESTView, attr='entity_get',
        request_method='GET', context=APIEntityEndpoint,
        renderer='json', permission='view'
    )
