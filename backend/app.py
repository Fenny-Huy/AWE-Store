from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import csv
import traceback
from models.product_catalogue import ProductCatalogue
from models.customer import Customer
from models.product import Product

app = Flask(__name__)
# Enable CORS for all routes and origins
CORS(app, resources={r"/api/*": {"origins": "*"}})

catalogue = ProductCatalogue()


@app.route("/api/customers", methods=["GET"])
def list_customers():
    print("Accessing customers endpoint")  # Debug print
    path = os.path.join("data", "cart.csv")
    if not os.path.exists(path):
        print(f"Cart file not found at {path}")  # Debug print
        return jsonify([])

    try:
        with open(path, newline="") as f:
            reader = csv.DictReader(f)
            ids = {row["customer_id"] for row in reader}
        print(f"Found customers: {ids}")  # Debug print
        return jsonify(sorted(list(ids)))
    except Exception as e:
        print(f"Error reading cart file: {str(e)}")  # Debug print
        return jsonify({"error": str(e)}), 500

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

@app.route("/api/checkout/<customer_id>", methods=["POST"])
def checkout(customer_id):
    print(f"Starting checkout for customer: {customer_id}")  # Debug print
    try:
        # Get the customer
        customer = Customer(customer_id)
        print(f"Customer object created")  # Debug print
        
        # Get cart items before checkout
        cart_items = customer.get_cart().get_cart_items()
        print(f"Current cart items: {cart_items}")  # Debug print
        
        if not cart_items:
            return jsonify({"error": "Cart is empty"}), 400
        
        # Create and process the order
        try:
            order_result = customer.place_order()
            print(f"Order result: {order_result}")  # Debug print
        except Exception as e:
            print(f"Error during place_order: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            raise
        
        if order_result.get("success", False):
            # Clear the cart after successful checkout
            cart_path = os.path.join("data", "cart.csv")
            if os.path.exists(cart_path):
                with open(cart_path, "r", newline="") as f:
                    reader = csv.DictReader(f)
                    rows = [row for row in reader if row["customer_id"] != customer_id]
                
                with open(cart_path, "w", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=["customer_id", "product_id", "quantity"])
                    writer.writeheader()
                    writer.writerows(rows)
            
            print("Checkout completed successfully")  # Debug print
            return jsonify({
                "message": "Checkout successful",
                "order_id": order_result.get("order_id")
            }), 200
        else:
            error_msg = order_result.get("error", "Unknown error")
            print(f"Checkout failed: {error_msg}")  # Debug print
            return jsonify({
                "error": "Checkout failed",
                "reason": error_msg
            }), 400
            
    except ValueError as e:
        print(f"ValueError during checkout: {str(e)}")  # Debug print
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"Unexpected error during checkout: {str(e)}")  # Debug print
        print(f"Traceback: {traceback.format_exc()}")  # Debug print
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True)
