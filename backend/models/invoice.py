# backend/models/invoice.py

from datetime import datetime

class Invoice:
    # Represents a finalized invoice for an order
    
    def __init__(
        self,
        order_id: str,
        customer_id: str,
        items: list,
        total_cost: float,
        status: str
    ):
        # Initialize all attributes, record current timestamp
        self.order_id = order_id
        self.customer_id = customer_id
        self.items = items
        self.total_cost = total_cost
        self.status = status
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def return_info(self) -> dict:
        # Return a JSON format string with all invoice details
        return {
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "items": self.items,
            "total_cost": self.total_cost,
            "status": self.status,
            "timestamp": self.timestamp
        }
