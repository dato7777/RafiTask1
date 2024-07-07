from __future__ import print_function
import os.path
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

# Combined SCOPES for both uploading and downloading
SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret_1064085980762-du2qefanrj9u323s3850pc9scsdgdsm3.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    return service

def upload_file(service, file_path, file_name, folder_id=None):
    file_metadata = {'name': file_name}
    if folder_id:
        file_metadata['parents'] = [folder_id]
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print('Uploaded File ID: %s' % file.get('id'))
    return file.get('id')

def download_file(service, file_id, file_path):
    try:
        request = service.files().get_media(fileId=file_id)
        fh = io.FileIO(file_path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            if status:
                print("Download %d%%." % int(status.progress() * 100))
        
        print(f"Downloaded file saved to: {file_path}")
        
    except Exception as e:
        print(f"Error downloading file: {e}")

if __name__ == '__main__':
    service = authenticate()
    
    # Upload a file
    file_path_to_upload = '/Users/dato/Desktop/mevarTesti1.jpeg'
    folder_id = '1cO-4OKgwnb3hdNrEQXpKusu1oRavPcR9'  # Add your folder ID here, or set to None
    uploaded_file_id = upload_file(service, file_path_to_upload, 'uploaded_file.jpeg', folder_id=folder_id)

    # Download a specific file
    file_id_to_download = '1DSxZQJnuwbk2gJDyYl-vY15B57xWPYS-'  # Specific file ID you want to download
    file_path_to_save = '/Users/dato/Desktop/sima1.jpg'  # Adjust as needed
    download_file(service, file_id_to_download, file_path_to_save)
