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
        print("[OK] PyInstaller is installed")
        return True
    except ImportError:
        print("[WARN] PyInstaller is not installed")
        return False

def install_pyinstaller():
    """Install PyInstaller if not present"""
    print("Installing PyInstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("[OK] PyInstaller installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("[ERROR] Failed to install PyInstaller")
        return False

def build_executable():
    """Build the executable using PyInstaller"""
    print("Building executable...")
    
    # Get the current directory
    current_dir = Path.cwd()
    icon_path = current_dir / "src" / "icon.png"
    main_script = current_dir / "main.py"
    build_dir = current_dir / "build"
    build_dir.mkdir(exist_ok=True)

    # Create a basic Windows version info file to embed metadata (helps reduce AV false positives)
    version_info_path = build_dir / "version_info.txt"
    try:
        version_info_path.write_text(
            """
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable('040904B0', [
        StringStruct('CompanyName', 'SimpleChrome'),
        StringStruct('FileDescription', 'SimpleChrome Application'),
        StringStruct('FileVersion', '1.0.0.0'),
        StringStruct('InternalName', 'SimpleChrome'),
        StringStruct('LegalCopyright', '(c) 2025 SimpleChrome'),
        StringStruct('OriginalFilename', 'SimpleChrome.exe'),
        StringStruct('ProductName', 'SimpleChrome'),
        StringStruct('ProductVersion', '1.0.0.0')
      ])
    ]),
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
""".strip(),
            encoding="utf-8"
        )
    except Exception as e:
        print(f"[WARN] Failed to write version info file: {e}")
    
    # Check if required files exist
    if not icon_path.exists():
        print(f"[ERROR] Icon file not found: {icon_path}")
        return False
    
    if not main_script.exists():
        print(f"[ERROR] Main script not found: {main_script}")
        return False
    
    # PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onedir",  # Prefer onedir to reduce AV false positives
        "--windowed",  # Don't show console window
        f"--icon={icon_path}",  # Set the icon
        "--name=SimpleChrome",  # Name of the executable
        "--distpath=dist",  # Output to dist folder; final dir will be dist/SimpleChrome
        "--clean",  # Clean cache before building
        "--noconfirm",  # Don't ask for confirmation
        "--noupx",  # Ensure UPX compression is not used
        f"--version-file={version_info_path}",  # Embed version metadata
        str(main_script)
    ]
    
    try:
        print("Running PyInstaller...")
        print(f"Command: {' '.join(cmd)}")
        subprocess.check_call(cmd)
        print("[OK] Executable built successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to build executable: {e}")
        return False

def copy_additional_files():
    """Copy additional files needed by the application"""
    print("Copying additional files...")
    
    current_dir = Path.cwd()
    dist_dir = current_dir / "dist" / "SimpleChrome"
    
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
            print(f"[OK] Copied {file_name}")
        else:
            print(f"[WARN] {file_name} not found, skipping...")
    
    # Copy src directory
    src_dir = current_dir / "src"
    dst_src_dir = dist_dir / "src"
    
    if src_dir.exists():
        if dst_src_dir.exists():
            shutil.rmtree(dst_src_dir)
        shutil.copytree(src_dir, dst_src_dir)
        print("[OK] Copied src directory")
    else:
        print("[WARN] src directory not found, skipping...")

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
    dist_dir = Path.cwd() / "dist" / "SimpleChrome"
    exe_path = dist_dir / "SimpleChrome.exe"
    print(f"Executable location: {exe_path}")
    print(f"Additional files have been copied to the {dist_dir} directory.")
    print("\nTo run the application:")
    print("1. Navigate to the dist/SimpleChrome directory")
    print("2. Double-click SimpleChrome.exe")
    print("\nNote: The first run may take a few seconds to start.")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
