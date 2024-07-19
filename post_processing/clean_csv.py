import csv

input_csv_file = 'C:/Users/Data acquisition/Desktop/Manual Data Processing/Session 02 (Isolated)/Darts/image_coordinates.csv'
output_csv_file = 'C:/Users/Data acquisition/Desktop/Manual Data Processing/Session 02 (Isolated)/Darts/cleaned.csv'


# Function to process the CSV file
def process_csv(input_file, output_file):
    with open(input_file, mode='r', newline='') as infile:
        reader = csv.reader(infile)
        rows = list(reader)

    # Remove the first row
    rows = rows[1:]

    # Remove '.png' from the end of the strings in the first column
    for row in rows:
        if row[0].endswith('.png'):
            row[0] = row[0][:-4]

    # Write the processed data to a new CSV file
    with open(output_file, mode='w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(rows)

# Call the function with the input and output file paths
process_csv(input_csv_file, output_csv_file)

print(f"Processed CSV has been saved to {output_csv_file}")
