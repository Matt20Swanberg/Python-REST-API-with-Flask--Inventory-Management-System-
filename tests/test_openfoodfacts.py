from unittest.mock import patch, Mock

from openfoodfacts import get_product_by_barcode


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