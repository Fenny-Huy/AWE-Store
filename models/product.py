class Product:
    def __init__(self, product_id, name, description, price):
        self.product_id = product_id
        self.name = name
        self.description = description
        self.price = price

    def to_dict(self):
        return {
            "id": self.product_id,
            "name": self.name,
            "description": self.description,
            "price": self.price
        }
