from .payment_strategy import PaymentStrategy

class ThirdParty(PaymentStrategy):

    def __init__(self, payment_details=None):
        self.payment_details = payment_details or {}

    def process_payment(self, total_cost: float) -> bool:
        print(f"[ThirdParty] Processing payment of ${float(total_cost):.2f}")
        # Actual third-party payment processing logic pending
        return True
