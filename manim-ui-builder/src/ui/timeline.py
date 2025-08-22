from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QSlider, QLineEdit
from PyQt5.QtCore import Qt

class Timeline(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Timeline Editor")
        self.setGeometry(100, 100, 800, 200)
        
        self.layout = QVBoxLayout()
        
        self.timeline_label = QLabel("Timeline")
        self.layout.addWidget(self.timeline_label)
        
        self.keyframe_list = QListWidget()
        self.layout.addWidget(self.keyframe_list)
        
        self.add_keyframe_button = QPushButton("Add Keyframe")
        self.add_keyframe_button.clicked.connect(self.add_keyframe)
        self.layout.addWidget(self.add_keyframe_button)
        
        self.remove_keyframe_button = QPushButton("Remove Keyframe")
        self.remove_keyframe_button.clicked.connect(self.remove_keyframe)
        self.layout.addWidget(self.remove_keyframe_button)
        
        self.duration_slider = QSlider(Qt.Horizontal)
        self.duration_slider.setRange(1, 100)
        self.duration_slider.setValue(50)
        self.layout.addWidget(QLabel("Animation Duration:"))
        self.layout.addWidget(self.duration_slider)
        
        self.setLayout(self.layout)

    def add_keyframe(self):
        keyframe_name = f"Keyframe {self.keyframe_list.count() + 1}"
        self.keyframe_list.addItem(keyframe_name)

    def remove_keyframe(self):
        selected_items = self.keyframe_list.selectedItems()
        if selected_items:
            for item in selected_items:
                self.keyframe_list.takeItem(self.keyframe_list.row(item))