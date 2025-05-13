#!/bin/bash

# AI Writers Workshop - Fast Agent Integration Setup
# This script installs and configures Fast Agent for MCP integration

# Determine the project root directory
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
VENV_DIR="$PROJECT_ROOT/.venv"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}AI Writers Workshop - Fast Agent Integration Setup${NC}"
echo

# Activate virtual environment
if [ -d "$VENV_DIR" ]; then
  echo -e "${YELLOW}Activating virtual environment...${NC}"
  source "$VENV_DIR/bin/activate" || { 
    echo -e "${RED}Failed to activate virtual environment${NC}"
    echo -e "${YELLOW}Run './run_server.sh setup' first${NC}"
    exit 1
  }
else
  echo -e "${RED}Virtual environment not found${NC}"
  echo -e "${YELLOW}Run './run_server.sh setup' first${NC}"
  exit 1
fi

# Install Fast Agent
echo -e "${YELLOW}Installing Fast Agent...${NC}"
uv pip install fast_agent_mcp || {
  echo -e "${RED}Failed to install Fast Agent${NC}"
  exit 1
}

# Configure Fast Agent
echo -e "${YELLOW}Configuring Fast Agent...${NC}"

# Ensure fastagent.config.yaml exists with correct configuration
cat > "$PROJECT_ROOT/mcp_server/fastagent.config.yaml" << EOL
# AI Writers Workshop MCP Server configuration

# Default model for all agents (can be overridden with --model flag)
default_model: "qwen3:latest"

# MCP servers configuration
mcp:
  servers:
    # Core AI Writers Workshop server
    ai_writers_workshop:
      command: "uv"
      args:
      - "--directory"
      - "$PROJECT_ROOT/mcp_server"
      - "run"
      - "server.py"
      env:
        PYTHONPATH: "$PROJECT_ROOT:\${PYTHONPATH}"

    # Ollama server integration (if needed)
    ollama:
      command: "ollama"
      args: ["serve"]

# Root configuration for file access
roots:
  prompts: "$PROJECT_ROOT/prompts"
  resources: "$PROJECT_ROOT/resources"
EOL

echo -e "${GREEN}Fast Agent configuration complete!${NC}"
echo
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Run './run_server.sh status' to verify Fast Agent integration"
echo "2. Run './run_server.sh install' to install in Claude Desktop"
echo "3. Run './run_server.sh inspect' to test with MCP Inspector"
