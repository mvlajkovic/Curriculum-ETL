from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
import json

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def get_drive_service(credentials_json_path):
    """
    Returns an authorized Google Drive service instance.
    """
    print("started get drive service")
    creds = service_account.Credentials.from_service_account_file(
        credentials_json_path, scopes=SCOPES
    )
    service = build('drive', 'v3', credentials=creds)
    print("finished get drive service")
    return service

def list_files_recursive(service, folder_id):

    files = []

    def recurse(fid, level=0):
        query = f"'{fid}' in parents and trashed=false"
        page_token = None

        print("  " * level + f"Entering folder level {level}")

        while True:
            response = service.files().list(
                q=query,
                spaces='drive',
                fields='nextPageToken, files(id, name, mimeType)',
                pageToken=page_token
            ).execute()

            for f in response.get('files', []):
                if f['mimeType'] == 'application/vnd.google-apps.folder':
                    recurse(f['id'], level + 1)
                else:
                    print("  " * level + f"Found file: {f['name']}")
                    files.append({'id': f['id'], 'name': f['name']})

            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

    recurse(folder_id)
    print("Finished listing")
    return files

# def download_file_content(service, file_id):
#     print("Downloading file...")

#     request = service.files().get_media(fileId=file_id)

#     file_stream = io.BytesIO()
#     downloader = MediaIoBaseDownload(file_stream, request)

#     done = False
#     while not done:
#         status, done = downloader.next_chunk()

#     file_stream.seek(0)
#     content = file_stream.read().decode("utf-8")

#     print("Download finished")
#     return content

def download_file_content(service, file_id):
    print("Downloading file...")

    request = service.files().get_media(fileId=file_id)

    file_stream = io.BytesIO()
    downloader = MediaIoBaseDownload(file_stream, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()

    file_stream.seek(0)
    content = file_stream.read().decode("utf-8")

    print("Download finished")

    return json.loads(content)  # now returns dict, not string