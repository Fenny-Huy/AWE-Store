class PaymentObserver:
    def __init__(self):
        self._observers = []

    def register(self, observer):
        #Register a new listener that implements on_payment_success(order_id)
        self._observers.append(observer)

    def notify_all(self, order_id: str):
        #Notify all registered listeners when a payment is successful
        print(f"[Observer] Notifying {len(self._observers)} observers for order {order_id}")
        for observer in self._observers:
            observer.on_payment_success(order_id)

# Shared instance used across the app
observer = PaymentObserver()