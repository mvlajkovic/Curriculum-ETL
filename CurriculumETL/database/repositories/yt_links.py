from pyodbc import Cursor
from pyodbc import Row

def insert_yt_links(cursor: Cursor, les_id: int, links: list[str]):
    for link in links:
        if not link or link == "":
            continue

        cursor.execute("""
            INSERT INTO yt_links (les_id, url)
            VALUES (?, ?)
        """, les_id, link)

def get_links(cursor: Cursor, other_stats_id: int) -> list[Row] | None:
    if (not isinstance(other_stats_id, int)) or (other_stats_id < 1):
        return None

    cursor.execute("""
        SELECT id, les_id, url
        FROM yt_links
        WHERE les_id = ?
    """, other_stats_id)

    return cursor.fetchall()

