#!/bin/bash
# setup.sh - Setup script for AI Writers Workshop

echo "Setting up AI Writers Workshop environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Initialize directory structure and default content
echo "Initializing AI Writers Workshop..."
python mcp_server/initialize.py

echo "Setup complete! You can now run the server with:"
echo "  source venv/bin/activate"
echo "  python mcp_server/server.py"
