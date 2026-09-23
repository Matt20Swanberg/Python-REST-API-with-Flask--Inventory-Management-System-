import requests

def get_product_by_barcode(barcode):
    url = f"https://world.openfoodfacts.net/api/v2/product/{barcode}"


    headers = {
        "User-Agent": "InventoryManagementSystem/1.0 (student@example.com)"
    }

    response = requests.get(url, headers=headers)

    response.raise_for_status()

    data = response.json()

    status = data.get("status")

    if status == 0:
        return None

    product = data.get("product")

    field_mapping = {
    "product_name": "product_name",
    "brand": "brands",
    "ingredients": "ingredients_text"
    }

    product_data = {}

    for inventory_field, api_field in field_mapping.items():
        product_data[inventory_field] = product.get(api_field)

    product_data["barcode"] = barcode 


    return product_data