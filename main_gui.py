import sys
import os
import datetime
import csv
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QLineEdit, QFormLayout, QFileDialog, QComboBox
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from gui.folder_dialog import FolderDialog
from gui.variable_display import VariableDisplay
from gui.traffic_light import TrafficLight
from common.constants import Constants, MetadataConstants, Components
from process import start_bodycam_left, start_bodycam_right, start_dartcam, start_gloves, start_eeg

def load_stylesheet(file_path):
    with open(file_path, "r") as file:
        return file.read()

class ProcessThread(QThread):
    update_traffic_light = pyqtSignal(str, bool)

    def __init__(self, component, trial_path, enabled):
        super(ProcessThread, self).__init__()
        self.component = component
        self.trial_path = trial_path
        self.enabled = enabled

    def run(self):
        if self.enabled:
            process_function = globals()[f"start_{self.component}"]
            process_function(self.trial_path)
            self.update_traffic_light.emit(self.component, False)

class ImageDisplayApp(QWidget):
    image_changed = pyqtSignal(str)
    def __init__(self, folder_path):
        super().__init__()
        self.setWindowTitle("Image Display App")
        self.setMinimumSize(500, 500)
        self.folder_path = folder_path
        self.current_image_index = 0
        self.image_paths = self.load_image_paths()
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.display_current_image()

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.image_label, alignment=Qt.AlignCenter)
        self.setLayout(layout)

    def load_image_paths(self):
        image_paths = []
        for filename in sorted(os.listdir(self.folder_path), key=lambda x: int(x.split('.')[0])):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                image_paths.append(os.path.join(self.folder_path, filename))
        return image_paths



    def display_current_image(self):
        if self.image_paths:
            pixmap = QPixmap(self.image_paths[self.current_image_index])
            pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio)
            self.image_label.setPixmap(pixmap)
            self.image_label.setFixedSize(150, 150)  # Set fixed size for the label
            self.image_changed.emit(os.path.basename(self.image_paths[self.current_image_index]))

    def next_image(self):
        if self.current_image_index < len(self.image_paths) - 1:
            self.current_image_index += 1
            self.display_current_image()

    def previous_image(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.display_current_image()

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
        
        #button layout
        buttonsLayout = QHBoxLayout()
        self.startBtn = QPushButton('Start', self)
        self.stopBtn = QPushButton('Stop', self)
        self.pauseBtn = QPushButton('Pause', self)

        # Add Next and Back buttons
        self.next_button = QPushButton("Next", self)
        self.next_button.clicked.connect(self.next_image)
        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(self.previous_image)

        # Add image name label
        self.image_name_label = QLabel(self)
        layout.addWidget(self.image_name_label)

        # Layout for the buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.next_button)

        # Set button size
        self.back_button.setFixedSize(80, 30)
        self.next_button.setFixedSize(80, 30)
        
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

        self.targetSelectionComboBox = QPushButton('Select Target Folder', self)
        self.targetSelectionComboBox.clicked.connect(self.select_target_folder)
        layout.addWidget(self.targetSelectionComboBox)

        self.update_metadata_constants(layout)
        layout.addLayout(self.traffic_light_layout)
        self.add_metadata_fields(layout)

        # next/previous button layout
        layout.addLayout(button_layout)

        # Set main widget
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        centralWidget.setMinimumSize(800, 600)
        self.setCentralWidget(centralWidget)

        self.imageDisplayApp = None

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
                writer.writerow(['Date', 'Participant ID', 'Handedness', 'Age', 'Gender', 'Trial Folder', 'Target', 'Comments'])
            
            # Write 
            selected_target_path = self.targetSelectionComboBox.currentData()
            selected_target = os.path.basename(selected_target_path) if selected_target_path else "None"
            writer.writerow([
                self.date_edit.text(),
                self.participant_id_edit.text(),
                self.handedness_edit.text(),
                self.age_edit.text(),
                self.gender_edit.text(),
                os.path.normpath(self.folderDialog.get_selected_folder()),
                selected_target,
                self.comments_edit.text()
            ])
    
    def start_batch(self):

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
        data_path = os.path.normpath(self.folderDialog.get_selected_folder())
        print(f"data_path : {data_path}")
        self.trial_path = common_utils.TrialManager.setup_trial(gui=True, data_path=data_path)

        for component, enabled in Components.ENABLED_COMPONENTS.items():
            if enabled:
                thread = ProcessThread(component, self.trial_path, enabled)
                thread.update_traffic_light.connect(self.update_traffic_lights)
                self.processes[component] = thread

        for key, thread in self.processes.items():
            thread.start()
            self.update_traffic_lights(key, True)
        
        # #TODO Adding this makes the GUI becomes unresponsive when the processes are running
        # TODO: need to fix this, since there might be too many zombie processes
        # for key, process in self.processes.items():
        #     process.join()
        #     print(key, "joined")
        #     self.update_traffic_lights(key, False)  # Set traffic light to red    

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

    def select_target_folder(self):
        folder_path = str(QFileDialog.getExistingDirectory(self, "Select Folder"))
        if folder_path:
            self.imageDisplayApp = ImageDisplayApp(folder_path)
            self.imageDisplayApp.show()
            # Connect the signal to the slot
            self.imageDisplayApp.image_changed.connect(self.update_image_name_label)

    def next_image(self):
        if self.imageDisplayApp:
            self.imageDisplayApp.next_image()

    def previous_image(self):
        if self.imageDisplayApp:
            self.imageDisplayApp.previous_image()

    def update_image_name_label(self, image_name):
        # Update the image name label
        self.image_name_label.setText(f"Current Image: {image_name}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainGUI()
    mainWin.show()
    sys.exit(app.exec_())
