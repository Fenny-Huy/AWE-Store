# from models.database import DatabaseManager
from database import DatabaseManager

class User():
    def __init__(self,customer_id):
        self.db = DatabaseManager()
        self.user_data = self.db.get_table("customerssss").get_row_by_column_value("customer_id",str(customer_id))

    def __getitem__(self, key):
        if self.user_data and key in self.user_data:
            return self.user_data[key]
        raise KeyError(f"{key} not found in user data.")