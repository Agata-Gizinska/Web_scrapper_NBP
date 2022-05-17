import pytest
import requests
from webscrap_currency_rate import scrap_and_print, main


def test_request_status(website):
    response = requests.get(website)
    assert response.status_code == 200


def test_headings():
    pass


def test_currency_name():
    pass


def test_mock_data():
    pass
