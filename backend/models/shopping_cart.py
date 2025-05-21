class ShoppingCart:
    def __init__(self):
        self.items = {}

    def add_to_cart(self, product, quantity=1):
        if product.product_id in self.items:
            self.items[product.product_id]["quantity"] += quantity
        else:
            self.items[product.product_id] = {
                "product": product,
                "quantity": quantity
            }

    def get_cart_items(self):
        return [
            {
                "id": p["product"].product_id,
                "name": p["product"].name,
                "price": p["product"].price,
                "quantity": p["quantity"]
            }
            for p in self.items.values()
        ]
