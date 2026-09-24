from flask import Flask, jsonify, request
from data import inventory
from openfoodfacts import get_product_by_barcode, get_products_by_name
from helpers import find_product_by_id, get_next_id, get_missing_field

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to the Inventory Management System API"
    }), 200

@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory), 200

@app.route("/inventory/<int:id>")
def get_product(id):

    product = find_product_by_id(id)

    if product is None:
        return jsonify({"error": "product not found"}), 404

    return jsonify(product), 200

@app.route("/inventory", methods=["POST"])
def create_product():
    data = request.get_json()

    required_fields = [
        "barcode",
        "product_name",
        "brand",
        "ingredients",
        "price",
        "stock"
    ]

    missing_field = get_missing_field(data, required_fields)

    if missing_field:
        return jsonify({"error": f"{missing_field} missing"}), 400

    new_id = get_next_id()

    new_product = {
        "id": new_id,
        "barcode": data["barcode"],
        "product_name": data["product_name"],
        "brand": data["brand"],
        "ingredients": data["ingredients"],
        "price": data["price"],
        "stock": data["stock"]
    }

    inventory.append(new_product)

    return jsonify(new_product), 201


@app.route("/inventory/<int:id>", methods=["PATCH"])
def update_product(id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "no change detected"}), 400

    product = find_product_by_id(id)

    if not product:
        return jsonify({"error": "product not found"}), 404

    updatable_fields = [
        "barcode",
        "product_name",
        "brand",
        "ingredients",
        "price",
        "stock"
    ]

    for field in updatable_fields:
        if field in data:
            product[field] = data[field]

    return jsonify(product), 200

@app.route("/inventory/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = find_product_by_id(id)

    if not product:
        return jsonify({"error": "product not found"}), 404

    inventory.remove(product)

    return jsonify(), 204

@app.route("/products/<barcode>", methods=["GET"])
def find_product(barcode):
    product = get_product_by_barcode(barcode)

    if product is None:
        return jsonify({"error": "product not found"}), 404

    return jsonify(product), 200

@app.route("/inventory/from-api/<barcode>", methods=["POST"])
def add_product_from_api(barcode):
    product = get_product_by_barcode(barcode)

    if product is None:
        return jsonify({"error": "product not found"}), 404

    data = request.get_json()

    required_fields = [
        "price",
        "stock"
    ]

    missing_field = get_missing_field(data, required_fields)

    if missing_field:
        return jsonify({"error": f"{missing_field} missing"}), 400

    product["price"] = data["price"]
    product["stock"] = data["stock"]

    new_id = get_next_id()
    product["id"] = new_id

    inventory.append(product)

    return jsonify(product), 201

@app.route("/products/search/<product_name>", methods=["GET"])
def search_products(product_name):
    products = get_products_by_name(product_name)

    if products is None:
        return jsonify({"error": "product not found"}), 404

    return jsonify(products), 200
 
if __name__ == "__main__":
    app.run(debug=True)