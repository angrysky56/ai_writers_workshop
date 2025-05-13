# AI Writers Workshop MCP Server

A Model Context Protocol (MCP) server that provides narrative, character, and archetypal storytelling tools to AI assistants.

## 🚀 Quick Start

Run the setup script to create a virtual environment and install dependencies:

```bash
# Setup the environment
./run_server.sh setup

# Check the status
./run_server.sh status

# Optional: Install Fast Agent integration
./setup_fastagent.sh

# Install in Claude Desktop
./run_server.sh install

# Run with MCP Inspector for testing
./run_server.sh inspect
```

## 📋 Overview

The AI Writers Workshop MCP server exposes a set of storytelling tools focused on:

- Archetypal narrative patterns (Hero's Journey, Transformation, etc.)
- Character archetypes and development
- Symbolic systems and thematic connections
- Narrative structure analysis and generation

This server integrates with:
- Ollama for local LLM inference (optional)
- Fast Agent for advanced workflow capabilities (optional)

## 🔧 Installation and Setup

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Ollama (optional) - Install from [ollama.ai](https://ollama.ai)

### Setup Options

#### Using the Setup Script

The easiest way to set up is using the provided shell script:

```bash
# Setup the environment
./run_server.sh setup

# Optional: Install Fast Agent integration
./setup_fastagent.sh
```

#### Manual Setup

If you prefer to set up manually:

1. Create a virtual environment:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   uv pip install setuptools
   uv pip install -r requirements.txt
   uv pip install -e .
   ```

3. Install Fast Agent (optional):
   ```bash
   uv pip install fast_agent_mcp
   ```

## 🚀 Usage

### Command-Line Interface

The `run_server.sh` script provides a convenient interface for managing the MCP server:

```bash
# Show help
./run_server.sh help

# Run the server with stdio transport (default)
./run_server.sh run

# Run with SSE transport
./run_server.sh run --transport=sse --port=8000

# Run with streamable-http transport
./run_server.sh run --transport=streamable-http --port=8000

# Run with MCP Inspector
./run_server.sh inspect

# Install in Claude Desktop
./run_server.sh install

# Check server status
./run_server.sh status
```

### Integration with Claude Desktop

To use the MCP server with Claude Desktop:

1. Install the server in Claude Desktop:
   ```bash
   ./run_server.sh install
   ```

2. Restart Claude Desktop to load the MCP server.

3. The AI Writers Workshop tools will now be available to Claude.

## 📚 Available Tools

### Narrative Pattern Tools

- `list_patterns`: List available narrative patterns
- `get_pattern_details`: Get detailed information about a pattern
- `analyze_narrative`: Analyze a narrative structure against a pattern
- `generate_outline`: Generate a structured outline based on a pattern

### Character Tools

- `list_archetypes`: List available character archetypes
- `get_archetype_details`: Get detailed information about an archetype
- `create_character`: Create a character based on archetypal patterns
- `develop_character_arc`: Develop a character arc within a narrative structure

### Storytelling Tools

- `generate_scene`: Generate a scene based on pattern elements
- `find_symbolic_connections`: Find symbolic connections for themes

### Ollama Integration (Optional)

- `list_ollama_models`: List available Ollama models
- `run_ollama_prompt`: Run a prompt with an Ollama LLM

### Fast Agent Integration (Optional)

- `list_fastagent_scripts`: List available Fast Agent scripts
- `create_fastagent_script`: Create a Fast Agent script
- `run_narrative_agent`: Run a narrative development agent

## 🔍 Resources

Access resources directly through resource URIs:

- `writers_workshop://patterns/{pattern_name}`: Access pattern information
- `writers_workshop://character/{archetype_name}`: Access character archetype information
- `writers_workshop://guide`: Access the usage guide

## 📄 Documentation

See the `docs` directory for more detailed documentation:

- [Development Guidelines](docs/development_guidelines.md)
- [Archetypal Concepts](docs/concepts.md)

## 📝 Troubleshooting

If you encounter issues:

1. **Environment Problems**:
   - Run `./run_server.sh setup` to ensure the environment is properly set up
   - Check status with `./run_server.sh status`

2. **MCP Server Issues**:
   - Test with MCP Inspector: `./run_server.sh inspect`
   - Check logs for error messages

3. **Claude Desktop Integration**:
   - Ensure Claude Desktop is configured correctly
   - Run `./run_server.sh install` to reinstall
   - Restart Claude Desktop after installation

## License

This project is licensed under the MIT License - see the LICENSE file for details.
