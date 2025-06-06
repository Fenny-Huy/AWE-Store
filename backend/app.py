from flask      import Flask, jsonify, request
from flask_cors import CORS
import random
import string

from models.database           import DatabaseManager
from models.customer           import Customer
from models.product            import Product
from models.product_catalogue  import ProductCatalogue

from models.admin              import Admin
from models.sales_analytics    import SalesAnalytics

from models.order import Order

from models.payment_observer import observer
from models.payment_listeners.receipt import Receipt
from models.payment_listeners.notification_system import NotificationSystem
from models.payment_listeners.shipment import Shipment

observer.register(Receipt())
observer.register(NotificationSystem())
observer.register(Shipment())

app = Flask(__name__)
CORS(app)




# ─────────────────────────────────────────────────────────────────────────────
# 1. Load ALL Product instances from 'products.csv'
# ─────────────────────────────────────────────────────────────────────────────
dbm = DatabaseManager()
prod_table = dbm.get_table("products")
all_product_objs = []
order_table = dbm.get_table("order")

if prod_table:
    for row in prod_table.rows:
        p = Product(
            product_id  = row["product_id"],
            name        = row["name"],
            description = row["description"],
            price       = float(row["price"])
        )
        all_product_objs.append(p)
else:
    # If no 'products.csv', create an empty table with columns
    prod_table = dbm.create_table("products", ["product_id","name","description","price"])

# Build a dict: product_id -> Product instance (for easy lookup)
all_products_dict = {p.product_id: p for p in all_product_objs}


# ─────────────────────────────────────────────────────────────────────────────
# 2. Load CUSTOMER instances from 'customers.csv'
# ─────────────────────────────────────────────────────────────────────────────
cust_table = dbm.get_table("customers")
all_customers = {}

if cust_table:
    for row in cust_table.rows:
        cid = row["customer_id"]
        try:
            all_customers[cid] = Customer(cid)
        except ValueError:
            # Skip invalid rows
            pass
else:
    dbm.create_table("customers", ["customer_id","account_id"])

# ─────────────────────────────────────────────────────────────────────────────
# 3. Load ADMIN instances from 'admins.csv'
# ─────────────────────────────────────────────────────────────────────────────
admins_table = dbm.get_table("admins")
all_admins = {}  # map email -> Admin instance

if admins_table:
    for row in admins_table.rows:
        acct_id = row["account_id"]
        pwd     = row["password"]
        try:
            admin_obj = Admin(acct_id, pwd)       # loads name, email from accounts.csv
            all_admins[admin_obj.email] = admin_obj
        except ValueError:
            # Skip if account_id not found in accounts.csv 
            pass
else:
    # If no 'admins.csv', create an empty one with the correct header
    dbm.create_table("admins", ["account_id","email","password"])


# ─────────────────────────────────────────────────────────────────────────────
# 4. Load PRODUCT_CATALOGUE instances from 'product_catalogues.csv'
# ─────────────────────────────────────────────────────────────────────────────
pc_table = dbm.get_table("product_catalogues")
# Map of catalogue_id -> {"name": <str>, "product_ids": [ ... ]}
catalogue_map = {}

if pc_table:
    for row in pc_table.rows:
        cat_id   = row["catalogue_id"]
        cat_name = row["name"]
        pid      = row["product_id"]

        if cat_id not in catalogue_map:
            catalogue_map[cat_id] = {
                "name": cat_name,
                "product_ids": []
            }
        catalogue_map[cat_id]["product_ids"].append(pid)
else:
    # If no CSV yet, create an empty one (with header row)
    dbm.create_table("product_catalogues", ["catalogue_id","name","product_id"])
    catalogue_map = {}

# Build a dict of ProductCatalogue instances
all_catalogues = {}
for cat_id, info in catalogue_map.items():
    # For each product_id in this catalogue, pick up the Product instance from all_products_dict
    product_list = [ all_products_dict[pid] 
                     for pid in info["product_ids"] 
                     if pid in all_products_dict ]
    all_catalogues[cat_id] = ProductCatalogue(cat_id, info["name"], product_list)


# ─────────────────────────────────────────────────────────────────────────────
# 5. API ROUTES
# ─────────────────────────────────────────────────────────────────────────────

@app.route("/api/products", methods=["GET"])
def get_all_products():
    
    #Return all products (regardless of catalogue).
    
    return jsonify([p.return_info() for p in all_products_dict.values()])


