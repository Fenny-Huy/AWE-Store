import os
import json

# from models.database import DatabaseManager
from models.database import DatabaseManager

class User:
    def __init__(self, customer_id):
        self.customer_id = str(customer_id)
        self.db = DatabaseManager()
        self.user_data = self._load_user_data()

    def _load_user_data(self):
        """Load user data from the database."""
        try:
            # First check the customers table
            customers_table = self.db.get_table("customers")
            if not customers_table:
                raise ValueError("Customers table not found")

            customer_data = customers_table.get_row_by_column_value("customer_id", self.customer_id)
            if not customer_data:
                raise ValueError(f"Customer {self.customer_id} not found")

            # Then get the account data
            accounts_table = self.db.get_table("accounts")
            if not accounts_table:
                raise ValueError("Accounts table not found")

            account_id = customer_data.get("account_id")
            if not account_id:
                raise ValueError(f"No account_id found for customer {self.customer_id}")

            account_data = accounts_table.get_row_by_column_value("account_id", account_id)
            if not account_data:
                raise ValueError(f"Account {account_id} not found")

            # Combine customer and account data
            return {
                "customer_id": self.customer_id,
                "account_id": account_id,
                "name": account_data.get("name", f"Customer {self.customer_id}"),
                "email": account_data.get("email", f"customer{self.customer_id}@example.com"),
                "role": account_data.get("role", "customer")
            }
        except Exception as e:
            print(f"Error loading user data: {str(e)}")
            # Return default data in case of error
            return {
                "customer_id": self.customer_id,
                "account_id": self.customer_id,
                "name": f"Customer {self.customer_id}",
                "email": f"customer{self.customer_id}@example.com",
                "role": "customer"
            }

    def __getitem__(self, key):
        if self.user_data and key in self.user_data:
            return self.user_data[key]
        raise KeyError(f"{key} not found in user data.")