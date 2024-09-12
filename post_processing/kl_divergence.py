# Step 1: Load the CSV file
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import entropy
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import os
import tkinter as tk

# Load data from CSV
data = []
try:
    with open('summary.csv', 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
except Exception as e:
    print(f"An error occurred while reading the CSV file: {e}")

# Step 2: Decide figure settings

# Step 2a: Group parameters
def group_params_gui():
    def return_values():
        global group_params
        size = int(group_size_entry.get())
        overlap = int(group_overlap_entry.get())
        group_params = [size, overlap]
        figure_params_root.destroy()

    figure_params_root = tk.Tk()
    figure_params_root.title("Figure Settings: Parameters")

    tk.Label(figure_params_root, text="Group Size").pack()
    group_size_entry = tk.Entry(figure_params_root)
    group_size_entry.pack()

    tk.Label(figure_params_root, text="Group Overlap").pack()
    group_overlap_entry = tk.Entry(figure_params_root)
    group_overlap_entry.pack()

    tk.Button(figure_params_root, text="Submit Group Parameters", command=return_values).pack()

    figure_params_root.mainloop()

    return group_params

group_params_final = group_params_gui()

# Step 2b: Generate groups
def generate_groups(group_size, group_overlap, total_trials=180):
    groups = []
    start = 1
    while start <= total_trials:
        end = min(start + group_size - 1, total_trials)
        groups.append(list(range(start, end + 1)))
        start += group_size - group_overlap
    return groups

groups = generate_groups(group_params_final[0], group_params_final[1])

# Step 3: Calculate KL Divergence for each pair of subsequent groups
def calculate_kl_divergence(data, groups):
    kl_values = []
    mean_trial_numbers = []
    df = pd.DataFrame(data[1:], columns=data[0])
    
    # Convert to numeric and handle missing data
    numerical_data = df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')

    for i in range(len(groups) - 1):
        group1_indices = [float(x) - 1 for x in groups[i]]
        group2_indices = [float(x) - 1 for x in groups[i + 1]]

        # Check if the groups have the same number of items
        if len(group1_indices) != len(group2_indices):
            continue  # Skip this comparison if the sizes are different

        # Calculate participant averages for each group
        group1_data = numerical_data.iloc[:, group1_indices].mean(axis=1).dropna().values
        group2_data = numerical_data.iloc[:, group2_indices].mean(axis=1).dropna().values

        # Calculate mean trial number for the x-axis
        mean_trial_number = (min(group1_indices) + max(group2_indices)) / 2 + 1  # Properly average the range
        mean_trial_numbers.append(mean_trial_number)

        # Normalize histograms
        p = np.histogram(group1_data, bins=10, density=True)[0]
        q = np.histogram(group2_data, bins=10, density=True)[0]

        # Add a small constant to avoid division by zero
        p += 1e-10
        q += 1e-10

        kl_div = entropy(p, q)
        kl_values.append(kl_div)

    return kl_values, mean_trial_numbers

# Use the corrected function
kl_divergences, mean_trial_numbers = calculate_kl_divergence(data, groups)

def generate_figure(kl_values, mean_trial_numbers, groups, group_size, group_overlap, save_folder='figures'):
    # Create the save folder if it doesn't exist
    os.makedirs(save_folder, exist_ok=True)

    # Create the title with group size and overlap
    title = f'KL Divergence (Group Size: {group_size}, Overlap: {group_overlap})'

    plt.figure(figsize=(10, 6))

    # Calculate the bar width based on the spacing between mean trial numbers
    # Subtract a small value to ensure bars don't touch each other
    bar_width = group_overlap - 0.1

    # Plot the bar graph for KL Divergence
    for i in range(len(mean_trial_numbers)):
        mean_trial_number = mean_trial_numbers[i]
        plt.bar(mean_trial_number, kl_values[i], width=bar_width, color='gray', alpha=0.9, align='center', edgecolor='black', zorder=3)

    # Create polynomial features of degree 6
    poly = PolynomialFeatures(degree=6)
    X_poly = poly.fit_transform(np.array(mean_trial_numbers).reshape(-1, 1))

    # Fit a linear regression model
    model = LinearRegression()
    model.fit(X_poly, kl_values)

    # Predict using the model
    X_fit = np.linspace(min(mean_trial_numbers), max(mean_trial_numbers), 500).reshape(-1, 1)
    X_poly_fit = poly.transform(X_fit)
    y_fit = model.predict(X_poly_fit)

    # Plot the polynomial regression line
    plt.plot(X_fit, y_fit, color='black', linestyle='-', linewidth=2, alpha=0.7, label='Regression Line', zorder=4)

    # Add labels and title
    plt.xlabel('Mean Trial Number')
    plt.ylabel('KL Divergence')
    plt.title(title)
    plt.legend()
    plt.grid(True, axis='y', zorder=1)  # Enable grid only on the y-axis

    # Save the figure with the title as the filename in the specified folder
    save_path = os.path.join(save_folder, title.replace(':', '').replace(',', '').replace(' ', '_') + '.png')
    plt.savefig(save_path)

    # Display the plot
    plt.show()

# Call the modified generate_figure function
generate_figure(kl_divergences, mean_trial_numbers, groups, group_params_final[0], group_params_final[1])
