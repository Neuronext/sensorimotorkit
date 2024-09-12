import os
import pandas as pd

# Define the threshold for Dart X and Dart Y values
threshold = 50

# Specify the path to the CSV file you want to process
input_file_path = 'data/Processed Data/7-26 part 1/Dart.csv'  # Replace with your file path

# Read the CSV file into a DataFrame
df = pd.read_csv(input_file_path)

# Check if the first trial listed is above 100
first_trial_number = df['Trial Number'].min()
if first_trial_number > 100:
    df['Trial Number'] = df['Trial Number'] - (first_trial_number - 1)

# Initialize the list for new rows with default values
new_rows = []

# Assuming the maximum trial number should be inclusive of all trials
max_trial_number = df['Trial Number'].max()

# Process each trial number in the expected range
for trial_number in range(1, max_trial_number + 1):  # Start from 1 after resetting
    if trial_number in df['Trial Number'].values:
        row = df[df['Trial Number'] == trial_number].iloc[0].to_dict()
        if row['Dart X'] < threshold and row['Dart Y'] < threshold:
            row['Dart X'] = 'NA'
            row['Dart Y'] = 'NA'
            row['Missed or Not Present'] = 1.0
        else:
            row['Missed or Not Present'] = 0.0
    else:
        row = {
            'Trial Number': trial_number,
            'Dart X': 'NA',
            'Dart Y': 'NA',
            'Target X': 'NA',
            'Target Y': 'NA',
            'Missed or Not Present': 'Images not present'
        }
    new_rows.append(row)

# Create a new DataFrame with the processed data
new_df = pd.DataFrame(new_rows)

# Get the directory of the input file
output_directory = os.path.dirname(input_file_path)

# Create a new filename with a prefix
output_file_name = f'processed_{os.path.basename(input_file_path)}'

# Combine the directory and new filename to form the full output path
output_file_path = os.path.join(output_directory, output_file_name)

# Save the new DataFrame to a CSV file in the same folder
new_df.to_csv(output_file_path, index=False)

print(f'Processed file saved to: {output_file_path}')
