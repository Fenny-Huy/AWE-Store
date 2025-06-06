# backend/models/customer.py

from models.account import Account
from models.database import DatabaseManager
from models.shopping_cart import ShoppingCart
from models.order import Order

class Customer(Account):
    
    #Customer inherits Account. 
    #On init, it validates its own row in 'customers.csv' and then creates a ShoppingCart object for this customer_id.
    
    

    def __init__(self, customer_id: str):
        # First, load the Account portion (email, name, etc.)
        super().__init__(customer_id)

        self.customer_id = str(customer_id)
        dbm = DatabaseManager()
        table = dbm.get_table("customers")
        if table is None:
            raise ValueError("Table 'customers' does not exist")

    

        # Initialize this customer's cart
        self.shopping_cart = ShoppingCart(self.customer_id)
        print(f"Initialized shopping cart for customer {self.customer_id} with items: {self.shopping_cart.get_cart_items()}")
        

    def get_cart(self):
        self.shopping_cart.reload_cart()
        return self.shopping_cart
        

    def get_role(self) -> str:
        return "customer"


    def place_order(self, order_id: str, total_cost: float, payment_method: str = "credit"):
        
        #Create and process an order with payment
        #Returns the order status and invoice information
        
        # Get current cart items
        cart = self.shopping_cart
        
        # Create new order
        order = Order(
            order_id=order_id,
            customer=self,
            items=cart,
            total_cost=total_cost
        )
        print(f"Cart items when place order: {cart.get_cart_items()}")
        
        # Process payment
        payment_success = order.make_payment(payment_method)
        
        if payment_success:
            print("Payment successful")
            # Generate invoice
            # invoice = order.invoice
            # Clear the cart after successful payment
            cart.clear_cart()
            return {
                "success": True,
                "invoice": order.invoice_info,
                "message": "Payment successful"
            }
        
        return {
            "success": False,
            "message": "Payment failed"
        }



    def get_customer_id(self) -> str:
        return self.customer_id
    

    

