import sys
import os
import json
import subprocess
import psutil
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QListWidget, QLabel, 
                             QLineEdit, QMessageBox, QDialog, QFormLayout,
                             QGroupBox, QSplitter, QFrame, QTextEdit)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QIcon, QPixmap


class ChromeProfileManager:
    """Manages Chrome profiles and their operations"""
    
    def __init__(self):
        self.chrome_data_path = self._get_chrome_data_path()
        self.profiles = {}
        self.refresh_profiles()
    
    def _get_chrome_data_path(self):
        """Get Chrome user data directory based on OS"""
        if sys.platform == "win32":
            return Path.home() / "AppData" / "Local" / "Google" / "Chrome" / "User Data"
        elif sys.platform == "darwin":  # macOS
            return Path.home() / "Library" / "Application Support" / "Google" / "Chrome"
        else:  # Linux
            return Path.home() / ".config" / "google-chrome"
    
    def refresh_profiles(self):
        """Refresh the list of available Chrome profiles"""
        self.profiles.clear()
        
        if not self.chrome_data_path.exists():
            return
        
        # Read Local State file to get profile information
        local_state_path = self.chrome_data_path / "Local State"
        if local_state_path.exists():
            try:
                with open(local_state_path, 'r', encoding='utf-8') as f:
                    local_state = json.load(f)
                    profile_info = local_state.get('profile', {}).get('info_cache', {})
                    
                    for profile_name, profile_data in profile_info.items():
                        self.profiles[profile_name] = {
                            'name': profile_data.get('name', profile_name),
                            'path': self.chrome_data_path / profile_name,
                            'is_ephemeral': profile_data.get('is_ephemeral', False),
                            'is_ephemeral_profile': profile_data.get('is_ephemeral_profile', False),
                            'managed_user_id': profile_data.get('managed_user_id', ''),
                            'signin': profile_data.get('signin', {}),
                            'gaia_id': profile_data.get('gaia_id', ''),
                            'user_name': profile_data.get('user_name', ''),
                            'avatar_icon': profile_data.get('avatar_icon', ''),
                            'background_apps': profile_data.get('background_apps', False),
                            'exit_type': profile_data.get('exit_type', ''),
                            'browser_show_home_button': profile_data.get('browser_show_home_button', False),
                            'last_active_time': profile_data.get('last_active_time', 0)
                        }
            except Exception as e:
                print(f"Error reading Local State: {e}")
        
        # Also check for profile directories
        for item in self.chrome_data_path.iterdir():
            if item.is_dir() and item.name.startswith('Profile '):
                if item.name not in self.profiles:
                    self.profiles[item.name] = {
                        'name': item.name,
                        'path': item,
                        'is_ephemeral': False,
                        'is_ephemeral_profile': False,
                        'managed_user_id': '',
                        'signin': {},
                        'gaia_id': '',
                        'user_name': '',
                        'avatar_icon': '',
                        'background_apps': False,
                        'exit_type': '',
                        'browser_show_home_button': False,
                        'last_active_time': 0
                    }
    
    def get_profile_list(self):
        """Get list of profile names"""
        return list(self.profiles.keys())
    
    def get_profile_info(self, profile_name):
        """Get detailed information about a profile"""
        return self.profiles.get(profile_name, {})
    
    def launch_profile(self, profile_name, url=None):
        """Launch Chrome with a specific profile"""
        if profile_name not in self.profiles:
            raise ValueError(f"Profile '{profile_name}' not found")
        
        # Build Chrome command
        chrome_cmd = self._get_chrome_executable()
        if not chrome_cmd:
            raise FileNotFoundError("Chrome executable not found")
        
        # Use the main Chrome user data directory and specify the profile
        cmd = [chrome_cmd, f"--user-data-dir={self.chrome_data_path}"]
        
        # Add profile directory flag (only for non-Default profiles)
        if profile_name != "Default":
            cmd.append(f"--profile-directory={profile_name}")
        
        if url:
            cmd.append(url)
        
        try:
            subprocess.Popen(cmd, start_new_session=True)
            return True
        except Exception as e:
            raise Exception(f"Failed to launch Chrome: {e}")
    
    def _get_chrome_executable(self):
        """Get Chrome executable path based on OS"""
        if sys.platform == "win32":
            # Common Chrome paths on Windows
            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                str(Path.home() / "AppData" / "Local" / "Google" / "Chrome" / "Application" / "chrome.exe")
            ]
        elif sys.platform == "darwin":  # macOS
            chrome_paths = [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            ]
        else:  # Linux
            chrome_paths = [
                "/usr/bin/google-chrome",
                "/usr/bin/google-chrome-stable",
                "/usr/bin/chromium-browser"
            ]
        
        for path in chrome_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def create_profile(self, profile_name):
        """Create a new Chrome profile"""
        if profile_name in self.profiles:
            raise ValueError(f"Profile '{profile_name}' already exists")
        
        # Create profile directory
        profile_path = self.chrome_data_path / profile_name
        profile_path.mkdir(exist_ok=True)
        
        # Refresh profiles to include the new one
        self.refresh_profiles()
        
        return profile_name
    
    def delete_profile(self, profile_name):
        """Delete a Chrome profile"""
        if profile_name not in self.profiles:
            raise ValueError(f"Profile '{profile_name}' not found")
        
        profile_path = self.profiles[profile_name]['path']
        
        # Check if Chrome is running with this profile
        if self._is_profile_running(profile_name):
            raise Exception(f"Cannot delete profile '{profile_name}' while Chrome is running with it")
        
        # Delete profile directory
        import shutil
        try:
            shutil.rmtree(profile_path)
            del self.profiles[profile_name]
            return True
        except Exception as e:
            raise Exception(f"Failed to delete profile: {e}")
    
    def _is_profile_running(self, profile_name):
        """Check if Chrome is running with a specific profile"""
        profile_path = self.profiles[profile_name]['path']
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'] and 'chrome' in proc.info['name'].lower():
                    cmdline = proc.info['cmdline']
                    if cmdline and any(str(profile_path) in arg for arg in cmdline):
                        return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return False


