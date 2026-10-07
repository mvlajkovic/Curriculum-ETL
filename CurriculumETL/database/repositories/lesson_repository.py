from database.db import get_connection

def insert_lesson(cursor, course_code, lesson_code):
    cursor.execute("""
        INSERT INTO lesson (course_code, lesson_code)
        OUTPUT INSERTED.id
        VALUES (?, ?)
    """, course_code, lesson_code)
    return cursor.fetchone()[0]

def get_lesson_id_by_code(code):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM lesson
        WHERE code = ?
    """, code)

    row = cursor.fetchone()

    conn.close()

    return row[0] if row else None