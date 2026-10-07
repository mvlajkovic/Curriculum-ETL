from pyodbc import Cursor
from pyodbc import Row

def insert_lesson_review(
        cursor: Cursor,
        lesson_version_id: int,
        json_file_name: str,
        drive_file_id: str
) -> int:
    cursor.execute("""
        INSERT INTO lesson_review (lesson_version_id, json_file_name, drive_file_id)
        OUTPUT INSERTED.id
        VALUES (?, ?, ?)
    """, lesson_version_id, json_file_name, drive_file_id)

    return cursor.fetchone()[0]

def get_lesson_review(cursor: Cursor, version_id: int) -> Row | None:
    if (not isinstance(version_id, int)) or (version_id < 1):
        return None

    cursor.execute("""
        SELECT id, lesson_version_id, json_file_name, drive_file_id, imported_at
        FROM lesson_review
        WHERE lesson_version_id = ?
    """, version_id)

    return cursor.fetchone()

