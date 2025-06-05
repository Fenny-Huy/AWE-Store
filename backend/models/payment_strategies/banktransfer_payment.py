from .payment_strategy import PaymentStrategy

class BankTransfer(PaymentStrategy):

    def __init__(self, payment_details=None):
        self.payment_details = payment_details or {}

    def process_payment(self, total_cost: float) -> bool:
        print(f"[BankTransfer] Processing payment of ${float(total_cost):.2f}")
        # Actual bank transfer processing logic pending
        return True
