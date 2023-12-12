import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap

class TrafficLight(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.label = QLabel(self)
        self.label.setMinimumSize(10, 10)
        self.label.setMaximumSize(10, 10)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        # traffic light images
        script_dir = os.path.dirname(os.path.realpath(__file__))
        self.red_light_image = os.path.join(script_dir, '..', 'assets', 'red_dot.jpeg')
        self.green_light_image = os.path.join(script_dir, '..', 'assets', 'green_dot.png')
        self.set_red()
        self.status = 'red'

    def set_red(self):
        pixmap = QPixmap(self.red_light_image)
        if pixmap.isNull():
            print("Failed to load red dot image")
        self.label.setPixmap(pixmap)

    def set_green(self):
        pixmap = QPixmap(self.green_light_image)
        if pixmap.isNull():
            print("Failed to load green dot image")
        self.label.setPixmap(pixmap)
