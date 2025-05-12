#!/bin/bash

# Ludo PNG Mixer CLI Shortcut
# Usage: ./cli.sh [options]

# Check if Python script exists
if [ ! -f "png_mixer_cli.py" ]; then
    echo "Error: png_mixer_cli.py not found in current directory!"
    exit 1
fi

# Check if running in virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    # Check if .venv exists and activate it
    if [ -d ".venv" ]; then
        echo "🔄 Activating virtual environment..."
        source .venv/bin/activate
        if [ $? -ne 0 ]; then
            echo "❌ Failed to activate virtual environment!"
            exit 1
        fi
    else
        echo "⚠️  Warning: No virtual environment detected. Consider creating one:"
        echo "   python3 -m venv .venv"
        echo "   source .venv/bin/activate"
        echo "   pip install -r requirements.txt"
        echo ""
    fi
fi

# Forward all arguments to the Python script
python png_mixer_cli.py "$@"

# Capture the exit code
EXIT_CODE=$?

# If we activated venv, deactivate it
if [ -n "$VIRTUAL_ENV" ] && [ -d ".venv" ]; then
    deactivate
fi

exit $EXIT_CODE
