from flask import Flask, jsonify, request, render_template
from models.product import Product
from models.product_catalogue import ProductCatalogue
from models.customer import Customer

app = Flask(__name__)
catalogue = ProductCatalogue()
customer = Customer(customer_id="guest")

# Sample data
catalogue.add_product(Product("1", "Laptop", "High-performance laptop", 999.99))
catalogue.add_product(Product("2", "Mouse", "Wireless mouse", 25.00))
catalogue.add_product(Product("3", "Keyboard", "Mechanical keyboard", 75.50))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/products", methods=["GET"])
def get_products():
    return jsonify(catalogue.get_all_products())

@app.route("/api/cart", methods=["POST"])
def add_to_cart():
    data = request.get_json()
    product = catalogue.get_product(data["product_id"])
    if product:
        customer.get_cart().add_to_cart(product, data.get("quantity", 1))
        return jsonify({"message": "Product added to cart"}), 200
    return jsonify({"error": "Product not found"}), 404

@app.route("/api/cart", methods=["GET"])
def get_cart():
    return jsonify(customer.get_cart().get_cart_items())

if __name__ == "__main__":
    app.run(debug=True)
