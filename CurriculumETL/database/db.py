import pyodbc
from pyodbc import Connection

from config.settings import get_db_connection_string

def get_connection() -> Connection | None:
    try:
        return pyodbc.connect(get_db_connection_string())
    except Exception as e:
        print(f"ERROR: Couldn't connect to the database.")
        print(f"ERROR: {e}")

        return None

# Helper function for cleaning up variables fetched from the database.
def sanitize(var, add_quotes: bool = False, if_none = "N/A"):
    if var is None or var == "":
        return if_none
    elif add_quotes:
        return f"\"{str(var)}\""
    else:
        return var
