from models.payment import Payment


class ManageOrder():
    def __init__(self, customer_id, shopping_cart):
        self.customer_id = customer_id
        self.shopping_cart = shopping_cart
        pass

    def _select_order(self):
        selected_product = []
        for item in self.shopping_cart:
            is_selected = input("Order this product?")
            if is_selected.lower() == "yes":
                print(f"Add {item} to order list")
                selected_product.append(item)
                # remove from shopping cart object
            else:
                print(f"Excluded {item}")
        return selected_product

        # selected_product = []
        # for item in self.get_cart():
        #     is_selected = input("Order this product?")
        #     if is_selected.lower() == "yes":
        #         print(f"Add {item} to order list")
        #         self.order_list[item] = 
        #     else:
        #         print(f"Excluded {item}")
        
        # return selected_product
        pass

    def get_order(self):
        pass

    def payment(self):
        payment = Payment()
        if payment.isTrue:
            #Call Receipt, Shipment
            pass    

    def create_invoice(self):
        pass