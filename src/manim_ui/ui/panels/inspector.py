"""
Inspector Panel
===============

Properties inspector for selected Manim objects.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QCheckBox,
    QSlider, QColorDialog, QGroupBox, QFormLayout, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QPalette

class ColorPicker(QPushButton):
    """Custom color picker button."""
    
    color_changed = pyqtSignal(QColor)
    
    def __init__(self, initial_color=QColor(255, 255, 255)):
        super().__init__()
        
        self.current_color = initial_color
        self.setFixedSize(40, 25)
        self.update_color_display()
        
        self.clicked.connect(self.pick_color)
    
    def update_color_display(self):
        """Update the button appearance to show the current color."""
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: rgb({self.current_color.red()}, 
                                     {self.current_color.green()}, 
                                     {self.current_color.blue()});
                border: 1px solid #555555;
                border-radius: 2px;
            }}
        """)
    
    def pick_color(self):
        """Open color picker dialog."""
        color = QColorDialog.getColor(self.current_color, self)
        if color.isValid():
            self.current_color = color
            self.update_color_display()
            self.color_changed.emit(color)
    
    def set_color(self, color):
        """Set the color programmatically."""
        self.current_color = color
        self.update_color_display()

class PropertyGroup(QGroupBox):
    """Base class for property groups in the inspector."""
    
    def __init__(self, title):
        super().__init__(title)
        
        self.layout = QFormLayout(self)
        self.layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        
        # Store property widgets for easy access
        self.property_widgets = {}
    
    def add_property(self, name, widget, label=None):
        """Add a property widget to the group."""
        if label is None:
            label = name.replace('_', ' ').title()
        
        self.property_widgets[name] = widget
        self.layout.addRow(QLabel(label + ":"), widget)
    
    def get_property_value(self, name):
        """Get the current value of a property."""
        widget = self.property_widgets.get(name)
        if widget is None:
            return None
        
        if isinstance(widget, (QSpinBox, QDoubleSpinBox)):
            return widget.value()
        elif isinstance(widget, QLineEdit):
            return widget.text()
        elif isinstance(widget, QComboBox):
            return widget.currentText()
        elif isinstance(widget, QCheckBox):
            return widget.isChecked()
        elif isinstance(widget, ColorPicker):
            return widget.current_color
        elif isinstance(widget, QSlider):
            return widget.value()
        else:
            return None
    
    def set_property_value(self, name, value):
        """Set the value of a property."""
        widget = self.property_widgets.get(name)
        if widget is None:
            return
        
        if isinstance(widget, (QSpinBox, QDoubleSpinBox)):
            widget.setValue(value)
        elif isinstance(widget, QLineEdit):
            widget.setText(str(value))
        elif isinstance(widget, QComboBox):
            index = widget.findText(str(value))
            if index >= 0:
                widget.setCurrentIndex(index)
        elif isinstance(widget, QCheckBox):
            widget.setChecked(bool(value))
        elif isinstance(widget, ColorPicker):
            if isinstance(value, QColor):
                widget.set_color(value)
        elif isinstance(widget, QSlider):
            widget.setValue(int(value))

class TransformGroup(PropertyGroup):
    """Property group for transform properties (position, rotation, scale)."""
    
    def __init__(self):
        super().__init__("Transform")
        
        # Position
        self.x_spin = QDoubleSpinBox()
        self.x_spin.setRange(-1000, 1000)
        self.x_spin.setSingleStep(0.1)
        self.add_property("x", self.x_spin, "X Position")
        
        self.y_spin = QDoubleSpinBox()
        self.y_spin.setRange(-1000, 1000)
        self.y_spin.setSingleStep(0.1)
        self.add_property("y", self.y_spin, "Y Position")
        
        self.z_spin = QDoubleSpinBox()
        self.z_spin.setRange(-1000, 1000)
        self.z_spin.setSingleStep(0.1)
        self.add_property("z", self.z_spin, "Z Position")
        
        # Rotation
        self.rotation_spin = QDoubleSpinBox()
        self.rotation_spin.setRange(-360, 360)
        self.rotation_spin.setSuffix("°")
        self.rotation_spin.setSingleStep(1.0)
        self.add_property("rotation", self.rotation_spin, "Rotation")
        
        # Scale
        self.scale_x_spin = QDoubleSpinBox()
        self.scale_x_spin.setRange(0.01, 100)
        self.scale_x_spin.setValue(1.0)
        self.scale_x_spin.setSingleStep(0.1)
        self.add_property("scale_x", self.scale_x_spin, "Scale X")
        
        self.scale_y_spin = QDoubleSpinBox()
        self.scale_y_spin.setRange(0.01, 100)
        self.scale_y_spin.setValue(1.0)
        self.scale_y_spin.setSingleStep(0.1)
        self.add_property("scale_y", self.scale_y_spin, "Scale Y")