class ProfileInfoDialog(QDialog):
    """Dialog to show detailed profile information"""
    
    def __init__(self, profile_info, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Profile Information")
        self.setModal(True)
        self.resize(500, 400)
        
        layout = QVBoxLayout()
        
        # Profile name
        name_label = QLabel(f"<h2>{profile_info.get('name', 'Unknown')}</h2>")
        layout.addWidget(name_label)
        
        # Profile details
        details_text = QTextEdit()
        details_text.setReadOnly(True)
        
        details = []
        details.append(f"<b>Path:</b> {profile_info.get('path', 'Unknown')}")
        details.append(f"<b>User Name:</b> {profile_info.get('user_name', 'Not set')}")
        details.append(f"<b>GAIA ID:</b> {profile_info.get('gaia_id', 'Not set')}")
        details.append(f"<b>Ephemeral:</b> {profile_info.get('is_ephemeral', False)}")
        details.append(f"<b>Background Apps:</b> {profile_info.get('background_apps', False)}")
        details.append(f"<b>Exit Type:</b> {profile_info.get('exit_type', 'Unknown')}")
        details.append(f"<b>Last Active:</b> {profile_info.get('last_active_time', 0)}")
        
        details_text.setHtml("<br>".join(details))
        layout.addWidget(details_text)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)


