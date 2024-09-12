#Step 1: Load the CSV file
import csv
data = []
try:
    with open('summary.csv', 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
except Exception as e:
    print(f"An error occurred: {e}")

#Step 2: Decide figure settings
import tkinter as tk
from tkinter import ttk
#Step 2a: Group parameters
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



#Step 2d: Group selection
def group_selection_gui():
    group_selection_root = tk.Tk()
    group_selection_root.title("Group Selection GUI")

    dropdown_vars = []  # List to store the StringVar objects
    dropdown_rows = []  # List to store the row frames for dropdowns

    groups = []
    start = 1
    while start <= 180:
        end = min(start + int(group_params_final[0]) - 1, 180)
        groups.append(list(range(start, end + 1)))
        start += int(group_params_final[0]) - int(group_params_final[1])

    def add_comparison_row():
        # Add a new row of dropdowns
        row_frame = tk.Frame(group_selection_root)
        row_frame.pack(fill="x", pady=5)

        var1 = tk.StringVar(value="Select Group 1")
        var2 = tk.StringVar(value="Select Group 2")
        dropdown_vars.append([var1, var2])

        dropdown1 = ttk.Combobox(row_frame, textvariable=var1, values=groups)
        dropdown1.pack(side="left", padx=5)

        dropdown2 = ttk.Combobox(row_frame, textvariable=var2, values=groups)
        dropdown2.pack(side="left", padx=5)

        remove_btn = tk.Button(row_frame, text="Remove", command=lambda: remove_comparison_row(row_frame, [var1, var2]))
        remove_btn.pack(side="left", padx=5)

        dropdown_rows.append(row_frame)

    def remove_comparison_row(row, vars_to_remove):
        # Remove a specific row of dropdowns
        dropdown_rows.remove(row)
        dropdown_vars.remove(vars_to_remove)
        row.destroy()

    def return_dropdown_values():
        global selected_values
        selected_values = [dropdown3.get(),[[var[0].get(), var[1].get()] for var in dropdown_vars]]
        group_selection_root.destroy()

    Comparison = tk.StringVar(value="Select Analysis Method")
    comparison_types = ['Paired T-Test:2-tails', 'Paired T-Test:1-tail', 'Independent T-Test:2-tails', 'Independent T-Test:1-tail']
    dropdown3 = ttk.Combobox(group_selection_root, textvariable=Comparison, values=comparison_types, state='readonly')
    dropdown3.pack(side="left", padx=5)

    add_comparison_btn = tk.Button(group_selection_root, text="Add Comparison", command=add_comparison_row)
    add_comparison_btn.pack(pady=5)

    return_values_btn = tk.Button(group_selection_root, text="Submit Comparisons", command=return_dropdown_values)
    return_values_btn.pack(pady=5)

    group_selection_root.mainloop()

    return selected_values

groups_final = group_selection_gui()

#Step 3: Run the analyses
#3a: Get group names and figure title
import pandas as pd
from scipy.stats import ttest_rel

def groups_title_gui(groups):
    # Converts location data to a DataFrame
    df = pd.DataFrame(data[1:], columns=data[0])

    # Extract the comparison groups
    comparisons = groups[1]

    # Turns the chosen groups into a string to be passed to the analysis
    unique_groups = sorted(set(group for comparison in comparisons for group in comparison))

    # Prepare a dictionary to hold group names and the figure title
    group_names_dict = {}
    figure_title = ""
    
    # Initialize list to store the groups being compared
    comparison_names = []

    # Creates a GUI to get the group names and figure title
    def get_group_names():
        entry_vars = {}

        def on_submit():
            nonlocal figure_title
            for group in unique_groups:
                group_names_dict[group] = entry_vars[group].get()
            figure_title = title_var.get()
            root.destroy()

        root = tk.Tk()
        root.title("Group Naming")

        # Create entry for the figure title
        title_label = ttk.Label(root, text="Enter the title of the figure:")
        title_label.pack(padx=10, pady=5)
        title_var = tk.StringVar()
        title_entry = ttk.Entry(root, textvariable=title_var)
        title_entry.pack(padx=10, pady=5)

        # Create a label and entry for each unique group
        for group in unique_groups:
            label = ttk.Label(root, text=f"Enter a name for group ({group}):")
            label.pack(padx=10, pady=5)
            entry_var = tk.StringVar()
            entry = ttk.Entry(root, textvariable=entry_var)
            entry.pack(padx=10, pady=5)
            entry_vars[group] = entry_var

        # Submit button
        submit_button = ttk.Button(root, text="Submit", command=on_submit)
        submit_button.pack(pady=20)

        root.mainloop()

    # Collect group names and figure title via GUI
    get_group_names()

    # Create the list of lists for group comparisons
    for comparison in comparisons:
        comparison_names.append([group_names_dict[group] for group in comparison])

    return figure_title, group_names_dict, comparison_names


title, group_names, comparisons = groups_title_gui(groups_final)

#3b: Group and average data
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

    # Second pass: Calculate averages only for valid participants
    group_data = []
    for group in group_names:
        name = group_names[group]
        indices = [int(x)-1 for x in group.split(" ")]
        group_averages = []
        for part_index, row in numerical_data.iterrows():
            if part_index not in valid_participants:
                continue  # Skip participants who have no values in any group
            
            part_group_values = [row[index] for index in indices if pd.notna(row[index]) and isinstance(row[index], (int, float))]
            
            if part_group_values:
                group_averages.append(sum(part_group_values) / len(part_group_values))

        group_data.append((name, group_averages))

    return group_data

averaged_data = group_data(data, group_names)

#3c: Perform Analyses
def ttest_1(data, comparisons):
    p_values = []
    for comparison in comparisons:
        group1 = comparison[0]
        group2 = comparison[1]
        group1_data = []
        group2_data = []
        for group in data:
            name = group[0]
            if name == group1:
                group1_data = group[1]
            elif name == group2:
                group2_data = group[1]
        t_stat, p_value = ttest_rel(group1_data, group2_data)
        p_values.append(p_value)
    return p_values

ps = ttest_1(averaged_data, comparisons)

#Step 4: Generate the figure
import matplotlib.pyplot as plt
import numpy as np

def generate_figure(title, data, comparisons, p_values, save_folder):
    # Prepare data for plotting
    group_names = [group[0] for group in data]
    grouped_data = [group[1] for group in data]

    # Calculate means and standard deviations for all groups
    stats = {group: (np.mean(values), np.std(values)) for group, values in zip(group_names, grouped_data)}

    # Increase figure size
    fig, ax = plt.subplots(figsize=(10, 6))  # Increased size for better visualization

    # Initialize position tracking for boxplots
    positions = []
    offset = 0

    # Plot box and whisker plots for each group
    x_labels = []
    for i, (group1, group2) in enumerate(comparisons):
        group1_index = group_names.index(group1)
        group2_index = group_names.index(group2)

        # Plot boxplots without outliers and with transparency
        ax.boxplot(grouped_data[group1_index], positions=[offset], widths=0.8, showfliers=False, patch_artist=True,
                   boxprops=dict(facecolor='grey', alpha=0.5))
        ax.boxplot(grouped_data[group2_index], positions=[offset + 1], widths=0.8, showfliers=False, patch_artist=True,
                   boxprops=dict(facecolor='grey', alpha=0.5))

        # Append labels without means and standard deviations
        x_labels.extend([group1, group2])

        # Record positions for connecting lines
        positions.append((offset, offset + 1))
        offset += 2.5  # Adding a gap between each pair

    # Plot lines only for each comparison at the correct x positions
    for i, (group1, group2) in enumerate(comparisons):
        group1_index = group_names.index(group1)
        group2_index = group_names.index(group2)

        # Get corresponding data for the groups in this comparison
        data1 = grouped_data[group1_index]
        data2 = grouped_data[group2_index]

        # Ensure data lengths are equal
        min_length = min(len(data1), len(data2))
        data1, data2 = data1[:min_length], data2[:min_length]

        # Retrieve x positions for the current comparison
        x_pos1, x_pos2 = positions[i]

        # Plot lines connecting each comparison at correct x positions
        for j in range(min_length):
            ax.plot([x_pos1, x_pos2], [data1[j], data2[j]], color='gray', linestyle='-', alpha=0.5, zorder=1)

    # Adding significance text without bars
    for (pos1, pos2), p_value in zip(positions, p_values):
        x_center = (pos1 + pos2) / 2
        y_max = max(max(grouped_data[group_names.index(comparisons[i][0])]),
                    max(grouped_data[group_names.index(comparisons[i][1])]))
        line_height = y_max + 0.15 * y_max  # Increased space between data and significance text

        # Determine significance text
        if p_value < 0.001:
            stars = '***'
        elif p_value < 0.01:
            stars = '**'
        elif p_value < 0.05:
            stars = '*'
        else:
            stars = 'n.s.'

        # Add significance text
        ax.text(x_center, line_height, stars, ha='center')

    # Customize plot
    ax.set_title(title, pad=40)  # Increased padding for title
    ax.set_xlabel('Group')
    ax.set_ylabel('Distance')
    ax.set_xticks([pos for pair in positions for pos in pair])
    ax.set_xticklabels(x_labels, rotation=45, ha='right')  # Rotate labels to avoid overlap

    # Set y-axis to start at 0
    ax.set_ylim(0)

    # Add significance threshold information to the right
    plt.text(1.02, 0.5, 'Significance:\n*** p < 0.001\n** p < 0.01\n* p < 0.05\nn.s. p >= 0.05',
             transform=ax.transAxes, verticalalignment='center', fontsize=10, bbox=dict(facecolor='white', alpha=0.8))

    # Create table with means and standard deviations, separate from the plot
    table_data = [[group, f"{mean:.2f}", f"{std:.2f}"] for group, (mean, std) in stats.items()]
    table = plt.table(cellText=table_data, colLabels=['Group', 'Mean', 'SD'], cellLoc='center', 
                      loc='bottom', bbox=[0.2, -0.8, 0.6, 0.45], fontsize=12)  # Made the table larger and lower

    # Adjust cell alignment
    for key, cell in table.get_celld().items():
        if key[1] == 0:  # First column
            cell.set_text_props(ha='right')  # Set alignment to the right for the first column
        else:  # Other columns
            cell.set_text_props(ha='center')  # Set alignment to center for the rest
        cell.set_height(0.05)  # Set cell height as needed

    # Adjust plot layout
    plt.subplots_adjust(bottom=0.45)  # Increased bottom margin to separate the table and figure further

    # Save the figure
    plt.savefig(f"{save_folder}/{title}.png", bbox_inches='tight')
    plt.close()




folder = 'data/Graphs'

generate_figure(title, averaged_data, comparisons, ps, folder)

