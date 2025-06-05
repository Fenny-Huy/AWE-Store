from models.payment_strategies.banktransfer_payment import BankTransfer
from models.payment_strategies.creditcard_payment import CreditCard
from models.payment_strategies.thirdparty_payment import ThirdParty
from models.payment_observer import observer
from models.shopping_cart import ShoppingCart  
from datetime import datetime
from models.database import DatabaseManager
import json

class Order():
    def __init__(self, order_id, customer_id, items, total_cost):
        self.order_id = order_id
        self.customer_id = customer_id
        self.items = items.get_cart_items() if hasattr(items, 'get_cart_items') else items
        self.total_cost = total_cost
        self.invoice = None
        self.status = "Pending"
        

    def save_order(self) -> bool:
        dbm = DatabaseManager()
        
        #Saves the order to the database.
        #Returns True if successful, False otherwise.
        
        print(f"Saving order: {self.order_id}")
        try:
            order_table = dbm.get_table("order")
            if not order_table:
                # Create order table if it doesn't exist
                print("Creating order table")
                order_table = dbm.create_table("order", ["order_id", "customer_id", "total_cost", "items", "status"])
            
            # Save order data
            order_table.add_row({
                "order_id": self.order_id,
                "customer_id": self.customer_id,
                "total_cost": self.total_cost,
                "items": json.dumps(self.items),  # items is already a list
                "status": self.status
            })
            return True
        except Exception as e:
            print(f"Error saving order: {e}")
            return False

    def make_payment(self, payment_method: str, payment_details: dict = None):
        
        #Process payment using the specified payment method.
        #payment_method should be one of: 'credit', 'bank', 'thirdparty'
        
        if self.invoice is None:
            self.create_invoice()

        method = payment_method.lower()
        print(f"Payment method: {method}")
        
        # Select the appropriate payment strategy
        if method == "credit":
            payment_strategy = CreditCard(payment_details)
        elif method == "bank":
            payment_strategy = BankTransfer(payment_details)
        elif method == "thirdparty":
            payment_strategy = ThirdParty(payment_details)
        else:
            print("Error: Unsupported payment method.")
            return False

        # Process payment
        success = payment_strategy.process_payment(self.total_cost)
        if success:
            self.status = "Paid"
            print(f"Order {self.order_id} marked as paid.")
            
            # Save the order to database
            if self.save_order():
                # Notify observers only if save was successful
                observer.notify_all(self.order_id)

                #Clear shopping cart only once order has been saved
                ShoppingCart(self.customer_id).clear_cart()
                return True
            else:
                print("Error: Order payment successful but failed to save order.")
                return False
        else:
            print("Payment failed.")
            return False

    def create_invoice(self):
        
        #Creates an invoice for the order containing all relevant details.
        #Returns a dictionary with order information.
        
        invoice = {
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "items": self.items,  # Now it's a list that can be JSON serialized
            "total_cost": self.total_cost,
            "status": self.status,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return invoice