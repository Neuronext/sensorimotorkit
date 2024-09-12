import os
import sys
import matplotlib.pyplot as plt
import csv
from matplotlib.patches import Ellipse
from matplotlib.widgets import Button

# Path setup (same as before)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.insert(0, parent_dir)

# Configuration variables
raw_data_format = "Old Format"
folder_to_process = "6-14 part 1"
dart_image_index = 3

unprocessed_folder_path = os.path.join("data/Raw Data/", raw_data_format, folder_to_process)

# Get list of all trials
trial_strings = os.listdir(unprocessed_folder_path)
trials_disordered = [int(trial_string) for trial_string in trial_strings]
trials = sorted(trials_disordered)

# Step 2: Check each trial for darts
dart_statuses = []
for trial in trials:
    trial_path = os.path.join(unprocessed_folder_path, str(trial))
    data_types = os.listdir(trial_path)
    if "dart" in data_types:
        dart_path = os.path.join(trial_path, "dart")
        dart_images = os.listdir(dart_path)
        dart_status = [trial, len(dart_images) > 0]
    else:
        dart_status = [trial, False]
    dart_statuses.append(dart_status)

# List to store all coordinates and missed statuses
all_coordinates = []

# Customizable ellipse parameters
ellipse_width = 68
ellipse_height = 48
ellipse_rotation = 330
ellipse_linewidth = 1

# Step 3: Cycle through dart images
def on_click(event):
    global click_count, dart_status, coordinates, fig, ax, ellipse, motion_cid, missed
    click_count += 1
    coordinates.append((event.xdata, event.ydata))
    if click_count == 1:
        if not missed:
            # Add an ellipse centered on the first click (dart location)
            ellipse = Ellipse((event.xdata, event.ydata), width=ellipse_width, height=ellipse_height,
                              angle=ellipse_rotation, edgecolor='r', facecolor='none', linewidth=ellipse_linewidth)
            ax.add_patch(ellipse)
            plt.draw()
            plt.title(f'Trial Number: {dart_status[0]} - move the target')
            motion_cid = fig.canvas.mpl_connect('motion_notify_event', on_motion)
        else:
            plt.title(f'Trial Number: {dart_status[0]} - select the target location')
    elif click_count == 2:
        if ellipse is not None:
            fig.canvas.mpl_disconnect(motion_cid)
            ellipse.remove()
            plt.draw()
        dart_x, dart_y = (coordinates[0][0], coordinates[0][1]) if not missed else ('NA', 'NA')
        target_x, target_y = coordinates[1][0], coordinates[1][1]
        all_coordinates.append([dart_status[0], dart_x, dart_y, target_x, target_y, missed])
        plt.close()

def on_motion(event):
    if ellipse is not None:
        ellipse.center = (event.xdata, event.ydata)
        plt.draw()

def missed_board(event):
    global missed, click_count
    missed = True
    click_count = 1  # Skip dart selection, directly move to target selection
    plt.title(f'Trial Number: {dart_status[0]} - select the target location')

click_count = 0
coordinates = []
ellipse = None
motion_cid = None
missed = False

for dart_status in dart_statuses:
    if dart_status[1]:
        dart_path = os.path.join(unprocessed_folder_path, str(dart_status[0]), "dart")
        dart_images = os.listdir(dart_path)
        
        if dart_image_index < len(dart_images):
            dart_image_path = os.path.join(dart_path, dart_images[dart_image_index])
        else:
            all_coordinates.append([dart_status[0], 'NA', 'NA', 'NA', 'NA', 'Images not present'])
            continue
        
        img = plt.imread(dart_image_path)
        
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.imshow(img)
        ax.axis('off')
        plt.title(f'Trial Number: {dart_status[0]} - select the dart')
        
        manager = plt.get_current_fig_manager()
        manager.window.setGeometry(0, 0, manager.window.width(), manager.window.height())
        
        click_count = 0
        coordinates = []
        ellipse = None
        motion_cid = None
        missed = False
        
        # Add missed button
        ax_button = plt.axes([0.81, 0.05, 0.1, 0.075])
        button = Button(ax_button, 'Missed')
        button.on_clicked(missed_board)
        
        cid = fig.canvas.mpl_connect('button_press_event', on_click)
        plt.show()
        fig.canvas.mpl_disconnect(cid)
    else:
        all_coordinates.append([dart_status[0], 'NA', 'NA', 'NA', 'NA', 'Images not present'])

# Ensure the directory exists
processed_data_path = os.path.join("data/Processed Data", folder_to_process)
os.makedirs(processed_data_path, exist_ok=True)

csv_file_path = os.path.join(processed_data_path, "Dart_unformatted.csv")

with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Trial Number", "Dart X", "Dart Y", "Target X", "Target Y", "Missed or Not Present"])
    
    # Function to safely convert values to float if possible, otherwise keep them as strings
    def safe_convert(value):
        try:
            return float(value)
        except (ValueError, TypeError):
            return str(value)
    
    # Process each row of coordinates
    for row in all_coordinates:
        safe_row = [safe_convert(item) for item in row]
        writer.writerow(safe_row)

print(f"Coordinates saved to {csv_file_path}")
