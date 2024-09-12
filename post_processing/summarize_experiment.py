import os
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy.polynomial import Polynomial

def calculate_distance(dart_x, dart_y, target_x, target_y):
    """Calculate the Euclidean distance between the dart and the target."""
    return np.sqrt((dart_x - target_x) ** 2 + (dart_y - target_y) ** 2)

def calculate_and_plot_region(trial_numbers, distances, region_start, region_end, color, label_prefix, stats=None):
    """Calculate and plot a boxplot for a region with transparency and buffer space, and optionally collect statistics."""
    region_indices = [i for i, trial in enumerate(trial_numbers) if region_start <= trial <= region_end]
    region_distances = [distances[i] for i in region_indices if not np.isnan(distances[i])]
    
    if region_distances:
        mean_distance = np.mean(region_distances)
        std_distance = np.std(region_distances)
        if stats is not None:
            stats[label_prefix] = {'Mean': round(mean_distance, 3), 'StdDev': round(std_distance, 3)}
        
        # Plot a box and whisker plot
        plt.boxplot(
            region_distances, 
            positions=[(region_start + region_end) / 2], 
            widths=(region_end - region_start),  # Adjust the width to cover 15 trials
            patch_artist=True, 
            boxprops=dict(facecolor=color, color=color, alpha=0.3),  # Make the box mostly transparent
            whiskerprops=dict(color=color), 
            capprops=dict(color=color), 
            medianprops=dict(color='black'),
            showfliers=False  # Do not display outliers
        )

def plot_dart_data(csv_file_path):
    trial_numbers = []
    distances = []
    missed_trials = []
    no_image_trials = []

    # Read the CSV file
    with open(csv_file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            trial_number = int(float(row['Trial Number']))  # Convert to float first, then to int
            dart_x = row['Dart X']
            dart_y = row['Dart Y']
            target_x = row['Target X']
            target_y = row['Target Y']
            missed_or_not_present = row['Missed or Not Present']

            trial_numbers.append(trial_number)

            if missed_or_not_present == '1.0':
                missed_trials.append(trial_number)
                distances.append(np.nan)
            elif missed_or_not_present == 'Images not present':
                no_image_trials.append(trial_number)
                distances.append(np.nan)
            else:
                try:
                    # Attempt to calculate the distance, skip the trial if conversion fails
                    distance = calculate_distance(float(dart_x), float(dart_y), float(target_x), float(target_y))
                    distances.append(distance)
                except ValueError:
                    # Skip this trial if it contains non-convertible values like 'NA'
                    continue

    # Prepare data for regression (exclude NaNs)
    trial_numbers_valid = np.array([trial for trial, dist in zip(trial_numbers, distances) if not np.isnan(dist)])
    valid_distances = np.array([dist for dist in distances if not np.isnan(dist)])

    # Fit a polynomial regression model of degree 5
    p = Polynomial.fit(trial_numbers_valid, valid_distances, 5)
    distance_predictions = p(trial_numbers_valid)

    # Plot the distance between dart and target using scatter plot
    fig, ax1 = plt.subplots(figsize=(12, 6))
    scatter1 = ax1.scatter(trial_numbers, distances, color='blue', label='Dart-Target Distance')

    # Plot the polynomial regression line
    line2 = ax1.plot(trial_numbers_valid, distance_predictions, color='blue', alpha=0.75, label='Predicted Distance (Poly Degree 5)')

    # Plot the missed trials and no image trials using scatter plot
    scatter2 = ax1.scatter(missed_trials, [0] * len(missed_trials), color='red', label=f'Missed Trials (Count: {len(missed_trials)})')
    scatter3 = ax1.scatter(no_image_trials, [0] * len(no_image_trials), color='grey', label=f'Images Not Present (Count: {len(no_image_trials)})')

    # Dictionary to store the statistics
    stats = {}

    # Plot box and whisker plots for each region with transparency and spacing
    calculate_and_plot_region(trial_numbers, distances, 1, 15, 'grey', 'BE Before', stats)
    calculate_and_plot_region(trial_numbers, distances, 16, 30, 'grey', 'ST Before', stats)
    calculate_and_plot_region(trial_numbers, distances, 31, 45, 'grey', 'MT Before', stats)
    calculate_and_plot_region(trial_numbers, distances, 135, 150, 'grey', 'BE After', stats)
    calculate_and_plot_region(trial_numbers, distances, 151, 165, 'grey', 'ST After', stats)
    calculate_and_plot_region(trial_numbers, distances, 166, 180, 'grey', 'MT After', stats)

    # Customize the plot
    file_name = os.path.basename(os.path.dirname(csv_file_path))  # Get the folder name as the title
    ax1.set_xlabel('Group')
    ax1.set_ylabel('Distance Between Dart and Target')
    ax1.set_title(file_name)

    # Change x-axis labels to match the group names
    ax1.set_xticks([7.5, 22.5, 37.5, 142.5, 157.5, 172.5])
    ax1.set_xticklabels(['BE', 'ST', 'MT', 'BE', 'ST', 'MT'])

    # Combine the legends and place it outside the plot area
    handles, labels = ax1.get_legend_handles_labels()
    ax1.legend(handles, labels, loc='center left', bbox_to_anchor=(1.15, 0.8), borderaxespad=0.)

    # Create a table with the statistics
    stats_df = pd.DataFrame(stats).T
    stats_df.index.name = 'Region'
    stats_df.columns = ['Mean', 'StdDev']

    # Organize the table to compare before and after
    comparison_df = pd.concat([
        stats_df.loc[['BE Before', 'BE After']],
        stats_df.loc[['ST Before', 'ST After']],
        stats_df.loc[['MT Before', 'MT After']]
    ])

    # Add the table to the right of the plot, aligned with the left side of the legend
    table = plt.table(cellText=comparison_df.values,
                      rowLabels=comparison_df.index,
                      colLabels=comparison_df.columns,
                      cellLoc='center', rowLoc='center',
                      loc='right', bbox=[1.25, 0, 0.30, 0.6])

    # Set line width to 0 for row and column headers
    for key, cell in table.get_celld().items():
        if key[0] == 0 or key[1] == -1:
            cell.set_linewidth(0)
        else:
            cell.set_linewidth(1)

    plt.tight_layout()

    # Save the plot as a PNG file in the same directory as the CSV file
    png_file_path = os.path.splitext(csv_file_path)[0] + '.png'
    plt.savefig(png_file_path)

    # Show the plot
    plt.show()

# Example usage
parent_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go up one level in the folder hierarchy
csv_file_path = os.path.join(parent_folder, "data/Processed Data", "7-24 part 1", "processed_Dart.csv")
plot_dart_data(csv_file_path)
