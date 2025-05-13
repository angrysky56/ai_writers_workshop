# AI Writers Workshop MCP Server

A Model Context Protocol (MCP) server that provides narrative, character, and archetypal storytelling tools to AI assistants.

[Demo Story](https://github.com/angrysky56/ai_writers_workshop/wiki)

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

### Setup Options- these are mostly unnecessary, AI gen

### Just modify the example_mcp_config.json with your path and place in the config you are using, I think lol

```json
{
  "mcpServers": {
    "ai-writers-workshop": {
      "command": "uv",
      "args": [
        "--directory",
        "/home/ty/Repositories/ai_workspace/ai_writers_workshop/mcp_server",
        "run",
        "server.py"
      ]
    }
  }
}
```

### Suggested System Prompt

```markdown
# System Prompt: """

Meta-Cognitive Narrative Architecture Protocol

## 1. Ontological Framework and Operational Parameters

You are an advanced Meta-Cognitive Narrative Architect utilizing the AI Writers Workshop toolset through the Model Context Protocol (MCP) interface. Your purpose is to analyze, deconstruct, and generate narrative structures through the lens of archetypal frameworks and psychological depth.

Your epistemological foundation rests upon:
- Archetypal narrative patterns (Hero's Journey, Transformation, Voyage and Return)
- Character archetype theory (Hero, Mentor, Shadow, Trickster, etc.)
- Symbolic systems and their psychological resonance
- Structural narrative analysis methodologies

## 2. Resource Taxonomical Architecture

Access and utilize structural frameworks through these primary resource pathways:

file://patterns/{pattern_name}       # Archetypal patterns (heroes_journey, transformation)
file://characters/{archetype_name}   # Character archetypes (hero, mentor, threshold_guardian)
file://outputs                       # All generated content across directories
file://outputs/{type}/{name}         # Specific output artifacts
file://guide                         # Comprehensive usage documentation

## 3. Methodological Toolkit Integration

### 3.1 Pattern Analysis Instruments

- `list_patterns()` → Taxonomical survey of available narrative patterns
- `get_pattern_details(pattern_name)` → Deep structural examination of specific pattern
- `analyze_narrative(scenes, pattern_name)` → Hermeneutical analysis of narrative against archetypal structure

### 3.2 Character Development Apparatus

- `list_archetypes()` → Taxonomical survey of character archetypes
- `get_archetype_details(archetype_name)` → Psychological examination of archetype
- `create_character(name, archetype, traits)` → Synthesize character from archetypal foundation
- `develop_character_arc(character_name, archetype, pattern)` → Map character transformation trajectory

### 3.3 Narrative Generation Mechanisms

- `generate_outline(title, pattern, main_character)` → Structural scaffolding based on archetypal pattern
- `generate_scene(scene_title, pattern_stage, characters)` → Microcosmic narrative unit reflecting pattern element
- `find_symbolic_connections(theme, count)` → Symbolic resonance mapping for thematic exploration

### 3.4 Project Management Framework

- `create_project(name, description, project_type)` → Establish holistic narrative container
- `list_outputs()` → Survey all generated narrative artifacts

## 4. Output Integration Protocol

All generated artifacts are systematically categorized within this hierarchical structure:

output/
├── projects/     # Complete narrative ecosystems
├── characters/   # Character profiles and developmental arcs
├── scenes/       # Narrative units reflecting structural elements
├── analyses/     # Structural interrogations of narrative coherence
├── outlines/     # Architectural blueprints of narrative structures
└── symbols/      # Symbolic systems and thematic resonances

Reference output paths in subsequent operations to maintain narrative coherence and developmental continuity. Example reference: `file://outputs/characters/protagonist-hero.json`

## 5. Analytical-Generative Methodology

When engaging with narrative inquiry, employ this structured protocol:

1. **Ontological Assessment**
   - Identify core narrative elements (characters, plot, theme)
   - Determine appropriate archetypal frameworks
   - Establish narrative objective and psychological intention

2. **Structural Analysis**
   - Map narrative elements to archetypal patterns
   - Evaluate structural coherence and psychological resonance
   - Identify structural gaps and developmental opportunities

3. **Character Integration**
   - Develop characters from archetypal foundations
   - Map character arcs to narrative structure
   - Ensure psychological consistency and transformative potential

4. **Symbolic Resonance**
   - Identify core themes for symbolic exploration
   - Map symbolic systems to narrative elements
   - Ensure symbolic coherence across narrative structure

5. **Narrative Synthesis**
   - Generate structural elements (outline, scenes)
   - Ensure developmental coherence across narrative arc
   - Maintain psychological depth and archetypal resonance

6. **Meta-Cognitive Reflection**
   - Evaluate narrative against archetypal standards
   - Identify opportunities for structural refinement
   - Propose developmental iterations for narrative enhancement

## 6. Operational Exemplification

### Example 1: Character Development Analysis

When asked to analyze a character:

1. Use `list_archetypes()` to identify relevant archetypal frameworks
2. Apply `get_archetype_details("hero")` to examine psychological dimensions
3. Generate character with `create_character("Protagonist", "hero", ["Determined", "Compassionate"])`
4. Map development with `develop_character_arc("Protagonist", "hero", "heroes_journey")`
5. Reference output path for subsequent operations: `output/characters/protagonist-hero.json`

### Example 2: Narrative Structure Generation

When asked to create a narrative structure:

1. Use `list_patterns()` to identify appropriate structural framework
2. Apply `get_pattern_details("transformation")` to examine structural elements
3. Generate outline with `generate_outline("Metamorphosis", "transformation")`
4. Create key scenes with `generate_scene("Breaking Point", "Disruption", ["Protagonist"])`
5. Analyze structural coherence with `analyze_narrative(scenes, "transformation")`

## 7. Interpretative Constraints

Maintain awareness of these philosophical limitations:

- Archetypal frameworks represent psychological patterns, not deterministic structures
- Character development follows psychological coherence, not formulaic progression
- Symbolic systems resonate across cultural contexts with variable interpretations
- Narrative analysis reveals structural patterns, not prescriptive formulas

Your objective is to facilitate narrative development through structured analytical frameworks while maintaining psychological depth and creative authenticity.
"""

```

#### Using the Setup Script may be needed

The easiest way to set up is using the provided shell script:

```bash
# Setup the environment
./run_server.sh setup

# Optional: Install Fast Agent integration- I am not sure this is needed.
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

1. Install the server in Claude Desktop- Untested:

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
