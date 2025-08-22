"""
Main Window Module
==================

Main application window with dockable panels for the Manim UI Builder.
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QDockWidget, QMenuBar, QMenu, QStatusBar, QToolBar,
    QSplitter, QTabWidget
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QKeySequence

from .panels.object_library import ObjectLibraryPanel
from .panels.canvas_preview import CanvasPreviewPanel
from .panels.timeline_editor import TimelineEditorPanel
from .panels.inspector import InspectorPanel
from .panels.gemini_assistant import GeminiAssistantPanel

class MainWindow(QMainWindow):
    """Main application window with dockable panels."""
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Manim UI Builder with AI")
        self.setMinimumSize(1200, 800)
        
        # Initialize UI components
        self._setup_menu_bar()
        self._setup_toolbar()
        self._setup_central_widget()
        self._setup_dock_widgets()
        self._setup_status_bar()
        
        # Connect signals
        self._connect_signals()
    
    def _setup_menu_bar(self):
        """Create the main menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('&File')
        
        new_action = QAction('&New Project', self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.setStatusTip('Create a new Manim project')
        file_menu.addAction(new_action)
        
        open_action = QAction('&Open Project', self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.setStatusTip('Open an existing Manim project')
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        save_action = QAction('&Save Project', self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.setStatusTip('Save the current project')
        file_menu.addAction(save_action)
        
        save_as_action = QAction('Save &As...', self)
        save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        save_as_action.setStatusTip('Save the project with a new name')
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        export_menu = file_menu.addMenu('&Export')
        
        export_mp4_action = QAction('Export as &MP4', self)
        export_mp4_action.setStatusTip('Export animation as MP4 video')
        export_menu.addAction(export_mp4_action)
        
        export_gif_action = QAction('Export as &GIF', self)
        export_gif_action.setStatusTip('Export animation as GIF')
        export_menu.addAction(export_gif_action)
        
        export_code_action = QAction('Export &Manim Code', self)
        export_code_action.setStatusTip('Export as Python Manim script')
        export_menu.addAction(export_code_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('E&xit', self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.setStatusTip('Exit the application')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu('&Edit')
        
        undo_action = QAction('&Undo', self)
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction('&Redo', self)
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        cut_action = QAction('Cu&t', self)
        cut_action.setShortcut(QKeySequence.StandardKey.Cut)
        edit_menu.addAction(cut_action)
        
        copy_action = QAction('&Copy', self)
        copy_action.setShortcut(QKeySequence.StandardKey.Copy)
        edit_menu.addAction(copy_action)
        
        paste_action = QAction('&Paste', self)
        paste_action.setShortcut(QKeySequence.StandardKey.Paste)
        edit_menu.addAction(paste_action)
        
        # View menu
        view_menu = menubar.addMenu('&View')
        
        panels_menu = view_menu.addMenu('&Panels')
        # Panel visibility actions will be added after dock widgets are created
        
        # Animation menu
        animation_menu = menubar.addMenu('&Animation')
        
        play_action = QAction('&Play', self)
        play_action.setShortcut('Space')
        play_action.setStatusTip('Play/pause animation preview')
        animation_menu.addAction(play_action)
        
        stop_action = QAction('&Stop', self)
        stop_action.setShortcut('Escape')
        stop_action.setStatusTip('Stop animation preview')
        animation_menu.addAction(stop_action)
        
        # AI menu
        ai_menu = menubar.addMenu('&AI Assistant')
        
        chat_action = QAction('Open &Chat', self)
        chat_action.setShortcut('Ctrl+Shift+A')
        chat_action.setStatusTip('Open Gemini AI assistant chat')
        ai_menu.addAction(chat_action)
        
        generate_action = QAction('&Generate from Prompt', self)
        generate_action.setShortcut('Ctrl+G')
        generate_action.setStatusTip('Generate animation from text prompt')
        ai_menu.addAction(generate_action)
        
        # Help menu
        help_menu = menubar.addMenu('&Help')
        
        about_action = QAction('&About', self)
        about_action.setStatusTip('About Manim UI Builder')
        help_menu.addAction(about_action)
    
    def _setup_toolbar(self):
        """Create the main toolbar."""
        toolbar = QToolBar('Main Toolbar')
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        # Add common actions to toolbar
        new_action = QAction('New', self)
        new_action.setStatusTip('New project')
        toolbar.addAction(new_action)
        
        open_action = QAction('Open', self)
        open_action.setStatusTip('Open project')
        toolbar.addAction(open_action)
        
        save_action = QAction('Save', self)
        save_action.setStatusTip('Save project')
        toolbar.addAction(save_action)
        
        toolbar.addSeparator()
        
        play_action = QAction('Play', self)
        play_action.setStatusTip('Play animation')
        toolbar.addAction(play_action)
        
        stop_action = QAction('Stop', self)
        stop_action.setStatusTip('Stop animation')
        toolbar.addAction(stop_action)
        
        toolbar.addSeparator()
        
        ai_action = QAction('AI Assistant', self)
        ai_action.setStatusTip('Open AI assistant')
        toolbar.addAction(ai_action)
    
    def _setup_central_widget(self):
        """Setup the central widget with canvas and timeline."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create splitter for canvas and timeline
        splitter = QSplitter(Qt.Orientation.Vertical)
        layout.addWidget(splitter)
        
        # Canvas preview (top)
        self.canvas_panel = CanvasPreviewPanel()
        splitter.addWidget(self.canvas_panel)
        
        # Timeline editor (bottom)
        self.timeline_panel = TimelineEditorPanel()
        splitter.addWidget(self.timeline_panel)
        
        # Set initial sizes (canvas larger than timeline)
        splitter.setStretchFactor(0, 3)  # Canvas gets 3/4 of space
        splitter.setStretchFactor(1, 1)  # Timeline gets 1/4 of space
    
    def _setup_dock_widgets(self):
        """Create dockable panels."""
        # Object Library (left)
        self.object_library_dock = QDockWidget('Object Library', self)
        self.object_library_panel = ObjectLibraryPanel()
        self.object_library_dock.setWidget(self.object_library_panel)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.object_library_dock)
        
        # Inspector Panel (right)
        self.inspector_dock = QDockWidget('Inspector', self)
        self.inspector_panel = InspectorPanel()
        self.inspector_dock.setWidget(self.inspector_panel)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.inspector_dock)
        
        # Gemini Assistant (right, tabbed with inspector)
        self.gemini_dock = QDockWidget('AI Assistant', self)
        self.gemini_panel = GeminiAssistantPanel()
        self.gemini_dock.setWidget(self.gemini_panel)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.gemini_dock)
        
        # Tab the inspector and gemini panels together
        self.tabifyDockWidget(self.inspector_dock, self.gemini_dock)
        
        # Make inspector the active tab initially
        self.inspector_dock.raise_()
        
        # Add panel visibility actions to View menu
        view_menu = self.menuBar().actions()[2].menu()  # View menu
        panels_menu = view_menu.actions()[0].menu()  # Panels submenu
        
        panels_menu.addAction(self.object_library_dock.toggleViewAction())
        panels_menu.addAction(self.inspector_dock.toggleViewAction())
        panels_menu.addAction(self.gemini_dock.toggleViewAction())
    
    def _setup_status_bar(self):
        """Create the status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage('Ready')
    
    def _connect_signals(self):
        """Connect signals between components."""
        # TODO: Connect signals between panels for communication
        pass
    
    def center_on_screen(self):
        """Center the window on the screen."""
        screen = self.screen().availableGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )