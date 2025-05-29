from .payment_listener import PaymentListener
import csv
import os

class Shipment(PaymentListener):
    def __init__(self):
        self.file_path = "data/shipments.csv"
        
        # Create file with headers if it doesn't exist
        if not os.path.exists(self.file_path):
            with open(self.file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Order ID", "Shipment Status", "Message"])

    def on_payment_success(self, order_id: str):
        print(f"[Shipment] Creating shipment for order {order_id}")

        with open(self.file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([order_id, "Queued", "Shipment initiated"])

    #Future implementations:
    def update_shipment(): ...
    def cancel_shipment(): ...