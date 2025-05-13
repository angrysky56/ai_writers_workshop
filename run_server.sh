#!/bin/bash

# AI Writers Workshop MCP Server Setup and Runner
# This script manages the virtual environment and runs the MCP server

# Determine the project root directory
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
VENV_DIR="$PROJECT_ROOT/.venv"

# Default settings
TRANSPORT="stdio"
PORT="8000"
HOST="127.0.0.1"
ACTION="run"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Show help message
show_help() {
  echo -e "${BLUE}AI Writers Workshop MCP Server${NC}"
  echo
  echo "Usage: $0 [action] [options]"
  echo
  echo "Actions:"
  echo "  setup               Setup or update the virtual environment"
  echo "  run                 Run the MCP server (default)"
  echo "  inspect             Run with MCP Inspector"
  echo "  install             Install in Claude Desktop"
  echo "  status              Check server status"
  echo "  help                Show this help message"
  echo
  echo "Options:"
  echo "  --transport=TYPE    Transport type (stdio, sse, streamable-http)"
  echo "  --port=PORT         Port for SSE or streamable-http transport"
  echo "  --host=HOST         Host for SSE or streamable-http transport"
  echo
  echo "Examples:"
  echo "  $0 setup                    Create or update the virtual environment"
  echo "  $0                          Run the server with stdio transport"
  echo "  $0 run --transport=sse      Run the server with SSE transport"
  echo "  $0 inspect                  Run with MCP Inspector"
  echo "  $0 install                  Install in Claude Desktop"
  echo
}

# Setup virtual environment and install dependencies
setup_environment() {
  echo -e "${BLUE}Setting up virtual environment...${NC}"
  
  # Check if uv is installed
  if ! command -v uv &> /dev/null; then
    echo -e "${RED}Error: uv is not installed. Please install it first.${NC}"
    echo "You can install uv with: pip install uv"
    exit 1
  fi
  
  # Create virtual environment if it doesn't exist
  if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Creating new virtual environment...${NC}"
    uv venv
  else
    echo -e "${YELLOW}Using existing virtual environment...${NC}"
  fi
  
  # Activate virtual environment and install dependencies
  echo -e "${YELLOW}Installing dependencies...${NC}"
  source "$VENV_DIR/bin/activate" || { echo -e "${RED}Failed to activate virtual environment${NC}"; exit 1; }
  
  # Install setuptools first to ensure setup.py works
  uv pip install setuptools || { echo -e "${RED}Failed to install setuptools${NC}"; exit 1; }
  
  # Install requirements
  uv pip install -r "$PROJECT_ROOT/requirements.txt" || { echo -e "${RED}Failed to install requirements${NC}"; exit 1; }
  
  # Install the package in development mode
  uv pip install -e "$PROJECT_ROOT" || { echo -e "${RED}Failed to install package${NC}"; exit 1; }
  
  echo -e "${GREEN}Setup complete!${NC}"
}

# Run the MCP server
run_server() {
  echo -e "${BLUE}Running AI Writers Workshop MCP Server with ${YELLOW}$TRANSPORT${BLUE} transport${NC}"
  
  # Make sure virtual environment exists
  if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Virtual environment not found. Setting up...${NC}"
    setup_environment
  fi
  
  # Activate virtual environment
  source "$VENV_DIR/bin/activate" || { echo -e "${RED}Failed to activate virtual environment${NC}"; exit 1; }
  
  # Add project root to PYTHONPATH for imports
  export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"
  
  # Run the server with selected transport
  if [ "$TRANSPORT" = "stdio" ]; then
    uv run --directory "$PROJECT_ROOT/mcp_server" server.py
  elif [ "$TRANSPORT" = "sse" ]; then
    uv run --directory "$PROJECT_ROOT/mcp_server" server.py --transport sse --port $PORT --host $HOST
  elif [ "$TRANSPORT" = "streamable-http" ]; then
    uv run --directory "$PROJECT_ROOT/mcp_server" server.py --transport streamable-http --port $PORT --host $HOST
  else
    echo -e "${RED}Unknown transport type: $TRANSPORT${NC}"
    echo "Supported types: stdio, sse, streamable-http"
    exit 1
  fi
}

# Run with MCP Inspector
run_inspector() {
  echo -e "${BLUE}Running AI Writers Workshop MCP Server with MCP Inspector${NC}"
  
  # Make sure virtual environment exists
  if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Virtual environment not found. Setting up...${NC}"
    setup_environment
  fi
  
  # Activate virtual environment
  source "$VENV_DIR/bin/activate" || { echo -e "${RED}Failed to activate virtual environment${NC}"; exit 1; }
  
  # Run with MCP Inspector
  mcp dev "$PROJECT_ROOT/mcp_server/server.py"
}

