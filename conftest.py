# Add conftest.py directory to PYTHONPATH
# it's currenty the same as tested program path
import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import pytest
from webscrap_currency_rate import get_url


@pytest.fixture
def website():
    url = get_url()
    return url
