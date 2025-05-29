from .payment_listener import PaymentListener

class NotificationSystem(PaymentListener):
    def __init__(self):
        pass

    def on_payment_success(self, order_id: str):
        print(f"[NotificationSystem] Sent confirmation email for order {order_id}")
        # Future implementation: integrate with email server or API

    #Possible future implementations:
    def send_shipping_update(self, order_id, status): ...
    def send_custom_alert(self, user_id, message): ...