# Install in Claude Desktop
install_claude() {
  echo -e "${BLUE}Installing AI Writers Workshop MCP Server in Claude Desktop${NC}"
  
  # Make sure virtual environment exists
  if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Virtual environment not found. Setting up...${NC}"
    setup_environment
  fi
  
  # Activate virtual environment
  source "$VENV_DIR/bin/activate" || { echo -e "${RED}Failed to activate virtual environment${NC}"; exit 1; }
  
  # Check if example_mcp_config.json exists
  if [ ! -f "$PROJECT_ROOT/example_mcp_config.json" ]; then
    echo -e "${RED}Error: example_mcp_config.json not found${NC}"
    exit 1
  fi
  
  # Copy to a temporary file with substituted ${HOME}
  TMP_CONFIG=$(mktemp)
  cat "$PROJECT_ROOT/example_mcp_config.json" | sed "s|\${HOME}|$HOME|g" > "$TMP_CONFIG"
  
  # Install with MCP CLI
  echo -e "${YELLOW}Installing with MCP CLI...${NC}"
  mcp install "$PROJECT_ROOT/mcp_server/server.py" --name "AI Writers Workshop"
  
  echo -e "${GREEN}Installation complete!${NC}"
  echo -e "${YELLOW}Note: You may need to restart Claude Desktop to use the MCP server.${NC}"
}

# Check server status
check_status() {
  echo -e "${BLUE}Checking AI Writers Workshop MCP Server status${NC}"
  
  # Make sure virtual environment exists
  if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Status: ${RED}Not set up${NC}"
    echo -e "Run '$0 setup' to set up the virtual environment."
    return
  fi
  
  echo -e "${YELLOW}Environment: ${GREEN}Set up${NC}"
  
  # Check if server is installed in Claude Desktop
  source "$VENV_DIR/bin/activate" || { echo -e "${RED}Failed to activate virtual environment${NC}"; exit 1; }
  
  if mcp list | grep -q "AI Writers Workshop"; then
    echo -e "${YELLOW}Claude Desktop: ${GREEN}Installed${NC}"
  else
    echo -e "${YELLOW}Claude Desktop: ${RED}Not installed${NC}"
    echo -e "Run '$0 install' to install in Claude Desktop."
  fi
  
  # Check Ollama integration
  if command -v ollama &> /dev/null; then
    if ollama list &> /dev/null; then
      echo -e "${YELLOW}Ollama: ${GREEN}Available${NC}"
      echo -e "${BLUE}Ollama models:${NC}"
      ollama list | tail -n +2 | head -n 5
      NUM_MODELS=$(ollama list | wc -l)
      if [ $NUM_MODELS -gt 6 ]; then
        echo -e "${BLUE}...and $((NUM_MODELS - 6)) more models.${NC}"
      fi
    else
      echo -e "${YELLOW}Ollama: ${RED}Installed but not running${NC}"
      echo -e "Start Ollama with 'ollama serve'"
    fi
  else
    echo -e "${YELLOW}Ollama: ${RED}Not installed${NC}"
    echo -e "Install Ollama from https://ollama.ai/"
  fi
  
  # Check Fast Agent integration
  if python -c "import fast_agent_mcp" &> /dev/null; then
    echo -e "${YELLOW}Fast Agent: ${GREEN}Available${NC}"
  else
    echo -e "${YELLOW}Fast Agent: ${RED}Not installed${NC}"
    echo -e "Install Fast Agent with 'uv pip install fast_agent_mcp'"
  fi
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    setup|run|inspect|install|status|help)
      ACTION="$1"
      shift
      ;;
    --transport=*)
      TRANSPORT="${1#*=}"
      shift
      ;;
    --port=*)
      PORT="${1#*=}"
      shift
      ;;
    --host=*)
      HOST="${1#*=}"
      shift
      ;;
    --help)
      show_help
      exit 0
      ;;
    *)
      echo -e "${RED}Unknown option: $1${NC}"
      echo "Run '$0 help' for usage information"
      exit 1
      ;;
  esac
done

# Execute the selected action
case $ACTION in
  setup)
    setup_environment
    ;;
  run)
    run_server
    ;;
  inspect)
    run_inspector
    ;;
  install)
    install_claude
    ;;
  status)
    check_status
    ;;
  help)
    show_help
    ;;
  *)
    echo -e "${RED}Unknown action: $ACTION${NC}"
    show_help
    exit 1
    ;;
esac
