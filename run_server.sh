#!/bin/bash
# run_server.sh - Run the AI Writers Workshop MCP Server

echo "Starting AI Writers Workshop MCP Server..."

# Ensure virtual environment is activated
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found!"
    echo "Please run setup.sh first."
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Run the initialization script if not already run
if [ ! -d "output/library" ]; then
    echo "Initializing AI Writers Workshop..."
    python mcp_server/initialize.py
fi

# Run the server with stdio transport by default
echo "Running MCP server with stdio transport..."
echo "(Ctrl+C to exit)"
python mcp_server/server.py "$@"

# Deactivate virtual environment
deactivate
