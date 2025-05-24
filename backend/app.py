from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import csv
from models.product_catalogue import ProductCatalogue
from models.customer import Customer
from models.product import Product

app = Flask(__name__)
CORS(app)

catalogue = ProductCatalogue()


@app.route("/api/customers", methods=["GET"])
def list_customers():
    path = os.path.join("data", "cart.csv")
    if not os.path.exists(path):
        return jsonify([])

    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        ids = {row["customer_id"] for row in reader}

    return jsonify(sorted(ids))

@app.route("/api/products", methods=["GET"])
def get_products():
    return jsonify(catalogue.get_all_products())

@app.route("/api/cart/<customer_id>", methods=["GET"])
def view_cart(customer_id):
    cust = Customer(customer_id)
    cart = cust.get_cart().get_cart_items()
    # enrich with product data
    detailed = []
    for entry in cart:
        p = catalogue.get_product(entry["product_id"])
        if p:
            detailed.append({
                "id": p.product_id,
                "name": p.name,
                "price": p.price,
                "quantity": entry["quantity"]
            })
    return jsonify(detailed)

@app.route("/api/cart/<customer_id>/add", methods=["POST"])
def add_to_cart(customer_id):
    data = request.get_json()
    pid = data.get("product_id")
    qty = data.get("quantity", 1)
    product = catalogue.get_product(pid)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    cust = Customer(customer_id)
    cust.get_cart().add_to_cart(product, qty)
    return jsonify({"message": "Added to cart"}), 200

if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True)
