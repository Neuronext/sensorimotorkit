import csv
import math

input_csv_file = 'C:/Users/Data acquisition/Desktop/Manual Data Processing/Session 02 (Isolated)/Darts/cleaned.csv'
output_csv_file = 'C:/Users/Data acquisition/Desktop/Manual Data Processing/Session 02 (Isolated)/Darts/distances.csv'

def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y1 - y2)**2)

# Function to process the CSV file
def process_csv(input_file, output_file):
    with open(input_file, mode='r', newline='') as infile:
        reader = csv.reader(infile)
        rows = list(reader)

    distances = []
    rows_with_distances = []

    # Process each row and calculate the distance
    for row in rows:
        x1, y1 = float(row[1]), float(row[2])
        x2, y2 = float(row[3]), float(row[4])
        if x1 == -1 and y1 == -1:
            distances.append(None)
        else:
            distance = calculate_distance(x1, y1, x2, y2)
            distances.append(distance)
            rows_with_distances.append(distance)
        row.append(distances[-1])

    # Find the highest distance value among valid distances
    max_distance = max(rows_with_distances)

    # Update rows with -1, -1 to have the max distance value
    for i, distance in enumerate(distances):
        if distance is None:
            rows[i][-1] = max_distance

    # Write the processed data to a new CSV file
    with open(output_file, mode='w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(rows)

# Call the function with the input and output file paths
process_csv(input_csv_file, output_csv_file)

print(f"Processed CSV with distances has been saved to {output_csv_file}")
