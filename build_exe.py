#!/usr/bin/env python3
"""
Build script for SimpleChrome executable with logo
Uses PyInstaller to create a standalone executable
"""

import os
import sys
import subprocess
import shutil
import ctypes
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
    
    # Try to clean up dist directory if it exists (handle permission errors gracefully)
    dist_dir = current_dir / "dist" / "SimpleChrome"
    if dist_dir.exists():
        try:
            shutil.rmtree(dist_dir)
            print("[OK] Cleaned existing dist directory")
        except (PermissionError, OSError) as e:
            print(f"[WARN] Could not clean dist directory (in use): {e}")
            print("[INFO] Proceeding with build anyway...")

    # Create enhanced Windows version info file to embed metadata (helps reduce AV false positives)
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
        StringStruct('CompanyName', 'SimpleChrome Development Team'),
        StringStruct('FileDescription', 'Chrome Profile Management Tool - Legitimate Application'),
        StringStruct('FileVersion', '1.0.0.0'),
        StringStruct('InternalName', 'SimpleChrome'),
        StringStruct('LegalCopyright', 'Copyright (c) 2025 SimpleChrome Development Team. All rights reserved.'),
        StringStruct('OriginalFilename', 'SimpleChrome.exe'),
        StringStruct('ProductName', 'SimpleChrome Profile Manager'),
        StringStruct('ProductVersion', '1.0.0.0'),
        StringStruct('Comments', 'Open source Chrome profile management utility built with PyQt6'),
        StringStruct('LegalTrademarks', 'SimpleChrome is an independent project, not affiliated with Google Chrome')
      ])
    ]),
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
""".strip(),
            encoding="utf-8"
        )
        print("[OK] Enhanced version info file created")
    except Exception as e:
        print(f"[WARN] Failed to write version info file: {e}")
    
    # Check if required files exist
    if not icon_path.exists():
        print(f"[ERROR] Icon file not found: {icon_path}")
        return False
    
    if not main_script.exists():
        print(f"[ERROR] Main script not found: {main_script}")
        return False
    
    # PyInstaller command with enhanced AV false positive mitigation
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onedir",  # Prefer onedir to reduce AV false positives
        "--windowed",  # Don't show console window
        f"--icon={icon_path}",  # Set the icon
        "--name=SimpleChrome",  # Name of the executable
        "--distpath=dist",  # Output to dist folder; final dir will be dist/SimpleChrome
        # Remove --clean to avoid directory lock issues
        "--noconfirm",  # Don't ask for confirmation
        "--noupx",  # Ensure UPX compression is not used
        "--strip",  # Strip debug symbols to reduce file size and false positives
        "--optimize=2",  # Enable Python bytecode optimization
        "--exclude-module=tkinter",  # Exclude unused modules that may trigger AV
        "--exclude-module=matplotlib",
        "--exclude-module=numpy",
        "--exclude-module=scipy",
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

def create_antivirus_readme():
    """Create a README file explaining antivirus false positives"""
    current_dir = Path.cwd()
    dist_dir = current_dir / "dist" / "SimpleChrome"
    readme_path = dist_dir / "ANTIVIRUS_README.txt"
    
    readme_content = """
ANTIVIRUS FALSE POSITIVE INFORMATION
===================================

If your antivirus software flags SimpleChrome.exe as suspicious, this is likely a 
FALSE POSITIVE. This is common with PyInstaller-generated executables.

WHY THIS HAPPENS:
- PyInstaller bundles Python applications into executables
- Some antivirus engines flag packed executables as suspicious
- Machine learning-based detection may trigger on legitimate software

THIS APPLICATION IS SAFE:
- Open source Chrome profile management tool
- Built with legitimate PyQt6 framework
- No network communication or data collection
- Source code available for inspection

WHAT TO DO:
1. Add SimpleChrome.exe to your antivirus whitelist/exclusions
2. Report false positive to your antivirus vendor
3. Verify file integrity by checking the embedded version information

TECHNICAL DETAILS:
- Built with PyInstaller and enhanced metadata
- Digital signature: Not available (requires paid certificate)
- Version info embedded to reduce false positives
- UPX compression disabled to avoid detection

For support or to report issues, visit the project repository.

Generated: 2025
SimpleChrome Development Team
"""
    
    try:
        readme_path.write_text(readme_content.strip(), encoding="utf-8")
        print("[OK] Created antivirus information README")
    except Exception as e:
        print(f"[WARN] Failed to create antivirus README: {e}")

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
    
    # Create src folder in exe directory and copy src/icon.png into it
    exe_src_dir = dist_dir / "src"
    exe_src_dir.mkdir(exist_ok=True)
    print("[OK] Created src folder in exe directory")
    
    icon_src = current_dir / "src" / "icon.png"
    icon_dst = exe_src_dir / "icon.png"  # Put it in the created src folder
    if icon_src.exists():
        shutil.copy2(icon_src, icon_dst)
        print("[OK] Copied src/icon.png to exe/src/icon.png")
    else:
        print("[WARN] src/icon.png not found, skipping copy...")

    # Create antivirus information file
    create_antivirus_readme()

    # Don't hide the src directory - user wants it visible
    print("[OK] Keeping src directory visible")

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
    print("\nIMPORTANT - Antivirus False Positives:")
    print("- If your antivirus flags the executable, it's likely a FALSE POSITIVE")
    print("- This is common with PyInstaller applications")
    print("- Add SimpleChrome.exe to your antivirus exclusions/whitelist")
    print("- See ANTIVIRUS_README.txt in the dist folder for detailed information")
    print("\nNote: The first run may take a few seconds to start.")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
