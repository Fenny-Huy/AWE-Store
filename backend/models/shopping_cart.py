# backend/models/shopping_cart.py

import os
from models.database import DatabaseManager

class ShoppingCart:
    """
    Each ShoppingCart is tied to a single customer_id. 
    Internally, the cart is stored in 'carts.csv' with columns:
      [customer_id, product_id, quantity]
    We load all rows for this customer, keep them in-memory (dict),
    and on each change we write back the entire 'carts.csv' 
    so that other customers’ rows remain intact.
    """

    def __init__(self, customer_id: str):
        self.customer_id = str(customer_id)
        dbm = DatabaseManager()
        # Ensure the 'carts' table exists with the correct columns
        self.table = dbm.get_table("carts")
        if self.table is None:
            # If the CSV doesn’t exist yet, create it with these columns:
            self.table = dbm.create_table("carts", ["customer_id", "product_id", "quantity"])

        # Build an in-memory map: product_id -> quantity
        self.items = {}
        for row in self.table.rows:
            if row["customer_id"] == self.customer_id:
                pid = row["product_id"]
                qty = int(row["quantity"])
                self.items[pid] = self.items.get(pid, 0) + qty

    def _persist_all_rows(self):
        """
        Overwrite 'carts.csv' so that:
        1) Rows belonging to other customers remain as-is.
        2) Rows for self.customer_id reflect self.items (one row per product_id).
        """
        all_rows = []
        # Collect rows for OTHER customers
        for row in self.table.rows:
            if row["customer_id"] != self.customer_id:
                all_rows.append(row)

        # Add this customer's current rows
        for pid, qty in self.items.items():
            all_rows.append({
                "customer_id": self.customer_id,
                "product_id": pid,
                "quantity": str(qty)
            })

        # Replace the table’s in-memory rows and save
        self.table.rows = all_rows
        self.table.save()

    def add_to_cart(self, product, quantity=1):
        """
        Increase quantity for product.product_id, or add new if missing.
        Then persist all carts back to 'carts.csv'.
        """
        pid = str(product.product_id)
        self.items[pid] = self.items.get(pid, 0) + int(quantity)
        self._persist_all_rows()

    def get_cart_items(self):
        """
        Return a list of dicts [{"product_id": "...", "quantity": N}, ...]
        representing this customer's cart.
        """
        return [{"product_id": pid, "quantity": qty} for pid, qty in self.items.items()]
    
    def clear_cart(self):
        """
        Remove all items from the cart and persist the change.
        """
        self.items = {}
        self._persist_all_rows()
