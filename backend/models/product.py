# backend/models/product.py

class Product:
    """
    Simple Product class. No DB calls here; it just stores values given by ProductCatalogue.
    """

    def __init__(self, product_id, name, description, price):
        self.product_id = str(product_id)
        self.name = name
        self.description = description
        self.price = float(price)

    def to_dict(self):
        """
        Return a JSON-serializable representation for the frontend.
        """
        return {
            "product_id": self.product_id,
            "name": self.name,
            "description": self.description,
            "price": self.price
        }
