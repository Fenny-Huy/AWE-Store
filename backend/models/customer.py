# backend/models/customer.py

from models.account import Account
from models.database import DatabaseManager
from models.shopping_cart import ShoppingCart
from models.order import Order

class Customer(Account):
    """
    Customer inherits Account. 
    On init, it validates its own row in 'customers.csv' 
    and then creates a ShoppingCart object for this customer_id.
    """

    def __init__(self, customer_id: str):
        # First, load the Account portion (email, name, etc.)
        super().__init__(customer_id)

        self.customer_id = str(customer_id)
        dbm = DatabaseManager()
        table = dbm.get_table("customers")
        if table is None:
            raise ValueError("Table 'customers' does not exist")

    

        # Initialize this customer's cart
        # self.shopping_cart = ShoppingCart(self.customer_id)

    def get_cart(self):
        return ShoppingCart(self.customer_id)

    def get_role(self) -> str:
        """
        Every concrete account subclass must implement this,
        returning something like "customer" or "admin".
        """
        return "customer"


    def place_order(self):
        """
        Create and process an order with payment
        Returns the order status and invoice information
        """
        order = self.create_order()
        cart_items = self.get_cart().get_cart_items()
        # Create invoice
        order = Order(self, cart_items)
        # return order
        invoice = order.create_invoice()
        # Process payment
        payment_result = order.process_payment()
        
        if payment_result["success"]:
            # Reload orders after successful payment
            self.orders = self._load_orders()
            self.get_cart().clear_cart()
            
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
