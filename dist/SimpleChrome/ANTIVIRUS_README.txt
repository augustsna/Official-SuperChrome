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