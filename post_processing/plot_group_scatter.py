import csv
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

# Step 1: Set the regression option at the start
regression_option = 'pentic'  # 'best_fit', 'linear', 'quadratic', 'cubic', 'quartic', 'pentic'

# Step 2: Load the CSV file
data = []
try:
    with open('data/summary_centered.csv', 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
except Exception as e:
    print(f"An error occurred: {e}")

# Step 3: Process the data to calculate the average for each trial
if data:
    trial_count = len(data[0]) - 1  # Assuming first column is the participant label
    averages = []

    for trial in range(1, trial_count + 1):
        trial_values = []
        for row in data[1:]:  # Skip the first row (labels)
            try:
                value = float(row[trial])
                trial_values.append(value)
            except ValueError:
                # Ignore non-numerical values
                continue

        if trial_values:
            trial_avg = np.mean(trial_values)
            averages.append(trial_avg)
        else:
            averages.append(np.nan)  # Handle cases where no valid numbers were found

    # Step 4: Plot the scatter plot with y-axis starting at 0
    plt.figure(figsize=(12, 6))  # Make the figure slightly wider
    plt.scatter(range(1, trial_count + 1), averages, color='blue', alpha=0.7)
    plt.title('Average Distance per Trial')
    plt.xlabel('Trial Number')
    plt.ylabel('Average Distance')
    plt.ylim(bottom=-75)  # Ensure y-axis starts at 0
    plt.grid(True)

    # Prepare data for regression
    trial_numbers = np.arange(1, trial_count + 1)
    valid_averages = np.array(averages)
    valid_trials = trial_numbers[~np.isnan(valid_averages)]
    valid_averages = valid_averages[~np.isnan(valid_averages)]

    # Function to find local minima, maxima, and inflection points
    def find_extrema(coeffs, degree):
        # Derivatives
        first_derivative = np.polyder(coeffs, 1)
        second_derivative = np.polyder(coeffs, 2)

        # Find roots of the first derivative for local minima and maxima
        local_extrema_x = np.roots(first_derivative)
        local_extrema_y = np.polyval(coeffs, local_extrema_x)

        # Find roots of the second derivative for inflection points (only for cubic and above)
        inflection_points_x = np.roots(second_derivative) if degree >= 3 else np.array([])
        inflection_points_y = np.polyval(coeffs, inflection_points_x) if degree >= 3 else np.array([])

        # Filter out complex numbers (keep only real values within trial range)
        local_extrema_x = local_extrema_x[np.isreal(local_extrema_x)].real
        local_extrema_y = local_extrema_y[np.isreal(local_extrema_y)].real
        inflection_points_x = inflection_points_x[np.isreal(inflection_points_x)].real
        inflection_points_y = inflection_points_y[np.isreal(inflection_points_y)].real

        # Keep points within the trial number range
        mask_extrema = (local_extrema_x >= 1) & (local_extrema_x <= trial_count)
        local_extrema_x = local_extrema_x[mask_extrema]
        local_extrema_y = local_extrema_y[mask_extrema]

        mask_inflection = (inflection_points_x >= 1) & (inflection_points_x <= trial_count)
        inflection_points_x = inflection_points_x[mask_inflection]
        inflection_points_y = inflection_points_y[mask_inflection]

        return (local_extrema_x, local_extrema_y, inflection_points_x, inflection_points_y)

    # Step 5: Perform the chosen regression
    if len(valid_trials) > 1:
        if regression_option == 'linear':
            # Linear Regression Calculation
            slope, intercept, r_value, p_value, std_err = stats.linregress(valid_trials, valid_averages)
            regression_line = slope * trial_numbers + intercept
            plt.plot(trial_numbers, regression_line, color='red', linestyle='--', label='Linear Regression')

            # Indicate slope and significance
            significance = 'n.s'
            if p_value < 0.001:
                significance = '***'
            elif p_value < 0.01:
                significance = '**'
            elif p_value < 0.05:
                significance = '*'

            plt.text(0.60, 0.05, f'Linear Component: {slope:.7f}, Significance: {significance}', 
                     transform=plt.gca().transAxes, fontsize=10, verticalalignment='bottom', horizontalalignment='left')

        elif regression_option in ['quadratic', 'cubic', 'quartic', 'pentic']:
            # Determine the degree of polynomial for the chosen option
            degree = {'quadratic': 2, 'cubic': 3, 'quartic': 4, 'pentic': 5}[regression_option]
            coeffs = np.polyfit(valid_trials, valid_averages, degree)
            regression_line = np.polyval(coeffs, trial_numbers)
            plt.plot(trial_numbers, regression_line, linestyle='--', label=f'{regression_option.capitalize()} Regression')

            # Find local minima, maxima, and inflection points
            local_extrema_x, local_extrema_y, inflection_points_x, inflection_points_y = find_extrema(coeffs, degree)

            # Plot local minima and maxima
            plt.plot(local_extrema_x, local_extrema_y, 'o', color='black', label='Local Min/Max')

            # Plot inflection points as arrows (only for cubic and above)
            if degree >= 3:
                for ix, iy in zip(inflection_points_x, inflection_points_y):
                    # Determine the direction of the inflection
                    second_derivative_at_inflection = np.polyval(np.polyder(coeffs, 2), ix)
                    arrow_direction = 1 if second_derivative_at_inflection > 0 else -1
                    plt.annotate('', xy=(ix, iy), xytext=(ix, iy + arrow_direction * 0.5),
                                 arrowprops=dict(facecolor='magenta', shrink=0.05, width=1.5))

            # Calculate significance
            model = np.poly1d(coeffs)
            residuals = valid_averages - model(valid_trials)
            ss_res = np.sum(residuals ** 2)
            ss_tot = np.sum((valid_averages - np.mean(valid_averages)) ** 2)
            r_squared = 1 - (ss_res / ss_tot)
            f_value = (r_squared / (1 - r_squared)) * ((len(valid_averages) - degree) / degree)
            p_value = 1 - stats.f.cdf(f_value, degree, len(valid_averages) - degree - 1)

            significance = 'n.s'
            if p_value < 0.001:
                significance = '***'
            elif p_value < 0.01:
                significance = '**'
            elif p_value < 0.05:
                significance = '*'

            # Display regression components with significance
            text_pos_y = 0.25
            # Display components from constant to the highest order
            for i in range(degree, -1, -1):
                component_name = ["Constant", "Linear", "Quadratic", "Cubic", "Quartic", "Pentic"][i]
                plt.text(0.7, text_pos_y, f'{component_name} Component: {coeffs[degree - i]:.7f} {significance}',
                         transform=plt.gca().transAxes, fontsize=10, verticalalignment='bottom', horizontalalignment='left')
                text_pos_y -= 0.05

        else:
            # Default: Line of Best Fit Calculation
            best_fit_params = np.polyfit(valid_trials, valid_averages, 1)
            best_fit_line = np.polyval(best_fit_params, trial_numbers)
            plt.plot(trial_numbers, best_fit_line, color='red', linestyle='--', label='Line of Best Fit')

        # Add a key for significance
        plt.text(1.01, 0.85, '*** p < 0.001\n** p < 0.01\n* p < 0.05\nn.s not significant', 
                 transform=plt.gca().transAxes, fontsize=8)

    # Step 6: Save the graph to a specified location with a specified name
    save_path = 'data/Graphs/Scatter w Reg (5).png'  # Change this to your desired path and filename
    plt.legend(loc='lower left')  # Legend at the bottom left corner
    plt.savefig(save_path, bbox_inches='tight')
    plt.show()
