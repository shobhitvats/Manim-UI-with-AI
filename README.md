# Manim UI Builder with AI

A cross-platform visual editor for creating Manim animations with AI assistance from Gemini Pro.

## 🎯 Features

- **Visual Drag-and-Drop Editor**: Create Manim animations without coding
- **AI-Powered Assistant**: Generate animations from natural language descriptions
- **Timeline-Based Editor**: Professional animation sequencing and keyframe management
- **Real-Time Preview**: See your animations as you build them
- **Export Options**: MP4, GIF, and Python code export
- **Project Management**: Save, load, and manage animation projects

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- PyQt6 (for GUI)
- Manim Community Edition (for rendering)
- Google Generative AI (for AI features) - optional

### Installation

1. Clone the repository:
```bash
git clone https://github.com/shobhitvats/Manim-UI-with-AI.git
cd Manim-UI-with-AI
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Set up Gemini AI integration:
```bash
export GEMINI_API_KEY="your-api-key-here"
```

4. Run the application:
```bash
python main.py
```

## 🛠️ Features Overview

### Object Library
- Basic shapes (Circle, Square, Rectangle, etc.)
- Text and LaTeX support
- 2D and 3D objects
- Graphs and plots
- Arrows and vectors

### Animation System
- Fade effects (FadeIn, FadeOut)
- Transformations (MoveTo, Rotate, Scale)
- Text animations (Write, Unwrite)
- Custom timing and sequencing

### AI Assistant
- Natural language to animation conversion
- Common animation templates
- Interactive chat interface
- Code generation and explanation

### Export Options
- High-quality MP4 videos
- Animated GIFs
- Raw Python Manim code
- Project files (JSON format)

## 📖 Usage Examples

### Creating a Simple Animation

1. Drag a Circle from the Object Library to the Canvas
2. Add a "FadeIn" animation in the Timeline
3. Preview your animation
4. Export as MP4 or Python code

### Using AI Assistant

1. Open the AI Assistant panel
2. Type: "Create a sine wave that grows in amplitude"
3. The AI will generate the corresponding Manim code
4. Apply the generated animation to your scene

### Timeline Editing

1. Add objects to the canvas
2. Use the Timeline Editor to sequence animations
3. Adjust timing and duration
4. Add multiple tracks for complex scenes

## 🏗️ Architecture

```
src/manim_ui/
├── app.py              # Main application
├── ui/                 # User interface components
│   ├── main_window.py  # Main application window
│   └── panels/         # UI panels
│       ├── object_library.py
│       ├── canvas_preview.py
│       ├── timeline_editor.py
│       ├── inspector.py
│       └── gemini_assistant.py
└── core/               # Core functionality
    ├── manim_integration.py  # Manim scene building
    └── project.py           # Project management
```

## 🔧 Development

### Running Tests

```bash
python test_basic.py
```

### Code Structure

- **UI Layer**: PyQt6-based interface with dockable panels
- **Core Layer**: Manim integration and project management
- **AI Layer**: Gemini Pro API integration for natural language processing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📋 Requirements

- Cross-platform compatibility (Windows, macOS, Linux)
- No-code animation creation
- Professional timeline editing
- AI-assisted content generation
- High-quality export options

## 🔮 Roadmap

- [ ] Advanced 3D animation support
- [ ] Plugin system for custom objects
- [ ] Cloud rendering capabilities
- [ ] Collaborative editing features
- [ ] Advanced AI templates
- [ ] Mobile companion app

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Manim Community Edition for the animation engine
- Google Gemini for AI capabilities
- PyQt6 for the user interface framework