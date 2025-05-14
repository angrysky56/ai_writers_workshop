#!/bin/bash
# Restart the AI Writers Workshop MCP Server

echo "Restarting AI Writers Workshop MCP Server..."

# Find and kill any running MCP server processes
echo "Stopping any running MCP server processes..."
pkill -f "python mcp_server/server.py"

# Wait a moment to ensure processes are terminated
sleep 2

# Change to the project directory
cd /home/ty/Repositories/ai_workspace/ai_writers_workshop/

# Ensure virtual environment is activated
source venv/bin/activate

# Start the server
echo "Starting MCP server with stdio transport..."
python mcp_server/server.py
