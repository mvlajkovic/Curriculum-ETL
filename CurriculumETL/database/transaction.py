from pyodbc import Connection
from pyodbc import Cursor

class TransactionManager:
    def __init__(self, connection: Connection):
        self.conn: Connection = connection

    def __enter__(self) -> Cursor:
        self.conn.autocommit = False
        return self.conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print("Rolling back transaction...")
            self.conn.rollback()
        else:
            self.conn.commit()
