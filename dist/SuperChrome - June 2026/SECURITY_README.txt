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