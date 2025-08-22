from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel
from PyQt5.QtCore import Qt
from ai.gemini_client import GeminiClient

class GeminiPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gemini Assistant")
        self.setGeometry(100, 100, 400, 300)
        
        self.layout = QVBoxLayout()
        
        self.prompt_label = QLabel("Enter your animation description:")
        self.layout.addWidget(self.prompt_label)
        
        self.prompt_input = QTextEdit()
        self.layout.addWidget(self.prompt_input)
        
        self.generate_button = QPushButton("Generate Animation")
        self.generate_button.clicked.connect(self.generate_animation)
        self.layout.addWidget(self.generate_button)
        
        self.response_label = QLabel("Response:")
        self.layout.addWidget(self.response_label)
        
        self.response_output = QTextEdit()
        self.response_output.setReadOnly(True)
        self.layout.addWidget(self.response_output)
        
        self.setLayout(self.layout)
        
        self.gemini_client = GeminiClient()

    def generate_animation(self):
        prompt = self.prompt_input.toPlainText()
        if prompt:
            response = self.gemini_client.send_prompt(prompt)
            self.response_output.setPlainText(response)
        else:
            self.response_output.setPlainText("Please enter a prompt.")