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
        self.header.setFixedHeight(60)
        self.header.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(20, 10, 20, 10)
        
        # App title
        title_label = QLabel("Modern PyQt6 App")
        title_label.setObjectName("app-title")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        
        # Navigation buttons
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(10)
        
        home_btn = QPushButton("Home")
        home_btn.setObjectName("nav-button")
        about_btn = QPushButton("About")
        about_btn.setObjectName("nav-button")
        settings_btn = QPushButton("Settings")
        settings_btn.setObjectName("nav-button")
        
        nav_layout.addWidget(home_btn)
        nav_layout.addWidget(about_btn)
        nav_layout.addWidget(settings_btn)
        nav_layout.addStretch()
        
        header_layout.addWidget(title_label)
        header_layout.addLayout(nav_layout)
        
        self.main_layout.addWidget(self.header)
        
    def create_body(self):
        """Create the main body area with content"""
        self.body = QFrame()
        self.body.setObjectName("body")
        self.body.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        body_layout = QVBoxLayout(self.body)
        body_layout.setContentsMargins(30, 20, 30, 20)
        body_layout.setSpacing(20)
        
        # Welcome section
        welcome_label = QLabel("Welcome to Your Modern Application")
        welcome_label.setObjectName("welcome-title")
        welcome_font = QFont()
        welcome_font.setPointSize(24)
        welcome_font.setBold(True)
        welcome_label.setFont(welcome_font)
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Description
        desc_label = QLabel("This is a modern PyQt6 application with a clean header, body, and footer layout. "
                           "The design follows modern UI principles with proper spacing and typography.")
        desc_label.setObjectName("description")
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Content area
        content_label = QLabel("Main Content Area")
        content_label.setObjectName("content-title")
        content_font = QFont()
        content_font.setPointSize(16)
        content_font.setBold(True)
        content_label.setFont(content_font)
        
        # Text area for content
        self.text_area = QTextEdit()
        self.text_area.setObjectName("text-area")
        self.text_area.setPlaceholderText("Enter your content here...")
        self.text_area.setMaximumHeight(200)
        
        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        action_btn1 = QPushButton("Action 1")
        action_btn1.setObjectName("action-button")
        action_btn2 = QPushButton("Action 2")
        action_btn2.setObjectName("action-button")
        action_btn3 = QPushButton("Action 3")
        action_btn3.setObjectName("action-button")
        
        button_layout.addWidget(action_btn1)
        button_layout.addWidget(action_btn2)
        button_layout.addWidget(action_btn3)
        button_layout.addStretch()
        
        body_layout.addWidget(welcome_label)
        body_layout.addWidget(desc_label)
        body_layout.addStretch()
        body_layout.addWidget(content_label)
        body_layout.addWidget(self.text_area)
        body_layout.addLayout(button_layout)
        
        self.main_layout.addWidget(self.body)
        
    def create_footer(self):
        """Create the footer area with status and info"""
        self.footer = QFrame()
        self.footer.setObjectName("footer")
        self.footer.setFixedHeight(50)
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
            background-color: #4a90e2;
            border-bottom: 1px solid #357abd;
        }
        
        #app-title {
            color: white;
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
