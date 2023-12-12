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

    def open_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        self.label.setText(f'Folder Path: {folder_path}')
