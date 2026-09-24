import argparse
import requests

from helpers import print_error


BASE_URL = "http://127.0.0.1:5000"


def print_product(product):
    """
    Print product details in a readable CLI format

    Args:
        product (dict): Product information containing name, brand,
        barcode, and ingredients
    """
    print(
        f"Product: {product['product_name']}\n"
        f"Brand: {product['brand']}\n"
        f"Barcode: {product['barcode']}\n"
        f"Ingredients: {product['ingredients']}"
    )


def view_inventory():
    """
    Retrieve and display all inventory items from the Flask API
    """
    response = requests.get(
        f"{BASE_URL}/inventory"
    )

    inventory = response.json()

    for product in inventory:
        print(
            f"ID: {product['id']} | "
            f"{product['product_name']} | "
            f"Price: ${product['price']} | "
            f"Stock: {product['stock']}"
        )


def add_product(args):
    """
    Add a new product to the local inventory through the Flask API

    Args:
        args: Parsed CLI arguments containing product details
    """
    product_data = {
        "barcode": args.barcode,
        "product_name": args.product_name,
        "brand": args.brand,
        "ingredients": args.ingredients,
        "price": args.price,
        "stock": args.stock
    }

    response = requests.post(
        f"{BASE_URL}/inventory",
        json=product_data
    )

    if response.status_code == 201:
        product = response.json()
        print(
            f"Product added: "
            f"{product['product_name']} "
            f"(ID: {product['id']})"
        )
    else:
        print_error(response)


def update_product(args):
    """
    Update the price and/or stock of an existing inventory item

    Args:
        args: Parsed CLI arguments containing the product ID
        and optional price or stock values
    """
    product_data = {}

    if args.price is not None:
        product_data["price"] = args.price

    if args.stock is not None:
        product_data["stock"] = args.stock

    response = requests.patch(
        f"{BASE_URL}/inventory/{args.id}",
        json=product_data
    )

    if response.status_code == 200:
        product = response.json()
        print(
            f"Product updated: "
            f"{product['product_name']} | "
            f"Price: ${product['price']} | "
            f"Stock: {product['stock']}"
        )
    else:
        print_error(response)


def delete_product(args):
    """
    Delete an inventory item by ID

    Args:
        args: Parsed CLI arguments containing the product ID
    """
    response = requests.delete(
        f"{BASE_URL}/inventory/{args.id}"
    )

    if response.status_code == 204:
        print(
            f"Product {args.id} deleted successfully."
        )
    else:
        print_error(response)


def find_product(args):
    """
    Find a single OpenFoodFacts product by barcode

    Args:
        args: Parsed CLI arguments containing the barcode
    """
    response = requests.get(
        f"{BASE_URL}/products/{args.barcode}"
    )

    if response.status_code == 200:
        product = response.json()
        print_product(product)
    else:
        print_error(response)


def search_products(args):
    """
    Search OpenFoodFacts for products by product name

    Args:
        args: Parsed CLI arguments containing the product name
    """
    response = requests.get(
        f"{BASE_URL}/products/search/{args.product_name}"
    )

    if response.status_code == 200:
        products = response.json()

        for product in products:
            print_product(product)
            print()
    else:
        print_error(response)


def add_product_from_api(args):
    """
    Retrieve a product from OpenFoodFacts by barcode and add it
    to the local inventory with a price and stock value

    Args:
        args: Parsed CLI arguments containing barcode, price,
        and stock values
    """
    product_data = {
        "price": args.price,
        "stock": args.stock
    }

    response = requests.post(
        f"{BASE_URL}/inventory/from-api/{args.barcode}",
        json=product_data
    )

    if response.status_code == 201:
        product = response.json()
        print(
            f"Product added: "
            f"{product['product_name']} "
            f"(ID: {product['id']})"
        )
    else:
        print_error(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Inventory Management System CLI"
    )

    subparsers = parser.add_subparsers(
        dest="command"
    )

    # View inventory
    subparsers.add_parser(
        "view",
        help="View all inventory items"
    )

    # Add inventory item manually
    add_parser = subparsers.add_parser(
        "add",
        help="Add a new inventory item"
    )

    for argument in [
        "--barcode",
        "--product-name",
        "--brand",
        "--ingredients"
    ]:
        add_parser.add_argument(
            argument,
            required=True
        )

    add_parser.add_argument(
        "--price",
        type=float,
        required=True
    )

    add_parser.add_argument(
        "--stock",
        type=int,
        required=True
    )

    # Update inventory item
    update_parser = subparsers.add_parser(
        "update",
        help="Update an inventory item"
    )

    update_parser.add_argument(
        "--id",
        type=int,
        required=True
    )

    update_parser.add_argument(
        "--price",
        type=float
    )

    update_parser.add_argument(
        "--stock",
        type=int
    )

    # Delete inventory item
    delete_parser = subparsers.add_parser(
        "delete",
        help="Delete an inventory item"
    )

    delete_parser.add_argument(
        "--id",
        type=int,
        required=True
    )

    # Find product by barcode
    find_parser = subparsers.add_parser(
        "find",
        help="Find a product using OpenFoodFacts"
    )

    find_parser.add_argument(
        "--barcode",
        type=str,
        required=True
    )

    # Search products by name
    search_parser = subparsers.add_parser(
        "search",
        help="Search OpenFoodFacts by product name"
    )

    search_parser.add_argument(
        "--product-name",
        required=True
    )

    # Add OpenFoodFacts product to inventory
    add_api_parser = subparsers.add_parser(
        "add-from-api",
        help="Add an OpenFoodFacts product to inventory"
    )

    add_api_parser.add_argument(
        "--barcode",
        type=str,
        required=True
    )

    add_api_parser.add_argument(
        "--price",
        type=float,
        required=True
    )

    add_api_parser.add_argument(
        "--stock",
        type=int,
        required=True
    )

    args = parser.parse_args()

    if args.command == "view":
        view_inventory()

    elif args.command == "add":
        add_product(args)

    elif args.command == "update":
        update_product(args)

    elif args.command == "delete":
        delete_product(args)

    elif args.command == "find":
        find_product(args)

    elif args.command == "search":
        search_products(args)

    elif args.command == "add-from-api":
        add_product_from_api(args)