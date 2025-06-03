from models.shopping_cart import ShoppingCart
from models.order import Order
from models.user import User
import os
import json

class Customer:
    def __init__(self, customer_id):
        self.customer_id = str(customer_id)
        self.shopping_cart = ShoppingCart(self.customer_id)
        self.user_data = self._load_user_data()
        self.orders = self._load_orders()

    def _load_user_data(self):
        # This would typically load from a database, but for now we'll use the User class
        user = User(self.customer_id)
        return user.user_data

    def _load_orders(self):
        orders = []
        orders_dir = os.path.join("backend", "data", "orders")
        if os.path.exists(orders_dir):
            for file in os.listdir(orders_dir):
                if file.endswith(".json"):
                    with open(os.path.join(orders_dir, file), 'r') as f:
                        order_data = json.load(f)
                        if order_data["customer_id"] == self.customer_id:
                            orders.append(order_data)
        return orders

    def get_cart(self):
        return self.shopping_cart

    def create_order(self):
        """
        Create a new order from the current shopping cart items
        Returns the created order object
        """
        cart_items = self.shopping_cart._load_items()
        if not cart_items:
            raise ValueError("Shopping cart is empty")

        order = Order(self, cart_items)
        return order

    def place_order(self):
        """
        Create and process an order with payment
        Returns the order status and invoice information
        """
        order = self.create_order()
        
        # Create invoice
        invoice = order.create_invoice()
        
        # Process payment
        payment_result = order.process_payment()
        
        if payment_result["success"]:
            # Reload orders after successful payment
            self.orders = self._load_orders()
            
        return payment_result

    def get_orders(self):
        """
        Get all orders for this customer
        """
        return self.orders

    def get_order_by_id(self, order_id):
        """
        Get a specific order by its ID
        """
        for order in self.orders:
            if order["order_id"] == order_id:
                return order
        return None


    def get_role(self) -> str:
        """
        Every concrete account subclass must implement this,
        returning something like "customer" or "admin".
        """
        return "customer"

    def get_customer_id(self) -> str:
        """Return this customer's ID (the same as account_id)."""
        return self.customer_id
    

    
# customer = Customer(2)
# print(customer.customer.user_data["name"])
