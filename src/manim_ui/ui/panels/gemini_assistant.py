"""
Gemini Assistant Panel
======================

AI-powered assistant panel for generating Manim animations from text prompts.
"""

import os
import json
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QLineEdit, QScrollArea, QFrame, QMessageBox,
    QSplitter, QListWidget, QListWidgetItem, QProgressBar
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QTimer
from PyQt6.QtGui import QFont, QTextCursor

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

class GeminiClient(QThread):
    """Thread for handling Gemini API calls."""
    
    response_received = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.model = None
        self.prompt = ""
        self.system_prompt = ""
        
        # Initialize Gemini if available
        self._initialize_gemini()
    
    def _initialize_gemini(self):
        """Initialize the Gemini client."""
        if not GEMINI_AVAILABLE:
            return
        
        # Get API key from environment
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            self.error_occurred.emit("Gemini API key not found. Please set GEMINI_API_KEY environment variable.")
            return
        
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        except Exception as e:
            self.error_occurred.emit(f"Failed to initialize Gemini: {str(e)}")
    
    def generate_response(self, prompt, system_prompt=""):
        """Generate a response from Gemini."""
        self.prompt = prompt
        self.system_prompt = system_prompt
        self.start()
    
    def run(self):
        """Run the Gemini API call in a separate thread."""
        if not self.model:
            self.error_occurred.emit("Gemini model not initialized")
            return
        
        try:
            # Combine system prompt with user prompt
            full_prompt = f"{self.system_prompt}\n\nUser: {self.prompt}" if self.system_prompt else self.prompt
            
            response = self.model.generate_content(full_prompt)
            
            if response.text:
                self.response_received.emit(response.text)
            else:
                self.error_occurred.emit("No response received from Gemini")
                
        except Exception as e:
            self.error_occurred.emit(f"Gemini API error: {str(e)}")

class ChatMessage(QFrame):
    """A single chat message widget."""
    
    def __init__(self, message, is_user=True):
        super().__init__()
        
        self.is_user = is_user
        self.message = message
        
        self.setFrameStyle(QFrame.Shape.Box)
        self.setStyleSheet(self._get_message_style())
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the message UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        
        # Sender label
        sender_label = QLabel("You" if self.is_user else "AI Assistant")
        sender_label.setStyleSheet("font-weight: bold; color: #ffffff;")
        layout.addWidget(sender_label)
        
        # Message text
        message_text = QLabel(self.message)
        message_text.setWordWrap(True)
        message_text.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        message_text.setStyleSheet("color: #ffffff; margin-top: 5px;")
        layout.addWidget(message_text)
    
    def _get_message_style(self):
        """Get the stylesheet for the message."""
        if self.is_user:
            return """
                QFrame {
                    background-color: #4a5568;
                    border: 1px solid #555555;
                    border-radius: 8px;
                    margin: 2px 50px 2px 2px;
                }
            """
        else:
            return """
                QFrame {
                    background-color: #2d3748;
                    border: 1px solid #555555;
                    border-radius: 8px;
                    margin: 2px 2px 2px 50px;
                }
            """

class TemplateItem(QListWidgetItem):
    """A template item for common animation patterns."""
    
    def __init__(self, name, description, prompt_template):
        super().__init__(name)
        
        self.name = name
        self.description = description
        self.prompt_template = prompt_template
        
        self.setToolTip(description)

