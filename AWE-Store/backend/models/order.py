from models.payment_strategies.banktransfer_payment import BankTransfer
from models.payment_strategies.creditcard_payment import CreditCard
from models.payment_strategies.thirdparty_payment import ThirdParty
from models.payment_observer import observer

class Order():
    def __init__(self, order_id, customer_id, items, total_cost):
        self.order_id = order_id
        self.customer_id = customer_id
        self.items = items
        self.total_cost = total_cost
        self.status = "Pending"

    def _select_order(self): # not sure what this function is for? - finn
        selected_product = []
        for item in self.shopping_cart:
            is_selected = input("Order this product?")
            if is_selected.lower() == "yes":
                print(f"Add {item} to order list")
                selected_product.append(item)
                # remove from shopping cart object
            else:
                print(f"Excluded {item}")
        return selected_product

        # selected_product = []
        # for item in self.get_cart():
        #     is_selected = input("Order this product?")
        #     if is_selected.lower() == "yes":
        #         print(f"Add {item} to order list")
        #         self.order_list[item] = 
        #     else:
        #         print(f"Excluded {item}")
        
        # return selected_product
        pass

    def get_order(self):
        pass

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
            return True
        else:
            print("Payment failed.")
            return False

    def create_invoice(self):
        pass