# CurriculumETL

A Python ETL tool for curriculum content analytics. It pulls lesson JSON files from a Google Drive folder, validates them, loads them into a SQL Server database, and provides a small desktop GUI for searching and browsing the imported lessons.

```
Google Drive (folder, recursive)
        │  Google Drive API + service account
        ▼
Local cache  ──►  data/*.json   (validated, normalized)
        │
        ▼
ETL layer  ──►  parameterized INSERTs inside one transaction per file
        │  pyodbc
        ▼
SQL Server (CurriculumDB)
        │
        ▼
Tkinter search GUI (Lesson Search)
```

## Features

- **Google Drive integration** – recursively walks a Drive folder (with pagination) and downloads every `.json` file using a read-only service account.
- **Validation layer** – files that are empty, invalid JSON, missing `fileId` or `data`, or that contain an `error` payload are skipped and never saved.
- **Idempotent loading** – each lesson is identified by its `fileId`; lessons already in the database are skipped, so the pipeline can be re-run safely. Already-downloaded files are not downloaded again.
- **Transactional inserts** – every file is loaded in a single transaction (commit on success, rollback on error) using parameterized queries only.
- **Search GUI** – search lessons by course code, title, lesson number, year, author or file ID, and expand any result to see its full imported data (overview, summary, learning objects and subobjects, LAMS activities, forums, stats, video stats, YouTube links).

## Project structure

```
CurriculumETL/
├── CurriculumETL.sln
└── CurriculumETL/
    ├── CurriculumETL.py            # Entry point: download -> load -> launch GUI
    ├── gui_app.py                  # Tkinter "Lesson Search" window
    ├── .env.example                # Template for local settings (copy to .env)
    ├── config/
    │   └── settings.py             # Reads settings from environment variables / .env
    ├── gui/
    │   └── lesson_info_loader.py   # Loads a lesson's data into the GUI tree
    ├── services/
    │   ├── drive_downloader_service.py  # Drive traversal, download, validation
    │   └── etl_service.py               # Maps JSON -> database rows
    ├── drive/
    │   └── drive_client.py         # Early Drive helper (not used by the main flow)
    ├── parsers/
    │   └── lesson_parser.py        # Early parser (not used by the main flow)
    └── database/
        ├── db.py                   # Connection string, connection helper
        ├── transaction.py          # Commit/rollback context manager
        └── repositories/           # One module per table (insert + query functions)
```

## Data model

Each JSON file becomes one lesson, linked to its related data:

| Table | Content |
| --- | --- |
| `lesson` | Course code, title, academic year, lesson number, author, scientific field |
| `lesson_version` | Source `fileId` (used for duplicate detection) |
| `lesson_review` | Drive file name / ID and import timestamp |
| `summary`, `overview` | Summary and overview IDs and titles |
| `learning_objects`, `learning_object_subobjects` | Learning objects and their subobjects with metadata (classification, difficulty, keywords, outcomes, competences, etc.) |
| `lams_activities` | LAMS activities and tool information |
| `forums` | Forum topics and descriptions |
| `lesson_stats` | Activity counters and which exercise types the lesson contains |
| `lesson_other_stats` | Word counts, media counts, video durations |
| `yt_videos`, `yt_links` | YouTube videos and links |
| `google_videos`, `google_videos_uvod`, `google_videos_lvl0` … `lvl3` | Google-hosted videos per level |
| `pokazne_vezbe_trajanje`, `individualne_vezbe_trajanje`, `zadatak_za_samostalni_rad_trajanje`, `domaci_zadatak_trajanje` | Durations per exercise type |

Relationship in short: `lesson` → `lesson_version` → `lesson_review` → (everything else).

> **Note:** Database setup: The project uses SQL Server for persistent storage. The database schema is intentionally not included because it is specific to the source environment. To run the project, configure a compatible database and adapt the repository mappings to your schema.

## Requirements

- Python **3.12+** (the entry point uses nested quotes inside f-strings, which older versions reject)
- Microsoft SQL Server (e.g. SQL Server Express) with a database named `CurriculumDB`
- [ODBC Driver 17 for SQL Server](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server)
- A Google Cloud service account with access to the Drive folder
- Python packages:

```bash
pip install google-api-python-client google-auth pyodbc python-dotenv
```

`python-dotenv` is optional: without it, set the variables from the Configuration section in your system environment instead of a `.env` file.

