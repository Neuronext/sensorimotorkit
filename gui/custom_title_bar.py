from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QWidget

class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Minimize Button
        self.minimizeButton = QPushButton("-")
        self.minimizeButton.clicked.connect(self.minimizeWindow)
        self.layout.addWidget(self.minimizeButton)

        # Maximize Button
        self.maximizeButton = QPushButton("[]")
        self.maximizeButton.clicked.connect(self.maximizeWindow)
        self.layout.addWidget(self.maximizeButton)

        # Close Button
        self.closeButton = QPushButton("X")
        self.closeButton.clicked.connect(self.closeWindow)
        self.layout.addWidget(self.closeButton)

        self.setLayout(self.layout)

    def minimizeWindow(self):
        self.parent().showMinimized()

    def maximizeWindow(self):
        if self.parent().isMaximized():
            self.parent().showNormal()
        else:
            self.parent().showMaximized()

    def closeWindow(self):
        self.parent().close()
