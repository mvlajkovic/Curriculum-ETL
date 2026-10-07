
from pyodbc import Cursor

def insert_google_videos_lvl3(
        cursor: Cursor,
        les_id: int,
        durations: list[str]
):
    for duration in durations:
        if not duration or duration == "":
            continue

        cursor.execute("""
            INSERT INTO google_videos_lvl3 (les_id, duration)
            VALUES (?, ?)
        """, les_id, duration)
