"""
Manim Integration Module
========================

Handles integration with Manim for scene creation and rendering.
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# Try to import Manim
try:
    from manim import *
    MANIM_AVAILABLE = True
except ImportError:
    MANIM_AVAILABLE = False

@dataclass
class ManimObject:
    """Represents a Manim object in the scene."""
    object_id: str
    object_type: str
    display_name: str
    properties: Dict[str, Any]
    position: tuple = (0, 0, 0)
    
    def to_dict(self):
        """Convert to dictionary for serialization."""
        return {
            'object_id': self.object_id,
            'object_type': self.object_type,
            'display_name': self.display_name,
            'properties': self.properties,
            'position': self.position
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create from dictionary."""
        return cls(**data)

@dataclass
class Animation:
    """Represents an animation in the timeline."""
    animation_id: str
    object_id: str
    animation_type: str
    start_time: float
    duration: float
    properties: Dict[str, Any]
    
    def to_dict(self):
        """Convert to dictionary for serialization."""
        return {
            'animation_id': self.animation_id,
            'object_id': self.object_id,
            'animation_type': self.animation_type,
            'start_time': self.start_time,
            'duration': self.duration,
            'properties': self.properties
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create from dictionary."""
        return cls(**data)

class ManimSceneBuilder:
    """Builds Manim scenes from UI objects and animations."""
    
    def __init__(self):
        self.objects: Dict[str, ManimObject] = {}
        self.animations: List[Animation] = []
        self.scene_properties = {
            'background_color': '#2b2b2b',
            'camera_config': {},
            'resolution': '1920x1080',
            'frame_rate': 30
        }
    
    def add_object(self, manim_object: ManimObject):
        """Add a Manim object to the scene."""
        self.objects[manim_object.object_id] = manim_object
    
    def remove_object(self, object_id: str):
        """Remove a Manim object from the scene."""
        if object_id in self.objects:
            del self.objects[object_id]
            
            # Remove related animations
            self.animations = [anim for anim in self.animations if anim.object_id != object_id]
    
    def add_animation(self, animation: Animation):
        """Add an animation to the timeline."""
        self.animations.append(animation)
        
        # Sort animations by start time
        self.animations.sort(key=lambda a: a.start_time)
    
    def remove_animation(self, animation_id: str):
        """Remove an animation from the timeline."""
        self.animations = [anim for anim in self.animations if anim.animation_id != animation_id]
    
    def generate_manim_code(self) -> str:
        """Generate Manim Python code from the scene."""
        code_lines = [
            "from manim import *",
            "",
            "class GeneratedScene(Scene):",
            "    def construct(self):",
        ]
        
        # Create objects
        object_vars = {}
        for obj_id, obj in self.objects.items():
            var_name = f"obj_{obj_id.replace('-', '_')}"
            object_vars[obj_id] = var_name
            
            creation_code = self._generate_object_creation_code(obj, var_name)
            code_lines.extend([f"        {line}" for line in creation_code])
        
        code_lines.append("")
        
        # Group animations by time
        time_groups = {}
        for anim in self.animations:
            start_time = anim.start_time
            if start_time not in time_groups:
                time_groups[start_time] = []
            time_groups[start_time].append(anim)
        
        # Generate animations
        for start_time in sorted(time_groups.keys()):
            animations_at_time = time_groups[start_time]
            
            if len(animations_at_time) == 1:
                anim = animations_at_time[0]
                var_name = object_vars.get(anim.object_id, 'unknown_object')
                anim_code = self._generate_animation_code(anim, var_name)
                code_lines.append(f"        {anim_code}")
            else:
                # Multiple animations at the same time
                anim_calls = []
                for anim in animations_at_time:
                    var_name = object_vars.get(anim.object_id, 'unknown_object')
                    anim_code = self._generate_animation_code(anim, var_name)
                    anim_calls.append(anim_code)
                
                code_lines.append(f"        self.play({', '.join(anim_calls)})")
        
        return "\n".join(code_lines)
    
    def _generate_object_creation_code(self, obj: ManimObject, var_name: str) -> List[str]:
        """Generate code for creating a Manim object."""
        lines = []
        
        # Basic object creation
        if obj.object_type == "Circle":
            radius = obj.properties.get('radius', 1.0)
            lines.append(f"{var_name} = Circle(radius={radius})")
        elif obj.object_type == "Square":
            side_length = obj.properties.get('side_length', 2.0)
            lines.append(f"{var_name} = Square(side_length={side_length})")
        elif obj.object_type == "Rectangle":
            width = obj.properties.get('width', 2.0)
            height = obj.properties.get('height', 1.0)
            lines.append(f"{var_name} = Rectangle(width={width}, height={height})")
        elif obj.object_type == "Text":
            text = obj.properties.get('text', 'Sample Text')
            font_size = obj.properties.get('font_size', 48)
            lines.append(f'{var_name} = Text("{text}", font_size={font_size})')
        elif obj.object_type == "Tex":
            tex = obj.properties.get('tex', 'x^2')
            lines.append(f'{var_name} = Tex(r"{tex}")')
        elif obj.object_type == "MathTex":
            math_tex = obj.properties.get('math_tex', 'f(x) = x^2')
            lines.append(f'{var_name} = MathTex(r"{math_tex}")')
        else:
            # Generic object
            lines.append(f"{var_name} = {obj.object_type}()")
        
        # Set properties
        if 'fill_color' in obj.properties:
            color = obj.properties['fill_color']
            if hasattr(color, 'name'):
                lines.append(f"{var_name}.set_fill({color.name().upper()})")
            else:
                lines.append(f"{var_name}.set_fill(BLUE)")  # Default
        
        if 'stroke_color' in obj.properties:
            color = obj.properties['stroke_color']
            if hasattr(color, 'name'):
                lines.append(f"{var_name}.set_stroke({color.name().upper()})")
            else:
                lines.append(f"{var_name}.set_stroke(WHITE)")  # Default
        
        # Set position
        x, y, z = obj.position
        if x != 0 or y != 0 or z != 0:
            lines.append(f"{var_name}.move_to(np.array([{x}, {y}, {z}]))")
        
        return lines
    
    def _generate_animation_code(self, anim: Animation, var_name: str) -> str:
        """Generate code for an animation."""
        anim_type = anim.animation_type
        duration = anim.duration
        
        if anim_type == "FadeIn":
            return f"FadeIn({var_name}, run_time={duration})"
        elif anim_type == "FadeOut":
            return f"FadeOut({var_name}, run_time={duration})"
        elif anim_type == "Write":
            return f"Write({var_name}, run_time={duration})"
        elif anim_type == "Unwrite":
            return f"Unwrite({var_name}, run_time={duration})"
        elif anim_type == "DrawBorderThenFill":
            return f"DrawBorderThenFill({var_name}, run_time={duration})"
        elif anim_type == "MoveTo":
            target = anim.properties.get('target', [0, 0, 0])
            return f"{var_name}.animate.move_to(np.array({target}))"
        elif anim_type == "Rotate":
            angle = anim.properties.get('angle', PI/2)
            return f"{var_name}.animate.rotate({angle})"
        elif anim_type == "Scale":
            factor = anim.properties.get('factor', 1.5)
            return f"{var_name}.animate.scale({factor})"
        else:
            return f"{anim_type}({var_name}, run_time={duration})"
    
    def render_scene(self, output_path: str, quality: str = 'medium_quality') -> bool:
        """Render the scene to a video file."""
        if not MANIM_AVAILABLE:
            return False
        
        try:
            # Generate code
            code = self.generate_manim_code()
            
            # Create temporary Python file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            # Run Manim
            cmd = [
                sys.executable, '-m', 'manim',
                temp_file, 'GeneratedScene',
                f'--{quality}',
                '--output_file', output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Clean up
            os.unlink(temp_file)
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"Error rendering scene: {e}")
            return False
    
    def save_project(self, file_path: str):
        """Save the project to a JSON file."""
        project_data = {
            'objects': {obj_id: obj.to_dict() for obj_id, obj in self.objects.items()},
            'animations': [anim.to_dict() for anim in self.animations],
            'scene_properties': self.scene_properties,
            'version': '1.0'
        }
        
        with open(file_path, 'w') as f:
            import json
            json.dump(project_data, f, indent=2, default=str)
    
    def load_project(self, file_path: str):
        """Load a project from a JSON file."""
        with open(file_path, 'r') as f:
            import json
            project_data = json.load(f)
        
        # Load objects
        self.objects = {}
        for obj_id, obj_data in project_data.get('objects', {}).items():
            self.objects[obj_id] = ManimObject.from_dict(obj_data)
        
        # Load animations
        self.animations = []
        for anim_data in project_data.get('animations', []):
            self.animations.append(Animation.from_dict(anim_data))
        
        # Load scene properties
        self.scene_properties = project_data.get('scene_properties', self.scene_properties)

class ManimRenderer:
    """Handles rendering of Manim scenes."""
    
    def __init__(self):
        self.output_dir = tempfile.mkdtemp(prefix='manim_ui_')
    
    def render_preview(self, scene_builder: ManimSceneBuilder) -> Optional[str]:
        """Render a preview of the scene."""
        if not MANIM_AVAILABLE:
            return None
        
        try:
            # Generate low quality preview
            preview_path = os.path.join(self.output_dir, 'preview.mp4')
            success = scene_builder.render_scene(preview_path, 'low_quality')
            
            return preview_path if success else None
            
        except Exception as e:
            print(f"Error rendering preview: {e}")
            return None
    
    def export_video(self, scene_builder: ManimSceneBuilder, output_path: str, quality: str = 'high_quality') -> bool:
        """Export the scene as a video."""
        return scene_builder.render_scene(output_path, quality)
    
    def export_gif(self, scene_builder: ManimSceneBuilder, output_path: str) -> bool:
        """Export the scene as a GIF."""
        # First render as video, then convert to GIF
        temp_video = os.path.join(self.output_dir, 'temp_video.mp4')
        
        if scene_builder.render_scene(temp_video, 'medium_quality'):
            try:
                # Convert to GIF using ffmpeg (if available)
                cmd = [
                    'ffmpeg', '-i', temp_video, '-vf',
                    'fps=15,scale=640:-1:flags=lanczos,palettegen',
                    '-y', output_path.replace('.gif', '_palette.png')
                ]
                subprocess.run(cmd, check=True)
                
                cmd = [
                    'ffmpeg', '-i', temp_video, '-i', output_path.replace('.gif', '_palette.png'),
                    '-lavfi', 'fps=15,scale=640:-1:flags=lanczos[x];[x][1:v]paletteuse',
                    '-y', output_path
                ]
                subprocess.run(cmd, check=True)
                
                # Clean up
                os.unlink(temp_video)
                os.unlink(output_path.replace('.gif', '_palette.png'))
                
                return True
                
            except subprocess.CalledProcessError:
                return False
        
        return False