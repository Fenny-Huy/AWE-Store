# backend/models/account.py

from database import Database

class Account:
    """
    Base class for any account. 
    On init, it loads *all* account rows into self.account_data,
    then finds the row matching self.account_id.
    """

    def __init__(self, account_id):
        self.account_id = str(account_id)
        self.db = Database()
        self.account_data = self.db.get_table("accounts")  # list of dicts

        # Find *this* account's row
        self.my_record = None
        for row in self.account_data:
            if row["account_id"] == self.account_id:
                self.my_record = row
                break

        if not self.my_record:
            raise ValueError(f"Account ID '{self.account_id}' not found in accounts table")

        # Expose some attributes
        self.email = self.my_record["email"]
        self.name = self.my_record["name"]
