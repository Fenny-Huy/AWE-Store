# backend/models/admin.py

from .account import Account
from .sales_analytics import SalesAnalytics

class Admin(Account):
    """
    Concrete Admin class. Inherits from Account.
    Provides a method to view sales analytics.
    """

    def __init__(self, admin_id: str):
        super().__init__(admin_id)
        # You might validate that this ID truly is an admin in a real system.

    def get_role(self) -> str:
        return "admin"

    def view_sales(self) -> dict:
        """
        Return whatever SalesAnalytics.generate_summary() produces.
        """
        analytics = SalesAnalytics()
        return analytics.generate_summary()
