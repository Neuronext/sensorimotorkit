from PyQt5.QtWidgets import QWidget, QPushButton, QFileDialog, QLabel, QVBoxLayout

class FolderDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.btn = QPushButton('Select Data Folder', self)
        self.btn.clicked.connect(self.open_dialog)
        self.label = QLabel('Folder Path: ', self)

        self.layout.addWidget(self.btn)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.folder_path = '../data'

    def open_dialog(self):
        self.folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        self.label.setText(f'Folder Path: {self.folder_path}')
    
    def get_selected_folder(self):
        return self.folder_path
