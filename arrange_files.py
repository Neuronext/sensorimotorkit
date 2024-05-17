import os
import shutil

# Base directory where the initial data structure is located
base_dir = r'C:\Users\Data acquisition\sensorimotorkit\data'

# New base directory for the reorganized structure
new_base_dir = os.path.join(base_dir, 'raw')

def reorganize_data():
    # Define the data types to look for
    data_types = ['dart', 'body_left', 'body_right', 'gloves']

    # Walk through the directory structure starting from the base directory
    for root, dirs, files in os.walk(base_dir):
        # Look for directories that might contain trial data
        parts = root.split(os.sep)
        if 'data' in parts and len(parts) > parts.index('data') + 2:
            date = parts[parts.index('data') + 1]
            trial = parts[parts.index('data') + 2]

            # Check each possible data type directory
            for data_type in data_types:
                data_type_path = os.path.join(root, data_type, 'raw')
                if os.path.exists(data_type_path):
                    # Directory exists and presumably contains files
                    for file in os.listdir(data_type_path):
                        src_path = os.path.join(data_type_path, file)
                        new_dir_path = os.path.join(new_base_dir, data_type, date, trial)
                        os.makedirs(new_dir_path, exist_ok=True)
                        dst_path = os.path.join(new_dir_path, file)
                        shutil.move(src_path, dst_path)
                        print(f'Moved {src_path} to {dst_path}')

# Execute the function
reorganize_data()
