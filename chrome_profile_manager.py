import sys
import os
import json
import subprocess
import psutil
from pathlib import Path
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                               QTextEdit, QTableWidget, QTableWidgetItem, 
                               QHeaderView, QMessageBox, QFileDialog, QGroupBox,
                               QGridLayout, QComboBox, QCheckBox, QSpinBox)
from PySide6.QtCore import Qt, QThread, Signal, QTimer
from PySide6.QtGui import QFont, QIcon, QPixmap, QPalette, QColor


class ChromeProfileManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chrome Profile Manager")
        self.setGeometry(100, 100, 1000, 700)
        
        # Chrome paths for different operating systems
        self.chrome_paths = {
            'Windows': [
                r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
                os.path.expanduser(r'~\AppData\Local\Google\Chrome\Application\chrome.exe')
            ],
            'Darwin': [
                '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
            ],
            'Linux': [
                '/usr/bin/google-chrome',
                '/usr/bin/google-chrome-stable',
                '/usr/bin/chromium-browser'
            ]
        }
        
        self.current_os = 'Windows' if os.name == 'nt' else 'Darwin' if sys.platform == 'darwin' else 'Linux'
        self.chrome_path = self.find_chrome_path()
        self.profiles_dir = self.get_profiles_directory()
        
        self.init_ui()
        self.load_existing_profiles()
        
    def find_chrome_path(self):
        """Find the Chrome executable path"""
        for path in self.chrome_paths.get(self.current_os, []):
            if os.path.exists(path):
                return path
        return None
    
    def get_profiles_directory(self):
        """Get the Chrome profiles directory based on OS"""
        if self.current_os == 'Windows':
            return os.path.expanduser(r'~\AppData\Local\Google\Chrome\User Data')
        elif self.current_os == 'Darwin':
            return os.path.expanduser('~/Library/Application Support/Google/Chrome')
        else:  # Linux
            return os.path.expanduser('~/.config/google-chrome')
    
    def init_ui(self):
        """Initialize the user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("Chrome Profile Manager")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        main_layout.addWidget(title_label)
        
        # Chrome status
        self.create_chrome_status_section(main_layout)
        
        # Create new profile section
        self.create_new_profile_section(main_layout)
        
        # Existing profiles section
        self.create_existing_profiles_section(main_layout)
        
        # Apply modern styling
        self.apply_styling()
    
    def create_chrome_status_section(self, parent_layout):
        """Create the Chrome status section"""
        status_group = QGroupBox("Chrome Status")
        status_layout = QGridLayout(status_group)
        
        # Chrome path
        status_layout.addWidget(QLabel("Chrome Path:"), 0, 0)
        self.chrome_path_label = QLabel(self.chrome_path or "Chrome not found")
        self.chrome_path_label.setStyleSheet("color: #e74c3c;" if not self.chrome_path else "color: #27ae60;")
        status_layout.addWidget(self.chrome_path_label, 0, 1)
        
        # Profiles directory
        status_layout.addWidget(QLabel("Profiles Directory:"), 1, 0)
        self.profiles_dir_label = QLabel(self.profiles_dir)
        status_layout.addWidget(self.profiles_dir_label, 1, 1)
        
        # Chrome running status
        status_layout.addWidget(QLabel("Chrome Status:"), 2, 0)
        self.chrome_status_label = QLabel("Checking...")
        status_layout.addWidget(self.chrome_status_label, 2, 1)
        
        # Refresh button
        refresh_btn = QPushButton("Refresh Status")
        refresh_btn.clicked.connect(self.refresh_chrome_status)
        status_layout.addWidget(refresh_btn, 3, 0, 1, 2)
        
        parent_layout.addWidget(status_group)
        
        # Start status check timer
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.check_chrome_status)
        self.status_timer.start(5000)  # Check every 5 seconds
        self.check_chrome_status()
    
    def create_new_profile_section(self, parent_layout):
        """Create the new profile creation section"""
        new_profile_group = QGroupBox("Create New Profile")
        new_profile_layout = QGridLayout(new_profile_group)
        
        # Profile name
        new_profile_layout.addWidget(QLabel("Profile Name:"), 0, 0)
        self.profile_name_input = QLineEdit()
        self.profile_name_input.setPlaceholderText("Enter profile name (e.g., Work, Personal)")
        new_profile_layout.addWidget(self.profile_name_input, 0, 1)
        
        # Profile directory
        new_profile_layout.addWidget(QLabel("Profile Directory:"), 1, 0)
        self.profile_dir_input = QLineEdit()
        self.profile_dir_input.setPlaceholderText("Auto-generated based on profile name")
        new_profile_layout.addWidget(self.profile_dir_input, 1, 1)
        
        # Launch options
        new_profile_layout.addWidget(QLabel("Launch Options:"), 2, 0)
        launch_options_layout = QHBoxLayout()
        
        self.incognito_checkbox = QCheckBox("Incognito Mode")
        self.no_sandbox_checkbox = QCheckBox("No Sandbox")
        self.disable_extensions_checkbox = QCheckBox("Disable Extensions")
        
        launch_options_layout.addWidget(self.incognito_checkbox)
        launch_options_layout.addWidget(self.no_sandbox_checkbox)
        launch_options_layout.addWidget(self.disable_extensions_checkbox)
        launch_options_layout.addStretch()
        
        new_profile_layout.addLayout(launch_options_layout, 2, 1)
        
        # Create profile button
        create_btn = QPushButton("Create Profile")
        create_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        create_btn.clicked.connect(self.create_new_profile)
        new_profile_layout.addWidget(create_btn, 3, 0, 1, 2)
        
        parent_layout.addWidget(new_profile_group)
    
    def create_existing_profiles_section(self, parent_layout):
        """Create the existing profiles management section"""
        existing_profiles_group = QGroupBox("Existing Profiles")
        existing_profiles_layout = QVBoxLayout(existing_profiles_group)
        
        # Profiles table
        self.profiles_table = QTableWidget()
        self.profiles_table.setColumnCount(5)
        self.profiles_table.setHorizontalHeaderLabels([
            "Profile Name", "Directory", "Created", "Last Used", "Actions"
        ])
        
        # Set table properties
        header = self.profiles_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        
        existing_profiles_layout.addWidget(self.profiles_table)
        
        # Action buttons
        actions_layout = QHBoxLayout()
        
        refresh_profiles_btn = QPushButton("Refresh Profiles")
        refresh_profiles_btn.clicked.connect(self.load_existing_profiles)
        
        delete_selected_btn = QPushButton("Delete Selected")
        delete_selected_btn.setStyleSheet("background-color: #e74c3c; color: white;")
        delete_selected_btn.clicked.connect(self.delete_selected_profile)
        
        actions_layout.addWidget(refresh_profiles_btn)
        actions_layout.addWidget(delete_selected_btn)
        actions_layout.addStretch()
        
        existing_profiles_layout.addLayout(actions_layout)
        
        parent_layout.addWidget(existing_profiles_group)
    
    def apply_styling(self):
        """Apply modern styling to the application"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ecf0f1;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
            QPushButton:pressed {
                background-color: #6c7b7d;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 4px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
            QTableWidget {
                border: 2px solid #bdc3c7;
                border-radius: 4px;
                background-color: white;
                gridline-color: #ecf0f1;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
    
    def check_chrome_status(self):
        """Check if Chrome is currently running"""
        chrome_running = False
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if 'chrome' in proc.info['name'].lower():
                    chrome_running = True
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        if chrome_running:
            self.chrome_status_label.setText("Running")
            self.chrome_status_label.setStyleSheet("color: #27ae60; font-weight: bold;")
        else:
            self.chrome_status_label.setText("Not Running")
            self.chrome_status_label.setStyleSheet("color: #e74c3c;")
    
    def refresh_chrome_status(self):
        """Refresh Chrome status information"""
        self.check_chrome_status()
        self.load_existing_profiles()
    
    def create_new_profile(self):
        """Create a new Chrome profile with direct directory creation and Local State update"""
        profile_name = self.profile_name_input.text().strip()
        if not profile_name:
            QMessageBox.warning(self, "Warning", "Please enter a profile name.")
            return
        
        # Generate unique profile directory name
        profile_dir = f"Profile {len([d for d in os.listdir(self.profiles_dir) if d.startswith('Profile') and os.path.isdir(os.path.join(self.profiles_dir, d))])}"
        if profile_dir == "Profile 0":
            profile_dir = "Default"
        
        # Create profile directory path
        profile_path = os.path.join(self.profiles_dir, profile_dir)
        
        try:
            # ✅ Direct profile directory creation
            os.makedirs(profile_path, exist_ok=True)
            
            # ✅ Basic Preferences file only
            preferences = {
                "profile": {
                    "name": profile_name,
                    "exit_type": "Normal",
                    "exited_cleanly": True
                }
            }
            
            preferences_path = os.path.join(profile_path, "Preferences")
            with open(preferences_path, 'w', encoding='utf-8') as f:
                json.dump(preferences, f, indent=2, ensure_ascii=False)
            
            # ✅ Local update state so Chrome recognizes profile immediately
            self.update_local_state(profile_dir, profile_name)
            
            # ✅ Simple error handling
            QMessageBox.information(self, "Success", f"Profile '{profile_name}' created successfully!\nDirectory: {profile_dir}")
            
            # Clear inputs and refresh profiles
            self.profile_name_input.clear()
            self.profile_dir_input.clear()
            self.load_existing_profiles()
            
        except Exception as e:
            # ✅ Clean, straightforward approach
            QMessageBox.critical(self, "Error", f"Failed to create profile: {str(e)}")
    
    def update_local_state(self, profile_dir, profile_name):
        """Update Chrome's Local State file to register the new profile"""
        try:
            local_state_path = os.path.join(self.profiles_dir, "Local State")
            
            # Read existing Local State or create new one
            if os.path.exists(local_state_path):
                with open(local_state_path, 'r', encoding='utf-8') as f:
                    local_state = json.load(f)
            else:
                local_state = {}
            
            # Ensure profile structure exists
            if 'profile' not in local_state:
                local_state['profile'] = {}
            if 'info_cache' not in local_state['profile']:
                local_state['profile']['info_cache'] = {}
            
            # Add new profile to info cache
            local_state['profile']['info_cache'][profile_dir] = {
                "name": profile_name,
                "avatar_index": 0,
                "background_apps": False,
                "is_using_default_name": False,
                "active_time": 0
            }
            
            # Update last active profile
            local_state['profile']['last_used'] = profile_dir
            
            # Write updated Local State
            with open(local_state_path, 'w', encoding='utf-8') as f:
                json.dump(local_state, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Warning: Could not update Local State: {e}")
    
    def load_existing_profiles(self):
        """Load and display existing Chrome profiles"""
        if not os.path.exists(self.profiles_dir):
            return
        
        profiles = []
        try:
            # Read Local State to get profile info
            local_state_path = os.path.join(self.profiles_dir, "Local State")
            if os.path.exists(local_state_path):
                with open(local_state_path, 'r', encoding='utf-8') as f:
                    local_state = json.load(f)
                    profile_info = local_state.get('profile', {}).get('info_cache', {})
                    
                    for profile_id, info in profile_info.items():
                        profile_name = info.get('name', 'Unknown')
                        profile_dir = profile_id
                        created_time = info.get('started_at', 'Unknown')
                        last_used = info.get('active_time', 'Unknown')
                        
                        profiles.append({
                            'name': profile_name,
                            'directory': profile_dir,
                            'created': created_time,
                            'last_used': last_used
                        })
            
            # Also check for profile directories
            for item in os.listdir(self.profiles_dir):
                item_path = os.path.join(self.profiles_dir, item)
                if os.path.isdir(item_path) and item not in ['Default', 'System Profile']:
                    # Check if this profile is not already in the list
                    if not any(p['directory'] == item for p in profiles):
                        profiles.append({
                            'name': item.replace('_', ' ').title(),
                            'directory': item,
                            'created': 'Unknown',
                            'last_used': 'Unknown'
                        })
            
        except Exception as e:
            print(f"Error loading profiles: {e}")
        
        # Populate table
        self.profiles_table.setRowCount(len(profiles))
        for row, profile in enumerate(profiles):
            self.profiles_table.setItem(row, 0, QTableWidgetItem(profile['name']))
            self.profiles_table.setItem(row, 1, QTableWidgetItem(profile['directory']))
            self.profiles_table.setItem(row, 2, QTableWidgetItem(str(profile['created'])))
            self.profiles_table.setItem(row, 3, QTableWidgetItem(str(profile['last_used'])))
            
            # Action buttons
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            launch_btn = QPushButton("Launch")
            launch_btn.setStyleSheet("background-color: #27ae60; color: white; padding: 4px 8px;")
            launch_btn.clicked.connect(lambda checked, p=profile: self.launch_profile(p))
            
            actions_layout.addWidget(launch_btn)
            actions_layout.addStretch()
            
            self.profiles_table.setCellWidget(row, 4, actions_widget)
    
    def launch_profile(self, profile):
        """Launch Chrome with the specified profile"""
        if not self.chrome_path:
            QMessageBox.critical(self, "Error", "Chrome executable not found!")
            return
        
        try:
            cmd = [self.chrome_path, f"--user-data-dir={self.profiles_dir}", f"--profile-directory={profile['directory']}"]
            
            # Add launch options
            if self.incognito_checkbox.isChecked():
                cmd.append("--incognito")
            if self.no_sandbox_checkbox.isChecked():
                cmd.append("--no-sandbox")
            if self.disable_extensions_checkbox.isChecked():
                cmd.append("--disable-extensions")
            
            subprocess.Popen(cmd, shell=True)
            QMessageBox.information(self, "Success", f"Launching profile '{profile['name']}'...")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to launch profile: {str(e)}")
    
    def delete_selected_profile(self):
        """Delete the selected profile"""
        current_row = self.profiles_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a profile to delete.")
            return
        
        profile_name = self.profiles_table.item(current_row, 0).text()
        profile_dir = self.profiles_table.item(current_row, 1).text()
        
        reply = QMessageBox.question(
            self, "Confirm Delete", 
            f"Are you sure you want to delete profile '{profile_name}'?\n\nThis will permanently remove all data for this profile.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                profile_path = os.path.join(self.profiles_dir, profile_dir)
                if os.path.exists(profile_path):
                    # Remove profile directory
                    import shutil
                    shutil.rmtree(profile_path)
                    
                    # Remove from Local State if possible
                    local_state_path = os.path.join(self.profiles_dir, "Local State")
                    if os.path.exists(local_state_path):
                        try:
                            with open(local_state_path, 'r', encoding='utf-8') as f:
                                local_state = json.load(f)
                            
                            if 'profile' in local_state and 'info_cache' in local_state['profile']:
                                if profile_dir in local_state['profile']['info_cache']:
                                    del local_state['profile']['info_cache'][profile_dir]
                                
                                with open(local_state_path, 'w', encoding='utf-8') as f:
                                    json.dump(local_state, f, indent=2, ensure_ascii=False)
                        except Exception as e:
                            print(f"Warning: Could not update Local State: {e}")
                    
                    QMessageBox.information(self, "Success", f"Profile '{profile_name}' deleted successfully!")
                    self.load_existing_profiles()
                else:
                    QMessageBox.warning(self, "Warning", f"Profile directory not found: {profile_path}")
                    
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete profile: {str(e)}")


def main():
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Chrome Profile Manager")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("Chrome Profile Manager")
    
    # Create and show the main window
    window = ChromeProfileManager()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
