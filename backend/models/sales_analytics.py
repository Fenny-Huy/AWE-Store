# backend/models/sales_analytics.py

import json
from .database import DatabaseManager

class SalesAnalytics:
    """
    Reads the 'order' table (backed by order.csv) and computes:
      - total_revenue
      - total_orders
      - product_sales: { product_id: total_quantity_sold }
    """

    def __init__(self):
        dbm = DatabaseManager()
        self.order_table = dbm.get_table("order")
        if self.order_table is None:
            # If no order table exists, create it with the expected columns:
            self.order_table = dbm.create_table(
                "order",
                ["order_id", "customer_id", "total_cost", "items", "status"]
            )

    def generate_summary(self) -> dict:
        total_revenue = 0.0
        total_orders = 0
        product_sales = {}  # product_id -> total quantity sold

        for row in self.order_table.rows:
            # Each row is a dict with keys: order_id, customer_id, total_cost, items (JSON), status
            try:
                total_cost = float(row.get("total_cost", 0))
            except ValueError:
                total_cost = 0.0
            total_revenue += total_cost
            total_orders += 1

            # 'items' is stored as a JSON string: [{"product_id":"3","quantity":4}, ...]
            try:
                items_list = json.loads(row.get("items", "[]"))
            except json.JSONDecodeError:
                items_list = []

            for entry in items_list:
                pid = entry.get("product_id")
                qty = int(entry.get("quantity", 0))
                if pid:
                    product_sales[pid] = product_sales.get(pid, 0) + qty

        return {
            "total_revenue": round(total_revenue, 2),
            "total_orders": total_orders,
            "product_sales": product_sales
        }
