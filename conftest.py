import pytest
from .webscrap_currency_rate import get_url


@pytest.fixture
def website():
    url = get_url()
    return url
