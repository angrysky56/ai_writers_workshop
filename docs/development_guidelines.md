# Development Guidelines

This document contains important guidelines for developing the AI Writers Workshop MCP server.

## Package Management

- **Always use `uv`** for Python package management
- **Never use `pip`** directly - this ensures consistent dependency management
- Install packages with: `uv add package`
- Install in development mode: `uv add --dev package`
- Run scripts with: `uv run script`

## Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/) guidelines
- Use type hints for all function parameters and return values
- Add docstrings to all public functions, classes, and modules
- Maximum line length: 88 characters
- Use [black](https://black.readthedocs.io/) for code formatting: `uv run black .`

## Project Structure

```
ai_writers_workshop/
├── .venv/                  # Virtual environment (create with uv venv)
├── docs/                   # Documentation files
├── mcp_server/             # MCP server implementation
│   ├── fastagent_integration/  # Fast Agent integration
│   ├── ollama_integration/     # Ollama integration
│   ├── server.py           # Main server implementation
│   └── ...
├── prompts/                # Prompt definitions
├── resources/              # Resource files
├── config.json             # Server configuration
├── example_mcp_config.json # Example MCP configuration for Claude Desktop
├── requirements.txt        # Project dependencies
├── run_server.sh           # Server runner script
└── setup.py                # Package setup script
```

## Committing Changes

- Write clear, concise commit messages
- Keep commits focused on a single change
- Reference issue numbers in commit messages when applicable

## Testing

- Write tests for new features
- Run tests with: `uv run pytest`
- Ensure existing tests pass before submitting changes

## Integration with Claude Desktop

To integrate with Claude Desktop:

1. Copy the `example_mcp_config.json` file to the Claude Desktop configuration directory
2. Modify paths as needed to point to your local installation
3. Restart Claude Desktop to load the new configuration

## MCP API Guidelines

When adding new tools or resources:

- Keep function signatures simple and clear
- Document parameters and return values thoroughly
- Follow the MCP [official documentation](https://modelcontextprotocol.io)
- Test tools with the MCP Inspector before deployment

## Troubleshooting

If you encounter issues:

- Check the server logs for error messages
- Verify that all dependencies are installed correctly
- Ensure the server is accessible to Claude Desktop
- Test with the MCP Inspector to isolate issues
