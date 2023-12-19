import sys
import multiprocessing
import os
import datetime
import csv
import time

# import PyQt5 modules
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QLineEdit, QLabel, QFormLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon


# import custom modules
from gui.folder_dialog import FolderDialog
from gui.variable_display import VariableDisplay
from gui.traffic_light import TrafficLight
from gui.custom_title_bar import CustomTitleBar
from common.constants import Constants, MetadataConstants, Components
from common import common_utils
from process import start_bodycam_left, start_bodycam_right, start_dartcam, start_gloves, start_eeg


def load_stylesheet(file_path):
    with open(file_path, "r") as file:
        return file.read()


class MainGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load and apply stylesheet
        stylesheet = load_stylesheet("gui/style.css")
        self.setStyleSheet(stylesheet)

        # Set window icon
        script_dir = os.path.dirname(os.path.realpath(__file__))
        self.icon_path = os.path.join(script_dir, 'assets', 'sensorimotorkit.png')
        self.setWindowIcon(QIcon(self.icon_path))
        self.setWindowTitle('Sensorimotor Kit')

        # Initialize UI components
        self.folderDialog = FolderDialog() 
        self.variableDisplay = VariableDisplay()
        layout = QVBoxLayout()

        # Start, Stop, Pause buttons
        self.trialCountLabel = QLabel(f"Trial: 0/{MetadataConstants.TRIALS_PER_BATCH}")
        
        buttonsLayout = QHBoxLayout()
        self.startBtn = QPushButton('Start', self)
        self.stopBtn = QPushButton('Stop', self)
        self.pauseBtn = QPushButton('Pause', self)
        
        self.traffic_light_layout = QHBoxLayout()        

        self.trafficLights = {}
        self.processes = {}

        for component, enabled in Components.ENABLED_COMPONENTS.items():
            if enabled:
                self.trafficLights[component] = TrafficLight()

        # Connect buttons to functions
        self.startBtn.clicked.connect(self.start_batch)
        self.stopBtn.clicked.connect(self.stop_batch)
        self.pauseBtn.clicked.connect(self.pause_batch)

        buttonsLayout.addWidget(self.startBtn)
        buttonsLayout.addWidget(self.stopBtn)
        buttonsLayout.addWidget(self.pauseBtn)
        

        # add traffic lights to layout
        for key, light in self.trafficLights.items():    
            label = QLabel(key.replace('_', ' ').title()) 
            label.setAlignment(Qt.AlignCenter)  
            self.traffic_light_layout.addWidget(label)
            self.traffic_light_layout.addWidget(light)

        # Add components to layout
        layout.addWidget(self.trialCountLabel)
        layout.addLayout(buttonsLayout)
        layout.addWidget(self.folderDialog)

        self.update_metadata_constants(layout)
        layout.addLayout(self.traffic_light_layout)
        self.add_metadata_fields(layout)

        # Set main widget
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        centralWidget.setMinimumSize(600, 400)
        self.setCentralWidget(centralWidget)

    #TODO remove variable display function
    def update_metadata_constants(self, layout):
        form_layout = QFormLayout()
        
        # currently only acquire time is a variable, can add more
        self.acquire_time = QLineEdit(str(Constants.ACQUIRE_TIME))
        form_layout.addRow("Acquire Time:", self.acquire_time)
        layout.addLayout(form_layout)


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
        file_exists = os.path.isfile(MetadataConstants.METADATA_FILE_NAME)
        
        with open(MetadataConstants.METADATA_FILE_NAME, mode='a', newline='\n') as file:
            writer = csv.writer(file)
            
            # if file doesn't exist, write headers
            if not file_exists:
                writer.writerow(['Date', 'Participant ID', 'Handedness', 'Age', 'Gender', 'Trial Folder' 'Comments'])
            
            # Write data
            writer.writerow([
                self.date_edit.text(),
                self.participant_id_edit.text(),
                self.handedness_edit.text(),
                self.age_edit.text(),
                self.gender_edit.text(),
                os.path.normpath(self.folderDialog.get_selected_folder()),
                self.comments_edit.text()
            ])
    
    def start_batch(self):

        #TODO use the self.acquire_time to get the acquire time, convert to int
        for trial in range(MetadataConstants.TRIALS_PER_BATCH): 
            self.trialCountLabel.setText(f"Trial: {trial+1}/{MetadataConstants.TRIALS_PER_BATCH}")
            QApplication.processEvents()
            self.run_trial()
            # sleep for 1 second between trials
            time.sleep(MetadataConstants.SLEEP_TIME_BETWEEN_TRIALS)

        # Reset the label after the batch is completed
        self.trialCountLabel.setText(f"Trial: 0/{MetadataConstants.TRIALS_PER_BATCH}")

        # Add metadata to csv
        print("Adding metadata to csv")
        self.append_metadata_to_csv()

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

    def run_trial(self):
        # Run the main trial process
        
        data_path = os.path.normpath(self.folderDialog.get_selected_folder())
        print(f"data_path : {data_path}")
        trial_path = common_utils.TrialManager.setup_trial(gui=True, data_path=data_path)


        for component, enabled in Components.ENABLED_COMPONENTS.items():
            if enabled:
                process_function = globals()[f"start_{component}"] 
                self.processes[component] = multiprocessing.Process(target=process_function, args=(trial_path,))
                
        for key, process in self.processes.items():
            process.start()
            self.update_traffic_lights(key, True)  # Set traffic light to green

        #TODO Adding this makes the GUI becomes unresponsive when the processes are running
        for key, process in self.processes.items():
            process.join()
            print(key, "joined")
            self.update_traffic_lights(key, False)  # Set traffic light to red        

    def update_traffic_lights(self, process_name, is_running):
        if is_running:
            # print("updating traffic light to green")
            self.trafficLights[process_name].updateColor.emit('green')
            self.trafficLights[process_name].status = 'green'
        else:
            # print("updating traffic light to red")
            self.trafficLights[process_name].updateColor.emit('red')
            self.trafficLights[process_name].status = 'red'
        QApplication.processEvents()
      

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainGUI()
    mainWin.show()
    sys.exit(app.exec_())
