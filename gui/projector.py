import sys, os
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QColorDialog, QFileDialog
from PyQt5.QtGui import QPixmap, QColor, QCursor
from PyQt5.QtCore import Qt, QPoint, QFile, QTextStream

class ImageDisplayApp(QWidget):
    def __init__(self, image_path):
        super().__init__()
        
        self.setWindowTitle("Image Display App")
        self.setMinimumSize(500, 500)
        self.image_path = image_path

        self.image_label = QLabel(self)
        self.display_selected_image()
        color_button = QPushButton("Change Background Color", self)
        color_button.clicked.connect(self.change_background_color)
        zoom_in_button = QPushButton("Zoom In", self)
        zoom_in_button.clicked.connect(self.zoom_in)
        zoom_out_button = QPushButton("Zoom Out", self)
        zoom_out_button.clicked.connect(self.zoom_out)
        save_button = QPushButton("Save", self)
        save_button.clicked.connect(self.save_settings)
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(color_button)
        layout.addWidget(zoom_in_button)
        layout.addWidget(zoom_out_button)
        layout.addWidget(save_button)
        self.setLayout(layout)

        self.scale_factor = 1.0
        self.offset = QPoint(0, 0)
        self.dragging = False

        self.load_settings()
    def set_image(self):
            pixmap = QPixmap(image_path)
            self.image_label.setPixmap(pixmap)
            self.image_label.setFixedSize(pixmap.size())

    def display_selected_image(self):
        pixmap = QPixmap(self.image_path)
        self.image_label.setPixmap(pixmap)
        self.image_label.setFixedSize(pixmap.size())

    def change_background_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
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
            self.dragging = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
                    new_pos = self.mapToParent(event.pos() - self.offset)
                    self.image_label.move(new_pos)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
                self.dragging = False

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

    def enterEvent(self, event):
        self.setCursor(QCursor(Qt.OpenHandCursor))

    def leaveEvent(self, event):
        self.setCursor(QCursor(Qt.ArrowCursor))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    image_path = sys.argv[1]
    imageDisplayApp = ImageDisplayApp(image_path)
    imageDisplayApp.show()
    sys.exit(app.exec_())