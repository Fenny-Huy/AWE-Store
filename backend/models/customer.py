# backend/models/customer.py

from models.account import Account
from models.database import DatabaseManager
from models.shopping_cart import ShoppingCart

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
        self.table = dbm.get_table("customers")
        if self.table is None:
            raise ValueError("Table 'customers' does not exist")

    

        # Initialize this customer's cart
        self.shopping_cart = ShoppingCart(self.customer_id)

    def get_cart(self):
        return self.shopping_cart

    def get_role(self) -> str:
        """
        Every concrete account subclass must implement this,
        returning something like "customer" or "admin".
        """
        return "customer"

    def get_customer_id(self) -> str:
        """Return this customer's ID (the same as account_id)."""
        return self.customer_id
