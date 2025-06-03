import os
import json

class User:
    def __init__(self, customer_id):
        self.customer_id = str(customer_id)
        self.user_data = self._load_user_data()

    def _load_user_data(self):
        """Load user data from JSON file, or return default data if not found."""
        try:
            # First, try to load from customers.json
            data_file = os.path.join("data", "customers.json")
            if os.path.exists(data_file):
                with open(data_file, 'r') as f:
                    customers = json.load(f)
                    if self.customer_id in customers:
                        return customers[self.customer_id]

            # If not found, return default data
            return {
                "customer_id": self.customer_id,
                "name": f"Customer {self.customer_id}",
                "email": f"customer{self.customer_id}@example.com"
            }
        except Exception as e:
            print(f"Error loading user data: {str(e)}")
            # Return default data in case of error
            return {
                "customer_id": self.customer_id,
                "name": f"Customer {self.customer_id}",
                "email": f"customer{self.customer_id}@example.com"
            }

    def __getitem__(self, key):
        if self.user_data and key in self.user_data:
            return self.user_data[key]
        raise KeyError(f"{key} not found in user data.")