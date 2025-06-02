# backend/app.py

import os, csv, json
from flask        import Flask, jsonify, request
from flask_cors   import CORS

from models.account           import Account
from models.customer          import Customer
from models.product           import Product
from models.product_catalogue import ProductCatalogue
from models.shopping_cart     import ShoppingCart
from database                 import Database

app = Flask(__name__)
CORS(app)

# ─── 1. Instantiate the ProductCatalogue (loads products.csv) ───
catalogue = ProductCatalogue()

def startup_info():
    """
    Print out loaded products, customers, and accounts for debugging.
    Called manually before app.run().
    """
    print("=== Startup: Checking loaded data ===")
    print("Products loaded:")
    for p in catalogue.get_all_products():
        print(" ", p)
    # load all customers from customers.csv
    db = Database()
    all_customers = db.get_table("customers")
    print("Customers found:", [row["customer_id"] for row in all_customers])
    # load all accounts from accounts.csv
    all_accounts = db.get_table("accounts")
    print("Accounts found:", [row["account_id"] for row in all_accounts])
    print("=====================================")


# ─── 2. List all products ─────────────────────────────────────────────────
@app.route("/api/products", methods=["GET"])
def get_products():
    return jsonify(catalogue.get_all_products())


# ─── 3. View a given customer’s cart ───────────────────────────────────────
@app.route("/api/cart/<customer_id>", methods=["GET"])
def view_cart(customer_id):
    try:
        cust = Customer(customer_id)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

    raw_items = cust.get_cart().get_cart_items()
    # Enrich each with product name and price
    detailed = []
    for entry in raw_items:
        p = catalogue.get_product(entry["product_id"])
        if not p:
            continue
        detailed.append({
            "product_id": p.product_id,
            "name": p.name,
            "price": p.price,
            "quantity": entry["quantity"]
        })
    return jsonify(detailed)


# ─── 4. Add a product to a given customer’s cart ───────────────────────────
@app.route("/api/cart/<customer_id>/add", methods=["POST"])
def add_to_cart(customer_id):
    payload = request.get_json()
    if not payload or "product_id" not in payload:
        return jsonify({"error": "Missing product_id in JSON"}), 400

    pid = str(payload["product_id"])
    qty = int(payload.get("quantity", 1))

    # Check product exists
    product = catalogue.get_product(pid)
    if not product:
        return jsonify({"error": f"Product ID '{pid}' not found"}), 404

    # Check customer exists (this will raise if invalid)
    try:
        cust = Customer(customer_id)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

    # Add to cart
    cust.get_cart().add_to_cart(product, qty)
    return jsonify({"message": "Product added to cart"}), 200


# ─── 5. List all unique customer IDs (for a dropdown, if you like) ─────────
@app.route("/api/customers", methods=["GET"])
def list_customers():
    db = Database()
    rows = db.get_table("customers")
    distinct_ids = sorted({row["customer_id"] for row in rows})
    return jsonify(distinct_ids)


if __name__ == "__main__":
    # Print out route map for sanity
    print(app.url_map)
    # Manually invoke our startup_info before running
    startup_info()
    app.run(debug=True)
