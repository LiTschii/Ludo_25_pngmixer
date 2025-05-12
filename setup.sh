#!/bin/bash

# Setup script for Ludo PNG Mixer

echo "=== Ludo PNG Mixer Setup ==="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    echo "Please install Python 3.8 or later from https://python.org"
    exit 1
fi

echo "Python 3 found: $(python3 --version)"

# Check if we're in a virtual environment
if [[ -n "$VIRTUAL_ENV" ]]; then
    echo "Virtual environment detected: $VIRTUAL_ENV"
    PIP_CMD="pip"
else
    echo "No virtual environment detected. Creating one..."
    python3 -m venv .venv
    echo "Virtual environment created. Please activate it:"
    echo "  source .venv/bin/activate"
    echo "Then run this script again."
    exit 0
fi

# Install dependencies
echo "Installing dependencies..."
$PIP_CMD install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Setup completed successfully!"
    echo ""
    echo "To run the PNG Mixer:"
    echo "  python png_mixer.py"
    echo ""
    echo "Make sure you have your images ready:"
    echo "  - A-Type: a.png (common), b.png (uncommon), c.png (legendary)"
    echo "  - B-Type: xp.png (normal), xpxd.png (special)"
    echo "  - All images should be 500x500 pixels PNG format"
else
    echo ""
    echo "✗ Error: Installation failed!"
    echo "Please check the error messages above."
    exit 1
fi
