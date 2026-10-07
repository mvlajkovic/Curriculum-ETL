
from pyodbc import Cursor
from tkinter import ttk

from database.db import sanitize

from database.repositories.learning_object_subobjects import get_subobjects
from database.repositories.learning_objects import get_learning_objects
from database.repositories.lesson_other_stats import get_other_stats
from database.repositories.lesson_version import get_lesson_version
from database.repositories.lesson_review import get_lesson_review
from database.repositories.lams_activities import get_activities
from database.repositories.lesson import get_lesson_by_id
from database.repositories.lesson_stats import get_stats
from database.repositories.overview import get_overview
from database.repositories.summary import get_summary
from database.repositories.yt_links import get_links
from database.repositories.forums import get_forums

# Load lesson info from the database and display it inside a Treeview.
def load_lesson_info(
        cursor: Cursor,
        lesson_id: int,
        tree: ttk.Treeview
):
    lesson_data = get_lesson_by_id(cursor, lesson_id)
    if not lesson_data:
        return

    tree.delete(*tree.get_children(lesson_id))

    tree.insert(
        lesson_id, "end",
        text=f"Author: {sanitize(lesson_data.lesson_author)}"
    )

    tree.insert(
        lesson_id, "end",
        text=f"Science field: {sanitize(lesson_data.naucno_polje)}"
    )

    tree.insert(
        lesson_id, "end",
        text=f"PDF generated: {sanitize(lesson_data.pdf_generated)}"
    )

    ### FILE INFO TAB ###
    version_data = get_lesson_version(cursor, lesson_id)
    if not version_data:
        return

    file_info_tab: str = tree.insert(lesson_id, "end", text="File Info")

    tree.insert(
        file_info_tab, "end",
        text=f"File ID: {sanitize(version_data.fileId, True)}"
    )

    review_data = get_lesson_review(cursor, version_data.id)
    if not review_data:
        return

    tree.insert(
        file_info_tab, "end",
        text=f"JSON file name: {sanitize(review_data.json_file_name, True)}"
    )

    tree.insert(
        file_info_tab, "end",
        text=f"Drive file ID: {sanitize(review_data.drive_file_id, True)}"
    )

    tree.insert(
        file_info_tab, "end",
        text=f"Imported at: {sanitize(review_data.imported_at)}"
    )

    ### OVERVIEW TAB ###
    overview_data = get_overview(cursor, review_data.id)

    if overview_data:
        overview_tab: str = tree.insert(lesson_id, "end", text="Overview")

        tree.insert(
            overview_tab, "end",
            text=f"ID: {sanitize(overview_data.overview_id)}"
        )

        tree.insert(
            overview_tab, "end",
            text=f"Title: {sanitize(overview_data.overview_title, True)}"
        )

    ### LEARNING OBJECTS TAB ###
    objects_data = get_learning_objects(cursor, review_data.id)

    if objects_data:
        objects_tab: str = tree.insert(lesson_id, "end", text="Learning Objects")

        for l_obj in objects_data:
            if not l_obj:
                continue

            type_str: str = sanitize(l_obj.type, if_none=None)
            if not type_str:
                type_str = ""
            else:
                type_str = f"({type_str})"

            l_obj_id: str = tree.insert(
                objects_tab, "end",
                text=f"{sanitize(l_obj.number)} - {sanitize(l_obj.title, True)} {type_str}"
            )

            tree.insert(
                l_obj_id, "end",
                text=f"Learning content ID: {sanitize(l_obj.learning_content_id)}"
            )

            tree.insert(
                l_obj_id, "end",
                text=f"Classification: {sanitize(l_obj.classification)}"
            )

            tree.insert(
                l_obj_id, "end",
                text=f"Difficulty level: {sanitize(l_obj.difficulty_level)}"
            )

            tree.insert(
                l_obj_id, "end",
                text=f"Keywords: {sanitize(l_obj.keywords, True)}"
            )

            tree.insert(
                l_obj_id, "end",
                text=f"Audience: {sanitize(l_obj.audience)}"
            )

            tree.insert(
                l_obj_id, "end",
                text=f"Learning duration: {sanitize(l_obj.learning_duration)}"
            )

            tree.insert(
                l_obj_id, "end",
                text=f"Curriculum: {sanitize(l_obj.curriculum)}"
            )

            tree.insert(
                l_obj_id, "end",
                text=f"Domain: {sanitize(l_obj.domain)}"
            )

            tree.insert(
                l_obj_id, "end",
                text=f"Learning outcomes: {sanitize(l_obj.learning_outcomes)}"
            )

            tree.insert(
                l_obj_id, "end",
                text=f"Competences: {sanitize(l_obj.competences)}"
            )

            tree.insert(
                l_obj_id, "end",
                text=f"Knowledge topic: {sanitize(l_obj.knowledge_topic)}"
            )

            tree.insert(
                l_obj_id, "end",
                text=f"Author: {sanitize(l_obj.learning_object_author)}"
            )

            tree.insert(
                l_obj_id, "end",
                text=f"School year: {sanitize(l_obj.school_year)}"
            )

            tree.insert(
                l_obj_id, "end",
                text=f"Faculty: {sanitize(l_obj.faculty)}"
            )

            ### LEARNING SUBOBJECTS TAB ###
            subobjects_data = get_subobjects(cursor, l_obj.id)
            if not subobjects_data:
                continue

            subobjects_tab: str = tree.insert(l_obj_id, "end", text="Subobjects")

            for sub in subobjects_data:
                if not sub:
                    continue

                type_str: str = sanitize(l_obj.type, if_none=None)
                if not type_str:
                    type_str = ""
                else:
                    type_str = f"({type_str})"

                sub_id: str = tree.insert(
                    subobjects_tab, "end",
                    text=f"{sanitize(sub.number)} - {sanitize(sub.title, True)} {type_str}"
                )

                tree.insert(
                    sub_id, "end",
                    text=f"Learning content ID: {sanitize(sub.learning_content_id)}"
                )

                tree.insert(
                    sub_id, "end",
                    text=f"Classification: {sanitize(sub.classification)}"
                )

                tree.insert(
                    sub_id, "end",
                    text=f"Difficulty level: {sanitize(sub.difficulty_level)}"
                )

                tree.insert(
                    sub_id, "end",
                    text=f"Keywords: {sanitize(sub.keywords, True)}"
                )

                tree.insert(
                    sub_id, "end",
                    text=f"Audience: {sanitize(sub.audience)}"
                )

                tree.insert(
                    sub_id, "end",
                    text=f"Learning duration: {sanitize(sub.learning_duration)}"
                )

                tree.insert(
                    sub_id, "end",
                    text=f"Curriculum: {sanitize(sub.curriculum)}"
                )

                tree.insert(
                    sub_id, "end",
                    text=f"Domain: {sanitize(sub.domain)}"
                )

                tree.insert(
                    sub_id, "end",
                    text=f"Learning outcomes: {sanitize(sub.learning_outcomes)}"
                )

                tree.insert(
                    sub_id, "end",
                    text=f"Competences: {sanitize(sub.competences)}"
                )

                tree.insert(
                    sub_id, "end",
                    text=f"Knowledge topic: {sanitize(sub.knowledge_topic)}"
                )

                tree.insert(
                    sub_id, "end",
                    text=f"Author: {sanitize(sub.subobject_author)}"
                )

                tree.insert(
                    sub_id, "end",
                    text=f"School year: {sanitize(sub.school_year)}"
                )

                tree.insert(
                    sub_id, "end",
                    text=f"Faculty: {sanitize(sub.faculty)}"
                )

    ### SUMMARY TAB ###
    summary_data = get_summary(cursor, review_data.id)

    if summary_data:
        summary_tab: str = tree.insert(lesson_id, "end", text="Summary")

        tree.insert(
            summary_tab, "end",
            text=f"ID: {sanitize(summary_data.summary_id)}"
        )

        tree.insert(
            summary_tab, "end",
            text=f"Title: {sanitize(summary_data.summary_title, True)}"
        )

    ### LAMS ACTIVITIES TAB ###
    activities_data = get_activities(cursor, review_data.id)

    if activities_data:
        activities_tab: str = tree.insert(lesson_id, "end", text="LAMS Activities")

        for activity in activities_data:
            if not activity:
                continue

            activity_id: str = tree.insert(
                activities_tab, "end",
                text=f"{sanitize(activity.activity_title, True)} ({sanitize(activity.tool_display_name)})"
            )

            tree.insert(
                activity_id, "end",
                text=f"Tool content ID: {sanitize(activity.tool_content_id)}"
            )

            tree.insert(
                activity_id, "end",
                text=f"Tool ID: {sanitize(activity.tool_id)}"
            )

            tree.insert(
                activity_id, "end",
                text=f"Parent: {sanitize(activity.parent)}"
            )

            tree.insert(
                activity_id, "end",
                text=f"Activity category ID: {sanitize(activity.activity_category_id)}"
            )

    ### FORUMS TAB ###
    forums_data = get_forums(cursor, review_data.id)

    if forums_data:
        forums_tab: str = tree.insert(lesson_id, "end", text="Forums")

        for forum in forums_data:
            if not forum:
                continue

            forum_id: str = tree.insert(
                forums_tab, "end",
                text=sanitize(forum.tema, True)
            )

            tree.insert(
                forum_id, "end",
                text=f"Description: {sanitize(forum.opis_teme, True)}"
            )

            tree.insert(
                forum_id, "end",
                text=f"After summary: {sanitize(forum.after_summary)}"
            )

    ### STATS TAB ###
    stats_data = get_stats(cursor, review_data.id)

    if stats_data:
        stats_tab: str = tree.insert(lesson_id, "end", text="Stats")

        tree.insert(
            stats_tab, "end",
            text=f"Total activity counter: {sanitize(stats_data.total_activity_counter)}"
        )

        tree.insert(
            stats_tab, "end",
            text=f"Forum counter: {sanitize(stats_data.forum_counter)}"
        )

        tree.insert(
            stats_tab, "end",
            text=f"Multiple choice counter: {sanitize(stats_data.multiple_choice_counter)}"
        )

        tree.insert(
            stats_tab, "end",
            text=f"Assessment counter: {sanitize(stats_data.assessment_counter)}"
        )

        tree.insert(
            stats_tab, "end",
            text=f"Q&A counter: {sanitize(stats_data.q_and_a_counter)}"
        )

        tree.insert(
            stats_tab, "end",
            text=f"Activity after summary counter: {sanitize(stats_data.activity_after_summary_counter)}"
        )

        tree.insert(
            stats_tab, "end",
            text=f"Forum after summary counter: {sanitize(stats_data.forum_after_summary_counter)}"
        )

        tree.insert(
            stats_tab, "end",
            text=f"Number of predavanja: {sanitize(stats_data.no_ou_predavanja)}"
        )

        tree.insert(
            stats_tab, "end",
            text=f"Number of pokazne vežbe: {sanitize(stats_data.no_ou_pokazne_vezbe)}"
        )

        tree.insert(
            stats_tab, "end",
            text=f"Number of individualne vežbe: {sanitize(stats_data.no_ou_individualne_vezbe)}"
        )

        tree.insert(
            stats_tab, "end",
            text=f"Number of zadatak za samostalni rad: {sanitize(stats_data.no_ou_zadatak_za_samostalni_rad)}"
        )

        tree.insert(
            stats_tab, "end",
            text=f"Number of domaći zadatak: {sanitize(stats_data.no_ou_domaci_zadatak)}"
        )

        tree.insert(
            stats_tab, "end",
            text=f"Number of projekat: {sanitize(stats_data.no_ou_projekat)}"
        )

        tree.insert(
            stats_tab, "end",
            text=f"Has pokazne vežbe: {sanitize(stats_data.has_pokazne_vezbe)}"
        )

        tree.insert(
            stats_tab, "end",
            text=f"Has individualne vežbe: {sanitize(stats_data.has_individualne_vezbe)}"
        )

        tree.insert(
            stats_tab, "end",
            text=f"Has zadatak za samostalni rad: {sanitize(stats_data.has_zadatak_za_samostalni_rad)}"
        )

        tree.insert(
            stats_tab, "end",
            text=f"Has domaći zadatak: {sanitize(stats_data.has_domaci_zadatak)}"
        )

        tree.insert(
            stats_tab, "end",
            text=f"Has projekat: {sanitize(stats_data.has_projekat)}"
        )

    ### OTHER STATS TAB ###
    other_stats_data = get_other_stats(cursor, review_data.id)

    if other_stats_data:
        other_stats_tab: str = tree.insert(lesson_id, "end", text="Other Stats")

        tree.insert(
            other_stats_tab, "end",
            text=f"Word count total: {sanitize(other_stats_data.word_count_total)}"
        )

        tree.insert(
            other_stats_tab, "end",
            text=f"Word count lv1: {sanitize(other_stats_data.word_count_lv1)}"
        )

        tree.insert(
            other_stats_tab, "end",
            text=f"Word count lv2: {sanitize(other_stats_data.word_count_lv2)}"
        )

        tree.insert(
            other_stats_tab, "end",
            text=f"Word count lv3: {sanitize(other_stats_data.word_count_lv3)}"
        )

        tree.insert(
            other_stats_tab, "end",
            text=f"Word count lv0: {sanitize(other_stats_data.word_count_lv0)}"
        )

        tree.insert(
            other_stats_tab, "end",
            text=f"Word count total per class: {sanitize(other_stats_data.word_count_total_per_class)}"
        )

        tree.insert(
            other_stats_tab, "end",
            text=f"Word count lv1 per class: {sanitize(other_stats_data.word_count_lv1_per_class)}"
        )

        tree.insert(
            other_stats_tab, "end",
            text=f"Word count lv2 per class: {sanitize(other_stats_data.word_count_lv2_per_class)}"
        )

        tree.insert(
            other_stats_tab, "end",
            text=f"Word count lv3 per class: {sanitize(other_stats_data.word_count_lv3_per_class)}"
        )

        tree.insert(
            other_stats_tab, "end",
            text=f"Word count lv0 per class: {sanitize(other_stats_data.word_count_lv0_per_class)}"
        )

        tree.insert(
            other_stats_tab, "end",
            text=f"Word count total per class percentage: {sanitize(other_stats_data.word_count_total_per_class_percentage)}"
        )

        tree.insert(
            other_stats_tab, "end",
            text=f"Snippet words: {sanitize(other_stats_data.snippet_words)}"
        )

        tree.insert(
            other_stats_tab, "end",
            text=f"Latex words: {sanitize(other_stats_data.latex_words)}"
        )

        tree.insert(
            other_stats_tab, "end",
            text=f"Last call: {sanitize(other_stats_data.last_call)}"
        )

        tree.insert(
            other_stats_tab, "end",
            text=f"Figure count: {sanitize(other_stats_data.figure_count)}"
        )

        tree.insert(
            other_stats_tab, "end",
            text=f"YouTube video count: {sanitize(other_stats_data.yt_video_count)}"
        )

        tree.insert(
            other_stats_tab, "end",
            text=f"Google video count: {sanitize(other_stats_data.google_video_count)}"
        )

        tree.insert(
            other_stats_tab, "end",
            text=f"Google video count lv1: {sanitize(other_stats_data.google_video_count_lvl1)}"
        )

        tree.insert(
            other_stats_tab, "end",
            text=f"Google video count lv2: {sanitize(other_stats_data.google_video_count_lvl2)}"
        )

        tree.insert(
            other_stats_tab, "end",
            text=f"Google video count lv3: {sanitize(other_stats_data.google_video_count_lvl3)}"
        )

        tree.insert(
            other_stats_tab, "end",
            text=f"Google video count lv0: {sanitize(other_stats_data.google_video_count_lvl0)}"
        )

        tree.insert(
            other_stats_tab, "end",
            text=f"Google uvod video count: {sanitize(other_stats_data.google_uvod_video_count)}"
        )

        tree.insert(
            other_stats_tab, "end",
            text=f"Audio count: {sanitize(other_stats_data.audio_count)}"
        )

        tree.insert(
            other_stats_tab, "end",
            text=f"Object count: {sanitize(other_stats_data.object_count)}"
        )

        tree.insert(
            other_stats_tab, "end",
            text=f"Subobject count: {sanitize(other_stats_data.subobject_count)}"
        )

        tree.insert(
            other_stats_tab, "end",
            text=f"Section count: {sanitize(other_stats_data.section_count)}"
        )

        tree.insert(
            other_stats_tab, "end",
            text=f"Average Google time: {sanitize(other_stats_data.average_google_time)}"
        )

        tree.insert(
            other_stats_tab, "end",
            text=f"Average Google uvod time: {sanitize(other_stats_data.average_google_uvod_time)}"
        )

        tree.insert(
            other_stats_tab, "end",
            text=f"Total time of Google videos: {sanitize(other_stats_data.total_time_of_google_videos)}"
        )

        tree.insert(
            other_stats_tab, "end",
            text=f"Total time of Google videos uvod: {sanitize(other_stats_data.total_time_of_google_videos_uvod)}"
        )

        tree.insert(
            other_stats_tab, "end",
            text=f"Total time of Google videos lv1: {sanitize(other_stats_data.total_time_of_google_videos_lvl1)}"
        )

        tree.insert(
            other_stats_tab, "end",
            text=f"Total time of Google videos lv2: {sanitize(other_stats_data.total_time_of_google_videos_lvl2)}"
        )

        tree.insert(
            other_stats_tab, "end",
            text=f"Total time of Google videos lv3: {sanitize(other_stats_data.total_time_of_google_videos_lvl3)}"
        )

        tree.insert(
            other_stats_tab, "end",
            text=f"Total time of Google videos lv0: {sanitize(other_stats_data.total_time_of_google_videos_lvl0)}"
        )

        ### YOUTUBE LINKS TAB ###
        yt_links_data = get_links(cursor, other_stats_data.id)

        if yt_links_data:
            yt_links_tab: str = tree.insert(other_stats_tab, "end", text="YouTube Links")

            for link in yt_links_data:
                tree.insert(
                    yt_links_tab, "end",
                    text=sanitize(link.url)
                )
