import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import csv

# Directory containing images
image_directory = 'C:/Users/Data acquisition/Desktop/Manual Data Processing/Session 02 (Isolated)/Darts'

# CSV file to save coordinates
csv_file = 'C:/Users/Data acquisition/Desktop/Manual Data Processing/Session 02 (Isolated)/Darts/image_coordinates.csv'

# List to hold image file names and their coordinates
image_data = []

# Global variables to manage state
current_image_index = 0
click_stage = 0  # 0 for dart click, 1 for target click
current_coordinates = [-1, -1, -1, -1]

def update_instruction_label():
    images_left = len(image_files) - current_image_index
    if click_stage == 0:
        instruction_label.config(text=f"Click on the dart ({images_left} images left)")
    else:
        instruction_label.config(text=f"Click the target ({images_left} images left)")

def on_image_click(event):
    global click_stage, current_coordinates

    if click_stage == 0:
        current_coordinates[0] = event.x
        current_coordinates[1] = event.y
        click_stage = 1
    elif click_stage == 1:
        current_coordinates[2] = event.x
        current_coordinates[3] = event.y
        save_data()
        load_next_image()

    update_instruction_label()

def on_button_click():
    global click_stage, current_coordinates

    if click_stage == 0:
        current_coordinates[0] = -1
        current_coordinates[1] = -1
        click_stage = 1
    else:
        current_coordinates[2] = -1
        current_coordinates[3] = -1
        save_data()
        load_next_image()

    update_instruction_label()

def save_data():
    global current_coordinates, current_image_index

    image_file = image_files[current_image_index]
    image_data.append([image_file, *current_coordinates])
    current_coordinates = [-1, -1, -1, -1]

def load_next_image():
    global current_image_index, click_stage

    current_image_index += 1
    click_stage = 0
    if current_image_index < len(image_files):
        display_image(image_files[current_image_index])
    else:
        save_to_csv()
        root.quit()

def display_image(image_file):
    image = Image.open(os.path.join(image_directory, image_file))

    # Resize image to twice its original size
    image = image.resize((round(image.width * 1.5), round(image.height * 1.5)), Image.ANTIALIAS)

    photo = ImageTk.PhotoImage(image)
    image_label.config(image=photo)
    image_label.image = photo

def save_to_csv():
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Image", "Dart X", "Dart Y", "Target X", "Target Y"])
        writer.writerows(image_data)

# Create the main window
root = tk.Tk()
root.title("Image Click Recorder")

# Add an instruction label
instruction_label = ttk.Label(root, text="")
instruction_label.pack(pady=10)

# Create a label to display the images
image_label = ttk.Label(root)
image_label.pack(pady=10)
image_label.bind("<Button-1>", on_image_click)

# Add a button for the dart click option
button = ttk.Button(root, text="Skip Dart Click", command=on_button_click)
button.pack(pady=10)

# Get the list of image files
image_files = [f for f in os.listdir(image_directory) if os.path.isfile(os.path.join(image_directory, f))]

# Display the first image
if image_files:
    display_image(image_files[0])
    update_instruction_label()
else:
    print("No images found in the specified directory.")
    root.quit()

# Run the application
root.mainloop()
