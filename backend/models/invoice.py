# backend/models/invoice.py

from datetime import datetime, timedelta

class Invoice:
    # Represents a finalized invoice for an order
    
    def __init__(
        self,
        order_id: str,
        customer_id: str,
        items: list,
        total_cost: float,
        status: str,
        customer_email: str = None,
        customer_name: str = None
    ):
        # Initialize all attributes, record current timestamp
        self.order_id = order_id
        self.customer_id = customer_id
        self.items = items
        self.total_cost = total_cost
        self.status = status
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.customer_email = customer_email
        self.customer_name = customer_name
        self.shipping_status = "Processing"
        self.estimated_delivery = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")

    def return_info(self) -> dict:
        # Return a JSON format string with all invoice details
        return {
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "customer_name": self.customer_name,
            "customer_email": self.customer_email,
            "items": self.items,
            "total_cost": self.total_cost,
            "status": self.status,
            "timestamp": self.timestamp,
            "shipping_details": {
                "status": self.shipping_status,
                "estimated_delivery": self.estimated_delivery
            }
        }
