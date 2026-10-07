from pyodbc import Cursor
from pyodbc import Row

def insert_learning_object_subobjects(
        cursor: Cursor,
        lea_id: int,
        subobjects: list
):
    for subobject in subobjects:
        if not subobject:
            continue

        cursor.execute("""
            INSERT INTO learning_object_subobjects (
                lea_id,
                number,
                learning_content_id,
                title,
                classification,
                difficulty_level,
                keywords,
                learning_duration,
                type,
                subobject_author,
                school_year,
                audience,
                curriculum,
                domain,
                learning_outcomes,
                competences,
                knowledge_topic,
                faculty
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            lea_id,
            subobject.get("Number"),
            subobject.get("LearningContentId"),
            subobject.get("Title"),
            subobject.get("Classification"),
            subobject.get("DifficultyLevel"),
            subobject.get("Keywords"),
            subobject.get("LearningDuration"),
            subobject.get("Type"),
            subobject.get("Author"),
            subobject.get("SchoolYear"),
            subobject.get("Audience"),
            subobject.get("Curriculum"),
            subobject.get("Domain"),
            subobject.get("LearningOutcomes"),
            subobject.get("Competences"),
            subobject.get("KnowledgeTopic"),
            subobject.get("Faculty")
        )

def get_subobjects(
        cursor: Cursor,
        learning_obj_id: int
) -> list[Row] | None:
    if (not isinstance(learning_obj_id, int)) or (learning_obj_id < 1):
        return None

    cursor.execute("""
        SELECT
            id,
            lea_id,
            number,
            learning_content_id,
            title,
            classification,
            difficulty_level,
            keywords,
            learning_duration,
            type,
            subobject_author,
            school_year,
            audience,
            curriculum,
            domain,
            learning_outcomes,
            competences,
            knowledge_topic,
            faculty
        FROM learning_object_subobjects
        WHERE lea_id = ?
        ORDER BY id ASC
    """, learning_obj_id)

    return cursor.fetchall()
