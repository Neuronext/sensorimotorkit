import sys
import multiprocessing
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from gui.folder_dialog import FolderDialog
from gui.variable_display import VariableDisplay
from gui.traffic_light import TrafficLight



# import custom modules
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

        self.trafficLights = {
            'bodycam_left': TrafficLight(),
            'bodycam_right': TrafficLight(),
            'dartcam': TrafficLight(),
            'gloves': TrafficLight(),
            'eeg': TrafficLight(),
            'emg': TrafficLight(),
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
        for light in self.trafficLights.values():
            layout.addWidget(light)

        # Set main widget
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def start_batch(self):
        for _ in range(MetadataConstants.TRIALS_PER_BATCH): 
            trial_path = self.folderDialog.get_selected_folder()
            self.run_trial(trial_path)

    def stop_batch(self):
        # To stop the batch, terminate all running processes
        for process in self.processes:
            process.terminate()

    def pause_batch(self):
        # To pause the batch, suspend all running processes
        for process in self.processes:
            process.suspend()

    def run_trial(self, trial_path):
        # Run the main trial process
        self.processes = [
            multiprocessing.Process(target=start_bodycam_left, args=(trial_path,)),
            multiprocessing.Process(target=start_bodycam_right, args=(trial_path,)),
            multiprocessing.Process(target=start_dartcam, args=(trial_path,)),
            multiprocessing.Process(target=start_gloves, args=(trial_path,)),
            multiprocessing.Process(target=start_eeg, args=(trial_path,))
        ]
        for process in self.processes:
            process.start()
            self.update_traffic_lights(process, True)  # Set traffic light to green

        for process in self.processes:
            process.join()
            self.update_traffic_lights(process, False)  # Set traffic light to red

    def update_traffic_lights(self, process, is_running):
        # Update the traffic light based on process status
        # Map each process to its corresponding traffic light
        traffic_light = self.trafficLights[process.name]
        if is_running:
            traffic_light.set_green()
        else:
            traffic_light.set_red()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainGUI()
    mainWin.show()
    sys.exit(app.exec_())
