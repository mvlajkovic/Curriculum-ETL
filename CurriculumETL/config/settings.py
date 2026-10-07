"""Central configuration. All secrets and machine-specific values come from
environment variables (optionally loaded from a git-ignored .env file)."""

import os
from pathlib import Path

# Load a local .env file if python-dotenv is installed (optional dependency).
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parents[1] / ".env")
except ImportError:
    pass


def _require(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(
            f"Missing required setting '{name}'. "
            f"Copy .env.example to .env and fill it in."
        )
    return value


def get_drive_folder_id() -> str:
    return _require("DRIVE_FOLDER_ID")


def get_service_account_path() -> str:
    path = _require("GOOGLE_APPLICATION_CREDENTIALS")
    if not Path(path).is_file():
        raise RuntimeError("GOOGLE_APPLICATION_CREDENTIALS does not point to an existing file.")
    return path


def get_db_connection_string() -> str:
    return (
        f"DRIVER={{{os.environ.get('DB_DRIVER', 'ODBC Driver 17 for SQL Server')}}};"
        f"SERVER={_require('DB_SERVER')};"
        f"DATABASE={_require('DB_NAME')};"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )
