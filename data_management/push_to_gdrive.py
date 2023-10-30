import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials

# Directory containing the contents to be uploaded
directory_path = input("enter the directory path to upload: ")

# Google Drive folder ID to upload the contents
folder_id = '18ChhYoMQfxdKA6XAQrvX8-YDZAOjF0-b'

# Google Drive API credentials
credentials = Credentials.from_service_account_file('credentials.json')
drive_service = build('drive', 'v3', credentials=credentials)

# Get the list of files already in the folder
response = drive_service.files().list(q=f"'{folder_id}' in parents",
                                      spaces='drive',
                                      fields='files(name)').execute()
all_files = response.get('files', [])
if not all_files:
    print("No files found in the folder {folder_id}")
existing_files = [file['name'] for file in all_files]

print("printing existing files: ", existing_files)
# Iterate over the files in the directory
for filename in os.listdir(directory_path):
    file_path = os.path.join(directory_path, filename)
    print("file_path: ", file_path)
    # Check if the item is a file
    if os.path.isfile(file_path):
        # Check if the file already exists in Google Drive
        if filename in existing_files:
            print(f"Skipped '{filename}' as it already exists in Google Drive.")
            continue

        # Create a file metadata
        file_metadata = {
            'name': filename,
            'parents': [folder_id]
        }

        # Create a media file upload
        media = MediaFileUpload(file_path, resumable=True)

        # Upload the file to Google Drive
        file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        print(f"Uploaded '{filename}' with ID: {file.get('id')} to Google Drive.")
