from .payment_strategy import PaymentStrategy

class CreditCard(PaymentStrategy):

    def __init__(self, payment_details=None):
        self.payment_details = payment_details or {}

    def process_payment(self, total_cost: float) -> bool:
        print(f"[CreditCard] Processing payment of ${float(total_cost):.2f}")
        # Actual credit card processing logic pending
        return True