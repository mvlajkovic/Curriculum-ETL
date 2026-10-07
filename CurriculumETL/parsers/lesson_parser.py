
class LessonParser:

    @staticmethod
    def parse(json_data):
        if "data" not in json_data or not json_data["data"]:
            raise ValueError("Invalid JSON format")

        lesson = json_data["data"][0]

        return {
            "course_code": lesson.get("CourseCode"),
            "lesson_code": lesson.get("Lesson"),
            "title": lesson.get("Title"),
            "school_year": lesson.get("Year"),
            "overview": lesson.get("Overview", ""),
            "summary": lesson.get("Summary", ""),
            "learning_objects": lesson.get("LearningObjects", [])
        }