#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Starting OCPI EMSP Backend..."

# Define the virtual environment directory
VENV_DIR="venv"
PYTHON_VERSION="python3.11"

# Check if the required Python version is available
if ! command -v $PYTHON_VERSION &> /dev/null; then
    echo "$PYTHON_VERSION is not installed. Please install Python 3.11 to continue."
    exit 1
fi

# Check if the virtual environment directory exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment with $PYTHON_VERSION..."
    $PYTHON_VERSION -m venv $VENV_DIR
fi

# Activate the virtual environment
source $VENV_DIR/bin/activate

# Install Python dependencies
echo "Installing Python dependencies from requirements.txt..."
pip install -r requirements.txt

# Run the application
echo "Running the application..."
cd core
uvicorn main:app --host 0.0.0.0 --port 8000 --reload --log-level info --access-log
