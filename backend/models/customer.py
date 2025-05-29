from models.shopping_cart import ShoppingCart
from models.order import Order
from models.user import User
import os
import csv

class Customer:
    def __init__(self, customer_id):
        self.customer_id = str(customer_id)
        self.shopping_cart = ShoppingCart(self.customer_id)
        self.customer = User(customer_id)
        self.order_list = {}

    def get_cart(self):
        # each call gives a fresh ShoppingCart tied to this customer and CSV persistence
        # return ShoppingCart(self.customer_id)
        return self.shopping_cart


    def ordering_product(self):
        order = Order(self.customer_id, self.shopping_cart._load_items())

        # selected_product = []
        # for item in self.get_cart():
        #     is_selected = input("Order this product?")
        #     if is_selected.lower() == "yes":
        #         print(f"Add {item} to order list")
        #         self.order_list[item] = 
        #     else:
        #         print(f"Excluded {item}")
        
        # return selected_product

customer = Customer(2)

print(customer.customer.user_data["name"])