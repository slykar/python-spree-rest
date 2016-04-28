"""
Events fired by :class:`spree.rest.traversal.views.TraversalResourceView`.
Note, that you can also use :class:`spree.rest.traversal.APIEndpoint`
(referenced as ``context``) methods to achieve similar results.
"""


class BeforeUpdate(object):
    """
    Fired before :meth:`spree.rest.traversal.APIEntity.update` is called.
    You can achieve similar results using :meth:`spree.rest.traversal.APIEntity.before_update`
    """
    def __init__(self, view, deserialized):
        self.view = view
        self.deserialized = deserialized


class AfterUpdate(object):
    """
    Fired after :meth:`spree.rest.traversal.APIEntity.update` is called.
    You can achieve similar results using :meth:`spree.rest.traversal.APIEntity.after_update`
    """
    def __init__(self, view, updated, deserialized):
        self.view = view
        self.updated = updated
        self.deserialized = deserialized


class BeforeCreate(object):
    """
    Fired before :meth:`spree.rest.traversal.APICollection.create` is called.
    You can achieve similar results using :meth:`spree.rest.traversal.APICollection.before_create`
    """
    def __init__(self, view, deserialized):
        self.view = view
        self.deserialized = deserialized


class AfterCreate(object):
    """
    Fired after :meth:`spree.rest.traversal.APICollection.create` is called.
    You can achieve similar results using :meth:`spree.rest.traversal.APICollection.after_create`
    """
    def __init__(self, view, created, deserialized):
        self.view = view
        self.created = created
        self.deserialized = deserialized
