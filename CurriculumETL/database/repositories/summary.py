from pyodbc import Cursor
from pyodbc import Row

def insert_summary(
        cursor: Cursor,
        les_id: int,
        summary_id: str,
        summary_title: str
):
    cursor.execute("""
        INSERT INTO summary (les_id, summary_id, summary_title)
        VALUES (?, ?, ?)
    """, les_id, summary_id, summary_title)

def get_summary(cursor: Cursor, review_id: int) -> Row | None:
    if (not isinstance(review_id, int)) or (review_id < 1):
        return None

    cursor.execute("""
        SELECT id, les_id, summary_id, summary_title
        FROM summary
        WHERE les_id = ?
    """, review_id)

    return cursor.fetchone()

