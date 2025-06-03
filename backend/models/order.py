from models.payment import Payment
from datetime import datetime
import os
import json
import uuid
from models.payment_strategies.banktransfer_payment import BankTransfer
from models.payment_strategies.creditcard_payment import CreditCard
from models.payment_strategies.thirdparty_payment import ThirdParty
from models.payment_observer import observer

class Order:
    def __init__(self, customer, cart_items):
        self.order_id = str(uuid.uuid4())
        self.customer = customer
        self.cart_items = cart_items
        self.order_date = datetime.now()
        self.status = "pending"
        self.total_amount = self._calculate_total()
        self.invoice = None

    def _calculate_total(self):
        total = 0
        for item in self.cart_items:
            total += float(item.get('price', 0)) * int(item.get('quantity', 0))
        return total

    def create_invoice(self):
        self.invoice = {
            "invoice_id": f"INV-{self.order_id[:8]}",
            "order_id": self.order_id,
            "date": self.order_date.strftime("%Y-%m-%d %H:%M:%S"),
            "customer": {
                "id": self.customer.customer_id,
                "name": self.customer.user_data.get("name", ""),
                "email": self.customer.user_data.get("email", "")
            },
            "items": self.cart_items,
            "total_amount": self.total_amount
        }
        
        # Save invoice to file
        os.makedirs(os.path.join("backend", "data", "invoices"), exist_ok=True)
        invoice_path = os.path.join("backend", "data", "invoices", f"{self.invoice['invoice_id']}.json")
        with open(invoice_path, 'w') as f:
            json.dump(self.invoice, f, indent=2)
        
        return self.invoice

    # def process_payment(self):
    #     if not self.invoice:
    #         self.create_invoice()
            
    #     payment = Payment()
    #     payment_result = payment.process_payment({
    #         "amount": self.total_amount,
    #         "order_id": self.order_id,
    #         "customer_id": self.customer.customer_id
    #     })
        
    #     if payment_result.get("success"):
    #         self.status = "paid"
    #         self._save_order()
    #         self._clear_cart()
    #         return {"success": True, "message": "Payment processed successfully", "invoice": self.invoice}
    #     else:
    #         self.status = "payment_failed"
    #         return {"success": False, "message": payment_result.get("error", "Payment processing failed")}

    def make_payment(self, method: str):
        method = method.lower()
        if not self.invoice:
            self.create_invoice()
        
        # Select the appropriate payment strategy
        if method == "credit":
            payment_strategy = CreditCard()
        elif method == "bank":
            payment_strategy = BankTransfer()
        elif method == "thirdparty":
            payment_strategy = ThirdParty()
        else:
            print("Error: Unsupported payment method.")
            return False

        # Process payment
        success = payment_strategy.process_payment(self.total_cost)
        if success:
            self.status = "Paid"
            print(f"Order {self.order_id} marked as paid.")
            observer.notify_all(self.order_id)
            return True
        else:
            print("Payment failed.")
            return False
        
    def _save_order(self):
        order_data = {
            "order_id": self.order_id,
            "customer_id": self.customer.customer_id,
            "date": self.order_date.strftime("%Y-%m-%d %H:%M:%S"),
            "items": self.cart_items,
            "total_amount": self.total_amount,
            "status": self.status
        }
        
        os.makedirs(os.path.join("backend", "data", "orders"), exist_ok=True)
        order_path = os.path.join("backend", "data", "orders", f"{self.order_id}.json")
        with open(order_path, 'w') as f:
            json.dump(order_data, f, indent=2)

    def _clear_cart(self):
        # Clear the shopping cart after successful order
        self.customer.shopping_cart.clear()

    def get_order_status(self):
        return {
            "order_id": self.order_id,
            "status": self.status,
            "total_amount": self.total_amount,
            "date": self.order_date.strftime("%Y-%m-%d %H:%M:%S")
        }
