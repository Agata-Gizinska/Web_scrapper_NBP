import pytest
import requests
from webscrap_currency_rate import (get_currency, 
                                    Webscrapper, get_url, get_currency)


def test_request_status(website):
    response = requests.get(website)
    assert response.status_code == 200

def test_webscrapper_currency_short(ws_instance):
    assert list(ws_instance.currency.keys()) == ['USD', 'EUR', 'CHF', 'GBP', 'JPY']


def test_get_html_components_and_prepare_data(ws_instance):
    with open('html_text.txt') as mock_html:
        ws_instance.get_html_components_and_prepare_data(mock_html)
        assert type(ws_instance.headings) == list
        assert type(ws_instance.content) == list
        assert ws_instance.headings[0] == 'Nazwa waluty'
        assert ws_instance.content[1][0] == 'euro'
        assert ws_instance.content[2][1] == '1 CHF'
        assert type(ws_instance.content[2][2]) == str


def test_mock_data():
    pass
