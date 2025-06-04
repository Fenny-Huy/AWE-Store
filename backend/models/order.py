from models.payment_strategies.banktransfer_payment import BankTransfer
from models.payment_strategies.creditcard_payment import CreditCard
from models.payment_strategies.thirdparty_payment import ThirdParty
from models.payment_observer import observer
# from models.customer import Customer
from datetime import datetime

class Order():
    def __init__(self, order_id, customer_id, items, total_cost):
        self.order_id = order_id
        # self.customer_id = customer_id
        self.items = items
        self.total_cost = total_cost
        self.status = "Pending"

    def make_payment(self, method: str):
        method = method.lower()
        
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

            # cust = Customer(self.customer_id)
            # cust.get_cart().clear_cart()
            return True
        else:
            print("Payment failed.")
            return False

    def create_invoice(self):
        """
        Creates an invoice for the order containing all relevant details.
        Returns a dictionary with order information.
        """
        invoice = {
            "order_id": self.order_id,
            "items": self.items,
            "total_cost": self.total_cost,
            "status": self.status,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return invoice