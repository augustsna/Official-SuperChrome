import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QTextEdit, 
                             QFrame, QSizePolicy, QScrollArea, QLineEdit)
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
        title_font = QFont("Segoe UI", 22)
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
        body_layout.setContentsMargins(30, 10, 30, 20)
        body_layout.setSpacing(15)
        
        # Search and Filter Section
        search_filter_layout = QHBoxLayout()
        search_filter_layout.setSpacing(15)
        search_filter_layout.setContentsMargins(0, 5, 0, 5)
        
        # Search input
        search_input = QLineEdit()
        search_input.setObjectName("text-area")
        search_input.setPlaceholderText("Search...")
        search_input.setFixedSize(120, 25)
        search_input.setFont(QFont("Segoe UI", 9))
        
        # Filter button
        filter_btn = QPushButton("Filter")
        filter_btn.setObjectName("action-button")
        filter_btn.setFixedSize(50, 25)
        filter_btn.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
        
        # Category button
        category_btn = QPushButton("Category")
        category_btn.setObjectName("action-button")
        category_btn.setFixedSize(70, 25)
        category_btn.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
        
        search_filter_layout.addWidget(search_input)
        search_filter_layout.addWidget(filter_btn)
        search_filter_layout.addWidget(category_btn)
        search_filter_layout.addStretch()
        
        # Scroll Area for List
        scroll_area = QScrollArea()
        scroll_area.setObjectName("scroll-area")
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setMinimumHeight(300)
        
        # Scroll content widget
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(5)
        scroll_layout.setContentsMargins(10, 10, 10, 10)
        
        # Column Headers
        header_widget = QFrame()
        header_widget.setObjectName("list-header")
        header_widget.setFixedHeight(40)
        
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(15, 10, 15, 10)
        header_layout.setSpacing(20)
        
        # Header labels with fixed widths for column alignment
        name_header = QLabel("Name")
        name_header.setObjectName("header-label")
        name_header.setFixedWidth(150)
        name_header.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        
        category_header = QLabel("Category")
        category_header.setObjectName("header-label")
        category_header.setFixedWidth(100)
        category_header.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        
        email_header = QLabel("Email")
        email_header.setObjectName("header-label")
        email_header.setFixedWidth(200)
        email_header.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        
        header_layout.addWidget(name_header)
        header_layout.addWidget(category_header)
        header_layout.addWidget(email_header)
        header_layout.addStretch()
        
        scroll_layout.addWidget(header_widget)
        
        # Sample list items (Name, Category, Email)
        sample_items = [
            ("John Doe", "Developer", "john@example.com"),
            ("Jane Smith", "Designer", "jane@example.com"),
            ("Mike Johnson", "Manager", "mike@example.com"),
            ("Sarah Wilson", "Developer", "sarah@example.com"),
            ("Tom Brown", "Designer", "tom@example.com"),
            ("Lisa Davis", "Manager", "lisa@example.com"),
            ("David Miller", "Developer", "david@example.com"),
            ("Emma Taylor", "Designer", "emma@example.com"),
            ("Chris Anderson", "Manager", "chris@example.com"),
            ("Anna White", "Developer", "anna@example.com")
        ]
        
        for name, category, email in sample_items:
            item_widget = QFrame()
            item_widget.setObjectName("list-item")
            item_widget.setFixedHeight(45)
            
            item_layout = QHBoxLayout(item_widget)
            item_layout.setContentsMargins(15, 10, 15, 10)
            item_layout.setSpacing(20)
            
            # Name column
            name_label = QLabel(name)
            name_label.setObjectName("item-name")
            name_label.setFixedWidth(150)
            name_label.setFont(QFont("Segoe UI", 11))
            
            # Category column
            category_label = QLabel(category)
            category_label.setObjectName("item-category")
            category_label.setFixedWidth(100)
            category_label.setFont(QFont("Segoe UI", 10))
            
            # Email column
            email_label = QLabel(email)
            email_label.setObjectName("item-email")
            email_label.setFixedWidth(200)
            email_label.setFont(QFont("Segoe UI", 10))
            
            item_layout.addWidget(name_label)
            item_layout.addWidget(category_label)
            item_layout.addWidget(email_label)
            item_layout.addStretch()
            
            scroll_layout.addWidget(item_widget)
        
        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_content)
        
        # Create Profile button
        create_profile_btn = QPushButton("Create Profile")
        create_profile_btn.setObjectName("action-button")
        create_profile_btn.setFixedSize(150, 40)
        create_profile_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        
        # Add all sections to body layout
        body_layout.addLayout(search_filter_layout)
        body_layout.addWidget(scroll_area)
        body_layout.addWidget(create_profile_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
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
        status_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        
        # Copyright info
        copyright_label = QLabel("© 2024 Lucky Chrome")
        copyright_label.setObjectName("copyright-label")
        copyright_label.setFont(QFont("Segoe UI", 9))
        
        # Version info
        version_label = QLabel("v1.0.0")
        version_label.setObjectName("version-label")
        version_label.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        
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
        
        #scroll-area {
            border: 2px solid #e1f0ff;
            border-radius: 6px;
            background-color: #f8fbff;
        }
        
        #list-item {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
        }
        
        #list-item:hover {
            background-color: #f0f8ff;
            border-color: #4a90e2;
        }
        
        #item-name {
            color: #2c3e50;
            font-weight: bold;
            font-size: 14px;
        }
        
        #item-category {
            color: #4a90e2;
            font-weight: bold;
            font-size: 12px;
            padding: 4px 8px;
            background-color: #e1f0ff;
            border-radius: 3px;
        }
        
        #item-email {
            color: #7f8c8d;
            font-size: 12px;
        }
        
        #list-header {
            background-color: #4a90e2;
            border: 1px solid #357abd;
            border-radius: 4px;
        }
        
        #header-label {
            color: #ffffff;
            font-weight: bold;
            font-size: 14px;
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
