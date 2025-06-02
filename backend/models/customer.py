# backend/models/customer.py

from models.account import Account
from database import Database

class Customer(Account):
    """
    Customer extends Account. It must be initialized with a customer_id.
    - First, we load the Account portion (via super().__init__).
    - Then we load the customers table to confirm existence.
    """

    def __init__(self, customer_id):
        # Load "account" fields first
        super().__init__(customer_id)

        self.customer_id = str(customer_id)
        self.db = Database()
        self.customer_data = self.db.get_table("customers")  # list of dicts

        # Verify that this customer_id exists in customers.csv
        self.my_customer_record = None
        for row in self.customer_data:
            if row["customer_id"] == self.customer_id:
                self.my_customer_record = row
                break

        if not self.my_customer_record:
            raise ValueError(f"Customer ID '{self.customer_id}' not found in customers table")

        # Now initialize a cart for this customer
        from models.shopping_cart import ShoppingCart
        self.shopping_cart = ShoppingCart(self.customer_id)

    def get_cart(self):
        """Return this customer's ShoppingCart instance."""
        return self.shopping_cart
