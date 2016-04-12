import pytest
from .api_structure import APIRoot


@pytest.fixture(scope='module')
def api_root():
    return APIRoot(parent=None, ref='')
