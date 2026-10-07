from pyodbc import Cursor
from pyodbc import Row

def insert_overview(
        cursor: Cursor,
        les_id: int,
        overview_id: str,
        overview_title: str
):
    cursor.execute("""
        INSERT INTO overview (les_id, overview_id, overview_title)
        VALUES (?, ?, ?)
    """, les_id, overview_id, overview_title)

def get_overview(cursor: Cursor, review_id: int) -> Row | None:
    if (not isinstance(review_id, int)) or (review_id < 1):
        return None

    cursor.execute("""
        SELECT id, les_id, overview_id, overview_title
        FROM overview
        WHERE les_id = ?
    """, review_id)

    return cursor.fetchone()

