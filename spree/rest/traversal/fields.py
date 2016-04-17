"""
This module contains :mod:`marshmallow` fields that are designed
to work with the Pyramid Traversal approach of :mod:`spree.rest.traversal` module.
"""
from marshmallow import fields


class NodeRef(fields.Field):
    """Field that takes the value from ``self.context['node'].ref``.
    It's only processed on load, a ``load_only`` parameter is forced,
    as well as ``missing`` parameter which is set to ``True``
    in order to always run the deserialization method.
    """
    def __init__(self, *args, **kwargs):
        """
        You can pass any parameters acceptable for a generic :class:`fields.Field`,
        except few of them, which are:

            ``load_only``: which is always set to True, as serialization should be supported
                by creating a specific schema that overrides this field with a specific, typed one.

            ``missing``: which is always set to True, in order to always trigger this field
                deserialization.

            ``required``: which is always set to True.

        :param args:
        :param kwargs:
        """
        kwargs.update({
            'load_only': True,
            'missing': True,
            'required': True
        })
        super(NodeRef, self).__init__(*args, **kwargs)

    def _deserialize(self, value, attr, data):
        """
        Returns the value of ``self.context['node'].ref``, which is supposed
        to be a ``ref`` attribute of :class:`spree.rest.traversal.endpoints.APIEntityEndpoint`.

        :param value: Value for deserialization, most likely the ``missing`` ``True`` value.
            This value is not used.
        :param attr: Name of the deserialized field
        :param data: All deserialized data
        :return: :class:`APIEndpoint` ``ref`` value
        :rtype: str
        """
        return self.context['node'].ref
