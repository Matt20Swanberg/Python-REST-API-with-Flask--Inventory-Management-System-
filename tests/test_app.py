import pytest

from app import app
from data import inventory


@pytest.fixture(autouse=True)
def reset_inventory():
    original_inventory = [product.copy() for product in inventory]

    yield

    inventory.clear()
    inventory.extend(original_inventory)


def test_get_inventory():
    client = app.test_client()

    response = client.get("/inventory")

    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_create_product():
    client = app.test_client()

    new_product = {
        "barcode": "1111111111111",
        "product_name": "Test Product",
        "brand": "Test Brand",
        "ingredients": "Test ingredients",
        "price": 4.99,
        "stock": 10
    }

    response = client.post("/inventory", json=new_product)

    assert response.status_code == 201
    assert response.get_json()["product_name"] == "Test Product"


def test_update_product():
    client = app.test_client()

    response = client.patch(
        "/inventory/1",
        json={"price": 7.99}
    )

    assert response.status_code == 200
    assert response.get_json()["price"] == 7.99


def test_delete_product():
    client = app.test_client()

    response = client.delete("/inventory/1")

    assert response.status_code == 204