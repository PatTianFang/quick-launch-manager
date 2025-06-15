# Quick Launch Manager

[简体中文](./README.md) | [English](./README.en.md)

## Introduction

Quick Launch Manager is a Python-based Windows utility that provides quick access to your frequently used programs and folders through a system tray icon. It helps you manage shortcuts efficiently and supports auto-startup with Windows.

## Features

- **System Tray Integration**: Runs in system tray for easy access
- **Visual Management**: Intuitive interface for shortcut management
- **File/Folder Support**: Add shortcuts to both programs and folders
- **Auto Startup**: Optional Windows startup integration
- **Single Instance**: Automatically manages program states
- **Easy Uninstall**: Complete uninstallation feature

## Installation

1. Ensure Python 3.6 or higher is installed
2. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/quick-launch-manager.git
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage Guide

### Basic Operations

1. **Start the Program**:
   ```bash
   python src/main.py
   ```
   The management interface will appear automatically with a tray icon

2. **Add Shortcuts**:
   - Click "Add" button
   - Enter shortcut name
   - In the selection dialog:
     * Choose "File" or "Folder"
     * Browse and select target
     * Confirm to add

3. **Manage Shortcuts**:
   - Edit: Select and click "Edit"
   - Delete: Select and click "Delete"
   - Use: Click through tray menu

### Advanced Features

1. **Auto Startup**:
   - Check "Auto Startup" in main interface
   - Uncheck to disable

2. **Minimize to Tray**:
   - Automatically minimizes when closing main window
   - Click tray icon > "Manage Shortcuts" to reopen

3. **Uninstall**:
   - Click "Uninstall" in tray menu
   - Automatically:
     * Removes startup settings
     * Closes all programs
     * Exits application

## Detailed Instructions

### Interface Overview

1. **Main Window**
   - Shortcut List: Shows all added shortcuts
   - Add Button: Create new shortcuts
   - Edit Button: Modify selected shortcut
   - Delete Button: Remove selected shortcut
   - Auto Startup: Control program startup behavior

2. **Tray Menu**
   - Manage Shortcuts: Open main interface
   - Shortcut List: Click to run
   - About: View program information
   - Uninstall: Remove program
   - Exit: Close program

### Operation Steps

1. **Adding Shortcuts**
   - Click "Add" button
   - Enter shortcut name (e.g., Notepad)
   - In the file selection dialog:
     * Choose "File" or "Folder" type
     * Navigate to target location
     * Select program or folder
     * Click "OK" to confirm

2. **Editing Shortcuts**
   - Select item in list
   - Click "Edit" button
   - Modify name and path
   - Save changes

3. **Deleting Shortcuts**
   - Select item in list
   - Click "Delete" button
   - Confirm deletion

4. **Using Shortcuts**
   - Click tray icon to open menu
   - Click desired shortcut
   - Previous program will close automatically

### Troubleshooting

1. **Program Won't Start**
   - Check Python version (3.6+ required)
   - Verify dependencies installation
   - Check permissions

2. **Shortcuts Not Showing**
   - Verify path correctness
   - Check file existence
   - Refresh tray menu

3. **Auto Startup Issues**
   - Check system permissions
   - Verify registry settings
   - Re-enable auto startup

### Tips & Tricks

1. **Efficient Usage**
   - Add frequently used programs
   - Use descriptive names
   - Organize shortcuts logically

2. **Management Tips**
   - Regularly clean unused shortcuts
   - Backup important configurations
   - Update invalid paths