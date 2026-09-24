from data import inventory


def find_product_by_id(product_id):
    """
    Find an inventory product by its ID

    Args:
        product_id (int): The ID of the product to find

    Returns:
        dict: The matching product
        None: If no product with the given ID exists
    """
    return next(
        (product for product in inventory if product["id"] == product_id),
        None
    )

def get_next_id():
    """
    Generate the next available inventory product ID

    Returns:
        int: One greater than the highest existing product ID
        Returns 1 if the inventory is empty
    """
    return max(
        (product["id"] for product in inventory),
        default=0
    ) + 1

def get_missing_field(data, required_fields):
    """
    Check request data for missing required fields

    Args:
        data (dict): The data to validate.
        required_fields (list): Fields that must contain values

    Returns:
        str: The name of the first missing field
        None: If all required fields are present
    """
    for field in required_fields:
        value = data.get(field)

        if value is None or value == "":
            return field

    return None

def print_error(response):
    """
    Print an error message from an API response

    Args:
        response: The HTTP response containing an error message
    """
    error = response.json()
    print(f"Error: {error['error']}")