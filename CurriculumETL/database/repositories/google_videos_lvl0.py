
from pyodbc import Cursor

def insert_google_videos_lvl0(
        cursor: Cursor,
        les_id: int,
        durations: list[str]
):
    for duration in durations:
        if not duration or duration == "":
            continue

        cursor.execute("""
            INSERT INTO google_videos_lvl0 (les_id, Integer)
            VALUES (?, ?)
        """, les_id, duration)
