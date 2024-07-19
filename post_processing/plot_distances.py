import csv
import matplotlib.pyplot as plt
import numpy as np

input_csv_file = 'C:/Users/Data acquisition/Desktop/Manual Data Processing/Session 02 (Isolated)/Darts/distances.csv'
output_image_file = 'C:/Users/Data acquisition/Desktop/Manual Data Processing/Session 02 (Isolated)/Darts/distances.png'

# Function to read CSV and extract data for the plot
def read_csv_data(input_file):
    x_data = []
    y_data = []
    with open(input_file, mode='r') as infile:
        reader = csv.reader(infile)
        for row in reader:
            x_data.append(int(row[0]))  # Convert the first column to integers
            y_data.append(float(row[-1]))  # Assuming the last column is numeric

    # Sort the data based on x_data
    sorted_data = sorted(zip(x_data, y_data))
    x_data, y_data = zip(*sorted_data)
    
    return x_data, y_data

# Function to calculate the moving average
def moving_average(y_data, window_size=3):
    y_avg = []
    for i in range(len(y_data)):
        start = max(0, i - window_size)
        end = min(len(y_data), i + window_size + 1)
        y_avg.append(np.mean(y_data[start:end]))
    return y_avg

# Function to create and save the plot
def create_plot(x_data, y_data, output_file):
    plt.figure(figsize=(10, 6))
    
    # Plot the data points
    plt.scatter(x_data, y_data, color='b', label='Data Points')
    
    # Calculate and plot the moving average as a smoothed trend line
    y_avg = moving_average(y_data, window_size=3)
    plt.plot(x_data, y_avg, color='r', linestyle='--', label='Smoothed Trend Line')
    
    # Add dashed vertical lines every 10 units on the x-axis
    x_min = min(x_data)
    x_max = max(x_data)
    for i in range(x_min, x_max + 1, 10):
        plt.axvline(x=i, color='gray', linestyle='--', linewidth=0.5)
    
    # Add a dashed horizontal line at the average of all the points
    y_mean = np.mean(y_data)
    plt.axhline(y=y_mean, color='gray', linestyle='--', linewidth=0.5, label=f'Average ({y_mean:.2f})')

    # Calculate and plot the overall trend line
    coefficients = np.polyfit(x_data, y_data, 1)
    polynomial = np.poly1d(coefficients)
    overall_trend_line = polynomial(x_data)
    plt.plot(x_data, overall_trend_line, color='black', linestyle='-', linewidth=1, label='Overall Trend Line')
    
    plt.xlabel('Trial #')
    plt.ylabel('Error (Pixels)')
    plt.title('Dart Performance Over Time')
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()

# Read the CSV data
x_data, y_data = read_csv_data(input_csv_file)

# Create and save the plot
create_plot(x_data, y_data, output_image_file)

print(f"Graph with smoothed trend line and averages has been saved to {output_image_file}")
