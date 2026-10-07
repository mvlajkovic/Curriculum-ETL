from pyodbc import Cursor
from pyodbc import Row

from database.repositories.zadatak_za_samostalni_rad_trajanje import insert_zadatak_za_samostalni_rad_trajanje
from database.repositories.pokazne_vezbe_trajanje import insert_pokazne_vezbe_trajanje
from database.repositories.individualne_vezbe_trajanje import insert_individualne_vezbe_trajanje
from database.repositories.domaci_zadatak_trajanje import insert_domaci_zadatak_trajanje

def insert_lesson_stats(cursor: Cursor, les_id: int, stats: dict) -> int:
    cursor.execute("""
        INSERT INTO lesson_stats (
            les_id,
            total_activity_counter,
            forum_counter,
            multiple_choice_counter,
            assessment_counter,
            q_and_a_counter,
            activity_after_summary_counter,
            forum_after_summary_counter,
            no_ou_predavanja,
            no_ou_pokazne_vezbe,
            no_ou_individualne_vezbe,
            no_ou_zadatak_za_samostalni_rad,
            no_ou_domaci_zadatak,
            no_ou_projekat,
            has_pokazne_vezbe,
            has_individualne_vezbe,
            has_zadatak_za_samostalni_rad,
            has_domaci_zadatak,
            has_projekat
        )
        OUTPUT INSERTED.id
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        les_id,
        stats.get("TotalActivityCounter", 0),
        stats.get("ForumCounter", 0),
        stats.get("MultipleChoiceCounter", 0),
        stats.get("AssessmentCounter", 0),
        stats.get("QandACounter", 0),
        stats.get("ActivityAfterSummaryCounter", 0),
        stats.get("ForumAfterSummaryCounter", 0),
        stats.get("noOuPredavanja", 0),
        stats.get("noOuPokazneVezbe", 0),
        stats.get("noOuIndividualneVezbe", 0),
        stats.get("noOuZadatakZaSamostalniRad", 0),
        stats.get("noOuDomaciZadatak", 0),
        stats.get("noOuProjekat", 0),
        stats.get("hasPokazneVezbe", False),
        stats.get("hasIndividualneVezbe", False),
        stats.get("hasZadatakZaSamostalniRad", False),
        stats.get("hasDomaciZadatak", False),
        stats.get("hasProjekat", False)
    )

    lesson_stats_id: int = cursor.fetchone()[0]

    zzsr_durations = stats.get("ZadatakZaSamostalniRadTrajanje", [])
    if zzsr_durations:
        insert_zadatak_za_samostalni_rad_trajanje(cursor, lesson_stats_id, zzsr_durations)

    pv_durations = stats.get("PokazneVezbeTrajanje", [])
    if pv_durations:
        insert_pokazne_vezbe_trajanje(cursor, lesson_stats_id, pv_durations)

    iv_durations = stats.get("IndividualneVezbeTrajanje", [])
    if iv_durations:
        insert_individualne_vezbe_trajanje(cursor, lesson_stats_id, iv_durations)

    dz_durations = stats.get("DomaciZadatakTrajanje", [])
    if dz_durations:
        insert_domaci_zadatak_trajanje(cursor, lesson_stats_id, dz_durations)

    return lesson_stats_id

def get_stats(cursor: Cursor, review_id: int) -> Row | None:
    if (not isinstance(review_id, int)) or (review_id < 1):
        return None

    cursor.execute("""
        SELECT
            id,
            les_id,
            total_activity_counter,
            forum_counter,
            multiple_choice_counter,
            assessment_counter,
            q_and_a_counter,
            activity_after_summary_counter,
            forum_after_summary_counter,
            no_ou_predavanja,
            no_ou_pokazne_vezbe,
            no_ou_individualne_vezbe,
            no_ou_zadatak_za_samostalni_rad,
            no_ou_domaci_zadatak,
            no_ou_projekat,
            has_pokazne_vezbe,
            has_individualne_vezbe,
            has_zadatak_za_samostalni_rad,
            has_domaci_zadatak,
            has_projekat
        FROM lesson_stats
        WHERE les_id = ?
    """, review_id)

    return cursor.fetchone()

