from pyodbc import Cursor
from pyodbc import Row

def insert_lesson_other_stats(
        cursor: Cursor,
        lesson_id: int,
        stats_json: dict
) -> int:
    cursor.execute("""
        INSERT INTO lesson_other_stats (
            les_id,
            word_count_total,
            word_count_lv1,
            word_count_lv2,
            word_count_lv3,
            word_count_lv0,
            word_count_total_per_class,
            word_count_lv1_per_class,
            word_count_lv2_per_class,
            word_count_lv3_per_class,
            word_count_lv0_per_class,
            word_count_total_per_class_percentage,
            snippet_words,
            latex_words,
            last_call,
            figure_count,
            yt_video_count,
            google_video_count,
            google_video_count_lvl1,
            google_video_count_lvl2,
            google_video_count_lvl3,
            google_video_count_lvl0,
            google_uvod_video_count,
            audio_count,
            object_count,
            subobject_count,
            section_count,
            average_google_time,
            average_google_uvod_time,
            total_time_of_google_videos,
            total_time_of_google_videos_uvod,
            total_time_of_google_videos_lvl1,
            total_time_of_google_videos_lvl2,
            total_time_of_google_videos_lvl3,
            total_time_of_google_videos_lvl0
        )
        OUTPUT INSERTED.id
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, 
        lesson_id,
        stats_json.get("WordCountTotal"),
        stats_json.get("WordCountLv1"),
        stats_json.get("WordCountLv2"),
        stats_json.get("WordCountLv3"),
        stats_json.get("WordCountLv0"),
        stats_json.get("WordCountTotalPerClass"),
        stats_json.get("WordCountLv1PerClass"),
        stats_json.get("WordCountLv2PerClass"),
        stats_json.get("WordCountLv3PerClass"),
        stats_json.get("WordCountLv0PerClass"),
        stats_json.get("WordCountTotalPerClassPercentage"),
        stats_json.get("SnippetWords"),
        stats_json.get("LatexWords"),
        stats_json.get("lastCall"),
        stats_json.get("FigureCount"),
        stats_json.get("YTVideoCount"),
        stats_json.get("GoogleVideoCount"),
        stats_json.get("GoogleVideoCountLvl1"),
        stats_json.get("GoogleVideoCountLvl2"),
        stats_json.get("GoogleVideoCountLvl3"),
        stats_json.get("GoogleVideoCountLvl0"),
        stats_json.get("GoogleUVODVideoCount"),
        stats_json.get("AudioCount"),
        stats_json.get("ObjectCount"),
        stats_json.get("SubobjectCount"),
        stats_json.get("SectionCount"),
        stats_json.get("AverageGoogleTime"),
        stats_json.get("AverageGoogleUVODTime"),
        stats_json.get("totalTimeOfGoogleVideos"),
        stats_json.get("totalTimeOfGoogleVideosUVOD"),
        stats_json.get("totalTimeOfGoogleVideosLvl1"),
        stats_json.get("totalTimeOfGoogleVideosLvl2"),
        stats_json.get("totalTimeOfGoogleVideosLvl3"),
        stats_json.get("totalTimeOfGoogleVideosLvl0")
    )

    return cursor.fetchone()[0]

def get_other_stats(cursor: Cursor, review_id: int) -> Row | None:
    if (not isinstance(review_id, int)) or (review_id < 1):
        return None

    cursor.execute("""
        SELECT
            id,
            les_id,
            word_count_total,
            word_count_lv1,
            word_count_lv2,
            word_count_lv3,
            word_count_lv0,
            word_count_total_per_class,
            word_count_lv1_per_class,
            word_count_lv2_per_class,
            word_count_lv3_per_class,
            word_count_lv0_per_class,
            word_count_total_per_class_percentage,
            snippet_words,
            latex_words,
            last_call,
            figure_count,
            yt_video_count,
            google_video_count,
            google_video_count_lvl1,
            google_video_count_lvl2,
            google_video_count_lvl3,
            google_video_count_lvl0,
            google_uvod_video_count,
            audio_count,
            object_count,
            subobject_count,
            section_count,
            average_google_time,
            average_google_uvod_time,
            total_time_of_google_videos,
            total_time_of_google_videos_uvod,
            total_time_of_google_videos_lvl1,
            total_time_of_google_videos_lvl2,
            total_time_of_google_videos_lvl3,
            total_time_of_google_videos_lvl0
        FROM lesson_other_stats
        WHERE les_id = ?
    """, review_id)

    return cursor.fetchone()

