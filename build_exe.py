#!/usr/bin/env python3
"""
Build script for SuperChrome executable with logo
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
    dist_dir = current_dir / "dist" / "SuperChrome"
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
        StringStruct('CompanyName', 'SuperChrome Development Team'),
        StringStruct('FileDescription', 'SuperChrome'),
        StringStruct('FileVersion', '1.0.0.0'),
        StringStruct('InternalName', 'SuperChrome'),
        StringStruct('LegalCopyright', 'Copyright (c) 2025 SuperChrome Development Team. All rights reserved.'),
        StringStruct('OriginalFilename', 'SuperChrome.exe'),
        StringStruct('ProductName', 'SuperChrome Profile Manager'),
        StringStruct('ProductVersion', '1.0.0.0'),
        StringStruct('Comments', 'Open source Chrome profile management utility built with PyQt6'),
        StringStruct('LegalTrademarks', 'SuperChrome is an independent project, not affiliated with Google Chrome')
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
        "--name=SuperChrome",  # Name of the executable
        "--distpath=dist",  # Output to dist folder; final dir will be dist/SuperChrome
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
    """Create a README file explaining antivirus and Smart App Control false positives"""
    current_dir = Path.cwd()
    dist_dir = current_dir / "dist" / "SuperChrome"
    readme_path = dist_dir / "SECURITY_README.txt"
    
    readme_content = """
SUPERCHROME SECURITY & SMART APP CONTROL INFO
=============================================

If Windows Smart App Control (SAC) or your Antivirus software blocks this program, 
this is a FALSE POSITIVE common with newly built Python executables.

WHY THIS HAPPENS:
- Windows Smart App Control (SAC) blocks apps that are not "known-good" or signed.
- PyInstaller bundles are often flagged by heuristics because they "unpack" code.
- This application is unsigned because code signing certificates are expensive.

HOW TO UNBLOCK FOR SMART APP CONTROL:
-------------------------------------
1. Right-click 'SuperChrome.exe' in this folder.
2. Select 'Properties'.
3. If you see an 'Unblock' checkbox at the bottom, check it and click 'Apply'.
4. If SAC still blocks it, you may need to set SAC to 'Evaluation' or 'Off' in:
   Windows Security -> App & browser control -> Smart App Control settings.

THIS APPLICATION IS SAFE:
-------------------------
- Open source tool for managing Chrome browser profiles.
- No network communication, no data collection, no telemetry.
- Source code: https://github.com/Official-SuperChrome (Check it yourself!)
- Built with PyQt6 (Standard GUI framework).

LOCAL SIGNING (FOR DEVELOPERS):
-------------------------------
If you are building this yourself and SAC keeps blocking it, you can "self-sign" 
the executable. A helper script 'sign_locally.ps1' has been generated in the 
build directory to help you do this.

To use it:
1. Right-click 'sign_locally.ps1' -> Run with PowerShell.
2. This creates a local certificate and signs the EXE.
3. You may still need to 'Unblock' the file in Properties afterwards.

Generated: 2026
SuperChrome Development Team
"""
    
    try:
        readme_path.write_text(readme_content.strip(), encoding="utf-8")
        # Remove old file if it exists
        old_readme = dist_dir / "ANTIVIRUS_README.txt"
        if old_readme.exists():
            old_readme.unlink()
        print("[OK] Created security information README")
    except Exception as e:
        print(f"[WARN] Failed to create security README: {e}")

def create_signing_script():
    """Create a PowerShell script to self-sign the executable locally"""
    current_dir = Path.cwd()
    dist_dir = current_dir / "dist" / "SuperChrome"
    script_path = dist_dir / "sign_locally.ps1"
    
    script_content = """
# SuperChrome Local Signing Script
# This script creates a local self-signed certificate and signs the EXE
# Run this if Smart App Control or Defender keeps blocking the program

$exePath = Join-Path $PSScriptRoot "SuperChrome.exe"

if (-not (Test-Path $exePath)) {
    Write-Host "Error: SuperChrome.exe not found in $PSScriptRoot" -ForegroundColor Red
    exit
}

Write-Host "Creating local self-signed certificate..." -ForegroundColor Cyan
$cert = New-SelfSignedCertificate -Type CodeSigningCert -Subject "CN=SuperChrome-Local-Dev" -KeyLength 2048 -NotAfter (Get-Date).AddYears(5) -CertStoreLocation "Cert:\\CurrentUser\\My"

Write-Host "Signing executable..." -ForegroundColor Cyan
Set-AuthenticodeSignature -FilePath $exePath -Certificate $cert

Write-Host "Trusting the certificate locally..." -ForegroundColor Cyan
$certPath = Join-Path $PSScriptRoot "SuperChromeLocal.cer"
Export-Certificate -Cert $cert -FilePath $certPath
Import-Certificate -FilePath $certPath -CertStoreLocation "Cert:\\CurrentUser\\Root"

Write-Host "`nSuccess! SuperChrome.exe has been signed and the certificate trusted." -ForegroundColor Green
Write-Host "If Windows still blocks it, right-click SuperChrome.exe -> Properties -> Check 'Unblock'." -ForegroundColor Yellow
Pause
"""
    try:
        script_path.write_text(script_content.strip(), encoding="utf-8")
        print("[OK] Created local signing helper script")
    except Exception as e:
        print(f"[WARN] Failed to create signing script: {e}")

def copy_additional_files():
    """Copy additional files needed by the application"""
    print("Copying additional files...")
    
    current_dir = Path.cwd()
    dist_dir = current_dir / "dist" / "SuperChrome"
    
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
    
    # Copy icon.png
    icon_src = current_dir / "src" / "icon.png"
    icon_dst = exe_src_dir / "icon.png"  # Put it in the created src folder
    if icon_src.exists():
        shutil.copy2(icon_src, icon_dst)
        print("[OK] Copied src/icon.png to exe/src/icon.png")
    else:
        print("[WARN] src/icon.png not found, skipping copy...")
    
    # Copy icon2.png
    icon2_src = current_dir / "src" / "icon2.png"
    icon2_dst = exe_src_dir / "icon2.png"
    if icon2_src.exists():
        shutil.copy2(icon2_src, icon2_dst)
        print("[OK] Copied src/icon2.png to exe/src/icon2.png")
    else:
        print("[WARN] src/icon2.png not found, skipping copy...")

    # Create antivirus information file
    create_antivirus_readme()
    
    # Create local signing script
    create_signing_script()

    # Don't hide the src directory - user wants it visible
    print("[OK] Keeping src directory visible")

def main():
    """Main build function"""
    print("=" * 50)
    print("SuperChrome Executable Builder")
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
    dist_dir = Path.cwd() / "dist" / "SuperChrome"
    exe_path = dist_dir / "SuperChrome.exe"
    print(f"Executable location: {exe_path}")
    print(f"Additional files have been copied to the {dist_dir} directory.")
    print("\nTo run the application:")
    print("1. Navigate to the dist/SuperChrome directory")
    print("2. Double-click SuperChrome.exe")
    print("\nIMPORTANT - Smart App Control & Antivirus:")
    print("- If Windows Smart App Control blocks the program, it's a FALSE POSITIVE.")
    print("- To unblock: Right-click SuperChrome.exe -> Properties -> Check 'Unblock' -> Apply.")
    print("- If it still blocks, run 'sign_locally.ps1' as administrator in the dist folder.")
    print("- See SECURITY_README.txt in the dist folder for detailed information.")
    print("\nNote: The first run may take a few seconds to start.")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
