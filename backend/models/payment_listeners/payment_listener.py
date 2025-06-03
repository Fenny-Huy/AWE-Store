from abc import ABC, abstractmethod

class PaymentListener(ABC):
    @abstractmethod
    def on_payment_success(self, order_id: str):
        #Called when a payment has been successfully processed
        pass