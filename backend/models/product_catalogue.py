import csv
from models.product import Product

class ProductCatalogue:
    def __init__(self, csv_path="data/products.csv"):
        self.csv_path = csv_path
        self.products = {}
        self._load_products()

    def _load_products(self):
        with open(self.csv_path, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                prod = Product(
                    product_id=row["product_id"],
                    name=row["name"],
                    description=row["description"],
                    price=float(row["price"])
                )
                self.products[prod.product_id] = prod

    def get_all_products(self):
        return [p.to_dict() for p in self.products.values()]

    def get_product(self, product_id):
        return self.products.get(str(product_id))
