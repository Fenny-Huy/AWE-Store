from .payment_strategy import PaymentStrategy

class ThirdParty(PaymentStrategy):
    def process_payment(self, total_cost: float) -> bool:
        print(f"[ThirdParty] Processing payment of ${total_cost:.2f}")
        # Actual third-party payment processing logic pending
        return True
