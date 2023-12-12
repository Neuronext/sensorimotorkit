import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from folder_dialog import FolderDialog
from variable_display import VariableDisplay

class MainGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize UI components
        self.folderDialog = FolderDialog()
        self.variableDisplay = VariableDisplay()

        # Setup layout
        layout = QVBoxLayout()

        # Start, Stop, Pause buttons
        self.startBtn = QPushButton('Start', self)
        self.stopBtn = QPushButton('Stop', self)
        self.pauseBtn = QPushButton('Pause', self)

        # Connect buttons to functions
        self.startBtn.clicked.connect(self.start_process)
        self.stopBtn.clicked.connect(self.stop_process)
        self.pauseBtn.clicked.connect(self.pause_process)

        # Add components to layout
        layout.addWidget(self.startBtn)
        layout.addWidget(self.stopBtn)
        layout.addWidget(self.pauseBtn)
        layout.addWidget(self.folderDialog)
        layout.addWidget(self.variableDisplay)

        # Set main widget
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def start_process(self):
        print("Starting process")
        pass  # Implement process start logic

    def stop_process(self):
        print("Stopping process")
        pass  # Implement process stop logic

    def pause_process(self):
        print("Pausing process")
        pass  # Implement process pause logic

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainGUI()
    mainWin.show()
    sys.exit(app.exec_())
