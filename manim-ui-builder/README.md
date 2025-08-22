# Manim UI Builder

## Overview
Manim UI Builder is a cross-platform visual editor for creating animations using the Manim library. This application allows users to design animations through a user-friendly drag-and-drop interface, making it accessible for educators, students, and anyone interested in creating mathematical animations without needing to write code.

## Features
- **Drag-and-Drop Interface**: Easily add shapes, text, and other objects to your animation.
- **Timeline Editor**: Manage keyframes and sequencing of animations with a visual timeline.
- **Real-Time Preview**: View your animations as you create them in the canvas area.
- **Gemini Pro Integration**: Use natural language prompts to generate and edit animations with AI assistance.
- **Export Options**: Save your animations as MP4, GIF, or export the raw Manim code.

## Technical Stack
- **Frontend**: Built using PyQt/PySide for a native desktop experience.
- **Backend**: Python with FastAPI/Flask for handling Gemini API calls.
- **Rendering**: Utilizes ManimCE (Community Edition) for rendering animations.

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/manim-ui-builder.git
   cd manim-ui-builder
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables for the Gemini Pro API key:
   ```
   export GEMINI_API_KEY='your_api_key_here'
   ```

4. Run the application:
   ```
   python src/main.py
   ```

## Usage
- Launch the application and create a new project.
- Use the Object Library to drag shapes, text, and other elements onto the canvas.
- Adjust properties in the Inspector panel and manage animations in the Timeline editor.
- Interact with the Gemini Assistant to generate animations using natural language prompts.
- Export your project in your desired format when finished.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.