class CreateProfileDialog(QDialog):
    """Dialog to create a new profile"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New Profile")
        self.setModal(True)
        self.resize(300, 150)
        
        layout = QFormLayout()
        
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter profile name")
        layout.addRow("Profile Name:", self.name_edit)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.create_btn = QPushButton("Create")
        self.cancel_btn = QPushButton("Cancel")
        
        self.create_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(self.create_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addRow(button_layout)
        
        self.setLayout(layout)
    
    def get_profile_name(self):
        return self.name_edit.text().strip()


class ChromeManagerUI(QMainWindow):
    """Main UI for Chrome Profile Manager"""
    
    def __init__(self):
        super().__init__()
        self.chrome_manager = ChromeProfileManager()
        self.init_ui()
        self.refresh_profile_list()
        
        # Auto-refresh timer (less frequent to avoid disrupting user interaction)
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_profile_list)
        self.refresh_timer.start(30000)  # Refresh every 30 seconds instead of 5
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Chrome Profile Manager")
        self.setGeometry(100, 100, 800, 600)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Title
        title_label = QLabel("Chrome Profile Manager")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Splitter for profile list and controls
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left panel - Profile list
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        profile_label = QLabel("Available Profiles:")
        profile_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        left_layout.addWidget(profile_label)
        
        self.profile_list = QListWidget()
        self.profile_list.itemSelectionChanged.connect(self.on_profile_selected)
        left_layout.addWidget(self.profile_list)
        
        splitter.addWidget(left_panel)
        
        # Right panel - Controls
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Profile info group
        info_group = QGroupBox("Profile Information")
        info_layout = QVBoxLayout(info_group)
        
        self.info_label = QLabel("Select a profile to view information")
        self.info_label.setWordWrap(True)
        info_layout.addWidget(self.info_label)
        
        right_layout.addWidget(info_group)
        
        # Actions group
        actions_group = QGroupBox("Actions")
        actions_layout = QVBoxLayout(actions_group)
        
        # Launch buttons
        self.launch_btn = QPushButton("Launch Profile")
        self.launch_btn.clicked.connect(self.launch_selected_profile)
        self.launch_btn.setEnabled(False)
        actions_layout.addWidget(self.launch_btn)
        
        self.launch_with_url_btn = QPushButton("Launch with URL")
        self.launch_with_url_btn.clicked.connect(self.launch_with_url)
        self.launch_with_url_btn.setEnabled(False)
        actions_layout.addWidget(self.launch_with_url_btn)
        
        # URL input
        self.url_edit = QLineEdit()
        self.url_edit.setPlaceholderText("Enter URL (e.g., https://www.google.com)")
        actions_layout.addWidget(self.url_edit)
        
        # Profile management buttons
        self.info_btn = QPushButton("View Details")
        self.info_btn.clicked.connect(self.show_profile_info)
        self.info_btn.setEnabled(False)
        actions_layout.addWidget(self.info_btn)
        
        self.delete_btn = QPushButton("Delete Profile")
        self.delete_btn.clicked.connect(self.delete_selected_profile)
        self.delete_btn.setEnabled(False)
        actions_layout.addWidget(self.delete_btn)
        
        # Create new profile
        self.create_btn = QPushButton("Create New Profile")
        self.create_btn.clicked.connect(self.create_new_profile)
        actions_layout.addWidget(self.create_btn)
        
        # Refresh controls
        refresh_layout = QHBoxLayout()
        
        self.refresh_btn = QPushButton("Refresh Profiles")
        self.refresh_btn.clicked.connect(self.refresh_profile_list)
        refresh_layout.addWidget(self.refresh_btn)
        
        self.auto_refresh_btn = QPushButton("Auto-Refresh: ON")
        self.auto_refresh_btn.setCheckable(True)
        self.auto_refresh_btn.setChecked(True)
        self.auto_refresh_btn.clicked.connect(self.toggle_auto_refresh)
        refresh_layout.addWidget(self.auto_refresh_btn)
        
        actions_layout.addLayout(refresh_layout)
        
        right_layout.addWidget(actions_group)
        
        splitter.addWidget(right_panel)
        
        # Set splitter proportions
        splitter.setSizes([300, 500])
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def refresh_profile_list(self):
        """Refresh the profile list"""
        # Store current selection before refreshing
        current_profile_name = self.get_selected_profile_name()
        
        self.chrome_manager.refresh_profiles()
        
        self.profile_list.clear()
        profiles = self.chrome_manager.get_profile_list()
        
        for profile_name in profiles:
            profile_info = self.chrome_manager.get_profile_info(profile_name)
            display_name = profile_info.get('name', profile_name)
            # Create item and store the actual profile name as item data
            from PyQt6.QtWidgets import QListWidgetItem
            item = QListWidgetItem(display_name)
            item.setData(Qt.ItemDataRole.UserRole, profile_name)
            self.profile_list.addItem(item)
        
        # Restore selection if it was previously selected
        if current_profile_name:
            for i in range(self.profile_list.count()):
                item = self.profile_list.item(i)
                if item.data(Qt.ItemDataRole.UserRole) == current_profile_name:
                    self.profile_list.setCurrentItem(item)
                    break
        
        self.statusBar().showMessage(f"Found {len(profiles)} profiles")
    
    def on_profile_selected(self):
        """Handle profile selection"""
        current_item = self.profile_list.currentItem()
        if current_item:
            # Get the actual profile name from item data
            profile_name = current_item.data(Qt.ItemDataRole.UserRole)
            if not profile_name:
                # Fallback to text if no data stored
                profile_name = current_item.text()
            
            profile_info = self.chrome_manager.get_profile_info(profile_name)
            
            # Update info label
            info_text = f"<b>Name:</b> {profile_info.get('name', 'Unknown')}<br>"
            info_text += f"<b>Path:</b> {profile_info.get('path', 'Unknown')}<br>"
            info_text += f"<b>User:</b> {profile_info.get('user_name', 'Not set')}<br>"
            info_text += f"<b>Ephemeral:</b> {profile_info.get('is_ephemeral', False)}"
            
            self.info_label.setText(info_text)
            
            # Enable buttons
            self.launch_btn.setEnabled(True)
            self.launch_with_url_btn.setEnabled(True)
            self.info_btn.setEnabled(True)
            self.delete_btn.setEnabled(True)
        else:
            self.info_label.setText("Select a profile to view information")
            self.launch_btn.setEnabled(False)
            self.launch_with_url_btn.setEnabled(False)
            self.info_btn.setEnabled(False)
            self.delete_btn.setEnabled(False)
    
    def get_selected_profile_name(self):
        """Get the name of the currently selected profile"""
        current_item = self.profile_list.currentItem()
        if current_item:
            # Get the actual profile name from item data
            profile_name = current_item.data(Qt.ItemDataRole.UserRole)
            if profile_name:
                return profile_name
            # Fallback to text if no data stored
            return current_item.text()
        return None
    
    def launch_selected_profile(self):
        """Launch the selected profile"""
        profile_name = self.get_selected_profile_name()
        if not profile_name:
            return
        
        try:
            self.chrome_manager.launch_profile(profile_name)
            self.statusBar().showMessage(f"Launched profile: {profile_name}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to launch profile: {e}")
    
    def launch_with_url(self):
        """Launch the selected profile with a specific URL"""
        profile_name = self.get_selected_profile_name()
        if not profile_name:
            return
        
        url = self.url_edit.text().strip()
        if not url:
            QMessageBox.warning(self, "Warning", "Please enter a URL")
            return
        
        # Add http:// if no protocol specified
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        try:
            self.chrome_manager.launch_profile(profile_name, url)
            self.statusBar().showMessage(f"Launched profile: {profile_name} with URL: {url}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to launch profile: {e}")
    
    def show_profile_info(self):
        """Show detailed profile information"""
        profile_name = self.get_selected_profile_name()
        if not profile_name:
            return
        
        profile_info = self.chrome_manager.get_profile_info(profile_name)
        dialog = ProfileInfoDialog(profile_info, self)
        dialog.exec()
    
    def delete_selected_profile(self):
        """Delete the selected profile"""
        profile_name = self.get_selected_profile_name()
        if not profile_name:
            return
        
        reply = QMessageBox.question(
            self, 
            "Confirm Delete", 
            f"Are you sure you want to delete profile '{profile_name}'?\n\nThis action cannot be undone!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.chrome_manager.delete_profile(profile_name)
                self.refresh_profile_list()
                self.statusBar().showMessage(f"Deleted profile: {profile_name}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete profile: {e}")
    
    def create_new_profile(self):
        """Create a new profile"""
        dialog = CreateProfileDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            profile_name = dialog.get_profile_name()
            if profile_name:
                try:
                    self.chrome_manager.create_profile(profile_name)
                    self.refresh_profile_list()
                    self.statusBar().showMessage(f"Created profile: {profile_name}")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to create profile: {e}")
            else:
                QMessageBox.warning(self, "Warning", "Please enter a profile name")
    
    def toggle_auto_refresh(self):
        """Toggle auto-refresh on/off"""
        if self.auto_refresh_btn.isChecked():
            self.refresh_timer.start(30000)  # 30 seconds
            self.auto_refresh_btn.setText("Auto-Refresh: ON")
            self.statusBar().showMessage("Auto-refresh enabled")
        else:
            self.refresh_timer.stop()
            self.auto_refresh_btn.setText("Auto-Refresh: OFF")
            self.statusBar().showMessage("Auto-refresh disabled")


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Chrome Profile Manager")
    app.setApplicationVersion("1.0")
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show the main window
    window = ChromeManagerUI()
    window.show()
    
    # Start the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
