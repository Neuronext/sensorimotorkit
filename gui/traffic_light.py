from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap

class TrafficLight(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.label = QLabel(self)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.set_red()

    def set_red(self):
        self.label.setPixmap(QPixmap('../assets/red_dot.jpeg'))

    def set_green(self):
        self.label.setPixmap(QPixmap('../assets/green_dot.png'))
