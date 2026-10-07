
from pyodbc import Cursor

def insert_individualne_vezbe_trajanje(
        cursor: Cursor,
        les_id: int,
        durations: list[str]
):
    for duration in durations:
        if not duration:
            continue

        cursor.execute("""
            INSERT INTO individualne_vezbe_trajanje (les_id, trajanje)
            VALUES (?, ?)
        """, les_id, duration)
