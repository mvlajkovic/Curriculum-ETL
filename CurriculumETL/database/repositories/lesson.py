from pyodbc import Cursor
from pyodbc import Row

def insert_lesson(
        cursor: Cursor,
        course_code: str,
        title: str,
        academic_year: str,
        lesson_number: str,
        lesson_author: str,
        naucno_polje: str
) -> int:
    cursor.execute("""
        INSERT INTO lesson (course_code, title, academic_year, lesson_number, lesson_author, naucno_polje)
        OUTPUT INSERTED.id
        VALUES (?, ?, ?, ?, ?, ?)
    """, course_code, title, academic_year, lesson_number, lesson_author, naucno_polje)

    return cursor.fetchone()[0]

def search_lessons(
        cursor: Cursor,
        course_code: str = "",
        title: str = "",
        lesson_number: str = "",
        academic_year: str = "",
        author: str = "",
        file_id: str = ""
) -> list[Row]:
    if (not isinstance(course_code, str)) or (course_code is None):
        course_code = ""
    if (not isinstance(title, str)) or (title is None):
        title = ""
    if (not isinstance(lesson_number, str)) or (lesson_number is None):
        lesson_number = ""
    if (not isinstance(academic_year, str)) or (academic_year is None):
        academic_year = ""
    if (not isinstance(author, str)) or (author is None):
        author = ""
    if (not isinstance(file_id, str)) or (file_id is None):
        file_id = ""

    cursor.execute("""
        SELECT TOP (5000)
            lesson.id,
            lesson.course_code,
            lesson.title,
            lesson.academic_year,
            lesson.lesson_number,
            lesson_version.fileId
        FROM lesson
        LEFT JOIN lesson_version
        ON lesson.id = lesson_version.les_id
        WHERE
            course_code LIKE ? AND
            title LIKE ? AND
            lesson_number LIKE ? AND
            academic_year LIKE ? AND
            lesson_author LIKE ? AND
            fileId LIKE ?
        ORDER BY course_code ASC, lesson_number ASC
    """,
        f"%{course_code}%",
        f"%{title}%",
        f"%{lesson_number}%",
        f"%{academic_year}%",
        f"%{author}%",
        f"%{file_id}%"
    )

    return cursor.fetchall()

def get_lesson_by_id(cursor: Cursor, id: int) -> Row | None:
    if (not isinstance(id, int)) or (id < 1):
        return None

    cursor.execute("""
        SELECT
            id,
            course_code,
            title,
            academic_year,
            lesson_number,
            pdf_generated,
            lesson_author,
            naucno_polje
        FROM lesson
        WHERE id = ?
    """, id)

    return cursor.fetchone()

