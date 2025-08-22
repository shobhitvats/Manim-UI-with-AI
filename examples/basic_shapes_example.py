"""
Basic Shapes Example - Generated Manim Code
============================================

This example demonstrates basic shapes and animations created with Manim UI Builder.
"""

from manim import *

class BasicShapesScene(Scene):
    def construct(self):
        # Create objects
        circle = Circle(radius=1.0)
        circle.set_fill(BLUE, opacity=0.7)
        circle.set_stroke(WHITE, width=2)
        circle.move_to(LEFT * 2 + UP)
        
        square = Square(side_length=1.5)
        square.set_fill(RED, opacity=0.7)
        square.set_stroke(WHITE, width=2)
        square.move_to(RIGHT * 2 + UP)
        
        title = Text("Basic Shapes", font_size=48)
        title.set_color(WHITE)
        title.move_to(DOWN * 2)
        
        # Animate
        self.play(FadeIn(circle), run_time=1)
        self.play(FadeIn(square), run_time=1)
        self.play(Write(title), run_time=2)
        
        # Hold the final frame
        self.wait(1)

# To render this scene, run:
# manim -pql basic_shapes_example.py BasicShapesScene