import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSlider
from PyQt5.QtGui import QPixmap, QPainter, QPalette
from PyQt5.QtCore import Qt, QSize

class ImageDisplayApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dart Diplay App")
        self.setMinimumSize(400, 400)  # Set the minimum size of the widget

        # Load images
        self.image_paths = ["C:/Users/janit/OneDrive/Pictures/red circle.jpg", "C:/Users/janit/OneDrive/Pictures/75f01dc94d1855666f6f5a9f0aa4f5ed.jpg"]  # Add your image paths here
        self.images = [QPixmap(path) for path in self.image_paths]
        self.current_image_index = 0

        # Display initial image
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.set_image(self.current_image_index)

        # Slider for resizing
        self.size_slider = QSlider(Qt.Horizontal)
        self.size_slider.setMinimum(0)
        self.size_slider.setMaximum(200)
        self.size_slider.setValue(100)
        self.size_slider.valueChanged.connect(self.resize_image)

        # Buttons to navigate through images
        prev_button = QPushButton("Previous", self)
        prev_button.clicked.connect(self.show_previous_image)
        next_button = QPushButton("Next", self)
        next_button.clicked.connect(self.show_next_image)

        # Layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(prev_button)
        button_layout.addWidget(next_button)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.size_slider)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def set_image(self, index):
        pixmap = self.images[index]
        scaled_pixmap = pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(scaled_pixmap)

    def resize_image(self, value):
        scale_factor = value / 100
        if scale_factor == 0:  # Reset to original size
            self.set_image(self.current_image_index)
        else:
            pixmap = self.images[self.current_image_index]
            scaled_width = max(1, int(pixmap.width() * scale_factor))
            scaled_height = max(1, int(pixmap.height() * scale_factor))
            scaled_pixmap = pixmap.scaled(QSize(scaled_width, scaled_height), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)

    def show_previous_image(self):
        self.current_image_index = (self.current_image_index - 1) % len(self.images)
        self.set_image(self.current_image_index)

    def show_next_image(self):
        self.current_image_index = (self.current_image_index + 1) % len(self.images)
        self.set_image(self.current_image_index)

def main():
    app = QApplication(sys.argv)
    image_display_app = ImageDisplayApp()
    image_display_app.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
