import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_rel
import numpy as np

# Load the CSV file
input_file = 'summary.csv'  # Replace with your input file path
output_file = 'averages.csv'  # Replace with your desired output file path

# Read the CSV file into a DataFrame
df = pd.read_csv(input_file)

# Check column names to identify the label column
print("Column names:", df.columns)

# Replace 'label' with the actual name of the first column if it's different
label_column = df.columns[0]  # Automatically uses the first column as the label

# Initialize a new DataFrame to store averages
averages_df = pd.DataFrame()
averages_df[label_column] = df[label_column]  # Copy the label column

# List to store average values for plotting
average_data = []

# Loop through each group of 15 trials and calculate averages, ignoring non-numerical values
for i in range(0, 180, 15):
    # Create a column name for each 15-trial window
    col_name = f'average_{i + 1}_{i + 15}'
    
    # Calculate the mean for each group of 15 trials, ignoring non-numerical data
    averages = df.iloc[:, i + 1:i + 16].apply(pd.to_numeric, errors='coerce').mean(axis=1)
    averages_df[col_name] = averages
    
    # Append averages to the list for plotting
    average_data.append(averages)

# Save the new DataFrame with averages to a CSV
averages_df.to_csv(output_file, index=False)
print(f"Averages saved to {output_file}")

# Select only the first three and last three groups
selected_data = [average_data[0], average_data[-3],  # BE pre, BE post
                 average_data[1], average_data[-2],  # ST pre, ST post
                 average_data[2], average_data[-1]]  # MT pre, MT post
labels = ['BE (Pre)', 'BE (Post)', 'ST (Pre)', 'ST (Post)', 'MT (Pre)', 'MT (Post)']

# Define colors for matching groups
colors = ['#1f77b4', '#1f77b4',  # Matching colors for BE
          '#ff7f0e', '#ff7f0e',  # Matching colors for ST
          '#2ca02c', '#2ca02c']  # Matching colors for MT

# Plot the selected averages on a box and whisker plot
plt.figure(figsize=(12, 6))
positions = np.array([1, 2, 4, 5, 7, 8])  # Adjust positions to place pre and post next to each other
boxplots = plt.boxplot(selected_data, patch_artist=True, positions=positions)

# Apply colors to box plots
for patch, color in zip(boxplots['boxes'], colors):
    patch.set_facecolor(color)

# Display the mean of each group above its box plot
for pos, data in zip(positions, selected_data):
    mean_value = np.mean(data)
    plt.text(pos, mean_value, f'{mean_value:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

# Set plot details
plt.title('Box and Whisker Plot of Selected Averages')
plt.xlabel('Groups')
plt.ylabel('Average Distance from Target')
plt.xticks(positions, labels)

# Perform paired t-tests and add significance bars
comparisons = [(0, 1), (2, 3), (4, 5)]  # Indices of the groups to compare
for idx, (pre, post) in enumerate(comparisons):
    t_stat, p_value = ttest_rel(selected_data[pre], selected_data[post], nan_policy='omit')
    print(f"T-test {labels[pre]} vs {labels[post]}: t-statistic = {t_stat:.4f}, p-value = {p_value:.4f}")
    
    # Adding significance bars
    y, h, col = np.max([selected_data[pre], selected_data[post]]) + 0.1, 0.05, 'k'
    plt.plot([positions[pre], positions[post]], [y, y], lw=1.5, c=col)
    plt.text((positions[pre] + positions[post]) * 0.5, y + h, f'p = {p_value:.3f}', ha='center', va='bottom', color=col)

# Save and show the plot
plt.tight_layout()
plt.savefig('selected_boxplot_rearranged.png')
plt.show()
