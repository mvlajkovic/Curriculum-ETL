
from pyodbc import Cursor

def insert_yt_videos(cursor: Cursor, les_id: int, durations: list[str]):
    for duration in durations:
        if not duration or duration == "":
            continue

        cursor.execute("""
            INSERT INTO yt_videos (les_id, duration)
            VALUES (?, ?)
        """, les_id, duration)
