import subprocess
import csv
import os

# Define the path to your metadata.csv file
metadata_path = '../metadata.csv'

#TODO: might have to fix it to check for processed in every folder for that date and check if there are any files in it
def get_latest_trial_folder(metadata_path):
    with open(metadata_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        latest_date = None
        latest_folder = None
        for row in reader:
            if latest_date is None or row['Date'] > latest_date:
                latest_date = row['Date']
                latest_folder = row['Trial Folder']
    return latest_folder

latest_folder = get_latest_trial_folder(metadata_path)


if latest_folder:
    body_right_path = os.path.join(latest_folder, 'body_right')
    # node_path = r'C:\Program Files\nodejs\node.exe'
    node_path = 'C:\\Program Files\\nodejs\\node.exe'
    result = subprocess.run([node_path, 'humanTracking.js', body_right_path], capture_output=True, text=True)
    print(result.stdout)
else:
    print("No trial folder found in metadata.")
