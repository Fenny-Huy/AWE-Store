# backend/models/admin.py

from .account import Account
from .database import DatabaseManager


class Admin(Account):
    """
    Concrete Admin class. Inherits from Account.
    Stores its own password (from admins.csv) and provides a check_password method.
    """

    def __init__(self, account_id: str, password: str):
        # Load basic info (account_id, email, name) from accounts.csv via Account
        super().__init__(account_id)
        # Override or set the password from admins.csv
        self.password = password

    def get_role(self) -> str:
        return "admin"

    def check_password(self, raw_password: str) -> bool:
        """
        Return True if raw_password matches the stored password.
        """
        return raw_password == self.password
