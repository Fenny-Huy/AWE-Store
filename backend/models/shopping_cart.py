# backend/models/shopping_cart.py

import csv
import os
from database import Database

class ShoppingCart:
    """
    Each ShoppingCart is tied to one customer_id. It loads existing rows from carts.csv
    on initialization, and writes back to carts.csv on every change.

    CSV schema (carts.csv):
      customer_id,product_id,quantity
    """

    def __init__(self, customer_id, csv_path="data/carts.csv"):
        self.customer_id = str(customer_id)
        self.csv_path = csv_path
        self.db = Database()
        self.items = {}  # in-memory map: product_id -> quantity

        # Load any existing cart rows for this customer
        self._load_items_from_csv()

    def _load_items_from_csv(self):
        if not os.path.exists(self.csv_path):
            return

        with open(self.csv_path, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["customer_id"] == self.customer_id:
                    pid = row["product_id"]
                    qty = int(row["quantity"])
                    self.items[pid] = self.items.get(pid, 0) + qty

    def _persist_all_rows(self, all_rows):
        """
        Overwrite carts.csv with all_rows, which is a list of dicts 
        having exactly the columns: customer_id,product_id,quantity
        """
        with open(self.csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["customer_id","product_id","quantity"])
            writer.writeheader()
            writer.writerows(all_rows)

    def _save_current_state(self):
        """
        1. Read *all* existing rows from carts.csv,
        2. Filter out any rows belonging to this.customer_id,
        3. Append rows for this.customer_id from self.items,
        4. Overwrite carts.csv with this combined list.
        """
        all_rows = []
        if os.path.exists(self.csv_path):
            with open(self.csv_path, newline="") as f:
                all_rows = list(csv.DictReader(f))

        # Remove existing rows for this customer
        all_rows = [r for r in all_rows if r["customer_id"] != self.customer_id]

        # Append the “current” items for this customer
        for pid, qty in self.items.items():
            all_rows.append({
                "customer_id": self.customer_id,
                "product_id": pid,
                "quantity": qty
            })

        # Overwrite the CSV
        self._persist_all_rows(all_rows)

    def add_to_cart(self, product, quantity=1):
        """
        Increase the quantity of product.product_id by `quantity`, then write out.
        """
        pid = str(product.product_id)
        self.items[pid] = self.items.get(pid, 0) + int(quantity)
        self._save_current_state()

    def get_cart_items(self):
        """
        Return a list of dicts like { "product_id": "...", "quantity": N } 
        for everything in this customer's cart.
        """
        return [{"product_id": pid, "quantity": qty} for pid, qty in self.items.items()]
