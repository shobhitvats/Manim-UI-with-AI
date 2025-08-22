from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout, QColorDialog, QPushButton, QHBoxLayout

class Inspector(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Inspector")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Object Properties
        self.object_label = QLabel("Selected Object Properties")
        layout.addWidget(self.object_label)

        self.color_label = QLabel("Color:")
        self.color_input = QLineEdit()
        self.color_button = QPushButton("Choose Color")
        self.color_button.clicked.connect(self.choose_color)

        color_layout = QHBoxLayout()
        color_layout.addWidget(self.color_input)
        color_layout.addWidget(self.color_button)

        layout.addWidget(self.color_label)
        layout.addLayout(color_layout)

        self.size_label = QLabel("Size:")
        self.size_input = QLineEdit()
        layout.addWidget(self.size_label)
        layout.addWidget(self.size_input)

        self.position_label = QLabel("Position:")
        self.position_input = QLineEdit()
        layout.addWidget(self.position_label)
        layout.addWidget(self.position_input)

        self.setLayout(layout)

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_input.setText(color.name())

    def update_properties(self, properties):
        self.color_input.setText(properties.get('color', ''))
        self.size_input.setText(str(properties.get('size', '')))
        self.position_input.setText(str(properties.get('position', '')))