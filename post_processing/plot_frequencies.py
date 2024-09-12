import os
import csv
import numpy as np
import matplotlib.pyplot as plt  # Import the matplotlib library for plotting

# Define the input and output file paths
input_folder = 'data'  # Replace with your folder path
output_filename = 'frequencies.csv'  # Replace with your desired output file name

output_filepath = os.path.join(input_folder, output_filename)

# Replace this with your list of lists (already generated data)
data = []
try:
    with open('summary.csv', 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
except Exception as e:
    print(f"An error occurred: {e}")

# Extract column headers and row labels
column_labels = data[0]  # First row as column labels
row_labels = [row[0] for row in data[1:]]  # First column as row labels
rows = data[1:]  # Data excluding headers

# Initialize a new list to store centered data and combined numeric values
centered_data = []
combined_numeric_values = []  # List to store all numeric values across all trials

# Process each row to compute centered values and plot histograms
for idx, row in enumerate(rows):
    # Separate the label and data values
    label = row[0]
    numeric_values = []

    # Identify numeric values, ignoring non-numeric ones
    for value in row[1:]:
        try:
            num_value = float(value)
            # Apply log function, handling values <= 0
            if num_value > 0:
                log_value = np.log(num_value)
                numeric_values.append(log_value)
            else:
                numeric_values.append(np.nan)  # Handle non-positive values
        except ValueError:
            numeric_values.append(np.nan)

    # Calculate the mean of the numeric values, ignoring NaNs
    numeric_mean = np.nanmean(numeric_values)

    # Center the numeric values and prepare the new row
    centered_row = [label]
    for value in numeric_values:
        if not np.isnan(value):
            centered_value = value - numeric_mean  # Center the numeric value
            centered_row.append(f'{centered_value:.7f}')  # Keep it formatted to 7 decimals
        else:
            centered_row.append('nan')  # Preserve NaNs

    centered_data.append(centered_row)

    # Filter out NaN values for plotting
    clean_numeric_values = [x for x in numeric_values if not np.isnan(x)]

    # Add clean numeric values to the combined list
    combined_numeric_values.extend(clean_numeric_values)

    # Plot histogram for each trial
    if clean_numeric_values:
        plt.figure(figsize=(8, 6))
        plt.hist(clean_numeric_values, bins=20, edgecolor='black')  # Adjust bins as needed
        plt.xlabel('Log of Distance')
        plt.ylabel('Frequency')
        plt.title(f'Histogram of Log Distances for {label}')
        plt.grid(True)

        # Save the histogram to a file
        plot_filename = f'histogram_{label}.png'.replace(' ', '_')
        plt.savefig(plot_filename)
        plt.close()  # Close the plot to free memory

        print(f'Histogram saved: {plot_filename}')

# Plot combined histogram for all trials
if combined_numeric_values:
    plt.figure(figsize=(8, 6))
    plt.hist(combined_numeric_values, bins=20, edgecolor='black')  # Adjust bins as needed
    plt.xlabel('Log of Distance')
    plt.ylabel('Frequency')
    plt.title('Histogram of Log Distances for All Trials')
    plt.grid(True)

    # Save the combined histogram to a file
    combined_plot_filename = 'histogram_all_trials.png'
    plt.savefig(combined_plot_filename)
    plt.close()  # Close the plot to free memory

    print(f'Combined histogram saved: {combined_plot_filename}')

# Write the centered data to a new CSV file
with open(output_filepath, 'w', newline='') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(column_labels)
    # Write the centered data
    writer.writerows(centered_data)

print(f'Centered CSV file created: {output_filepath}')
