import json
import os
from datetime import datetime

class Payment:
    def __init__(self):
        self.payments_dir = os.path.join("data", "payments")
        os.makedirs(self.payments_dir, exist_ok=True)

    def process_payment(self, payment_data):
        """
        Process a payment for an order.
        
        Args:
            payment_data (dict): Contains amount, order_id, and customer_id
            
        Returns:
            dict: Payment result with success status and message
        """
        try:
            # In a real system, this would integrate with a payment gateway
            # For this demo, we'll simulate a successful payment
            payment_record = {
                "payment_id": f"PAY-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "order_id": payment_data["order_id"],
                "customer_id": payment_data["customer_id"],
                "amount": payment_data["amount"],
                "status": "completed",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            # Save payment record
            payment_file = os.path.join(self.payments_dir, f"{payment_record['payment_id']}.json")
            with open(payment_file, 'w') as f:
                json.dump(payment_record, f, indent=2)

            return {
                "success": True,
                "payment_id": payment_record["payment_id"],
                "message": "Payment processed successfully"
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Payment processing failed: {str(e)}"
            }

