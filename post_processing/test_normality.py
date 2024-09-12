import os
import csv
import numpy as np
from scipy.stats import shapiro  # Import Shapiro-Wilk test

# Define the input and output file paths
input_folder = 'data'  # Replace with your folder path
output_filename = 'normality.csv'  # Replace with your desired output file name

output_filepath = os.path.join(input_folder, output_filename)

# Replace this with your list of lists (already generated data)
data = []
try:
    with open('data/summary_centered.csv', 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
except Exception as e:
    print(f"An error occurred: {e}")

# Extract column headers and row labels
column_labels = data[0]  # First row as column labels
row_labels = [row[0] for row in data[1:]]  # First column as row labels
rows = data[1:]  # Data excluding headers

# Initialize a new list to store centered data
centered_data = []

# Process each row to compute centered values and check for normal distribution
for row in rows:
    # Separate the label and data values
    label = row[0]
    numeric_values = []

    # Identify numeric values, ignoring non-numeric ones
    for value in row[1:]:
        try:
            numeric_values.append(float(value))
        except ValueError:
            numeric_values.append(np.nan)

    # Calculate the mean of the numeric values, ignoring NaNs
    numeric_mean = np.nanmean(numeric_values)

    # Center the numeric values and prepare the new row
    centered_row = [label]
    for value in row[1:]:
        try:
            centered_value = float(value) - numeric_mean  # Center the numeric value
            centered_row.append(f'{centered_value:.7f}')  # Keep it formatted to 7 decimals
        except ValueError:
            centered_row.append(value)  # Preserve the non-numeric value

    # Check for normality using the Shapiro-Wilk test, ignoring NaNs
    clean_numeric_values = [x for x in numeric_values if not np.isnan(x)]
    if len(clean_numeric_values) > 1:  # At least two values are needed for the test
        stat, p_value = shapiro(clean_numeric_values)
        normality = 'Yes' if p_value > 0.05 else 'No'
    else:
        normality = 'N/A'  # Not enough data to perform normality test

    # Add normality result to the row
    centered_row.append(normality)
    centered_data.append(centered_row)

# Add a new column header for normality check
column_labels.append('Normality (Shapiro-Wilk p > 0.05)')

# Write the centered data to a new CSV file
with open(output_filepath, 'w', newline='') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(column_labels)
    # Write the centered data
    writer.writerows(centered_data)

print(f'Centered CSV file created: {output_filepath}')
