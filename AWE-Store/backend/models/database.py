import os
from threading import Lock
import csv

class SingletonMeta(type):
    """
    A thread-safe implementation of Singleton.
    """
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:  # Ensure thread-safe instantiation
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Table:
    def __init__(self, name: str, columns: list, path: str = "data"):
        self.name = name
        self.columns = columns
        self.rows = []
        self.file_path = os.path.join(path, f"{self.name}.csv")

        os.makedirs(path, exist_ok=True)
        self.load()

    def add_row(self, row: dict):
        if not set(row.keys()).issubset(set(self.columns)):
            raise ValueError("Row has invalid columns")
        self.rows.append(row)
        self.save()

    def delete_row(self, index: int):
        if 0 <= index < len(self.rows):
            del self.rows[index]
            self.save()

    def update_row(self, index: int, new_row: dict):
        if 0 <= index < len(self.rows):
            if not set(new_row.keys()).issubset(set(self.columns)):
                raise ValueError("New row has invalid columns")
            self.rows[index] = new_row
            self.save()

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
                self.rows[idx] = new_row
                self.save()
                return
        raise ValueError(f"No row found where {column} == {match_value}")

    def get_row_by_column_value(self, column: str, value: str) -> dict:
        """
        Retrieve the first row where column == value.
        Returns the row as a dict or None if not found.
        """
        for row in self.rows:
            if row.get(column) == value:
                return row
        return None

    def save(self):
        with open(self.file_path, "w", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.columns)
            writer.writeheader()
            writer.writerows(self.rows)

    def load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                reader = csv.DictReader(f)
                self.rows = list(reader)



class DatabaseManager(metaclass=SingletonMeta):
    def __init__(self, db_path: str = "data"):
        self.tables = {}
        self.csv_path = db_path
        os.makedirs(self.csv_path, exist_ok=True)

    def create_table(self, name: str, columns: list):
        if name not in self.tables:
            table = Table(name, columns, path=self.csv_path)
            self.tables[name] = table
        return self.tables[name]

    def get_table(self, name: str):
        if name in self.tables:
            return self.tables[name]

        csv_file = os.path.join(self.csv_path, f"{name}.csv")
        if os.path.exists(csv_file):
            with open(csv_file, "r") as f:
                header = f.readline().strip().split(",")
            table = Table(name, header, path=self.csv_path)
            self.tables[name] = table
            return table

        return None

    def list_tables(self):
        csv_files = [f for f in os.listdir(self.csv_path) if f.endswith(".csv")]
        table_names = [os.path.splitext(f)[0] for f in csv_files]

        for name in table_names:
            if name not in self.tables:
                self.get_table(name)

        return list(self.tables.values())


def sample_data(db):
    customers_table = db.create_table("customerssss", ["customer_id", "name", "email"])

    customers_table.add_row({"customer_id": "1", "name": "Fin", "email": "fin@swin.edu.au"})
    customers_table.add_row({"customer_id": "2", "name": "Huy", "email": "huy@swin.edu.au"})
    customers_table.add_row({"customer_id": "3", "name": "Khai", "email": "khai@swin.edu.au"})
    customers_table.add_row({"customer_id": "4", "name": "Toan", "email": "toan@swin.edu.au"})
    customers_table.add_row({"customer_id": "5", "name": "Random", "email": "random@swin.edu.au"})

    print("Before update:")
    print(customers_table.rows)

    # Update by finding the row where customer_id == "5"
    customers_table.update_row_by_column_value("customer_id", "5", {
        "customer_id": "5",
        "name": "New Name Updated",
        "email": "new_name@example.com"
    })

    print("After full row update:")
    print(customers_table.rows)

    print("Tables in database:")
    for table in db.list_tables():
        print(f"- {table.name}")

def update_sample(table):
    # Update only the email of customer_id '5'
    table.update_column_value_by_index(4, "email", "updated_random@swin.edu.au")

    print("After column update by index:")
    print(table.rows)


if __name__ == "__main__":
    db = DatabaseManager(db_path= os.path.join("backend", "data"))
    # sample_data(db)
    
    # print(db.get_table('products'))
    tables = db.list_tables()
    for table in tables:
        print(f"Table: {table.name}, Rows: {len(table.rows)}")
    # update_sample(db.get_table('customerssss'))