class AppearanceGroup(PropertyGroup):
    """Property group for appearance properties (color, opacity, etc.)."""
    
    def __init__(self):
        super().__init__("Appearance")
        
        # Fill color
        self.fill_color = ColorPicker(QColor(100, 100, 255))
        self.add_property("fill_color", self.fill_color, "Fill Color")
        
        # Stroke color
        self.stroke_color = ColorPicker(QColor(255, 255, 255))
        self.add_property("stroke_color", self.stroke_color, "Stroke Color")
        
        # Stroke width
        self.stroke_width_spin = QDoubleSpinBox()
        self.stroke_width_spin.setRange(0, 20)
        self.stroke_width_spin.setValue(2.0)
        self.stroke_width_spin.setSingleStep(0.1)
        self.add_property("stroke_width", self.stroke_width_spin, "Stroke Width")
        
        # Opacity
        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setRange(0, 100)
        self.opacity_slider.setValue(100)
        self.add_property("opacity", self.opacity_slider, "Opacity (%)")

class TextGroup(PropertyGroup):
    """Property group for text properties."""
    
    def __init__(self):
        super().__init__("Text")
        
        # Text content
        self.text_edit = QLineEdit()
        self.text_edit.setPlaceholderText("Enter text...")
        self.add_property("text", self.text_edit, "Content")
        
        # Font family
        self.font_combo = QComboBox()
        fonts = ["Arial", "Times", "Helvetica", "Courier", "Comic Sans MS"]
        self.font_combo.addItems(fonts)
        self.add_property("font_family", self.font_combo, "Font")
        
        # Font size
        self.font_size_spin = QDoubleSpinBox()
        self.font_size_spin.setRange(8, 100)
        self.font_size_spin.setValue(48)
        self.font_size_spin.setSuffix(" pt")
        self.add_property("font_size", self.font_size_spin, "Size")
        
        # Text color
        self.text_color = ColorPicker(QColor(255, 255, 255))
        self.add_property("text_color", self.text_color, "Color")

class ShapeGroup(PropertyGroup):
    """Property group for shape-specific properties."""
    
    def __init__(self):
        super().__init__("Shape")
        
        # Width (for rectangles, etc.)
        self.width_spin = QDoubleSpinBox()
        self.width_spin.setRange(0.1, 100)
        self.width_spin.setValue(2.0)
        self.width_spin.setSingleStep(0.1)
        self.add_property("width", self.width_spin, "Width")
        
        # Height (for rectangles, etc.)
        self.height_spin = QDoubleSpinBox()
        self.height_spin.setRange(0.1, 100)
        self.height_spin.setValue(2.0)
        self.height_spin.setSingleStep(0.1)
        self.add_property("height", self.height_spin, "Height")
        
        # Radius (for circles, etc.)
        self.radius_spin = QDoubleSpinBox()
        self.radius_spin.setRange(0.1, 100)
        self.radius_spin.setValue(1.0)
        self.radius_spin.setSingleStep(0.1)
        self.add_property("radius", self.radius_spin, "Radius")
        
        # Fill
        self.fill_checkbox = QCheckBox()
        self.fill_checkbox.setChecked(True)
        self.add_property("fill", self.fill_checkbox, "Fill")

