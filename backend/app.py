from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json

from models.customer import Customer
from models.product import Product
from models.product_catalogue import ProductCatalogue

app = Flask(__name__)
CORS(app)

# Initialize product catalogue and customer
catalogue = ProductCatalogue()
customer = Customer(customer_id="C001")

# Load products from JSON
with open(os.path.join("data", "products.json")) as f:
    product_data = json.load(f)
    for p in product_data:
        product = Product(
            product_id=p["product_id"],  # updated key
            name=p["name"],
            description=p["description"],
            price=p["price"]
        )
        catalogue.add_product(product)

@app.route("/api/products", methods=["GET"])
def get_all_products():
    return jsonify(catalogue.get_all_products())

@app.route("/api/cart", methods=["GET"])
def get_cart_items():
    return jsonify(customer.get_cart().get_cart_items())

@app.route("/api/cart/add/<product_id>", methods=["POST"])
def add_to_cart(product_id):
    data = request.get_json()
    quantity = data.get("quantity", 1)
    product = catalogue.get_product(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    customer.get_cart().add_to_cart(product, quantity)
    return jsonify({"message": "Product added to cart"}), 200

if __name__ == "__main__":
    app.run(debug=True)
