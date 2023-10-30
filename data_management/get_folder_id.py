from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# Google Drive API credentials
credentials = Credentials.from_service_account_file('credentials.json')
drive_service = build('drive', 'v3', credentials=credentials)

# Retrieve a list of all folders
results = drive_service.files().list(q="mimeType='application/vnd.google-apps.folder'",
                                     pageSize=1000,  # Adjust as needed to retrieve all folders
                                     fields='files(id, name)').execute()
folders = results.get('files', [])

# Print the names and IDs of all folders
if folders:
    print("Folders in Google Drive:")
    for folder in folders:
        print(f"Name: {folder['name']}, ID: {folder['id']}")
else:
    print("No folders found in Google Drive.")
