# backend/models/account.py

from models.database import DatabaseManager
import abc

class Account(abc.ABC):
    """
    Base class for any account. 
    On init, it retrieves its own record from the 'accounts' table.
    """

    def __init__(self, account_id: str):
        self.account_id = str(account_id)
        dbm = DatabaseManager()
        self.table = dbm.get_table("accounts")
        if self.table is None:
            raise ValueError("Table 'accounts' does not exist")

        self.my_record = self.table.get_row_by_column_value("account_id", self.account_id)
        if self.my_record is None:
            raise ValueError(f"Account ID '{self.account_id}' not found in accounts table")

        # Expose attributes
        self.email = self.my_record.get("email")
        self.name = self.my_record.get("name")
    
    @abc.abstractmethod
    def get_role(self) -> str:
        """
        Every concrete account subclass must implement this,
        returning something like "customer" or "admin".
        """
        pass
