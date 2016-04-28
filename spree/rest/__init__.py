from pyramid.events import NewRequest
from .cors import apply_cors
from .traversal import (
    APIEndpoint,
    APIEntity,
    APICollection,
    APIAction,
    TraversalResourceView,
    NodeRef
)


def wrap_request(event):
    request = event.request
    request.add_response_callback(apply_cors)


def includeme(config):
    config.add_subscriber(wrap_request, NewRequest)
