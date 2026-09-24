import requests

FIELD_MAPPING = {
    "product_name": "product_name",
    "brand": "brands",
    "ingredients": "ingredients_text"
}

def get_product_by_barcode(barcode):
    """
    Retrieve a single product from OpenFoodFacts using a barcode

    Args:
        barcode (str): The barcode used to search for a product

    Returns:
        dict: Product data formatted for the local inventory system
        None: If the API request fails or the product is not found
    """
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

    # Convert OpenFoodFacts field names to the local inventory format
    for inventory_field, api_field in FIELD_MAPPING.items():
        product_data[inventory_field] = product.get(api_field)

    product_data["barcode"] = barcode 


    return product_data

def get_products_by_name(product_name):
    """
    Search OpenFoodFacts for products using a product name

    Args:
        product_name (str): The product name or keyword to search for

    Returns:
        list: Up to five matching products formatted for the
        local inventory system
        None: If the API request fails or no products are found
    """
    url = "https://world.openfoodfacts.org/cgi/search.pl"

    params = {
        "search_terms": product_name,
        "json": 1,
        "action": "process",
        "search_simple": 1
    }

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

    # Normalize each OpenFoodFacts result to match local inventory fields
    for product in products:
        product_data = {"barcode": product.get("code")}

        for inventory_field, api_field in FIELD_MAPPING.items():
            product_data[inventory_field] = product.get(api_field)

        product_results.append(product_data)

    # Limit results to keep API and CLI output manageable
    return product_results[:5]
    