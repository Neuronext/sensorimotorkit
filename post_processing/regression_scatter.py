import tkinter as tk
import pandas as pd
from scipy.stats import linregress


# Step 1: Load data from CSV file
data = []
try:
    # Replace 'summary.csv' with the correct path to your CSV file
    with open('summary.csv', 'r') as file:
        data = pd.read_csv(file)  # Directly read CSV into a pandas DataFrame
except Exception as e:
    print(f"An error occurred while reading the CSV file: {e}")

def group_params_gui():
    def return_values():
        global group_params
        size = group_size_entry.get()
        overlap = group_overlap_entry.get()
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

def group_data(data, group_names):
    df = pd.DataFrame(data[1:], columns=data[0])

    # Converts trials that were not a miss or missing images to numbers
    numerical_data = df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')

    # Determine which participants have values in all groups
    valid_participants = set(numerical_data.index)  # Start with all participants

    # First pass: Identify participants with no values for any specific group
    for group in group_names:
        indices = [int(x)-1 for x in group.split(" ")]
        for part_index, row in numerical_data.iterrows():
            part_group_values = [row[index] for index in indices if pd.notna(row[index]) and isinstance(row[index], (int, float))]
            # If no values for the group, exclude this participant
            if not part_group_values:
                valid_participants.discard(part_index)

    # Second pass: Calculate regression slopes for valid participants
    group_data = []
    for group in group_names:
        name = group_names[group]
        indices = [int(x)-1 for x in group.split(" ")]
        slopes = []
        for part_index, row in numerical_data.iterrows():
            if part_index not in valid_participants:
                continue  # Skip participants who have no values in any group
            
            # Prepare data points (trial number, distance) only with valid numeric values
            part_group_values = [(row[index], index+1) for index in indices if pd.notna(row[index]) and isinstance(row[index], (int, float))]
            
            if len(part_group_values) >= 2:  # Ensure at least two data points are available for regression
                y_values, x_values = zip(*part_group_values)
                slope, intercept, r_value, p_value, std_err = linregress(x_values, y_values)
                slopes.append(slope)
            else:
                # Handle cases with fewer than two points, maybe append None or another placeholder
                slopes.append(None)

        group_data.append((name, slopes))

    return group_data