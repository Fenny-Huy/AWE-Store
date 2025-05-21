from models.product import Product

class ProductCatalogue:
    def __init__(self):
        self.products = {}

    def add_product(self, product: Product):
        self.products[product.product_id] = product

    def get_all_products(self):
        return [p.to_dict() for p in self.products.values()]

    def get_product(self, product_id):
        return self.products.get(product_id)
