from pyodbc import Cursor
from pyodbc import Row

def insert_lesson_version (cursor: Cursor, les_id: int, file_id: str) -> int:
    cursor.execute("""
        INSERT INTO lesson_version (les_id, fileId)
        OUTPUT INSERTED.id
        VALUES (?, ?)
    """, les_id, file_id)

    return cursor.fetchone()[0]

def get_lesson_version(cursor: Cursor, lesson_id: int) -> Row | None:
    if (not isinstance(lesson_id, int)) or (lesson_id < 1):
        return None

    cursor.execute("""
        SELECT id, les_id, fileId
        FROM lesson_version
        WHERE les_id = ?
    """, lesson_id)

    return cursor.fetchone()

def file_id_exists(cursor: Cursor, file_id: str) -> bool:
    cursor.execute("""
        SELECT id
        FROM lesson_version
        WHERE fileId = ?
    """, file_id)

    if cursor.fetchone() is None:
        return False
    else:
        return True