class GeminiAssistantPanel(QWidget):
    """AI assistant panel for Manim animation generation."""
    
    animation_generated = pyqtSignal(str)  # Emitted when AI generates animation code
    
    def __init__(self):
        super().__init__()
        
        self.gemini_client = GeminiClient()
        self.chat_history = []
        
        self.setMinimumWidth(300)
        self._setup_ui()
        self._setup_templates()
        self._connect_signals()
        
        # Check if Gemini is available
        if not GEMINI_AVAILABLE:
            self._show_gemini_unavailable()
    
    def _setup_ui(self):
        """Setup the user interface."""
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("AI Assistant (Gemini)")
        title_label.setStyleSheet("font-weight: bold; font-size: 14px; padding: 5px;")
        layout.addWidget(title_label)
        
        # Main splitter
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Chat area (top)
        chat_widget = self._create_chat_widget()
        splitter.addWidget(chat_widget)
        
        # Templates area (bottom)
        templates_widget = self._create_templates_widget()
        splitter.addWidget(templates_widget)
        
        # Set splitter proportions
        splitter.setStretchFactor(0, 3)  # Chat gets more space
        splitter.setStretchFactor(1, 1)  # Templates get less space
        
        layout.addWidget(splitter)
    
    def _create_chat_widget(self):
        """Create the chat interface."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Chat history
        self.chat_scroll = QScrollArea()
        self.chat_scroll.setWidgetResizable(True)
        self.chat_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.chat_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setContentsMargins(5, 5, 5, 5)
        self.chat_layout.addStretch()
        
        self.chat_scroll.setWidget(self.chat_container)
        layout.addWidget(self.chat_scroll)
        
        # Input area
        input_layout = QVBoxLayout()
        
        # Progress bar for API calls
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.progress_bar.hide()
        input_layout.addWidget(self.progress_bar)
        
        # Prompt input
        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText("Ask me to create or modify animations...\n\nExample: \"Create a sine wave that grows in amplitude and add a red arrow pointing to the peak\"")
        self.prompt_input.setMaximumHeight(100)
        input_layout.addWidget(self.prompt_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.send_btn = QPushButton("Send")
        self.send_btn.setStyleSheet("QPushButton { background-color: #4299e1; }")
        button_layout.addWidget(self.send_btn)
        
        self.clear_btn = QPushButton("Clear Chat")
        button_layout.addWidget(self.clear_btn)
        
        input_layout.addLayout(button_layout)
        layout.addLayout(input_layout)
        
        return widget
    
    def _create_templates_widget(self):
        """Create the templates widget."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Title
        templates_label = QLabel("Quick Templates")
        templates_label.setStyleSheet("font-weight: bold; font-size: 12px; padding: 2px;")
        layout.addWidget(templates_label)
        
        # Templates list
        self.templates_list = QListWidget()
        self.templates_list.setMaximumHeight(150)
        layout.addWidget(self.templates_list)
        
        # Use template button
        self.use_template_btn = QPushButton("Use Template")
        layout.addWidget(self.use_template_btn)
        
        return widget
    
    def _setup_templates(self):
        """Setup animation templates."""
        templates = [
            {
                "name": "Function Plot",
                "description": "Create a function plot with axes",
                "prompt": "Create a function plot showing f(x) = x^2 with labeled axes and a title."
            },
            {
                "name": "Text Animation",
                "description": "Animate text appearing and transforming",
                "prompt": "Create a text animation that writes 'Hello, Manim!' and then transforms it to 'Welcome to AI Animation!'"
            },
            {
                "name": "Shape Morphing",
                "description": "Transform one shape into another",
                "prompt": "Create an animation where a circle transforms into a square, then into a triangle."
            },
            {
                "name": "Mathematical Proof",
                "description": "Visualize a mathematical proof",
                "prompt": "Create a visual proof of the Pythagorean theorem using squares on the sides of a right triangle."
            },
            {
                "name": "3D Scene",
                "description": "Create a 3D scene with rotating objects",
                "prompt": "Create a 3D scene with a rotating cube and sphere, with proper lighting and camera movement."
            },
            {
                "name": "Vector Field",
                "description": "Visualize a vector field",
                "prompt": "Create a vector field visualization showing the gradient of a 2D function."
            }
        ]
        
        for template in templates:
            item = TemplateItem(template["name"], template["description"], template["prompt"])
            self.templates_list.addItem(item)
    
    def _connect_signals(self):
        """Connect signals between components."""
        # Chat interface
        self.send_btn.clicked.connect(self._send_message)
        self.clear_btn.clicked.connect(self._clear_chat)
        self.prompt_input.textChanged.connect(self._on_text_changed)
        
        # Templates
        self.use_template_btn.clicked.connect(self._use_template)
        self.templates_list.itemDoubleClicked.connect(self._use_template)
        
        # Gemini client
        self.gemini_client.response_received.connect(self._on_response_received)
        self.gemini_client.error_occurred.connect(self._on_error_occurred)
    
    def _show_gemini_unavailable(self):
        """Show message when Gemini is not available."""
        self.add_message("Gemini AI integration is not available. Please install the google-generativeai package and set your GEMINI_API_KEY environment variable.", is_user=False)
        self.send_btn.setEnabled(False)
        self.send_btn.setText("Gemini Unavailable")
    
    def _on_text_changed(self):
        """Handle text changes in the prompt input."""
        has_text = bool(self.prompt_input.toPlainText().strip())
        self.send_btn.setEnabled(has_text and GEMINI_AVAILABLE)
    
    def _send_message(self):
        """Send a message to Gemini."""
        prompt = self.prompt_input.toPlainText().strip()
        if not prompt:
            return
        
        # Add user message to chat
        self.add_message(prompt, is_user=True)
        
        # Clear input
        self.prompt_input.clear()
        
        # Show progress
        self.progress_bar.show()
        self.send_btn.setEnabled(False)
        
        # Create system prompt for Manim code generation
        system_prompt = """You are an expert Manim (Mathematical Animation Engine) assistant. 
        Your task is to help users create animations by providing clear explanations and generating Manim Python code.
        
        When generating code:
        1. Use ManimCE (Community Edition) syntax
        2. Include necessary imports
        3. Create a complete Scene class
        4. Add comments explaining each step
        5. Use appropriate animation methods (FadeIn, Write, Transform, etc.)
        6. Consider the visual layout and timing
        
        If the user asks for modifications to existing animations, provide incremental changes.
        Always explain what the code does and suggest improvements or variations.
        """
        
        # Send to Gemini
        self.gemini_client.generate_response(prompt, system_prompt)
    
    def _on_response_received(self, response):
        """Handle response from Gemini."""
        self.progress_bar.hide()
        self.send_btn.setEnabled(True)
        
        # Add AI response to chat
        self.add_message(response, is_user=False)
        
        # Check if response contains code and emit signal
        if "```python" in response or "class" in response:
            self.animation_generated.emit(response)
    
    def _on_error_occurred(self, error):
        """Handle errors from Gemini."""
        self.progress_bar.hide()
        self.send_btn.setEnabled(True)
        
        # Add error message to chat
        self.add_message(f"Error: {error}", is_user=False)
    
    def add_message(self, message, is_user=True):
        """Add a message to the chat history."""
        # Create message widget
        message_widget = ChatMessage(message, is_user)
        
        # Insert before the stretch
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, message_widget)
        
        # Scroll to bottom
        QTimer.singleShot(100, self._scroll_to_bottom)
        
        # Store in history
        self.chat_history.append({"message": message, "is_user": is_user})
    
    def _scroll_to_bottom(self):
        """Scroll chat to the bottom."""
        scrollbar = self.chat_scroll.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def _clear_chat(self):
        """Clear the chat history."""
        # Remove all message widgets except the stretch
        while self.chat_layout.count() > 1:
            child = self.chat_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Clear history
        self.chat_history.clear()
    
    def _use_template(self):
        """Use the selected template."""
        current_item = self.templates_list.currentItem()
        if isinstance(current_item, TemplateItem):
            self.prompt_input.setPlainText(current_item.prompt_template)
            self.prompt_input.setFocus()
    
    def get_manim_system_prompt(self):
        """Get the system prompt for Manim code generation."""
        return """You are an expert Manim animation assistant. Generate clean, working Manim code that:

1. Uses proper ManimCE syntax
2. Includes all necessary imports
3. Creates a complete Scene class with construct() method
4. Uses appropriate animations (FadeIn, Write, Transform, MoveTo, etc.)
5. Has good timing and visual composition
6. Includes helpful comments

Example structure:
```python
from manim import *

class MyScene(Scene):
    def construct(self):
        # Your animation code here
        pass
```

Focus on creating visually appealing and educational animations."""