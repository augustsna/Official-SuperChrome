import os
import sys
import json
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QScrollArea, QGroupBox, QFormLayout, QCheckBox, QComboBox,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt, QSettings, QSize
from PyQt6.QtGui import QIcon, QPixmap

# Sample configuration constants
WINDOW_SIZE = (600, 500)
WINDOW_TITLE = "Sample SuperCut UI"
ICON_PATH = "src/sources/icon.png"
PROJECT_ROOT = "."

# Sample stylesheet with correct colors matching SuperCut
STYLE_SHEET = """
QWidget {
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 12px;
    color: #333333;
    background-color: #f5f7fa;
}

QGroupBox {
    font-weight: bold;
    border: 2px solid #cccccc;
    border-radius: 6px;
    margin-top: 10px;
    padding-top: 10px;
    background-color: white;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px 0 5px;
    color: #333333;
}

QPushButton {
    background-color: #4a90e2;
    color: white;
    border-radius: 6px;
    padding: 6px 12px;
}

QPushButton:hover {
    background-color: #357ABD;
}

QLineEdit {
    background-color: #ffffff;
    border: 1px solid #d0d0d0;
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 12px;
    color: #333;
    font-family: 'Segoe UI', sans-serif;
}

QLineEdit:hover {
    border: 2px solid #4a90e2;
    background-color: #ffffff;
}

QComboBox {
    background-color: #ffffff;
    border: 1px solid #d0d0d0;
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 12px;
    color: #333;
    font-family: 'Segoe UI', sans-serif;
}

QComboBox:hover {
    border: 2px solid #4687f4;
}

QComboBox::drop-down {
    border: none;
    width: 0px;
}

QComboBox::down-arrow {
    image: none;
    border: none;
    width: 0px;
}

QComboBox QAbstractItemView {
    background-color: #ffffff;
    selection-background-color: #3f92e3;
    border: 1px solid #ccc;
    outline: none;
}

QCheckBox {
    spacing: 8px;
    font-size: 13px;
    color: #333;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border-radius: 6px;
    border: 1px solid #ccc;
    background: #ffffff;
}

QCheckBox::indicator:hover {
    background: #f5f9ff;
}

QCheckBox::indicator:unchecked {
    background: #ffffff;
    border: 1px solid #ccc;
}

QCheckBox::indicator:unchecked:hover {
    background: #f5f9ff;
}

QCheckBox::indicator:checked {
    background: #ffffff;
    border: 1px solid #ccc;
    image: url(src/sources/black_tick.svg);
}

QScrollBar:vertical {
    background: rgba(240, 240, 240, 0.20);
    width: 12px;
    border-radius: 6px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: rgba(192, 192, 192, 0.20);
    border-radius: 6px;
    min-height: 20px;
    margin: 0px;
}

QScrollBar::handle:vertical:hover {
    background: rgba(160, 160, 160, 0.35);
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
"""

