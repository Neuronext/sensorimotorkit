import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap
from common.constants import MetadataConstants
from PyQt5.QtCore import pyqtSignal


class TrafficLight(QWidget):
    updateColor = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.label = QLabel(self)
        self.label.setMinimumSize(MetadataConstants.TRAFFIC_LIGHT_SIZE, MetadataConstants.TRAFFIC_LIGHT_SIZE)
        self.label.setMaximumSize(MetadataConstants.TRAFFIC_LIGHT_SIZE, MetadataConstants.TRAFFIC_LIGHT_SIZE)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        # traffic light images
        script_dir = os.path.dirname(os.path.realpath(__file__))
        self.red_light_image = os.path.join(script_dir, '..', 'assets', 'red_dot.jpeg')
        self.green_light_image = os.path.join(script_dir, '..', 'assets', 'green_dot.png')
        self.set_red()
        self.status = 'red'
        self.updateColor.connect(self._updateColor)


    def _updateColor(self, color):
        if color == 'red':
            self.set_red()
        elif color == 'green':
            self.set_green()
    
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
