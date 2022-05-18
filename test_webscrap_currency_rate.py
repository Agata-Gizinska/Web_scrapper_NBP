import pytest
import requests
from webscrap_currency_rate import get_currency, Webscrapper


def test_request_status(website):
    response = requests.get(website)
    assert response.status_code == 200

def test_webscrapper_currency_short(ws_instance):
    assert list(ws_instance.currency.keys()) == ['USD', 'EUR', 'CHF', 'GBP', 'JPY']


def test_get_html_components_and_prepare_data():
    pass


def test_mock_data():
    pass
