#!/usr/bin/env python3
"""
Simple test script to verify the application runs without dependencies.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all modules can be imported."""
    try:
        from manim_ui.app import ManimUIApp
        from manim_ui.ui.main_window import MainWindow
        from manim_ui.ui.panels.object_library import ObjectLibraryPanel
        from manim_ui.ui.panels.canvas_preview import CanvasPreviewPanel
        from manim_ui.ui.panels.timeline_editor import TimelineEditorPanel
        from manim_ui.ui.panels.inspector import InspectorPanel
        from manim_ui.ui.panels.gemini_assistant import GeminiAssistantPanel
        from manim_ui.core.manim_integration import ManimSceneBuilder, ManimObject, Animation
        from manim_ui.core.project import Project, ProjectManager
        
        print("✓ All modules imported successfully")
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality without GUI."""
    try:
        # Test project creation
        from manim_ui.core.project import ProjectManager
        from manim_ui.core.manim_integration import ManimObject, Animation
        
        manager = ProjectManager()
        project = manager.new_project("Test Project")
        
        # Test object creation
        test_object = ManimObject(
            object_id="test-1",
            object_type="Circle",
            display_name="Test Circle",
            properties={'radius': 1.0, 'fill_color': 'blue'},
            position=(0, 0, 0)
        )
        
        project.scene_builder.add_object(test_object)
        
        # Test animation creation
        test_animation = Animation(
            animation_id="anim-1",
            object_id="test-1",
            animation_type="FadeIn",
            start_time=0.0,
            duration=1.0,
            properties={}
        )
        
        project.scene_builder.add_animation(test_animation)
        
        # Test code generation
        code = project.scene_builder.generate_manim_code()
        print("✓ Code generation successful")
        print("Generated code preview:")
        print(code[:200] + "..." if len(code) > 200 else code)
        
        return True
        
    except Exception as e:
        print(f"✗ Functionality test error: {e}")
        return False

if __name__ == "__main__":
    print("Testing Manim UI Builder...")
    print("=" * 40)
    
    success = True
    
    # Test imports
    success &= test_imports()
    
    # Test basic functionality
    success &= test_basic_functionality()
    
    print("=" * 40)
    if success:
        print("✓ All tests passed!")
        print("\nTo run the full application:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set GEMINI_API_KEY environment variable (optional)")
        print("3. Run: python main.py")
    else:
        print("✗ Some tests failed!")
        sys.exit(1)