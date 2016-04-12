import pytest
from spree.rest import APIEndpoint


def traverse(source, path: str, sep='/'):
    parts = path.split(sep)
    for p in parts:
        try:
            new_value = source[p]
        except KeyError:
            return None
        source = new_value
    return source


@pytest.mark.parametrize('test_path', [
    pytest.mark.xfail('offers'),
    pytest.mark.xfail('orders/foo'),
    'orders/1',
    'customers',
    'customers/1',
    'customers/2',
    'customers/1/orders',
    'customers/2/orders',
    'customers/1/orders/1',
    'customers/2/orders/2'
])
def test_can_traverse(api_root, test_path):
    """
    Test if we can traverse the API tree
    """
    assert isinstance(traverse(api_root, test_path), APIEndpoint)


@pytest.mark.parametrize('test_path', [
    'foo',
    'bar.baz',
    'bar.zen',
    'bar.zet.asd',
    pytest.mark.xfail('nope.nope.nope')
])
def test_traverse_func(test_path):
    """
    Test if we can walk dictionaries with our helper function
    """
    source = {
        'foo': 'foo',
        'bar': {
            'baz': 'bar.baz',
            'zen': 'bar.zen',
            'zet': {
                'asd': 'bar.zet.asd'
            }
        }
    }
    assert traverse(source, test_path, sep='.') == test_path