class InspectorPanel(QWidget):
    """Properties inspector panel for selected objects."""
    
    property_changed = pyqtSignal(str, str, object)  # object_id, property_name, value
    
    def __init__(self):
        super().__init__()
        
        self.current_object = None
        self.property_groups = {}
        
        self.setMinimumWidth(250)
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        """Setup the user interface."""
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("Inspector")
        title_label.setStyleSheet("font-weight: bold; font-size: 14px; padding: 5px;")
        layout.addWidget(title_label)
        
        # Object info
        self.object_info_label = QLabel("No object selected")
        self.object_info_label.setStyleSheet("color: #888888; padding: 5px;")
        layout.addWidget(self.object_info_label)
        
        # Scroll area for properties
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Container for property groups
        self.properties_container = QWidget()
        self.properties_layout = QVBoxLayout(self.properties_container)
        self.properties_layout.setContentsMargins(5, 5, 5, 5)
        
        # Create property groups
        self.transform_group = TransformGroup()
        self.appearance_group = AppearanceGroup()
        self.text_group = TextGroup()
        self.shape_group = ShapeGroup()
        
        # Add groups to layout
        self.properties_layout.addWidget(self.transform_group)
        self.properties_layout.addWidget(self.appearance_group)
        self.properties_layout.addWidget(self.text_group)
        self.properties_layout.addWidget(self.shape_group)
        self.properties_layout.addStretch()
        
        # Store groups for easy access
        self.property_groups = {
            'transform': self.transform_group,
            'appearance': self.appearance_group,
            'text': self.text_group,
            'shape': self.shape_group
        }
        
        scroll_area.setWidget(self.properties_container)
        layout.addWidget(scroll_area)
        
        # Initially hide all groups
        self._hide_all_groups()
    
    def _connect_signals(self):
        """Connect signals from property widgets."""
        # Transform group
        self.transform_group.x_spin.valueChanged.connect(
            lambda v: self._emit_property_changed('x', v))
        self.transform_group.y_spin.valueChanged.connect(
            lambda v: self._emit_property_changed('y', v))
        self.transform_group.z_spin.valueChanged.connect(
            lambda v: self._emit_property_changed('z', v))
        self.transform_group.rotation_spin.valueChanged.connect(
            lambda v: self._emit_property_changed('rotation', v))
        self.transform_group.scale_x_spin.valueChanged.connect(
            lambda v: self._emit_property_changed('scale_x', v))
        self.transform_group.scale_y_spin.valueChanged.connect(
            lambda v: self._emit_property_changed('scale_y', v))
        
        # Appearance group
        self.appearance_group.fill_color.color_changed.connect(
            lambda c: self._emit_property_changed('fill_color', c))
        self.appearance_group.stroke_color.color_changed.connect(
            lambda c: self._emit_property_changed('stroke_color', c))
        self.appearance_group.stroke_width_spin.valueChanged.connect(
            lambda v: self._emit_property_changed('stroke_width', v))
        self.appearance_group.opacity_slider.valueChanged.connect(
            lambda v: self._emit_property_changed('opacity', v))
        
        # Text group
        self.text_group.text_edit.textChanged.connect(
            lambda t: self._emit_property_changed('text', t))
        self.text_group.font_combo.currentTextChanged.connect(
            lambda f: self._emit_property_changed('font_family', f))
        self.text_group.font_size_spin.valueChanged.connect(
            lambda s: self._emit_property_changed('font_size', s))
        self.text_group.text_color.color_changed.connect(
            lambda c: self._emit_property_changed('text_color', c))
        
        # Shape group
        self.shape_group.width_spin.valueChanged.connect(
            lambda v: self._emit_property_changed('width', v))
        self.shape_group.height_spin.valueChanged.connect(
            lambda v: self._emit_property_changed('height', v))
        self.shape_group.radius_spin.valueChanged.connect(
            lambda v: self._emit_property_changed('radius', v))
        self.shape_group.fill_checkbox.toggled.connect(
            lambda v: self._emit_property_changed('fill', v))
    
    def _emit_property_changed(self, property_name, value):
        """Emit property changed signal."""
        if self.current_object:
            object_id = getattr(self.current_object, 'object_id', str(id(self.current_object)))
            self.property_changed.emit(object_id, property_name, value)
    
    def _hide_all_groups(self):
        """Hide all property groups."""
        for group in self.property_groups.values():
            group.hide()
    
    def _show_groups_for_object_type(self, object_type):
        """Show relevant property groups for the given object type."""
        self._hide_all_groups()
        
        # Always show transform and appearance
        self.transform_group.show()
        self.appearance_group.show()
        
        # Show type-specific groups
        if object_type in ["Text", "Tex", "MathTex", "Title", "Paragraph"]:
            self.text_group.show()
        elif object_type in ["Circle", "Square", "Rectangle", "Triangle", "Polygon", "Ellipse"]:
            self.shape_group.show()
    
    def set_selected_object(self, obj):
        """Set the currently selected object for inspection."""
        self.current_object = obj
        
        if obj is None:
            self.object_info_label.setText("No object selected")
            self._hide_all_groups()
        else:
            # Update object info
            object_type = getattr(obj, 'object_type', 'Unknown')
            display_name = getattr(obj, 'display_name', 'Object')
            self.object_info_label.setText(f"Selected: {display_name} ({object_type})")
            
            # Show relevant property groups
            self._show_groups_for_object_type(object_type)
            
            # Load current properties
            self._load_object_properties(obj)
    
    def _load_object_properties(self, obj):
        """Load the object's current properties into the inspector."""
        # TODO: Extract properties from the actual object
        # For now, we'll use default values
        
        # Transform properties
        pos = getattr(obj, 'pos', lambda: (0, 0))()
        if hasattr(pos, 'x') and hasattr(pos, 'y'):
            self.transform_group.set_property_value('x', pos.x())
            self.transform_group.set_property_value('y', pos.y())
        
        # Appearance properties from object
        if hasattr(obj, 'pen_color'):
            self.appearance_group.set_property_value('stroke_color', obj.pen_color)
        if hasattr(obj, 'fill_color'):
            self.appearance_group.set_property_value('fill_color', obj.fill_color)
        if hasattr(obj, 'pen_width'):
            self.appearance_group.set_property_value('stroke_width', obj.pen_width)
    
    def update_object_property(self, object_id, property_name, value):
        """Update a property of the current object."""
        if not self.current_object:
            return
        
        current_id = getattr(self.current_object, 'object_id', str(id(self.current_object)))
        if current_id != object_id:
            return
        
        # Update the object's property
        # TODO: Apply the property change to the actual Manim object
        
        # Update visual representation
        if hasattr(self.current_object, 'update'):
            self.current_object.update()