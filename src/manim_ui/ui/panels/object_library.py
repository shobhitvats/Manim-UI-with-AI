"""
Object Library Panel
====================

Panel containing draggable Manim objects (shapes, text, etc.)
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QGroupBox, QGridLayout, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt, pyqtSignal, QMimeData
from PyQt6.QtGui import QDrag, QPainter, QPixmap

class DraggableObjectItem(QListWidgetItem):
    """A draggable item representing a Manim object."""
    
    def __init__(self, object_type, display_name, icon_path=None):
        super().__init__(display_name)
        self.object_type = object_type
        self.display_name = display_name
        
        # Set item properties
        self.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsDragEnabled)
        
        # TODO: Set icon if provided
        if icon_path:
            pass  # self.setIcon(QIcon(icon_path))

class ObjectLibraryList(QListWidget):
    """List widget with drag and drop support for Manim objects."""
    
    object_dragged = pyqtSignal(str, str)  # object_type, display_name
    
    def __init__(self):
        super().__init__()
        
        # Enable drag and drop
        self.setDragDropMode(QListWidget.DragDropMode.DragOnly)
        self.setDefaultDropAction(Qt.DropAction.CopyAction)
    
    def startDrag(self, supportedActions):
        """Start drag operation for an object."""
        item = self.currentItem()
        if not item:
            return
        
        # Create drag object
        drag = QDrag(self)
        mimeData = QMimeData()
        
        # Set mime data for the object
        mimeData.setText(f"{item.object_type}:{item.display_name}")
        mimeData.setData("application/x-manim-object", item.object_type.encode())
        drag.setMimeData(mimeData)
        
        # Create drag pixmap (simple text for now)
        pixmap = QPixmap(100, 30)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setPen(Qt.GlobalColor.white)
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, item.display_name)
        painter.end()
        drag.setPixmap(pixmap)
        
        # Emit signal
        self.object_dragged.emit(item.object_type, item.display_name)
        
        # Start the drag
        drag.exec(supportedActions)

class ObjectLibraryPanel(QWidget):
    """Panel containing the object library with categorized Manim objects."""
    
    def __init__(self):
        super().__init__()
        
        self.setMinimumWidth(200)
        self._setup_ui()
        self._populate_objects()
    
    def _setup_ui(self):
        """Setup the user interface."""
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("Object Library")
        title_label.setStyleSheet("font-weight: bold; font-size: 14px; padding: 5px;")
        layout.addWidget(title_label)
        
        # Scroll area for object categories
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Container widget for scroll area
        container = QWidget()
        container_layout = QVBoxLayout(container)
        
        # Basic Objects group
        self.basic_group = self._create_object_group("Basic Objects")
        container_layout.addWidget(self.basic_group)
        
        # Text Objects group
        self.text_group = self._create_object_group("Text & LaTeX")
        container_layout.addWidget(self.text_group)
        
        # Shapes group
        self.shapes_group = self._create_object_group("Shapes")
        container_layout.addWidget(self.shapes_group)
        
        # Graphs group
        self.graphs_group = self._create_object_group("Graphs & Plots")
        container_layout.addWidget(self.graphs_group)
        
        # Arrows group
        self.arrows_group = self._create_object_group("Arrows & Vectors")
        container_layout.addWidget(self.arrows_group)
        
        # 3D Objects group
        self.objects_3d_group = self._create_object_group("3D Objects")
        container_layout.addWidget(self.objects_3d_group)
        
        container_layout.addStretch()
        
        scroll_area.setWidget(container)
        layout.addWidget(scroll_area)
    
    def _create_object_group(self, title):
        """Create a collapsible group for object categories."""
        group = QGroupBox(title)
        group.setCheckable(True)
        group.setChecked(True)  # Expanded by default
        
        layout = QVBoxLayout(group)
        
        # Create list widget for this group
        list_widget = ObjectLibraryList()
        layout.addWidget(list_widget)
        
        return group
    
    def _populate_objects(self):
        """Populate the object library with available Manim objects."""
        # Basic Objects
        basic_list = self.basic_group.findChild(ObjectLibraryList)
        basic_objects = [
            ("Dot", "Dot"),
            ("Point", "Point"),
            ("VGroup", "Group"),
        ]
        
        for obj_type, display_name in basic_objects:
            item = DraggableObjectItem(obj_type, display_name)
            basic_list.addItem(item)
        
        # Text & LaTeX
        text_list = self.text_group.findChild(ObjectLibraryList)
        text_objects = [
            ("Text", "Text"),
            ("Tex", "LaTeX"),
            ("MathTex", "Math LaTeX"),
            ("Title", "Title"),
            ("Paragraph", "Paragraph"),
        ]
        
        for obj_type, display_name in text_objects:
            item = DraggableObjectItem(obj_type, display_name)
            text_list.addItem(item)
        
        # Shapes
        shapes_list = self.shapes_group.findChild(ObjectLibraryList)
        shapes = [
            ("Circle", "Circle"),
            ("Square", "Square"),
            ("Rectangle", "Rectangle"),
            ("Triangle", "Triangle"),
            ("Polygon", "Polygon"),
            ("Line", "Line"),
            ("Ellipse", "Ellipse"),
            ("Arc", "Arc"),
        ]
        
        for obj_type, display_name in shapes:
            item = DraggableObjectItem(obj_type, display_name)
            shapes_list.addItem(item)
        
        # Graphs & Plots
        graphs_list = self.graphs_group.findChild(ObjectLibraryList)
        graphs = [
            ("Axes", "Axes"),
            ("NumberPlane", "Number Plane"),
            ("FunctionGraph", "Function Graph"),
            ("ParametricFunction", "Parametric Curve"),
            ("ImplicitFunction", "Implicit Function"),
            ("BarChart", "Bar Chart"),
        ]
        
        for obj_type, display_name in graphs:
            item = DraggableObjectItem(obj_type, display_name)
            graphs_list.addItem(item)
        
        # Arrows & Vectors
        arrows_list = self.arrows_group.findChild(ObjectLibraryList)
        arrows = [
            ("Arrow", "Arrow"),
            ("Vector", "Vector"),
            ("DoubleArrow", "Double Arrow"),
            ("CurvedArrow", "Curved Arrow"),
            ("VectorField", "Vector Field"),
        ]
        
        for obj_type, display_name in arrows:
            item = DraggableObjectItem(obj_type, display_name)
            arrows_list.addItem(item)
        
        # 3D Objects
        objects_3d_list = self.objects_3d_group.findChild(ObjectLibraryList)
        objects_3d = [
            ("Sphere", "Sphere"),
            ("Cube", "Cube"),
            ("Cylinder", "Cylinder"),
            ("Cone", "Cone"),
            ("Surface", "Surface"),
            ("ThreeDAxes", "3D Axes"),
        ]
        
        for obj_type, display_name in objects_3d:
            item = DraggableObjectItem(obj_type, display_name)
            objects_3d_list.addItem(item)