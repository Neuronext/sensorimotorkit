import sys
import multiprocessing
import os
import datetime
import csv

# import PyQt5 modules
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QLineEdit, QLabel, QFormLayout
from PyQt5.QtCore import Qt

# import custom modules
from gui.folder_dialog import FolderDialog
from gui.variable_display import VariableDisplay
from gui.traffic_light import TrafficLight

from acquire_data.gloves import gloves
from acquire_data.eeg import eeg
from acquire_data.emg import emg
from acquire_data.images import body_cam, dart_cam
from common import common_utils
from common.constants import Paths, Constants, MetadataConstants
from feature_extraction.apply_tracking import process_body_cam_images
from test_process import start_bodycam_left, start_bodycam_right, start_dartcam, start_gloves, start_eeg, capture_board # using test_process.py for now


class MainGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize UI components
        self.folderDialog = FolderDialog() #TODO: change this because it needs to be asked per trail
        self.variableDisplay = VariableDisplay()

        # Setup layout
        layout = QVBoxLayout()

        # Start, Stop, Pause buttons
        self.startBtn = QPushButton('Start', self)
        self.stopBtn = QPushButton('Stop', self)
        self.pauseBtn = QPushButton('Pause', self)
        self.h_layout = QHBoxLayout()

        self.trafficLights = {
            'bodycam_left': TrafficLight(),
            'bodycam_right': TrafficLight(),
            'dartcam': TrafficLight(),
            'gloves': TrafficLight(),
            'eeg': TrafficLight(),
        }

        # Connect buttons to functions
        self.startBtn.clicked.connect(self.start_batch)
        self.stopBtn.clicked.connect(self.stop_batch)
        self.pauseBtn.clicked.connect(self.pause_batch)

        # Add components to layout
        layout.addWidget(self.startBtn)
        layout.addWidget(self.stopBtn)
        layout.addWidget(self.pauseBtn)
        layout.addWidget(self.folderDialog)
        layout.addWidget(self.variableDisplay)
        
        # add traffic lights to layout
        for key, light in self.trafficLights.items():    
            label = QLabel(key.replace('_', ' ').title()) 
            label.setAlignment(Qt.AlignCenter)  
            self.h_layout.addWidget(label)
            self.h_layout.addWidget(light)
        
        layout.addLayout(self.h_layout)
        
        self.add_metadata_fields(layout)

        # Set main widget
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        centralWidget.setMinimumSize(600, 400)
        self.setCentralWidget(centralWidget)

    def add_metadata_fields(self, layout):
        form_layout = QFormLayout()

        # Metadata fields
        self.date_edit = QLineEdit(datetime.datetime.now().strftime("%Y-%m-%d"))
        self.participant_id_edit = QLineEdit()
        self.handedness_edit = QLineEdit()
        self.age_edit = QLineEdit()
        self.gender_edit = QLineEdit()
        self.comments_edit = QLineEdit()

        form_layout.addRow("Date:", self.date_edit)
        form_layout.addRow("Participant ID:", self.participant_id_edit)
        form_layout.addRow("Handedness:", self.handedness_edit)
        form_layout.addRow("Age:", self.age_edit)
        form_layout.addRow("Gender:", self.gender_edit)
        form_layout.addRow("Comments:", self.comments_edit)

        # Add the form layout to the main layout
        layout.addLayout(form_layout)


    def append_metadata_to_csv(self):
        # Check if file exists, and whether we need to write headers
        file_exists = os.path.isfile('metadata.csv')
        
        with open('metadata.csv', mode='a', newline='\n') as file:
            writer = csv.writer(file)
            
            # Write header if file doesn't exist
            if not file_exists:
                writer.writerow(['Date', 'Participant ID', 'Handedness', 'Age', 'Gender', 'Comments'])
            
            # Write data
            writer.writerow([
                self.date_edit.text(),
                self.participant_id_edit.text(),
                self.handedness_edit.text(),
                self.age_edit.text(),
                self.gender_edit.text(),
                self.comments_edit.text()
            ])
    
    def start_batch(self):
        trial_path = self.folderDialog.get_selected_folder()
        for _ in range(MetadataConstants.TRIALS_PER_BATCH): 
            self.run_trial(trial_path)

    def stop_batch(self):
        # To stop the batch, terminate all running processes
        for key, process in self.processes.items():
            if process.is_alive():
                process.terminate()
                self.update_traffic_lights(key, False)

    def pause_batch(self):
        # To pause the batch, suspend all running processes
        for _, process in self.processes.items():
            process.suspend()

    def run_trial(self, trial_path):
        # Run the main trial process
        self.processes = {
            "bodycam_left" : multiprocessing.Process(target=start_bodycam_left, args=(trial_path,)),
            "bodycam_right" : multiprocessing.Process(target=start_bodycam_right, args=(trial_path,)),
            "dartcam" : multiprocessing.Process(target=start_dartcam, args=(trial_path,)),
            "gloves" : multiprocessing.Process(target=start_gloves, args=(trial_path,)),
            "eeg" : multiprocessing.Process(target=start_eeg, args=(trial_path,))
        }
        for key, process in self.processes.items():
            process.start()
            self.update_traffic_lights(key, True)  # Set traffic light to green

        for key, process in self.processes.items():
            process.join()
            print(key, "joined")
            self.update_traffic_lights(key, False)  # Set traffic light to red
        
        print("Adding metadata to csv")
        self.append_metadata_to_csv()

    def update_traffic_lights(self, process_name, is_running):
        if is_running:
            print("updating traffic light to green")
            self.trafficLights[process_name].updateColor.emit('green')
            self.trafficLights[process_name].status = 'green'
        else:
            print("updating traffic light to red")
            self.trafficLights[process_name].updateColor.emit('red')
            self.trafficLights[process_name].status = 'red'
      

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainGUI()
    mainWin.show()
    sys.exit(app.exec_())
