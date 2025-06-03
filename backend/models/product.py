# backend/models/product.py

class Product:
    """
    Simple in-memory representation of a product.
    Instances are constructed by ProductCatalogue from table rows.
    """

    def __init__(self, product_id: str, name: str, description: str, price: float):
        self.product_id = str(product_id)
        self.name = name
        self.description = description
        self.price = float(price)

    def return_info(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "description": self.description,
            "price": self.price
        }
