from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem

class ObjectLibrary(QWidget):
    def __init__(self, parent=None):
        super(ObjectLibrary, self).__init__(parent)
        self.setWindowTitle("Object Library")
        self.setGeometry(100, 100, 300, 400)

        self.layout = QVBoxLayout()
        self.label = QLabel("Select an Object:")
        self.layout.addWidget(self.label)

        self.object_list = QListWidget()
        self.populate_object_list()
        self.layout.addWidget(self.object_list)

        self.setLayout(self.layout)

    def populate_object_list(self):
        objects = [
            "Circle",
            "Square",
            "Polygon",
            "Line",
            "Arrow",
            "Text (Normal)",
            "Text (LaTeX)",
            "2D Graph",
            "3D Object",
            "Image/SVG Import"
        ]
        for obj in objects:
            item = QListWidgetItem(obj)
            self.object_list.addItem(item)

    def get_selected_object(self):
        selected_items = self.object_list.selectedItems()
        if selected_items:
            return selected_items[0].text()
        return None