from models.shopping_cart import ShoppingCart

class Customer:
    def __init__(self, customer_id):
        self.customer_id = str(customer_id)

    def get_cart(self):
        # each call gives a fresh ShoppingCart tied to this customer and CSV persistence
        return ShoppingCart(self.customer_id)
