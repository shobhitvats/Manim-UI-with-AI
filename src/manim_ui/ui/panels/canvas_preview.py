"""
Canvas Preview Panel
====================

Interactive canvas for previewing and editing Manim scenes.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGraphicsView, QGraphicsScene, QGraphicsItem, QGraphicsEllipseItem,
    QGraphicsRectItem, QGraphicsTextItem, QMenu
)
from PyQt6.QtCore import Qt, QRectF, QPointF, pyqtSignal
from PyQt6.QtGui import QPen, QBrush, QColor, QFont, QAction

class ManimObjectItem(QGraphicsItem):
    """Base class for Manim objects in the graphics scene."""
    
    def __init__(self, object_type, display_name):
        super().__init__()
        
        self.object_type = object_type
        self.display_name = display_name
        
        # Make item movable and selectable
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        
        # Default properties
        self.pen_color = QColor(255, 255, 255)
        self.fill_color = QColor(100, 100, 255, 100)
        self.pen_width = 2
    
    def boundingRect(self):
        """Return the bounding rectangle of the item."""
        return QRectF(-50, -50, 100, 100)
    
    def paint(self, painter, option, widget):
        """Paint the item - to be overridden by subclasses."""
        # Default implementation draws a placeholder rectangle
        painter.setPen(QPen(self.pen_color, self.pen_width))
        painter.setBrush(QBrush(self.fill_color))
        painter.drawRect(self.boundingRect())
        
        # Draw label
        painter.setPen(QPen(QColor(255, 255, 255)))
        painter.setFont(QFont("Arial", 8))
        painter.drawText(self.boundingRect(), Qt.AlignmentFlag.AlignCenter, self.display_name)

class CircleItem(ManimObjectItem):
    """Graphics item representing a Manim Circle."""
    
    def paint(self, painter, option, widget):
        painter.setPen(QPen(self.pen_color, self.pen_width))
        painter.setBrush(QBrush(self.fill_color))
        painter.drawEllipse(self.boundingRect())

class RectangleItem(ManimObjectItem):
    """Graphics item representing a Manim Rectangle."""
    
    def paint(self, painter, option, widget):
        painter.setPen(QPen(self.pen_color, self.pen_width))
        painter.setBrush(QBrush(self.fill_color))
        painter.drawRect(self.boundingRect())

class TextItem(ManimObjectItem):
    """Graphics item representing Manim Text."""
    
    def __init__(self, object_type, display_name, text="Sample Text"):
        super().__init__(object_type, display_name)
        self.text = text
    
    def paint(self, painter, option, widget):
        painter.setPen(QPen(self.pen_color, self.pen_width))
        painter.setFont(QFont("Arial", 16))
        painter.drawText(self.boundingRect(), Qt.AlignmentFlag.AlignCenter, self.text)

class ManimCanvas(QGraphicsView):
    """Graphics view for displaying and editing Manim scenes."""
    
    object_selected = pyqtSignal(object)  # Emitted when an object is selected
    object_moved = pyqtSignal(object, QPointF)  # Emitted when an object is moved
    
    def __init__(self):
        super().__init__()
        
        # Create scene
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        
        # Configure view
        self.setRenderHint(self.renderHints() | self.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.setAcceptDrops(True)
        
        # Scene properties
        self.scene.setSceneRect(-400, -300, 800, 600)  # Standard Manim aspect ratio
        self.scene.setBackgroundBrush(QBrush(QColor(40, 40, 40)))
        
        # Grid
        self._draw_grid()
        
        # Connect signals
        self.scene.selectionChanged.connect(self._on_selection_changed)
    
    def _draw_grid(self):
        """Draw a grid on the canvas."""
        pen = QPen(QColor(80, 80, 80))
        pen.setWidth(1)
        
        # Vertical lines
        for x in range(-400, 401, 50):
            self.scene.addLine(x, -300, x, 300, pen)
        
        # Horizontal lines
        for y in range(-300, 301, 50):
            self.scene.addLine(-400, y, 400, y, pen)
        
        # Axes
        axes_pen = QPen(QColor(120, 120, 120))
        axes_pen.setWidth(2)
        self.scene.addLine(0, -300, 0, 300, axes_pen)  # Y-axis
        self.scene.addLine(-400, 0, 400, 0, axes_pen)  # X-axis
    
    def dragEnterEvent(self, event):
        """Handle drag enter events for object drops."""
        if event.mimeData().hasText() or event.mimeData().hasFormat("application/x-manim-object"):
            event.acceptProposedAction()
        else:
            event.ignore()
    
    def dragMoveEvent(self, event):
        """Handle drag move events."""
        if event.mimeData().hasText() or event.mimeData().hasFormat("application/x-manim-object"):
            event.acceptProposedAction()
        else:
            event.ignore()
    
    def dropEvent(self, event):
        """Handle drop events to create new objects."""
        if event.mimeData().hasText():
            # Parse the dropped object data
            data = event.mimeData().text()
            if ":" in data:
                object_type, display_name = data.split(":", 1)
                
                # Convert view coordinates to scene coordinates
                scene_pos = self.mapToScene(event.position().toPoint())
                
                # Create the appropriate object
                item = self._create_object_item(object_type, display_name)
                if item:
                    item.setPos(scene_pos)
                    self.scene.addItem(item)
                    
                    # Select the new item
                    self.scene.clearSelection()
                    item.setSelected(True)
                
                event.acceptProposedAction()
            else:
                event.ignore()
        else:
            event.ignore()
    
    def _create_object_item(self, object_type, display_name):
        """Create a graphics item based on the object type."""
        if object_type in ["Circle", "Dot"]:
            return CircleItem(object_type, display_name)
        elif object_type in ["Square", "Rectangle"]:
            return RectangleItem(object_type, display_name)
        elif object_type in ["Text", "Tex", "MathTex", "Title"]:
            return TextItem(object_type, display_name)
        else:
            # Default item for unsupported types
            return ManimObjectItem(object_type, display_name)
    
    def _on_selection_changed(self):
        """Handle selection changes in the scene."""
        selected_items = self.scene.selectedItems()
        if selected_items:
            self.object_selected.emit(selected_items[0])
        else:
            self.object_selected.emit(None)
    
    def contextMenuEvent(self, event):
        """Show context menu for right-click."""
        item = self.itemAt(event.pos())
        if isinstance(item, ManimObjectItem):
            menu = QMenu()
            
            delete_action = QAction("Delete", self)
            delete_action.triggered.connect(lambda: self.scene.removeItem(item))
            menu.addAction(delete_action)
            
            duplicate_action = QAction("Duplicate", self)
            duplicate_action.triggered.connect(lambda: self._duplicate_item(item))
            menu.addAction(duplicate_action)
            
            menu.addSeparator()
            
            properties_action = QAction("Properties...", self)
            properties_action.triggered.connect(lambda: self._show_properties(item))
            menu.addAction(properties_action)
            
            menu.exec(event.globalPos())
    
    def _duplicate_item(self, item):
        """Duplicate an item on the canvas."""
        if isinstance(item, ManimObjectItem):
            new_item = self._create_object_item(item.object_type, item.display_name)
            if new_item:
                new_item.setPos(item.pos() + QPointF(20, 20))
                self.scene.addItem(new_item)
    
    def _show_properties(self, item):
        """Show properties dialog for an item."""
        # TODO: Implement properties dialog
        pass

class CanvasPreviewPanel(QWidget):
    """Panel containing the canvas preview and controls."""
    
    def __init__(self):
        super().__init__()
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the user interface."""
        layout = QVBoxLayout(self)
        
        # Header with controls
        header_layout = QHBoxLayout()
        
        # Title
        title_label = QLabel("Canvas Preview")
        title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Control buttons
        self.zoom_in_btn = QPushButton("Zoom In")
        self.zoom_out_btn = QPushButton("Zoom Out")
        self.zoom_fit_btn = QPushButton("Fit to View")
        self.reset_view_btn = QPushButton("Reset View")
        
        header_layout.addWidget(self.zoom_in_btn)
        header_layout.addWidget(self.zoom_out_btn)
        header_layout.addWidget(self.zoom_fit_btn)
        header_layout.addWidget(self.reset_view_btn)
        
        layout.addLayout(header_layout)
        
        # Canvas
        self.canvas = ManimCanvas()
        layout.addWidget(self.canvas)
        
        # Connect button signals
        self.zoom_in_btn.clicked.connect(lambda: self.canvas.scale(1.2, 1.2))
        self.zoom_out_btn.clicked.connect(lambda: self.canvas.scale(0.8, 0.8))
        self.zoom_fit_btn.clicked.connect(self._fit_to_view)
        self.reset_view_btn.clicked.connect(self._reset_view)
    
    def _fit_to_view(self):
        """Fit all items to the view."""
        self.canvas.fitInView(self.canvas.scene.itemsBoundingRect(), Qt.AspectRatioMode.KeepAspectRatio)
    
    def _reset_view(self):
        """Reset the view to the default."""
        self.canvas.resetTransform()
        self.canvas.centerOn(0, 0)