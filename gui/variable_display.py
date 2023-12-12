from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class VariableDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        # Example variable display
        self.varLabel = QLabel('Variable Display', self)

        self.layout.addWidget(self.varLabel)
        self.setLayout(self.layout)

    def update_variable(self, var_value):
        self.varLabel.setText(f'Variable: {var_value}')
