from data import inventory


def find_product_by_id(product_id):
    return next((product for product in inventory if product["id"] == product_id), None)

def get_next_id():
    return max((product["id"] for product in inventory),default=0) + 1

def get_missing_field(data, required_fields):
    for field in required_fields:
        value = data.get(field)

        if value is None or value == "":
            return field

    return None

def print_error(response):
    error = response.json()
    print(f"Error: {error['error']}")