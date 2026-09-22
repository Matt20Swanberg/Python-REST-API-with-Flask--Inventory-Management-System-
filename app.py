from flask import Flask, jsonify, request
from data import inventory

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to the Inventory Management System API"
    }), 200

@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory), 200

@app.route("/inventory/<int:id>", )
def get_product(id):

    product = next((p for p in inventory if p['id'] == id), None)

    if product is None:
        return jsonify({}), 404

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

    for field in required_fields:
        value = data.get(field)

        if  value is None or value == "":
            return jsonify({"error": f"{field} missing"}), 400

    new_id = max((p["id"]for p in inventory), default=0) + 1

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

    product = next((p for p in inventory if p["id"] == id), None)

    if not update_product:
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
            product[field] = data [field]

    return jsonify(product)

@app.route("/inventory/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = next((p for p in inventory if p["id"] == id), None)

    if not product:
        return jsonify({"error": "product not found"}), 404

    inventory.remove(product)

    return jsonify(), 204

if __name__ == "__main__":
    app.run(debug=True)