@app.route("/api/catalogues", methods=["GET"])
def list_catalogues():
    
    #Return a list of all catalogues with their IDs and names:[ { "catalogue_id": "1", "name": "Organic" }, ... ]
      
    
    result = [
        { "catalogue_id": cat.get_catalogue_id(), "name": cat.get_name() }
        for cat in all_catalogues.values()
    ]
    return jsonify(result)


@app.route("/api/catalogues/<catalogue_id>/products", methods=["GET"])
def get_catalogue_products(catalogue_id):
    
    #Return all products belonging to the given catalogue_id.
    
    if catalogue_id not in all_catalogues:
        return jsonify({ "error": f"Catalogue '{catalogue_id}' not found" }), 404

    cat = all_catalogues[catalogue_id]
    return jsonify(cat.get_all_products())


@app.route("/api/customers", methods=["GET"])
def list_customers():
    
    #Return a sorted list of all customer IDs.
    
    return jsonify(sorted([cust.get_customer_id() for cust in all_customers.values()]))


@app.route("/api/cart/<customer_id>", methods=["GET"])
def view_cart(customer_id):
    if customer_id not in all_customers:
        return jsonify({ "error": f"Customer '{customer_id}' not found" }), 404

    cust = all_customers[customer_id]
    raw_items = cust.get_cart().get_cart_items()
    # from models.shopping_cart import ShoppingCart
    # fresh_cart = ShoppingCart(customer_id)
    # raw_items = fresh_cart.get_cart_items()
    detailed = []
    for entry in raw_items:
        pid = entry["product_id"]
        p = all_products_dict.get(pid)
        if p:
            detailed.append({
                "product_id": p.product_id,
                "name": p.name,
                "price": p.price,
                "quantity": entry["quantity"]
            })
    return jsonify(detailed)


@app.route("/api/cart/<customer_id>/add", methods=["POST"])
def add_to_cart(customer_id):
    if customer_id not in all_customers:
        return jsonify({ "error": f"Customer '{customer_id}' not found" }), 404

    payload = request.get_json()
    if not payload or "product_id" not in payload:
        return jsonify({ "error": "Missing product_id in request body" }), 400

    pid = str(payload["product_id"])
    qty = int(payload.get("quantity", 1))
    if pid not in all_products_dict:
        return jsonify({ "error": f"Product ID '{pid}' not found" }), 404

    cust = all_customers[customer_id]
    cust.get_cart().add_to_cart(all_products_dict[pid], qty)

    # from models.shopping_cart import ShoppingCart
    # fresh_cart = ShoppingCart(customer_id)
    # fresh_cart.add_to_cart(all_products_dict[pid], qty)
    return jsonify({ "message": "Product added to cart" }), 200


@app.route("/api/payment", methods=["POST"])
def checkout():
    data = request.get_json()
    
    customer_id = data["customerId"]
    cust = all_customers[customer_id]
    cart_items = cust.get_cart().get_cart_items()

    total_cost = sum(all_products_dict[item["product_id"]].price * item["quantity"] for item in cart_items)

    payment_details = data.get("payment_details", {})

    order_id = "O" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    order = Order(
        order_id,
        customer=cust,
        items=cart_items,
        total_cost=total_cost
    )

    success = order.make_payment(data["paymentMethod"], payment_details)
    
    if success:
        return jsonify({"status": "success", "message": "Payment successful!"})
    else:
        return jsonify({"status": "fail", "message": "Payment failed."}), 400


@app.route("/api/admin/login", methods=["POST"])
def admin_login():
    
    #Body: { "email": "...", "password": "..." }. Check against instantiated Admin objects in all_admins.
    
    
    data = request.get_json()
    if not data or "email" not in data or "password" not in data:
        return jsonify({ "error": "Missing email or password" }), 400

    email = data["email"]
    pwd   = data["password"]

    # Look up that email in our in-memory admin dictionary
    admin_obj = all_admins.get(email)
    if not admin_obj or not admin_obj.check_password(pwd):
        return jsonify({ "error": "Invalid credentials" }), 401

    return jsonify({ "message": "Login successful" }), 200


@app.route("/api/admin/sales", methods=["GET"])
def get_sales_summary():
    analytics = SalesAnalytics()
    summary = analytics.generate_summary()
    return jsonify(summary), 200
    

# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Loaded Products:", list(all_products_dict.keys()))
    print("Loaded Customers:", list(all_customers.keys()))
    print("Loaded Catalogues:", [(c.get_catalogue_id(), c.get_name()) for c in all_catalogues.values()])
    app.run(debug=True)
