import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QColorDialog
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import Qt, QSize

class ImageDisplayApp(QWidget):
    def __init__(self, image_folder):
        super().__init__()
        
        self.setWindowTitle("Dart Display App")
        self.setMinimumSize(400, 400)  # Set the minimum size of the widget

        self.image_folder = image_folder  # Store the folder path

        # Display initial image
        self.image_label = QLabel(self)
        self.display_selected_image()  # Display the initial image

        # Buttons for changing background color and scaling
        color_button = QPushButton("Change Background Color", self)
        color_button.clicked.connect(self.change_background_color)

        zoom_in_button = QPushButton("Zoom In", self)
        zoom_in_button.clicked.connect(self.zoom_in)

        zoom_out_button = QPushButton("Zoom Out", self)
        zoom_out_button.clicked.connect(self.zoom_out)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(color_button)
        layout.addWidget(zoom_in_button)
        layout.addWidget(zoom_out_button)
        self.setLayout(layout)

        # Initial scale factor
        self.scale_factor = 1.0

    def display_selected_image(self):
        # Load and display the image from the selected folder
        if self.image_folder:
            image_path = os.path.join(self.image_folder, 'example.jpg')  # Example image path, modify as needed
            pixmap = QPixmap(image_path)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def change_background_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.setAutoFillBackground(True)
            palette = self.palette()
            palette.setColor(self.backgroundRole(), color)
            self.setPalette(palette)

    def zoom_in(self):
        self.scale_factor *= 1.25
        self.image_label.resize(self.image_label.pixmap().size() * self.scale_factor)
        self.display_selected_image()

    def zoom_out(self):
        self.scale_factor *= 0.8
        self.image_label.resize(self.image_label.pixmap().size() * self.scale_factor)
        self.display_selected_image()

class ImageDisplayController:
    def __init__(self, image_display_app):
        self.image_display_app = image_display_app

    def update_displayed_image(self, folder_path):
        # Update the displayed image based on the selected folder path
        self.image_display_app.image_folder = folder_path
        self.image_display_app.display_selected_image()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    image_folder = "C:/Users/Dataacquisition/sensorimotorkit/assets/targets/"  # Example folder path, modify as needed
    image_display_app = ImageDisplayApp(image_folder)
    image_display_app.show()
    sys.exit(app.exec_())
