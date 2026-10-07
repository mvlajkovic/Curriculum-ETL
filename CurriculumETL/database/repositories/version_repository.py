from database.db import get_connection

def insert_lesson_version (lesson_id, title, school_year):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO lesson_version (les_id, title, school_year)
        VALUES (?, ?, ?)
    """, lesson_id, title, school_year)
    #return cursor.fetchone()[0]
    conn.commit()
    conn.close()
    conn.close()