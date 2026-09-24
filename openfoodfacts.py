import requests

FIELD_MAPPING = {
    "product_name": "product_name",
    "brand": "brands",
    "ingredients": "ingredients_text"
}

def get_product_by_barcode(barcode):
    url = f"https://world.openfoodfacts.org/api/v3/product/{barcode}"


    headers = {
        "User-Agent": "InventoryManagementSystem/1.0 (student@example.com)"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return None

    data = response.json()

    status = data.get("status")

    if status == 0:
        return None

    product = data.get("product")

    product_data = {}

    for inventory_field, api_field in FIELD_MAPPING.items():
        product_data[inventory_field] = product.get(api_field)

    product_data["barcode"] = barcode 


    return product_data

def get_products_by_name(product_name):
    url = "https://world.openfoodfacts.org/cgi/search.pl"

    params = {
        "search_terms": product_name,
        "json": 1,
        "action": "process",
        "search_simple": 1
    }

    response = requests.get(url, params=params)

    headers = {
        "User-Agent": "InventoryManagementSystem/1.0 (student@example.com)"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return None

    data = response.json()

    products = data.get("products", [])

    if not products:
        return None

    product_results = []

    for product in products:
        product_data = {"barcode": product.get("code")}

        for inventory_field, api_field in FIELD_MAPPING.items():
            product_data[inventory_field] = product.get(api_field)

        product_results.append(product_data)

    return product_results[:5]
    