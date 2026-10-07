
from pyodbc import Cursor
from pyodbc import Row

def insert_forums(cursor: Cursor, les_id: int, forums: list):
    for forum in forums:
        if not forum:
            continue

        cursor.execute("""
            INSERT INTO forums (les_id, after_summary, tema, opis_teme)
            VALUES (?, ?, ?, ?)
        """,
            les_id,
            forum.get("AfterSummary"),
            forum.get("Tema"),
            forum.get("OpisTeme")
        )

def get_forums(cursor: Cursor, review_id: int) -> list[Row] | None:
    if (not isinstance(review_id, int)) or (review_id < 1):
        return None

    cursor.execute("""
        SELECT id, les_id, after_summary, tema, opis_teme
        FROM forums
        WHERE les_id = ?
    """, review_id)

    return cursor.fetchall()
