# backend/models/shopping_cart.py

import os
import csv
from models.database import DatabaseManager

class ShoppingCart:
    """
    Each ShoppingCart is tied to a single customer_id. 
    Internally, the cart is stored in 'carts.csv' with columns:
      [customer_id, product_id, quantity]
    We load all rows for this customer, keep them in-memory (dict),
    and on each change we write back the entire 'carts.csv' 
    so that other customers' rows remain intact.
    """

    def __init__(self, customer_id: str, csv_path=None):
        self.customer_id = str(customer_id)
        self.csv_path = csv_path or os.path.join("backend", "data", "cart.csv")
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.csv_path), exist_ok=True)
        self.items = {}  # Dictionary to store complete product info
        self._load_items()

    def _load_items(self):
        try:
            if not os.path.exists(self.csv_path):
                # Create the file with headers if it doesn't exist
                with open(self.csv_path, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=["customer_id", "product_id", "quantity"])
                    writer.writeheader()
                return

            with open(self.csv_path, newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["customer_id"] == self.customer_id:
                        pid = row["product_id"]
                        qty = int(row["quantity"])
                        if pid not in self.items:
                            self.items[pid] = {
                                "product_id": pid,
                                "quantity": qty
                            }
                        else:
                            self.items[pid]["quantity"] += qty
        except Exception as e:
            print(f"Error loading cart items: {str(e)}")
            self.items = {}

    def _save_all(self, all_rows):
        """Overwrite cart.csv with all_rows (list of dicts)."""
        with open(self.csv_path, "w", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["customer_id","product_id","quantity"])
            writer.writeheader()
            writer.writerows(all_rows)

    def _persist(self):
        # read existing rows, replace this customer's entries, then write all back
        all_rows = []
        # read existing
        if os.path.exists(self.csv_path):
            with open(self.csv_path, newline='') as f:
                all_rows = list(csv.DictReader(f))
        # filter out this customer's rows
        all_rows = [r for r in all_rows if r["customer_id"] != self.customer_id]
        # append current state
        for pid, item in self.items.items():
            all_rows.append({
                "customer_id": self.customer_id,
                "product_id": pid,
                "quantity": item["quantity"]
            })
        self._save_all(all_rows)

    def add_to_cart(self, product, quantity=1):
        """
        Add or update product in cart with complete product information
        """
        pid = str(product.product_id)
        if pid not in self.items:
            self.items[pid] = {
                "product_id": pid,
                "name": product.name,
                "price": product.price,
                "quantity": int(quantity)
            }
        else:
            self.items[pid]["quantity"] += int(quantity)
        self._persist()

    def get_cart_items(self):
        """
        Return a list of dicts with complete product information
        """
        return list(self.items.values())

    def clear(self):
        """Clear all items from the cart."""
        self.items = {}
        self._persist()
