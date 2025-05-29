from .payment_strategy import PaymentStrategy

class CreditCard(PaymentStrategy):
    def process_payment(self, total_cost: float) -> bool:
        print(f"[CreditCard] Processing payment of ${total_cost:.2f}")
        # Actual credit card processing logic pending
        return True