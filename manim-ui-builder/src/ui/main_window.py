from PyQt5.QtWidgets import QMainWindow, QMenuBar, QAction, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manim UI Builder")
        self.setGeometry(100, 100, 1200, 800)

        self.init_ui()

    def init_ui(self):
        self.create_menu()
        self.setCentralWidget(QWidget(self))
        layout = QVBoxLayout(self.centralWidget())
        self.centralWidget().setLayout(layout)

    def create_menu(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        export_action = QAction("Export", self)
        file_menu.addAction(export_action)

        edit_menu = menu_bar.addMenu("Edit")
        undo_action = QAction("Undo", self)
        redo_action = QAction("Redo", self)
        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)

        help_menu = menu_bar.addMenu("Help")
        about_action = QAction("About", self)
        help_menu.addAction(about_action)