from unittest.mock import patch, Mock
from argparse import Namespace

from cli import (
    view_inventory,
    add_product,
    update_product,
    delete_product,
    find_product
)


@patch("cli.requests.get")
def test_view_inventory(mock_get, capsys):
    mock_response = Mock()

    mock_response.json.return_value = [
        {
            "id": 1,
            "product_name": "Test Product",
            "price": 4.99,
            "stock": 10
        }
    ]

    mock_get.return_value = mock_response

    view_inventory()

    output = capsys.readouterr().out

    assert "Test Product" in output


@patch("cli.requests.post")
def test_add_product(mock_post, capsys):
    mock_response = Mock()

    mock_response.status_code = 201
    mock_response.json.return_value = {
        "id": 4,
        "product_name": "Test Product"
    }

    mock_post.return_value = mock_response

    args = Namespace(
        barcode="123456",
        product_name="Test Product",
        brand="Test Brand",
        ingredients="Test ingredients",
        price=3.99,
        stock=5
    )

    add_product(args)

    output = capsys.readouterr().out

    assert "Product added" in output


@patch("cli.requests.patch")
def test_update_product(mock_patch, capsys):
    mock_response = Mock()

    mock_response.status_code = 200
    mock_response.json.return_value = {
        "product_name": "Test Product",
        "price": 6.99,
        "stock": 10
    }

    mock_patch.return_value = mock_response

    args = Namespace(
        id=1,
        price=6.99,
        stock=None
    )

    update_product(args)

    output = capsys.readouterr().out

    assert "Product updated" in output


@patch("cli.requests.delete")
def test_delete_product(mock_delete, capsys):
    mock_response = Mock()
    mock_response.status_code = 204

    mock_delete.return_value = mock_response

    args = Namespace(id=1)

    delete_product(args)

    output = capsys.readouterr().out

    assert "deleted successfully" in output


@patch("cli.requests.get")
def test_find_product(mock_get, capsys):
    mock_response = Mock()

    mock_response.status_code = 200
    mock_response.json.return_value = {
        "product_name": "Nutella",
        "brand": "Ferrero",
        "barcode": "3017624010701",
        "ingredients": "Sugar, hazelnuts"
    }

    mock_get.return_value = mock_response

    args = Namespace(
        barcode="3017624010701"
    )

    find_product(args)

    output = capsys.readouterr().out

    assert "Nutella" in output