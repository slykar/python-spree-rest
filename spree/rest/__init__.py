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
    """
    Add response callback to Pyramid request.
    :param event: Pyramid request event
    :type event: pyramid.events.NewRequest
    :return:
    """
    request = event.request
    request.add_response_callback(apply_cors)


def includeme(config):
    """
    Include hook for Pyramid. Adds request subscribers.
    :param config: Paste config
    :type config: pyramid.config.Configurator
    :return:
    """
    config.add_subscriber(wrap_request, NewRequest)
