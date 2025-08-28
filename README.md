# SuperChrome

A PyQt6-based application for managing Chrome browser profiles with a modern, Chrome-like interface.

## Features

- **Chrome Profile Management**: Automatically detect and manage Chrome browser profiles
- **Modern UI**: Clean, Chrome-inspired interface with smooth animations
- **Profile Organization**: Categorize profiles by channel types and sub-types
- **Search & Filter**: Advanced search and filtering capabilities
- **Profile Launching**: One-click Chrome profile launching
- **Profile Editing**: Edit profile metadata and settings
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Building the Executable

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Quick Build

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the build script**:
   ```bash
   python build_exe.py
   ```

The build script will:
- Check if PyInstaller is installed and install it if needed
- Build a standalone executable with your logo
- Copy all necessary files to the `dist` directory

### Manual Build

If you prefer to build manually:

1. **Install PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

2. **Build the executable**:
   ```bash
   pyinstaller --onefile --windowed --icon=src/icon.png --name=SuperChrome --clean --noconfirm main.py
   ```

3. **Copy additional files** to the `dist` directory:
   - `config.json`
   - `profile.json`
   - `down_arrow.svg`
   - `src/` directory

## Running the Application

### From Source
```bash
python main.py
```

### From Executable
1. Navigate to the `dist` directory
2. Double-click `SuperChrome.exe`

## File Structure

```
SuperChrome/
├── main.py              # Main application file
├── build_exe.py         # Build script for executable
├── requirements.txt     # Python dependencies
├── config.json          # Application configuration
├── profile.json         # Profile data storage
├── down_arrow.svg       # UI assets
└── src/
    └── icon.png         # Application icon
```

## Configuration

The application uses `config.json` for configuration:

```json
{
  "channel_types": ["user_custom", "Chrome Profile", "Standard", "Premium", "Basic"],
  "sub_types": ["Personal", "Business", "Gaming", "Development", "Testing", "Marketing", "Education"],
  "app_settings": {
    "window_title": "Super Chrome",
    "window_size": [760, 577],
    "icon_path": "src/icon.png"
  }
}
```

## Usage

1. **Launch the application**
2. **Collect Chrome Profiles**: Click "Collect" to automatically detect Chrome profiles
3. **Search & Filter**: Use the search bar and filters to find specific profiles
4. **Edit Profiles**: Select a profile and click "Edit" to modify metadata
5. **Launch Profiles**: Select a profile and click "Launch" to open Chrome with that profile
6. **Cleanup**: Use "Clean" to remove profiles that no longer exist in Chrome

## Troubleshooting

### Build Issues

- **PyInstaller not found**: Run `pip install pyinstaller`
- **Missing dependencies**: Run `pip install -r requirements.txt`
- **Icon not found**: Ensure `src/icon.png` exists

### Runtime Issues

- **Chrome not found**: Ensure Google Chrome is installed in the default location
- **No profiles detected**: Make sure Chrome has been used at least once
- **Permission errors**: Run as administrator if needed

### Performance

- The first run of the executable may take a few seconds to start
- Large numbers of profiles may slow down the interface
- Use the search and filter features to manage large profile lists

## Development

### Running in Development Mode
```bash
python main.py
```

### Dependencies
- **PyQt6**: GUI framework
- **PyInstaller**: Executable creation (build time only)

### Adding New Features
1. Modify `main.py` for UI changes
2. Update `config.json` for new configuration options
3. Test thoroughly before building new executable

## License

This project is open source. Feel free to modify and distribute.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the configuration options
3. Ensure all dependencies are properly installed

