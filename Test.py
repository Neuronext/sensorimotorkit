import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSlider, QColorDialog
from PyQt5.QtGui import QPixmap, QPainter, QPalette, QColor
from PyQt5.QtCore import Qt, QSize, QPoint

class ImageDisplayApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dart Display App")
        self.setMinimumSize(400, 400)  # Set the minimum size of the widget

        # Load images
        self.image_paths = ["C:/Users/janit/OneDrive/Pictures/red circle.jpg", "C:/Users/janit/OneDrive/Pictures/75f01dc94d1855666f6f5a9f0aa4f5ed.jpg"]  # Add your image paths here
        self.images = [QPixmap(path) for path in self.image_paths]
        self.current_image_index = 0

        # Display initial image
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.set_image(self.current_image_index)

        # Slider for horizontal resizing
        self.horizontal_slider = QSlider(Qt.Horizontal)
        self.horizontal_slider.setMinimum(0)
        self.horizontal_slider.setMaximum(200)
        self.horizontal_slider.setValue(100)
        self.horizontal_slider.valueChanged.connect(self.resize_image)

        # Slider for vertical movement
        self.vertical_slider = QSlider(Qt.Vertical)
        self.vertical_slider.setMinimum(-100)
        self.vertical_slider.setMaximum(100)
        self.vertical_slider.setValue(0)
        self.vertical_slider.valueChanged.connect(self.move_image_vertically)

        # Labels for sliders
        self.up_label = QLabel("Up", self)
        self.down_label = QLabel("Down", self)

        # Label to display current scale factor
        self.scale_label = QLabel("Scale Factor: 1.00", self)

        # Buttons to navigate through images
        prev_button = QPushButton("Previous", self)
        prev_button.clicked.connect(self.show_previous_image)
        next_button = QPushButton("Next", self)
        next_button.clicked.connect(self.show_next_image)

        # Button to change background color
        color_button = QPushButton("Change Background Color", self)
        color_button.clicked.connect(self.change_background_color)

        # Layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(prev_button)
        button_layout.addWidget(next_button)

        slider_layout = QVBoxLayout()
        slider_layout.addWidget(self.horizontal_slider)
        slider_layout.addWidget(self.up_label)
        slider_layout.addWidget(self.vertical_slider)
        slider_layout.addWidget(self.down_label)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addLayout(slider_layout)
        layout.addWidget(self.scale_label)
        layout.addLayout(button_layout)
        layout.addWidget(color_button)
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
        self.scale_label.setText("Scale Factor: {:.2f}".format(scale_factor))

    def move_image_vertically(self, value):
        pixmap = self.images[self.current_image_index]
        scaled_pixmap = self.image_label.pixmap()
        if pixmap and scaled_pixmap:
            current_pos = self.image_label.pos()
            new_y = current_pos.y() + value
            max_y = self.height() - scaled_pixmap.height()
            new_y = max(0, min(new_y, max_y))
            new_pos = QPoint(current_pos.x(), new_y)
            self.image_label.move(new_pos)

    def show_previous_image(self):
        self.current_image_index = (self.current_image_index - 1) % len(self.images)
        self.set_image(self.current_image_index)

    def show_next_image(self):
        self.current_image_index = (self.current_image_index + 1) % len(self.images)
        self.set_image(self.current_image_index)

    def change_background_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            palette = self.palette()
            palette.setColor(QPalette.Window, color)
            self.setPalette(palette)

def main():
    app = QApplication(sys.argv)
    image_display_app = ImageDisplayApp()
    image_display_app.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
