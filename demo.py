#!/usr/bin/env python3
"""
Manim UI Builder Demo
=====================

Demonstrates the core functionality without requiring GUI dependencies.
"""

import sys
import os
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def demo_project_creation():
    """Demonstrate project creation and manipulation."""
    print("🎨 Creating a new project...")
    
    from manim_ui.core.project import ProjectManager
    from manim_ui.core.manim_integration import ManimObject, Animation
    
    # Create project manager and new project
    manager = ProjectManager()
    project = manager.new_project("Demo Animation")
    
    print(f"✅ Created project: {project.name}")
    
    # Add some objects
    circle = ManimObject(
        object_id="circle-1",
        object_type="Circle",
        display_name="Blue Circle",
        properties={
            'radius': 1.5,
            'fill_color': 'blue',
            'stroke_color': 'white',
            'stroke_width': 2.0
        },
        position=(-2, 0, 0)
    )
    
    text = ManimObject(
        object_id="text-1",
        object_type="Text",
        display_name="Welcome Text",
        properties={
            'text': 'Welcome to Manim UI!',
            'font_size': 48,
            'text_color': 'white'
        },
        position=(0, -2, 0)
    )
    
    project.scene_builder.add_object(circle)
    project.scene_builder.add_object(text)
    
    print(f"✅ Added {project.get_object_count()} objects to the scene")
    
    # Add animations
    fade_in_circle = Animation(
        animation_id="anim-1",
        object_id="circle-1",
        animation_type="FadeIn",
        start_time=0.0,
        duration=1.0,
        properties={}
    )
    
    write_text = Animation(
        animation_id="anim-2", 
        object_id="text-1",
        animation_type="Write",
        start_time=1.0,
        duration=2.0,
        properties={}
    )
    
    project.scene_builder.add_animation(fade_in_circle)
    project.scene_builder.add_animation(write_text)
    
    print(f"✅ Added {project.get_animation_count()} animations")
    print(f"📏 Total duration: {project.get_duration():.1f} seconds")
    
    return project

def demo_code_generation(project):
    """Demonstrate Manim code generation."""
    print("\n🐍 Generating Manim code...")
    
    code = project.scene_builder.generate_manim_code()
    
    print("✅ Generated Manim code:")
    print("-" * 50)
    print(code)
    print("-" * 50)
    
    return code

def demo_project_save_load(project):
    """Demonstrate project save and load."""
    print("\n💾 Testing project save/load...")
    
    # Save project
    demo_file = "demo_project.json"
    success = project.save(demo_file)
    
    if success:
        print(f"✅ Saved project to {demo_file}")
        
        # Load project
        from manim_ui.core.project import ProjectManager
        manager = ProjectManager()
        loaded_project = manager.open_project(demo_file)
        
        if loaded_project:
            print(f"✅ Loaded project: {loaded_project.name}")
            print(f"   Objects: {loaded_project.get_object_count()}")
            print(f"   Animations: {loaded_project.get_animation_count()}")
            print(f"   Duration: {loaded_project.get_duration():.1f}s")
            
            # Clean up
            os.unlink(demo_file)
            return True
        else:
            print("❌ Failed to load project")
            return False
    else:
        print("❌ Failed to save project")
        return False

def demo_ai_integration():
    """Demonstrate AI integration concepts."""
    print("\n🤖 AI Integration Demo...")
    
    # Show example prompts and expected outputs
    example_prompts = [
        {
            "prompt": "Create a sine wave that grows in amplitude",
            "description": "Would generate a parametric function with animation"
        },
        {
            "prompt": "Show the Pythagorean theorem with squares on triangle sides",
            "description": "Would create geometric proof visualization"
        },
        {
            "prompt": "Animate text that writes 'Hello World' and then transforms to 'Welcome!'",
            "description": "Would create text animation sequence"
        }
    ]
    
    print("Example AI prompts supported:")
    for i, example in enumerate(example_prompts, 1):
        print(f"  {i}. '{example['prompt']}'")
        print(f"     → {example['description']}")
    
    # Check if Gemini is available
    gemini_available = os.getenv('GEMINI_API_KEY') is not None
    
    if gemini_available:
        print("✅ Gemini API key found - AI features available")
        
        try:
            import google.generativeai as genai
            print("✅ Gemini SDK available")
        except ImportError:
            print("⚠️  Gemini SDK not installed (pip install google-generativeai)")
    else:
        print("ℹ️  Set GEMINI_API_KEY environment variable to enable AI features")
    
    return gemini_available

def demo_export_capabilities():
    """Demonstrate export capabilities."""
    print("\n📤 Export Capabilities Demo...")
    
    export_formats = [
        ("MP4 Video", ".mp4", "High-quality video export using Manim renderer"),
        ("GIF Animation", ".gif", "Optimized GIF for web and social media"),
        ("Python Code", ".py", "Complete Manim script for further customization"),
        ("Project File", ".json", "Save/load project with all settings and animations")
    ]
    
    print("Supported export formats:")
    for name, ext, description in export_formats:
        print(f"  • {name} ({ext}): {description}")
    
    print("\nExport quality options:")
    print("  • Low Quality: Fast preview rendering")
    print("  • Medium Quality: Balanced quality and speed")
    print("  • High Quality: Production-ready output")

def main():
    """Run the demo."""
    print("🎬 Manim UI Builder - Functionality Demo")
    print("=" * 50)
    
    try:
        # Demo project creation
        project = demo_project_creation()
        
        # Demo code generation
        demo_code_generation(project)
        
        # Demo save/load
        demo_project_save_load(project)
        
        # Demo AI integration
        demo_ai_integration()
        
        # Demo export capabilities
        demo_export_capabilities()
        
        print("\n" + "=" * 50)
        print("🎉 Demo completed successfully!")
        print("\nTo run the full application with GUI:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Run: python main.py")
        print("\nTo set up AI features:")
        print("  1. Get Gemini API key: https://makersuite.google.com/app/apikey")
        print("  2. Set environment variable: export GEMINI_API_KEY=your-key")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)