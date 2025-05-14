#!/bin/bash
# Restart the AI Writers Workshop MCP Server with proper virtual environment handling

echo "Restarting AI Writers Workshop MCP Server..."

# Find and kill any running MCP server processes
echo "Stopping any running MCP server processes..."
pkill -f "python mcp_server/server.py"

# Wait a moment to ensure processes are terminated
sleep 2

# Change to the project directory
cd /home/ty/Repositories/ai_workspace/ai_writers_workshop/

# Check if .venv directory exists and use it, otherwise try venv
if [ -d ".venv" ]; then
    echo "Activating virtual environment (.venv)..."
    source .venv/bin/activate
elif [ -d "venv" ]; then
    echo "Activating virtual environment (venv)..."
    source venv/bin/activate
else
    echo "No virtual environment found. Creating one..."
    python -m venv .venv
    source .venv/bin/activate
    pip install -e .
fi

# Start the server
echo "Starting MCP server with stdio transport..."
python mcp_server/server.py
