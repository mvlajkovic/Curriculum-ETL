
from pyodbc import Cursor
from pyodbc import Row

def insert_lams_activities(cursor: Cursor, les_id: int, activities: list):
    for activity in activities:
        if not activity:
            continue

        cursor.execute("""
            INSERT INTO lams_activities (
                les_id,
                activity_title,
                tool_content_id,
                parent,
                activity_category_id,
                tool_display_name,
                tool_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            les_id,
            activity.get("ActivityTitle"),
            activity.get("ToolContentId"),
            activity.get("Parent"),
            activity.get("ActivityCategoryId"),
            activity.get("ToolDisplayName"),
            activity.get("ToolId")
        )

def get_activities(cursor: Cursor, review_id: int) -> list[Row] | None:
    if (not isinstance(review_id, int)) or (review_id < 1):
        return None

    cursor.execute("""
        SELECT
            id,
            les_id,
            activity_title,
            tool_content_id,
            parent,
            activity_category_id,
            tool_display_name,
            tool_id
        FROM lams_activities
        WHERE les_id = ?
    """, review_id)

    return cursor.fetchall()
