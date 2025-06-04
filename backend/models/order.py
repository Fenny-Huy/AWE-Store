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
        
        # Ensure required directories exist
        self.data_dir = os.path.join("backend", "data")
        self.orders_dir = os.path.join(self.data_dir, "orders")
        self.invoices_dir = os.path.join(self.data_dir, "invoices")
        os.makedirs(self.orders_dir, exist_ok=True)
        os.makedirs(self.invoices_dir, exist_ok=True)

    def _calculate_total(self):
        total = 0
        for item in self.cart_items:
            total += float(item.get('price', 0)) * int(item.get('quantity', 0))
        return total

    def create_invoice(self):
        try:
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
            invoice_path = os.path.join(self.invoices_dir, f"{self.invoice['invoice_id']}.json")
            with open(invoice_path, 'w') as f:
                json.dump(self.invoice, f, indent=2)
            
            return self.invoice
        except Exception as e:
            print(f"Error creating invoice: {str(e)}")
            raise

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
        try:
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
            success = payment_strategy.process_payment(self.total_amount)
            if success:
                self.status = "Paid"
                print(f"Order {self.order_id} marked as paid.")
                observer.notify_all(self.order_id)
                self._save_order()
                self._clear_cart()
                return True
            else:
                print("Payment failed.")
                return False
        except Exception as e:
            print(f"Error processing payment: {str(e)}")
            return False

    def process_payment(self):
        """
        Process payment using default payment method (credit card)
        Returns dict with success status and additional info
        """
        try:
            if not self.invoice:
                self.create_invoice()
                
            success = self.make_payment("credit")
            
            if success:
                return {
                    "success": True, 
                    "message": "Payment processed successfully", 
                    "order_id": self.order_id,
                    "invoice": self.invoice
                }
            else:
                return {
                    "success": False, 
                    "message": "Payment processing failed"
                }
        except Exception as e:
            print(f"Error in process_payment: {str(e)}")
            return {
                "success": False,
                "message": f"Payment processing error: {str(e)}"
            }
        
    def _save_order(self):
        try:
            order_data = {
                "order_id": self.order_id,
                "customer_id": self.customer.customer_id,
                "date": self.order_date.strftime("%Y-%m-%d %H:%M:%S"),
                "items": self.cart_items,
                "total_amount": self.total_amount,
                "status": self.status
            }
            
            order_path = os.path.join(self.orders_dir, f"{self.order_id}.json")
            with open(order_path, 'w') as f:
                json.dump(order_data, f, indent=2)
        except Exception as e:
            print(f"Error saving order: {str(e)}")
            raise

    def _clear_cart(self):
        try:
            # Clear the shopping cart after successful order
            self.customer.shopping_cart.clear()
        except Exception as e:
            print(f"Error clearing cart: {str(e)}")
            raise

    def get_order_status(self):
        return {
            "order_id": self.order_id,
            "status": self.status,
            "total_amount": self.total_amount,
            "date": self.order_date.strftime("%Y-%m-%d %H:%M:%S")
        }
