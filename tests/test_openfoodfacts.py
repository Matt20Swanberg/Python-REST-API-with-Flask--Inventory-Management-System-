from unittest.mock import patch, Mock
from openfoodfacts import get_product_by_barcode, get_products_by_name
from requests.exceptions import RequestException


@patch("openfoodfacts.requests.get")
def test_get_product_by_barcode(mock_get):
    mock_response = Mock()

    mock_response.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Test Cereal",
            "brands": "Test Foods",
            "ingredients_text": "Oats, sugar, salt"
        }
    }

    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    product = get_product_by_barcode("123456789")

    assert product["product_name"] == "Test Cereal"
    assert product["brand"] == "Test Foods"
    assert product["ingredients"] == "Oats, sugar, salt"
    assert product["barcode"] == "123456789"

@patch("openfoodfacts.requests.get")
def test_product_not_found(mock_get):
    mock_response = Mock()

    mock_response.json.return_value = {
        "status": 0
    }

    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    product = get_product_by_barcode("0000000000000")

    assert product is None

@patch("openfoodfacts.requests.get")
def test_api_request_failure(mock_get):
    mock_get.side_effect = RequestException

    product = get_product_by_barcode("3017624010701")

    assert product is None

@patch("openfoodfacts.requests.get")
def test_get_products_by_name(mock_get):
    mock_response = Mock()

    mock_response.json.return_value = {
        "products": [
            {
                "code": "123456789",
                "product_name": "Test Product",
                "brands": "Test Brand",
                "ingredients_text": "Test ingredients"
            }
        ]
    }

    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    products = get_products_by_name("Test Product")

    assert products[0]["product_name"] == "Test Product"
    assert products[0]["brand"] == "Test Brand"
    assert products[0]["ingredients"] == "Test ingredients"
    assert products[0]["barcode"] == "123456789"