class SampleSuperCutUI(QWidget):
    """Sample main application window demonstrating SuperCut UI structure"""
    
    def __init__(self):
        super().__init__()
        self.settings = QSettings('SampleSuperCut', 'SampleSuperCutUI')
        self.profiles = self.load_profiles()
        self.init_ui()

    def load_profiles(self):
        """Load profiles from profile.json file"""
        try:
            with open('profile.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data.get('profiles', [])
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading profiles: {e}")
            return []

    def init_ui(self):
        """Initialize the user interface"""
        # Set window properties
        self.setWindowTitle(WINDOW_TITLE)
        self.setMinimumSize(400, 400)
        self.resize(WINDOW_SIZE[0], WINDOW_SIZE[1])
        self.setStyleSheet(STYLE_SHEET)
        
        # Create main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(14, 18, 0, 2)
        layout.setSpacing(0)

        # --- TITLE AREA ---
        self.create_title_area(layout)
        
        # --- SCROLLABLE CONTENT AREA ---
        self.create_scrollable_content(layout)
        
        # --- BOTTOM ACTION AREA ---
        self.create_bottom_action_area(layout)
        
        self.setLayout(layout)

    def create_title_area(self, layout):
        """Create the title area with icon and app name"""
        title_widget = QtWidgets.QWidget()
        title_widget.setFixedHeight(70)
        title_widget.setStyleSheet("background-color: transparent;")
        
        # Title icon
        title_icon = QLabel()
        icon_path = os.path.join(PROJECT_ROOT, "src", "sources", "icon.png")
        if os.path.exists(icon_path):
            title_icon.setPixmap(QPixmap(icon_path).scaled(45, 45, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            # Fallback icon if file doesn't exist
            title_icon.setText("")
            title_icon.setStyleSheet("font-size: 45px; background-color: transparent;")
        
        # Title label
        title_label = QLabel("SuperCut")
        title_label.setStyleSheet("font-size: 35px; font-weight: bold; background-color: transparent; color: #333333;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Static icon (placeholder)
        static_icon = QLabel("📹")
        static_icon.setStyleSheet("font-size: 24px; background-color: transparent;")
        static_icon.setVisible(True)
        
        # Title layout
        title_layout = QtWidgets.QHBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(0)
        title_layout.addSpacing(35)
        title_layout.addStretch()
        title_layout.addWidget(title_icon)
        title_layout.addSpacing(10)
        title_layout.addWidget(title_label)
        title_layout.addSpacing(10)
        title_layout.addWidget(static_icon)
        title_layout.addStretch()
        title_widget.setLayout(title_layout)
        
        layout.addWidget(title_widget)
        layout.addSpacing(0)



    def create_scrollable_content(self, layout):
        """Create the scrollable content area"""
        # Create scroll area
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
                margin-right: 0px;
                padding-right: 0px;
            }
        """)
        
        # Create scrollable content widget
        scroll_content = QtWidgets.QWidget()
        scroll_content.setStyleSheet("background-color: transparent;")
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(8, 0, 32, 0)
        scroll_layout.setSpacing(10)
        
        # Add profiles section
        self.create_profiles_section(scroll_layout)
        
        # Set the scroll content widget
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)
        
        # Store scroll area reference
        self.scroll_area = scroll_area

    def create_profiles_section(self, layout):
        """Create the profiles display section"""
        # Create table widget for profiles
        self.profiles_table = QTableWidget()
        self.profiles_table.setColumnCount(3)
        self.profiles_table.setHorizontalHeaderLabels(["#", "Name", "Type"])
        
        # Set table properties
        self.profiles_table.setAlternatingRowColors(False)
        self.profiles_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.profiles_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        # Hide the row selection indicator column (first column)
        self.profiles_table.verticalHeader().setVisible(False)
        
        # Set header properties
        header = self.profiles_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # Number
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Name
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Type
        
        # Set table style
        self.profiles_table.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                border: 2px solid #e0e0e0;
                border-radius: 0px;
                gridline-color: #f0f0f0;
                outline: none;
                selection-background-color: #4a90e2;
                selection-color: white;
            }
            QTableWidget::item {
                padding: 12px 8px;
                border-bottom: 1px solid #f5f5f5;
                background-color: transparent;
                color: #333333;
            }
            QTableWidget::item:hover {
                background-color: #f8f9fa;
            }
            QTableWidget::item:selected {
                background-color: #4a90e2;
                color: white;
                border-bottom: 1px solid #4a90e2;
            }
            QTableWidget::item:selected:hover {
                background-color: #357ABD;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 4px 8px;
                border: none;
                border-bottom: 2px solid #dee2e6;
                border-right: 1px solid #e9ecef;
                font-weight: bold;
                color: #495057;
                font-size: 13px;
            }
            QHeaderView::section:first {
                border-top-left-radius: 6px;
            }
            QHeaderView::section:last {
                border-top-right-radius: 6px;
                border-right: none;
            }
            QTableCornerButton::section {
                background-color: #f8f9fa;
                border: none;
                border-bottom: 2px solid #dee2e6;
                border-right: 1px solid #e9ecef;
            }
            QTableWidget::item[column="0"] {
                background-color: #f8f9fa;
                color: #6c757d;
                font-weight: bold;
                font-size: 12px;
            }
            QTableWidget::item[column="0"]:selected {
                background-color: #4a90e2;
                color: white;
            }
        """)
        
        # Populate table with profile data
        self.populate_profiles_table()
        
        # Add refresh button
        refresh_btn = QPushButton("Refresh Profiles")
        refresh_btn.setFixedSize(120, 30)
        refresh_btn.clicked.connect(self.refresh_profiles)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border-radius: 4px;
                padding: 4px 8px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        
        layout.addWidget(self.profiles_table)
        layout.addWidget(refresh_btn)

    def populate_profiles_table(self):
        """Populate the profiles table with data from profile.json"""
        self.profiles_table.setRowCount(len(self.profiles))
        
        for row, profile in enumerate(self.profiles):
            # Number
            number_item = QTableWidgetItem(str(row + 1))
            number_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.profiles_table.setItem(row, 0, number_item)
            
            # Name
            name_item = QTableWidgetItem(profile.get('name', ''))
            self.profiles_table.setItem(row, 1, name_item)
            
            # Type
            type_item = QTableWidgetItem(profile.get('type', ''))
            type_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.profiles_table.setItem(row, 2, type_item)

    def refresh_profiles(self):
        """Refresh the profiles table with updated data from profile.json"""
        self.profiles = self.load_profiles()
        self.populate_profiles_table()
        print("Profiles refreshed successfully!")

    def create_bottom_action_area(self, layout):
        """Create the bottom action area with buttons"""
        # Action buttons
        action_layout = QHBoxLayout()
        action_layout.setContentsMargins(14, 10, 14, 10)
        action_layout.setSpacing(10)
        
        # Add spacing to push buttons to the left
        action_layout.addStretch()
        
        layout.addLayout(action_layout)

def main():
    """Main function to run the sample application"""
    app = QApplication(sys.argv)
    
    # Create and show the main window
    window = SampleSuperCutUI()
    window.show()
    
    # Run the application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
