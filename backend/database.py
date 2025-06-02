# backend/database.py

import csv
import os

class Database:
    """
    A simple CSV-backed "database" that returns rows of data for each table.
    Usage: db = Database(); rows = db.get_table("accounts")
    """

    def __init__(self, data_dir="data"):
        # data_dir is where your .csv files live
        self.data_dir = data_dir

    def get_table(self, table_name):
        """
        Looks for a file named "<table_name>.csv" under data_dir.
        Returns a list of dicts (one per row). If file not found, returns [].
        """
        path = os.path.join(self.data_dir, f"{table_name}.csv")
        rows = []
        if not os.path.exists(path):
            return rows

        with open(path, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
        return rows
