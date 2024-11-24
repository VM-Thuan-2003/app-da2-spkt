#!/bin/bash

# Check if PyInstaller is installed, and install it if not
if ! command -v pyinstaller &>/dev/null; then
    echo "PyInstaller not found, installing..."
    pip install pyinstaller
fi

# Define your script
SCRIPT_NAME="app.py"
ICON_NAME="icon.ico"

# Detect the operating system
OS=$(uname -s)

if [[ "$OS" == "Linux" ]]; then
    echo "Detected OS: Ubuntu (Linux)"

    # Build the executable for Linux
    echo "Building Linux executable..."
    pyinstaller --onefile --windowed "$SCRIPT_NAME"

    # Check if the executable is created
    if [ -f "dist/app" ]; then
        echo "Build successful! The executable is in the 'dist' folder."
        chmod +x "dist/app"
        echo "Running the executable..."
        "./dist/app"
    else
        echo "Build failed. Please check for errors above."
    fi

elif [[ "$OS" == "MINGW"* || "$OS" == "CYGWIN"* || "$OS" == "MSYS"* ]]; then
    echo "Detected OS: Windows"

    # Build the EXE for Windows
    if [ -f "$ICON_NAME" ]; then
        echo "Building Windows EXE with icon..."
        pyinstaller --onefile --windowed --icon="$ICON_NAME" "$SCRIPT_NAME"
    else
        echo "Building Windows EXE without icon..."
        pyinstaller --onefile --windowed "$SCRIPT_NAME"
    fi

    # Check if the EXE is created
    if [ -f "dist/app.exe" ]; then
        echo "Build successful! The EXE is in the 'dist' folder."
        echo "Running the EXE..."
        "./dist/app.exe"
    else
        echo "Build failed. Please check for errors above."
    fi

else
    echo "Unsupported OS: $OS"
fi