Tkinter ships with the standard Python installer on Windows.

## Configuration

No secrets or machine-specific values live in the source code. They are read from environment variables, which can be provided through a local `.env` file (git-ignored).

1. Copy the template:

   ```bash
   cd CurriculumETL
   copy .env.example .env      # Windows (use "cp" on macOS/Linux)
   ```

2. Fill in `.env`:

| Variable | Description |
| --- | --- |
| `GOOGLE_APPLICATION_CREDENTIALS` | Full path to your service account key file (keep it outside the repository) |
| `DRIVE_FOLDER_ID` | ID of the Google Drive root folder to read |
| `DB_SERVER` | SQL Server instance, e.g. `localhost\SQLEXPRESS` |
| `DB_NAME` | Database name, e.g. `CurriculumDB` |
| `DB_DRIVER` | ODBC driver name (default `ODBC Driver 17 for SQL Server`) |

If a required variable is missing, the app stops with a clear message telling you which one.

Non-secret behaviour flags are still constants at the top of `CurriculumETL.py`:

| Setting | Description |
| --- | --- |
| `JSON_DATA_DIR` | Local folder for downloaded JSON files (default `data`) |
| `DOWNLOAD_DATA_BEFORE_PROCESSING` | Set to `False` to skip downloading and use files already in `JSON_DATA_DIR` |
| `RUN_GUI_AFTER_PROCESSING` | Open the search GUI when the import finishes |

### Google Drive setup

1. Create a service account in Google Cloud and enable the **Google Drive API**.
2. Download the service account key (JSON) and store it **outside the repository**.
3. Share the Drive folder with the service account's email address (read-only is enough).
4. Put the key path and the folder ID (the last part of the folder URL) into `.env`.

## Usage

Run from the inner project folder so that module imports resolve:

```bash
cd CurriculumETL
python CurriculumETL.py
```

What happens:

1. JSON files are downloaded from Drive into `data/` (existing files are skipped).
2. Each file is validated and inserted into SQL Server; duplicates (by `fileId`) are skipped.
3. A summary is printed (`Processed N JSON files in X seconds`).
4. The **Lesson Search** window opens.

To open only the GUI against an already-populated database:

```bash
python gui_app.py
```

In the GUI, type into any search field and press **Enter** or **SEARCH**. Results are capped at 5000 rows. Expand a lesson to load its details, and press **Ctrl+C** on a selected row to copy its text.

## Expected JSON format

After download, each file is normalized to this shape:

```json
{
  "fileId": "…",
  "driveFileName": "…",
  "driveFileId": "…",
  "data": {
    "CourseCode": "…",
    "Title": "…",
    "Year": "…",
    "Lesson": "…",
    "Author": "…",
    "Summary": { "SummaryId": "…", "SummaryTitle": "…" },
    "Overview": { "OverviewId": "…", "OverviewTitle": "…" },
    "Forums": [],
    "LamsActivities": [],
    "LearningObject": [],
    "Stats": {},
    "OtherStats": { "lessons": [ { "NaucnoPolje": "…", "ytVideos": [], "googleVideos": [] } ] }
  }
}
```

In the Drive originals `data` is a list; the downloader keeps only its first element and adds `driveFileName` and `driveFileId`.

## Security notes

- **Never commit secrets.** `.env`, key files (`*.pem`, `*.key`, `*service-account*.json`, `curriculumetl-*.json`) and the downloaded `data/` folder are listed in `.gitignore`. Only `.env.example` (with placeholders) is tracked.
- Keep the service account key outside the project folder, and share the Drive folder with it as read-only (the app only requests the `drive.readonly` scope).
- If a key is ever pushed to GitHub, treat it as compromised: delete it in Google Cloud Console (IAM & Admin > Service Accounts > Keys), create a new one, and remove it from git history (e.g. with `git filter-repo`). Deleting the file in a later commit is not enough.
- The database connection uses Windows authentication, so no database password is stored anywhere.
- All database access uses parameterized queries.
- The downloaded lesson JSON files are not committed; check them for sensitive content before sharing them anywhere.

## Roadmap

- Add a `schema.sql` with all table definitions
- Replace `print` output with `logging`
- Remove or integrate the unused `drive/` and `parsers/` modules
- Add a `requirements.txt` and basic tests for the ETL mapping
