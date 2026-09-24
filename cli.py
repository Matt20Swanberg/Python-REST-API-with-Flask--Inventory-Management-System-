import argparse
import requests

BASE_URL = "http://127.0.0.1:5000"

def view_inventory():
    response = requests.get(f"{BASE_URL}/inventory")

    inventory = response.json()

    for product in inventory:
        print(
            f"ID: {product['id']} | {product['product_name']} | Price: ${product['price']} | Stock: {product['stock']}"
        )

def add_product(args):
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
        print(f"Product added: {product['product_name']} (ID: {product['id']})")

    else:
        error = response.json()
        print(f"Error: {error['error']}")

def update_product(args):
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
        print(f"Product updated: {product['product_name']} | Price: ${product['price']} | Stock: {product['stock']}")

    else:
        error = response.json()
        print(f"Error: {error['error']}")

def delete_product(args):
    response = requests.delete(
            f"{BASE_URL}/inventory/{args.id}"
        )
    if response.status_code == 204:
        print(f"Product {args.id} deleted successfully.")
    else:
        error = response.json()
        print(f"Error: {error['error']}")

def find_product(args):
    response = requests.get(
                f"{BASE_URL}/products/{args.barcode}"
            )
    if response.status_code == 200:
        product = response.json()
        print(
            f"Product: {product['product_name']}\n",
            f"Brand: {product['brand']}\n",
            f"Barcode: {product['barcode']}\n",
            f"Ingredients: {product['ingredients']}"
        )
    else:
        error = response.json()
        print(f"Error: {error['error']}")

def add_product_from_api(args):
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
        print(f"Product added: {product['product_name']} (ID: {product['id']})")

    else:
        error = response.json()
        print(f"Error: {error['error']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Inventory Management System CLI"
    )

    subparsers = parser.add_subparsers(dest="command")

    view_parser = subparsers.add_parser(
        "view",
        help="View all inventory items"
    )

    add_parser = subparsers.add_parser(
        "add",
        help="Add a new inventory item"
    )

    update_parser = subparsers.add_parser(
        "update",
        help="Update an inventory item"
    )

    delete_parser = subparsers.add_parser(
        "delete",
        help="Delete an inventory item"
    )

    find_parser = subparsers.add_parser(
        "find",
        help="Find a product using OpenFoodFacts"
    )

    add_api_parser = subparsers.add_parser(
        "add-from-api",
        help="Add an OpenFoodFacts product to inventory"
    )

    add_parser.add_argument(
        "--barcode",
        required=True
    )

    add_parser.add_argument(
        "--product-name",
        required=True
    )
    add_parser.add_argument(
        "--brand",
        required=True
    )
    add_parser.add_argument(
        "--ingredients",
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

    update_parser.add_argument(
        "--id",
        type=int,
        required=True
    )

    update_parser.add_argument(
        "--price",
        type=float,
        required=False
    )

    update_parser.add_argument(
        "--stock",
        type=int,
        required=False
    )

    delete_parser.add_argument(
        "--id",
        type=int,
        required=True
    )

    find_parser.add_argument(
        "--barcode",
        type=str,
        required=True
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

    elif args.command == "add-from-api":
        add_product_from_api(args)