
NOTE = """
    - Cart.csv: I don't think cart should have quantity, 
    quantity should belongs to order

    - Customer.py: 
        - Customer __init__ create cart object for one time,
        no need to recreate when get_cart()
        - Or ShoppingCart() will created in order

    - shopping_cart.py:
        - Add remove_cart()

    - Should create DatabaseManager():
        - To manipulate data in csv (Can add/remove)
        - just called DatabaseManager object if want to do something 
        - Should be in Singleton -> cannot have data duplication

    - product.py
        - Load information about product should be in Product() object 
        (Product object can use DatabaseManager())

    - product_catalogue.py
        - When user add product to shopping cart, should add the Product object
        - 

    - customer.py: Should have CustomerManager class to manage Customer object


    ** IMPORTANT **
    The system will:
        1. Create an order from the cart items
        2. Generate an invoice
        3. Process the payment
        4. Save all order data
        5. Clear the cart if successful
        6. The data is persisted in JSON files:
            - Invoices: backend/data/invoices/INV-{order_id}.json
            - Orders: backend/data/orders/{order_id}.json
"""