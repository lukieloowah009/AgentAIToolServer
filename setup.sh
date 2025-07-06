#!/bin/bash
# Setup script for Agent AI POC project

echo "Setting up virtual environment..."

# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Initialize the application
echo "Initializing the application..."
python app_init.py

echo ""
echo "Setup complete!"
echo "To activate the virtual environment, run:"
echo "source .venv/bin/activate"
echo ""
echo "To start the server, run:"
echo "uvicorn main:app --reload"
