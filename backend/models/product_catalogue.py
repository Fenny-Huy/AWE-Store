# backend/models/product_catalogue.py

from database import Database
from models.product import Product

class ProductCatalogue:
    """
    On init, loads every row from products.csv and turns each into a Product object.
    """

    def __init__(self):
        self.db = Database()
        self.products = {}  # maps product_id -> Product instance
        self._load_products()

    def _load_products(self):
        rows = self.db.get_table("products")  # list of dicts
        for row in rows:
            p = Product(
                product_id = row["product_id"],
                name       = row["name"],
                description= row["description"],
                price      = row["price"]
            )
            self.products[p.product_id] = p

    def get_all_products(self):
        """Return a list of dicts (for JSON) for every Product."""
        return [p.to_dict() for p in self.products.values()]

    def get_product(self, product_id):
        """Return the Product instance matching product_id, or None if not found."""
        return self.products.get(str(product_id))
