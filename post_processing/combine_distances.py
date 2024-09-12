import os
import pandas as pd
import numpy as np

def calculate_distance(target_x, target_y, dart_x, dart_y):
    """Calculate the distance between target and dart positions."""
    try:
        x_offset = float(dart_x) - float(target_x)
        y_offset = float(dart_y) - float(target_y)
        distance = np.sqrt(x_offset**2 + y_offset**2)
        return distance
    except ValueError:
        return 'NA'  # Handle non-numeric values

def process_csv_files(base_path, output_file):
    result = []

    # Iterate over each directory and subdirectory
    for root, dirs, files in os.walk(base_path):
        # Check if 'processed_Dart.csv' is in the current directory's files
        if 'processed_Dart.csv' in files:
            file_path = os.path.join(root, 'processed_Dart.csv')
            experiment_id = os.path.basename(root)  # Use the folder name as experiment ID
            try:
                # Read the CSV file
                df = pd.read_csv(file_path)

                # Initialize a dictionary to store distances for each trial
                distance_data = {'experiment_id': experiment_id}

                # Iterate over rows to calculate distances
                for idx, row in df.iterrows():
                    dart_x, dart_y = row.get('Dart X'), row.get('Dart Y')
                    target_x, target_y = row.get('Target X'), row.get('Target Y')
                    images_status = row.iloc[-1]  # Assuming the last column indicates image status or miss status

                    # Check if the trial was missed or images are not present
                    if images_status == '1' or images_status == '1.0' or images_status == 1:
                        distance = 'miss'
                    elif images_status == 'Images not present':
                        distance = 'NA'
                    else:
                        # Calculate distance for valid data
                        distance = calculate_distance(target_x, target_y, dart_x, dart_y)

                    # Save the distance in a specific column for each trial
                    distance_data[f'trial_{idx + 1}_distance'] = distance

                # Append the dictionary of distances to the result list
                result.append(distance_data)

            except Exception as e:
                # Handle exceptions such as file read errors
                print(f"Error reading {file_path}: {e}")

    # Create a DataFrame from the list of dictionaries
    result_df = pd.DataFrame(result)

    # Save the result to a new CSV file
    result_df.to_csv(output_file, index=False)
    print(f"Results saved to {output_file}")

# Set the path where you want to start the search and the output file name
base_path = 'data/Processed Data'  # Replace this with the desired path as a string
output_file = 'summary.csv'  # Set the desired output file name

# Run the function to process files and save results
process_csv_files(base_path, output_file)
