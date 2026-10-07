
# This tool downloads all of the JSON data from Google Drive,
# validates it, reformats it and stores it in a local folder.
# Empty JSON files and JSON files with invalid data don't get saved.

import io
import json
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from config.settings import get_drive_folder_id, get_service_account_path

SCOPES: list[str]         = ['https://www.googleapis.com/auth/drive.readonly']
DOWNLOAD_DIR: str         = "data" # Where should the files be stored.

# Download all JSON files from Google Drive and store them locally.
def download_drive_data(
        download_dir: str = DOWNLOAD_DIR,
        service_acc_json: str | None = None
):
    # Secrets and IDs come from environment variables / .env (see .env.example).
    service_acc_json = service_acc_json or get_service_account_path()
    folder_id = get_drive_folder_id()

    # Fetch Google service.
    print("Creating Google drive service...")
    creds = service_account.Credentials.from_service_account_file(
        service_acc_json, scopes=SCOPES
    )
    service = build('drive', 'v3', credentials=creds)

    # Find all files stored on the drive.
    files = []

    def recurse(fid, level=0):
        query = f"'{fid}' in parents and trashed=false"
        page_token = None

        while True:
            response = service.files().list(
                q=query,
                spaces='drive',
                fields='nextPageToken, files(id, name, mimeType)',
                pageToken=page_token
            ).execute()

            for file in response.get('files', []):
                if file['mimeType'] == 'application/vnd.google-apps.folder':
                    recurse(file['id'], level + 1)
                else:
                    files.append({'id': file['id'], 'name': file['name']})

            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

    print("Looking for files on the drive... (This may take a while.)")
    recurse(folder_id)

    file_count = len(files)
    print(f"Found {file_count} files.")

    # Download all files locally.
    print("Downloading files...")

    counter = 0
    Path(download_dir).mkdir(parents=True, exist_ok=True)

    for file in files:
        counter += 1
        file_name = file["name"]
        file_id = file["id"]

        if not file_name.endswith(".json"):
            continue

        file_path = f"{download_dir}/{file_name}"

        if Path(file_path).exists():
            continue

        file_stream = io.BytesIO()
        request = service.files().get_media(fileId=file_id)
        downloader = MediaIoBaseDownload(file_stream, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()

        file_stream.seek(0)

        # Load file as JSON data, check if it's valid, insert file name and id
        # into it and then save it back as a file.
        try:
            json_data = json.load(file_stream)

            if not json_data:
                continue

            if ("fileId" not in json_data) or (not json_data["fileId"]):
                continue

            if ("data" not in json_data) or (not json_data["data"]):
                continue

            json_data["data"] = json_data["data"][0]

            if "error" in json_data["data"]:
                continue

            json_data["driveFileName"] = file_name
            json_data["driveFileId"] = file_id

            # Save JSON data to a file.
            with open(file_path, "w", encoding="utf-8") as out_file:
                json.dump(json_data, out_file, indent=2, ensure_ascii=False)
        except json.JSONDecodeError as e:
            print(f"Error parsing downloaded file as JSON: {e}")

        if counter % 10 == 0:
            print(f"Download progress: {round((counter / file_count) * 100.0, 2)}% ({counter} files downloaded.)")
    
    print("Download complete.")

def main():
    download_drive_data()

if __name__ == "__main__":
    main()
