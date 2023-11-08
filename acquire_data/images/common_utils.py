import os

def get_folder_count(folder):
    # return len([name for name in os.listdir(folder) if os.path.isdir(os.path.join(folder, name))]) weird windows error
    try:
        return len([name for name in os.listdir(folder) if os.path.isdir(os.path.join(folder, name))])
    except FileNotFoundError:
        print(f"Folder not found: {folder}")
        return 0

def get_file_count(folder):
    return len([name for name in os.listdir(folder) if os.path.isfile(os.path.join(folder, name))])

def init_structure(date_folder):
    cams_structure = {
        'body_tracking/camera_1': ['raw'],
        'body_tracking/camera_2': ['raw'],
        'dart_tracking': ['raw']
    }
    for cam, folders in cams_structure.items():
        for folder in folders:
            raw_path = os.path.normpath(os.path.join(date_folder, cam, folder))
            full_path = os.path.abspath(raw_path)
            print(f"full path {full_path}")
            os.makedirs(raw_path, exist_ok=True)

            index = get_folder_count(raw_path)
            os.makedirs(os.path.join(raw_path, str(index)), exist_ok=True)
