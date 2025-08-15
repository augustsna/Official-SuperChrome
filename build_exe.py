#!/usr/bin/env python3
"""
Build script for SimpleChrome executable with logo
Uses PyInstaller to create a standalone executable
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        print("✓ PyInstaller is installed")
        return True
    except ImportError:
        print("✗ PyInstaller is not installed")
        return False

def install_pyinstaller():
    """Install PyInstaller if not present"""
    print("Installing PyInstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install PyInstaller")
        return False

def build_executable():
    """Build the executable using PyInstaller"""
    print("Building executable...")
    
    # Get the current directory
    current_dir = Path.cwd()
    icon_path = current_dir / "src" / "icon.png"
    main_script = current_dir / "main.py"
    
    # Check if required files exist
    if not icon_path.exists():
        print(f"✗ Icon file not found: {icon_path}")
        return False
    
    if not main_script.exists():
        print(f"✗ Main script not found: {main_script}")
        return False
    
    # PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",  # Create a single executable file
        "--windowed",  # Don't show console window
        f"--icon={icon_path}",  # Set the icon
        "--name=SimpleChrome",  # Name of the executable
        "--clean",  # Clean cache before building
        "--noconfirm",  # Don't ask for confirmation
        str(main_script)
    ]
    
    try:
        print("Running PyInstaller...")
        print(f"Command: {' '.join(cmd)}")
        subprocess.check_call(cmd)
        print("✓ Executable built successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to build executable: {e}")
        return False

def copy_additional_files():
    """Copy additional files needed by the application"""
    print("Copying additional files...")
    
    current_dir = Path.cwd()
    dist_dir = current_dir / "dist"
    
    # Files to copy
    files_to_copy = [
        "config.json",
        "profile.json",
        "down_arrow.svg"
    ]
    
    for file_name in files_to_copy:
        src_file = current_dir / file_name
        dst_file = dist_dir / file_name
        
        if src_file.exists():
            shutil.copy2(src_file, dst_file)
            print(f"✓ Copied {file_name}")
        else:
            print(f"⚠ Warning: {file_name} not found, skipping...")
    
    # Copy src directory
    src_dir = current_dir / "src"
    dst_src_dir = dist_dir / "src"
    
    if src_dir.exists():
        if dst_src_dir.exists():
            shutil.rmtree(dst_src_dir)
        shutil.copytree(src_dir, dst_src_dir)
        print("✓ Copied src directory")
    else:
        print("⚠ Warning: src directory not found, skipping...")

def main():
    """Main build function"""
    print("=" * 50)
    print("SimpleChrome Executable Builder")
    print("=" * 50)
    
    # Check and install PyInstaller if needed
    if not check_pyinstaller():
        if not install_pyinstaller():
            print("Failed to install PyInstaller. Please install it manually:")
            print("pip install pyinstaller")
            return False
    
    # Build the executable
    if not build_executable():
        return False
    
    # Copy additional files
    copy_additional_files()
    
    print("\n" + "=" * 50)
    print("Build completed successfully!")
    print("=" * 50)
    print("Executable location: dist/SimpleChrome.exe")
    print("Additional files have been copied to the dist directory.")
    print("\nTo run the application:")
    print("1. Navigate to the dist directory")
    print("2. Double-click SimpleChrome.exe")
    print("\nNote: The first run may take a few seconds to start.")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
