import csv
import os

class ShoppingCart:
    def __init__(self, customer_id, csv_path="data/cart.csv"):
        self.customer_id = str(customer_id)
        self.csv_path = csv_path
        self.items = self._load_items()

    def _load_items(self):
        items = {}
        if not os.path.exists(self.csv_path):
            return items
        with open(self.csv_path, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["customer_id"] == self.customer_id:
                    pid = row["product_id"]
                    qty = int(row["quantity"])
                    items[pid] = items.get(pid, 0) + qty
        return items

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
        for pid, qty in self.items.items():
            all_rows.append({
                "customer_id": self.customer_id,
                "product_id": pid,
                "quantity": qty
            })
        self._save_all(all_rows)

    def add_to_cart(self, product, quantity=1):
        pid = str(product.product_id)
        self.items[pid] = self.items.get(pid, 0) + int(quantity)
        self._persist()

    def get_cart_items(self):
        """Return list of {"id","quantity"} dicts."""
        return [{"product_id": pid, "quantity": qty} for pid, qty in self.items.items()]
