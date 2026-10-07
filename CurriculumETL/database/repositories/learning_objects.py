from pyodbc import Cursor
from pyodbc import Row

from database.repositories.learning_object_subobjects import insert_learning_object_subobjects

def insert_learning_objects(
        cursor: Cursor,
        les_id: int,
        learning_objects: list[dict]
):
    for object in learning_objects:
        if not object:
            continue

        cursor.execute("""
            INSERT INTO learning_objects (
                les_id,
                number,
                learning_content_id,
                title,
                classification,
                difficulty_level,
                keywords,
                audience,
                learning_duration,
                type,
                curriculum,
                domain,
                learning_outcomes,
                competences,
                knowledge_topic,
                learning_object_author,
                school_year,
                faculty
            )
            OUTPUT INSERTED.id
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            les_id,
            object.get("Number"),
            object.get("LearningContentId"),
            object.get("Title"),
            object.get("Classification"),
            object.get("DifficultyLevel"),
            object.get("Keywords"),
            object.get("Audience"),
            object.get("LearningDuration"),
            object.get("Type"),
            object.get("Curriculum"),
            object.get("Domain"),
            object.get("LearningOutcomes"),
            object.get("Competences"),
            object.get("KnowledgeTopic"),
            object.get("Author"),
            object.get("SchoolYear"),
            object.get("Faculty")
        )

        object_id: int = cursor.fetchone()[0]
        subobjects = object.get("Subobjects", [])

        if subobjects:
            insert_learning_object_subobjects(
                cursor,
                object_id,
                subobjects
            )

def get_learning_objects(cursor: Cursor, review_id: int) -> list[Row] | None:
    if (not isinstance(review_id, int)) or (review_id < 1):
        return None

    cursor.execute("""
        SELECT
            id,
            les_id,
            number,
            learning_content_id,
            title,
            classification,
            difficulty_level,
            keywords,
            audience,
            learning_duration,
            type,
            curriculum,
            domain,
            learning_outcomes,
            competences,
            knowledge_topic,
            learning_object_author,
            school_year,
            faculty
        FROM learning_objects
        WHERE les_id = ?
        ORDER BY id ASC
    """, review_id)

    return cursor.fetchall()

