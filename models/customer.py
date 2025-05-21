from models.shopping_cart import ShoppingCart

class Customer:
    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.shopping_cart = ShoppingCart()

    def get_cart(self):
        return self.shopping_cart
