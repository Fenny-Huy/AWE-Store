# backend/database.py

import os
import csv
from threading import Lock

class SingletonMeta(type):
    """
    A thread-safe implementation of Singleton.
    """
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Table:
    """
    Represents a CSV-backed table.
    """

    def __init__(self, name: str, columns: list, path: str):
        self.name = name
        self.columns = columns[:]   # copy
        self.rows = []
        self.file_path = os.path.join(path, f"{self.name}.csv")

        os.makedirs(path, exist_ok=True)
        self.load()

    def add_row(self, row: dict):
        if not set(row.keys()).issubset(set(self.columns)):
            raise ValueError(f"Row has invalid columns: {row.keys()} not subset of {self.columns}")
        self.rows.append(row.copy())
        self.save()

    def delete_row(self, index: int):
        if 0 <= index < len(self.rows):
            del self.rows[index]
            self.save()
        else:
            raise IndexError(f"Row index {index} out of range")

    def update_row(self, index: int, new_row: dict):
        if 0 <= index < len(self.rows):
            if not set(new_row.keys()).issubset(set(self.columns)):
                raise ValueError("New row has invalid columns")
            self.rows[index] = new_row.copy()
            self.save()
        else:
            raise IndexError(f"Row index {index} out of range")

    def update_column_value_by_index(self, index: int, column: str, value):
        if 0 <= index < len(self.rows):
            if column not in self.columns:
                raise ValueError(f"Column '{column}' does not exist")
            self.rows[index][column] = value
            self.save()
        else:
            raise IndexError(f"Row index {index} out of range")

    def update_row_by_column_value(self, column: str, match_value, new_row: dict):
        if column not in self.columns:
            raise ValueError(f"Column '{column}' does not exist")

        for idx, row in enumerate(self.rows):
            if row.get(column) == match_value:
                if not set(new_row.keys()).issubset(set(self.columns)):
                    raise ValueError("New row has invalid columns")
                self.rows[idx] = new_row.copy()
                self.save()
                return
        raise ValueError(f"No row found where {column} == {match_value}")

    def get_row_by_column_value(self, column: str, value: str) -> dict:
        if column not in self.columns:
            raise ValueError(f"Column '{column}' does not exist")
        for row in self.rows:
            if row.get(column) == value:
                return row.copy()
        return None

    def save(self):
        with open(self.file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.columns)
            writer.writeheader()
            writer.writerows(self.rows)

    def load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                self.rows = [row for row in reader]
        else:
            # Create an empty CSV with header row
            with open(self.file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=self.columns)
                writer.writeheader()


class DatabaseManager(metaclass=SingletonMeta):
    """
    Manages multiple Table instances. Ensures only one Table per CSV.
    """

    def __init__(self, db_path: str = "data"):
        # Always compute data directory relative to this file's location
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.csv_path = os.path.join(base_dir, db_path)
        os.makedirs(self.csv_path, exist_ok=True)

        self.tables = {}  # name -> Table instance

    def create_table(self, name: str, columns: list) -> Table:
        if name in self.tables:
            return self.tables[name]
        table = Table(name, columns, path=self.csv_path)
        self.tables[name] = table
        return table

    def get_table(self, name: str) -> Table:
        if name in self.tables:
            return self.tables[name]

        csv_file = os.path.join(self.csv_path, f"{name}.csv")
        if os.path.exists(csv_file):
            # Read header to infer columns
            with open(csv_file, "r", newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                header = next(reader)
            table = Table(name, header, path=self.csv_path)
            self.tables[name] = table
            return table
        return None

    def list_tables(self) -> list:
        csv_files = [f for f in os.listdir(self.csv_path) if f.endswith(".csv")]
        for fname in csv_files:
            tablename = os.path.splitext(fname)[0]
            if tablename not in self.tables:
                self.get_table(tablename)
        return list(self.tables.values())
