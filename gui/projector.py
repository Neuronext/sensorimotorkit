import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QColorDialog, QFileDialog, QComboBox
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import Qt

class ImageDisplayApp(QWidget):
    def __init__(self, image_path):
        super().__init__()
        
        self.setWindowTitle("Image Display App")
        self.setMinimumSize(400, 400)

        self.image_path = image_path

        self.image_label = QLabel(self)
        self.display_selected_image()

        color_button = QPushButton("Change Background Color", self)
        color_button.clicked.connect(self.change_background_color)

        zoom_in_button = QPushButton("Zoom In", self)
        zoom_in_button.clicked.connect(self.zoom_in)

        zoom_out_button = QPushButton("Zoom Out", self)
        zoom_out_button.clicked.connect(self.zoom_out)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(color_button)
        layout.addWidget(zoom_in_button)
        layout.addWidget(zoom_out_button)
        self.setLayout(layout)

        self.scale_factor = 1.0

    def set_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap)

    def display_selected_image(self):
        pixmap = QPixmap(self.image_path)
        self.image_label.setPixmap(pixmap)

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

    def zoom_out(self):
        self.scale_factor *= 0.8
        self.image_label.resize(self.image_label.pixmap().size() * self.scale_factor)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    image_path = sys.argv[1]
    imageDisplayApp = ImageDisplayApp(image_path)
    imageDisplayApp.show()
    app.exec_()

