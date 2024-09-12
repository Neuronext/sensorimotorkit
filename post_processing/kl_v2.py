import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import entropy
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import os

# Step 1: Load data from CSV file
data = []
try:
    # Replace 'summary.csv' with the correct path to your CSV file
    with open('summary.csv', 'r') as file:
        data = pd.read_csv(file)  # Directly read CSV into a pandas DataFrame
except Exception as e:
    print(f"An error occurred while reading the CSV file: {e}")

# Step 2: Manually input for group parameters
group_size = 6  # Example group size, replace with your input
group_overlap = 4  # Example overlap size, replace with your input

# Step 3: Calculate KL Divergence for each pair with shifting windows
def calculate_kl_divergence_shifted(data, group_size, group_overlap, total_trials=180):
    kl_values = []
    mean_trial_numbers = []

    # Convert to numeric and handle missing data
    numerical_data = data.apply(pd.to_numeric, errors='coerce')

    for start in range(total_trials - group_size - group_overlap + 1):
        group1_indices = list(range(start, start + group_size))
        group2_indices = list(range(start + group_overlap, start + group_overlap + group_size))

        if max(group2_indices) >= total_trials:
            break  # Stop if the second group exceeds the total trials

        # Calculate participant averages for each group
        group1_data = numerical_data.iloc[:, group1_indices].mean(axis=1).dropna().values
        group2_data = numerical_data.iloc[:, group2_indices].mean(axis=1).dropna().values

        # Calculate mean trial number for the x-axis
        mean_trial_number = (np.mean(group1_indices) + np.mean(group2_indices)) / 2 + 1
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

kl_divergences, mean_trial_numbers = calculate_kl_divergence_shifted(data, group_size, group_overlap)

# Step 4: Generate scatter plot with regression line
def generate_scatter_plot(kl_values, mean_trial_numbers, group_size, group_overlap, save_folder='figures'):
    # Create the save folder if it doesn't exist
    os.makedirs(save_folder, exist_ok=True)

    # Create the title with group size and overlap
    title = f'KL Divergence (Group Size: {group_size}, Overlap: {group_overlap})'

    plt.figure(figsize=(10, 6))

    # Scatter plot for KL Divergence
    plt.scatter(mean_trial_numbers, kl_values, color='gray', alpha=0.7, edgecolor='black', zorder=3, label='KL Divergence')

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

# Call the scatter plot function
generate_scatter_plot(kl_divergences, mean_trial_numbers, group_size, group_overlap)
