import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QTextEdit, 
                             QFrame, QSizePolicy)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPalette, QColor


class ModernApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modern PyQt6 Application")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(600, 400)
        
        # Set up the main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Create the three main areas
        self.create_header()
        self.create_body()
        self.create_footer()
        
        # Apply modern styling
        self.apply_styles()
        
    def create_header(self):
        """Create the header area with title and navigation"""
        self.header = QFrame()
        self.header.setObjectName("header")
        self.header.setFixedHeight(80)
        self.header.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(20, 10, 20, 10)
        
        # App title
        title_label = QLabel("Lucky Chrome")
        title_label.setObjectName("app-title")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        
        header_layout.addStretch()
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        self.main_layout.addWidget(self.header)
        
    def create_body(self):
        """Create the main body area with content"""
        self.body = QFrame()
        self.body.setObjectName("body")
        self.body.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        body_layout = QVBoxLayout(self.body)
        body_layout.setContentsMargins(30, 20, 30, 20)
        body_layout.setSpacing(20)
        
        # Body area is now empty but ready for content
        # Design preserved for later use:
        # - Welcome section with centered title (welcome-title)
        # - Description text with word wrap (description)
        # - Content area with title (content-title)
        # - Text area for input (text-area)
        # - Action buttons layout (action-button)
        
        self.main_layout.addWidget(self.body)
        
    def create_footer(self):
        """Create the footer area with status and info"""
        self.footer = QFrame()
        self.footer.setObjectName("footer")
        self.footer.setFixedHeight(35)
        self.footer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        footer_layout = QHBoxLayout(self.footer)
        footer_layout.setContentsMargins(20, 10, 20, 10)
        
        # Status label
        status_label = QLabel("Ready")
        status_label.setObjectName("status-label")
        
        # Copyright info
        copyright_label = QLabel("© 2024 Modern PyQt6 App")
        copyright_label.setObjectName("copyright-label")
        
        # Version info
        version_label = QLabel("v1.0.0")
        version_label.setObjectName("version-label")
        
        footer_layout.addWidget(status_label)
        footer_layout.addStretch()
        footer_layout.addWidget(copyright_label)
        footer_layout.addWidget(version_label)
        
        self.main_layout.addWidget(self.footer)
        
    def apply_styles(self):
        """Apply modern styling to the application"""
        style_sheet = """
        QMainWindow {
            background-color: #ffffff;
        }
        
        #header {
            background-color: #ffffff;
            border-bottom: 1px solid #e0e0e0;
        }
        
        #app-title {
            color: #4a90e2;
        }
        
        #nav-button {
            background-color: transparent;
            border: 1px solid #ffffff;
            color: #ffffff;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }
        
        #nav-button:hover {
            background-color: #ffffff;
            color: #4a90e2;
        }
        
        #nav-button:pressed {
            background-color: #f0f8ff;
            color: #4a90e2;
        }
        
        #body {
            background-color: #ffffff;
            border: none;
        }
        
        #welcome-title {
            color: #4a90e2;
        }
        
        #description {
            color: #5a6c7d;
            font-size: 14px;
        }
        
        #content-title {
            color: #4a90e2;
        }
        
        #text-area {
            border: 2px solid #e1f0ff;
            border-radius: 6px;
            padding: 10px;
            font-size: 14px;
            background-color: #f8fbff;
        }
        
        #text-area:focus {
            border-color: #4a90e2;
            background-color: white;
        }
        
        #action-button {
            background-color: #4a90e2;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            font-weight: bold;
            font-size: 14px;
        }
        
        #action-button:hover {
            background-color: #357abd;
        }
        
        #action-button:pressed {
            background-color: #2d5aa0;
        }
        
        #footer {
            background-color: #4a90e2;
            border-top: 1px solid #357abd;
        }
        
        #status-label {
            color: #ffffff;
            font-weight: bold;
        }
        
        #copyright-label {
            color: #ffffff;
            font-size: 12px;
        }
        
        #version-label {
            color: #ffffff;
            font-size: 12px;
            font-weight: bold;
        }
        """
        
        self.setStyleSheet(style_sheet)


def main():
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Modern PyQt6 App")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Modern Apps")
    
    # Create and show the main window
    window = ModernApp()
    window.show()
    
    # Start the event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
