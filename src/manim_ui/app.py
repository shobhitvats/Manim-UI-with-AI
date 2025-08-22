"""
Main Application Module
========================

Central application class that manages the entire Manim UI Builder.
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from .ui.main_window import MainWindow

class ManimUIApp(QApplication):
    """Main application class for Manim UI Builder."""
    
    def __init__(self, argv):
        super().__init__(argv)
        
        # Set application properties
        self.setStyle('Fusion')  # Use Fusion style for consistent cross-platform look
        
        # Apply dark theme
        self.setStyleSheet(self._get_dark_stylesheet())
        
        # Initialize main window
        self.main_window = None
    
    def show_main_window(self):
        """Create and show the main application window."""
        self.main_window = MainWindow()
        self.main_window.show()
        
        # Center the window on screen
        self.main_window.center_on_screen()
    
    def _get_dark_stylesheet(self):
        """Return a dark theme stylesheet for the application."""
        return """
        QMainWindow {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        
        QWidget {
            background-color: #2b2b2b;
            color: #ffffff;
            border: none;
        }
        
        QMenuBar {
            background-color: #3c3c3c;
            border-bottom: 1px solid #555555;
        }
        
        QMenuBar::item {
            background-color: transparent;
            padding: 4px 8px;
        }
        
        QMenuBar::item:selected {
            background-color: #555555;
        }
        
        QMenu {
            background-color: #3c3c3c;
            border: 1px solid #555555;
        }
        
        QMenu::item:selected {
            background-color: #555555;
        }
        
        QDockWidget {
            background-color: #353535;
            border: 1px solid #555555;
            titlebar-close-icon: url(close.png);
            titlebar-normal-icon: url(undock.png);
        }
        
        QDockWidget::title {
            background-color: #404040;
            padding: 4px;
            border-bottom: 1px solid #555555;
        }
        
        QTabWidget::pane {
            border: 1px solid #555555;
            background-color: #353535;
        }
        
        QTabBar::tab {
            background-color: #404040;
            border: 1px solid #555555;
            padding: 4px 8px;
            margin: 1px;
        }
        
        QTabBar::tab:selected {
            background-color: #555555;
        }
        
        QPushButton {
            background-color: #404040;
            border: 1px solid #555555;
            padding: 4px 8px;
            border-radius: 2px;
        }
        
        QPushButton:hover {
            background-color: #555555;
        }
        
        QPushButton:pressed {
            background-color: #606060;
        }
        
        QSlider::groove:horizontal {
            border: 1px solid #555555;
            height: 6px;
            background-color: #404040;
        }
        
        QSlider::handle:horizontal {
            background-color: #ffffff;
            border: 1px solid #555555;
            width: 12px;
            margin: -4px 0;
            border-radius: 6px;
        }
        
        QScrollBar:vertical {
            background-color: #404040;
            width: 12px;
            border-radius: 6px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #606060;
            border-radius: 6px;
            min-height: 20px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #707070;
        }
        """