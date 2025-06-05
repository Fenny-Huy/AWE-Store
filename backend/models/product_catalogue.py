# backend/models/product_catalogue.py

from .product import Product

class ProductCatalogue:
    #Represents a single catalogue (e.g. "Organic", "Discounted", "Dairy").
    #Each instance holds a subset of Product instances, passed in at construction.

    def __init__(self, catalogue_id: str, name: str, product_list: list[Product]):
        self.catalogue_id = str(catalogue_id)
        self.name = name
        # Map product_id -> Product instance
        self.products = {p.product_id: p for p in product_list}

    def get_catalogue_id(self) -> str:
        return self.catalogue_id

    def get_name(self) -> str:
        return self.name

    def get_all_products(self) -> list[dict]:
        #Return a JSON‐serializable list (dicts) of every Product in this catalogue.
        return [p.return_info() for p in self.products.values()]

    def get_product(self, product_id: str):
        
        #Return the Product instance (or None if not in this catalogue).
        return self.products.get(str(product_id))
