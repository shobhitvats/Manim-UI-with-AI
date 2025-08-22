#!/usr/bin/env python3
"""
Manim UI Builder with Gemini Integration
========================================

A cross-platform visual editor for Manim animations with AI assistance.

Author: AI Assistant
License: MIT
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from manim_ui.app import ManimUIApp

def main():
    """Main entry point for the Manim UI Builder application."""
    app = ManimUIApp(sys.argv)
    
    # Set application metadata
    app.setApplicationName("Manim UI Builder")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Manim UI")
    
    # Show the main window
    app.show_main_window()
    
    # Start the application event loop
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())