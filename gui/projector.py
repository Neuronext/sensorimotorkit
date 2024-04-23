import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QColorDialog
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import Qt, QFile, QTextStream

class ImageDisplayApp(QWidget):
    def __init__(self, image_path, data_point):
        super().__init__()
        
        self.setWindowTitle("Image Display App")
        self.setMinimumSize(500, 500)

        self.image_path = image_path

        self.image_label = QLabel(self)
        self.display_selected_image(image_path)

        self.data_point_label = QLabel("", self)

        self.color_button = QPushButton("Change Background Color", self)
        self.color_button.clicked.connect(self.change_background_color)

        self.zoom_in_button = QPushButton("Zoom In", self)
        self.zoom_in_button.clicked.connect(self.zoom_in)

        self.zoom_out_button = QPushButton("Zoom Out", self)
        self.zoom_out_button.clicked.connect(self.zoom_out)

        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_settings)

        # Vertical layout for buttons at the bottom
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.color_button)
        buttons_layout.addWidget(self.zoom_in_button)
        buttons_layout.addWidget(self.zoom_out_button)
        buttons_layout.addWidget(self.save_button)

        # Vertical layout for the whole widget
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.image_label)
        main_layout.addWidget(self.data_point_label)
        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

        self.scale_factor = 1.0
        self.drag_start_pos = None
        self.setMouseTracking(True)
        self.image_label.raise_()

        self.load_settings()

    def display_selected_image(self, image_path):
        self.image_path = image_path
        pixmap = QPixmap(self.image_path)
        self.image_label.setPixmap(pixmap)
        self.image_label.setFixedSize(pixmap.size())

    def change_background_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.setAutoFillBackground(True)
            palette = self.palette()
            palette.setColor(self.backgroundRole(), color)
            self.setPalette(palette)

    def zoom_in(self):
        self.scale_factor *= 1.25
        scaled_pixmap = self.image_label.pixmap().scaled(
            self.image_label.pixmap().size() * self.scale_factor,
            aspectRatioMode=Qt.KeepAspectRatio
        )
        self.image_label.setPixmap(scaled_pixmap)

    def zoom_out(self):
        self.scale_factor *= 0.8
        scaled_pixmap = self.image_label.pixmap().scaled(
            self.image_label.pixmap().size() * self.scale_factor,
            aspectRatioMode=Qt.KeepAspectRatio
        )
        self.image_label.setPixmap(scaled_pixmap)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.image_label.geometry().contains(event.pos()):
            self.drag_start_pos = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_start_pos:
            delta = event.pos() - self.drag_start_pos
            new_pos = self.image_label.pos() + delta

            # Ensure the new position stays within the boundaries of the window
            if new_pos.x() >= 0 and new_pos.y() >= 0 \
                    and new_pos.x() + self.image_label.width() <= self.width() \
                    and new_pos.y() + self.image_label.height() <= self.height():
                self.image_label.move(new_pos)
                self.drag_start_pos = event.pos()
                self.update_data_point_label(self.image_label.pos())
                self.raise_()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_pos = None

    def update_data_point_label(self, pos):
        data_point = f"Data Point: ({pos.x()}, {pos.y()})"
        self.data_point_label.setText(data_point)

    def save_settings(self):
        settings_file = QFile("settings.txt")
        if settings_file.open(QFile.WriteOnly | QFile.Text):
            out = QTextStream(settings_file)
            out << f"Background Color: {self.palette().color(self.backgroundRole()).name()}\n"
            out << f"Image Position: {self.image_label.pos().x()}, {self.image_label.pos().y()}\n"
            out << f"Zoom Level: {self.scale_factor}\n"
            settings_file.close()

    def load_settings(self):
        settings_file = QFile("settings.txt")
        if settings_file.open(QFile.ReadOnly | QFile.Text):
            settings = QTextStream(settings_file).readAll().split("\n")
            for setting in settings:
                if setting.startswith("Background Color"):
                    color = QColor(setting.split(":")[1].strip())
                    palette = self.palette()
                    palette.setColor(self.backgroundRole(), color)
                    self.setPalette(palette)
                elif setting.startswith("Image Position"):
                    pos = setting.split(":")[1].strip().split(",")
                    self.image_label.move(int(pos[0]), int(pos[1]))
                elif setting.startswith("Zoom Level"):
                    self.scale_factor = float(setting.split(":")[1].strip())
                    scaled_pixmap = self.image_label.pixmap().scaled(
                        self.image_label.pixmap().size() * self.scale_factor,
                        aspectRatioMode=Qt.KeepAspectRatio
                    )
                    self.image_label.setPixmap(scaled_pixmap)
            settings_file.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    image_path = sys.argv[1]
    imageDisplayApp = ImageDisplayApp(image_path)
    imageDisplayApp.show()
    sys.exit(app.exec_())
