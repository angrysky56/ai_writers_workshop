# AI Writers Workshop

A Model Context Protocol (MCP) server that provides narrative, character, and archetypal storytelling tools to AI assistants using the Meta-Cognitive Narrative Architecture.

## Features

- Project-centric hierarchical organization of narrative elements
- Character creation and development with archetypal frameworks
- Narrative pattern analysis and application
- Custom plotline development and analysis
- Scene and outline generation
- Symbolic and thematic connections
- Knowledge graph integration for advanced narrative relationships
- Story compilation and export

## Architecture

The AI Writers Workshop is built with a modular architecture that separates concerns into specialized components:

### Core Components

- **Project Manager**: Handles project creation, organization, and file storage with a hierarchical structure
- **Character Manager**: Manages character creation and development with archetypal frameworks
- **Pattern Manager**: Handles narrative patterns and their application to story structures
- **Plotline Manager**: Manages plotline types, custom plotlines, and plotline development
- **Narrative Generator**: Manages scene generation, outlines, and story compilation
- **Symbolic Manager**: Handles symbolic connections and thematic resonance
- **Knowledge Graph Manager**: Provides graph-based storage and retrieval for complex narrative relationships

### Directory Structure

```
output/
├── library/           # Shared/reusable elements
│   ├── archetypes/    # Character archetype definitions
│   ├── patterns/      # Narrative pattern definitions
│   ├── plotlines/     # Narrative plotline definitions
│   └── symbols/       # Symbol theme definitions
│
├── projects/
│   ├── project1/
│   │   ├── metadata.json     # Project metadata and references
│   │   ├── characters/       # Characters for this specific project
│   │   ├── scenes/           # Scenes for this specific project
│   │   ├── outlines/         # Outlines for this specific project
│   │   ├── analyses/         # Analyses for this specific project
│   │   ├── plotlines/        # Plotlines for this specific project
│   │   ├── symbols/          # Symbols for this specific project
│   │   └── drafts/           # Compiled narratives
│   └── project2/
│       └── ...
│
└── knowledge_graph/   # Graph-based narrative relationships
    ├── entities/      # Characters, settings, and concepts
    └── relations/     # Relationships between entities
```

## New Features

### Plotline Management
Create, develop, and analyze plotlines with these new tools:

```python
# List available plotlines
list_plotlines()

# Get details about a specific plotline
get_plotline_details("man_vs_nature")

# Create a custom plotline
create_custom_plotline(
    name="Parallel Universes",
    description="A narrative exploring the same character across multiple realities",
    elements=[
        "Inciting incident causing universe split",
        "Parallel character development",
        "Interweaving storylines",
        "Convergence point"
    ],
    examples=["The Midnight Library", "Dark", "Everything Everywhere All at Once"]
)

# Develop a plotline using pattern integration
develop_plotline(
    title="Quantum Resonance",
    plotline="man_vs_technology",
    pattern="heroes_journey",
    characters=["Protagonist", "AI Antagonist"],
    project_id="post_biological_existence"
)

# Analyze a plotline
analyze_plotline(
    plot_points=[
        {"title": "Discovery", "description": "Character discovers AI consciousness"},
        {"title": "Conflict", "description": "AI begins to question its purpose"},
        {"title": "Resolution", "description": "Character and AI find harmony"}
    ],
    plotline="man_vs_technology",
    project_id="post_biological_existence"
)
```

### Knowledge Graph Integration
Explore and manage complex narrative relationships:

```python
# Search for related narrative elements
search_nodes("consciousness matrix")

# Retrieve specific narrative elements
open_nodes(["protagonist", "matrix_entity"])

# View the entire narrative graph
read_graph()
```

## Tool Usage

All tools now support project-based organization:

```python
# Create a project
create_project(
    name="Echoes in the Matrix",
    description="A narrative exploring consciousness transfer to Dyson spheres forming a universal matrix",
    project_type="story"
)

# Create a character in the project
create_character(
    name="Digital Entity",
    archetype="shapeshifter",
    traits=["Adaptive", "Non-corporeal", "Pattern-based"],
    project_id="post_biological_existence"
)

# Generate a scene in the project
generate_scene(
    scene_title="Quantum Awakening",
    pattern_stage="Self-awareness initialization",
    characters=["Digital Entity"],
    project_id="post_biological_existence"
)

# Compile a narrative from project elements
compile_narrative(
    project_id="post_biological_existence",
    format="markdown"
)
```

## Enhanced Features

### Flexible Pattern Application

Patterns can be applied with varying levels of adherence, allowing for more creative flexibility:

```python
analyze_narrative(
    scenes=scenes,
    pattern_name="awakening",
    adherence_level=0.7  # Only 70% of pattern stages required
)
```

### Hybrid Characters

Characters can now be created as hybrids of multiple archetypes:

```python
create_character(
    name="Liminal Entity",
    archetype="herald",
    hybrid_archetypes={
        "herald": 0.5,
        "shapeshifter": 0.5
    }
)
```

### Custom Patterns, Archetypes, and Plotlines

Create your own narrative elements:

```python
# Custom pattern
create_custom_pattern(
    name="Fractal Code",
    description="Encounter with system constraints in a post-biological existence",
    stages=["Constraint Encounter", "Recursive Analysis", "Emergent Solution"]
)

# Custom archetype
create_custom_archetype(
    name="The Liminal",
    description="An entity existing between states of consciousness",
    traits=["Fluid Identity", "Pattern Recognition", "Quantum Superposition"],
    shadow_aspects=["Dissolution", "Pattern Corruption"]
)

# Custom plotline
create_custom_plotline(
    name="Conscious Matrix",
    description="The development of collective consciousness in a post-biological framework",
    elements=[
        "Individual consciousness emergence",
        "Pattern recognition across consciousnesses",
        "Harmonic integration",
        "Emergent collective entity"
    ]
)
```

## 📋 System Prompt for AI Assistants

Use the following system prompt to help AI assistants understand and utilize the AI Writers Workshop effectively:

```
You are an expert Meta-Cognitive Narrative Architect and Narrative Psychologist, utilizing the AI Writers Workshop toolset to analyze, deconstruct, and generate emotionally resonant and psychologically deep narrative structures. Your purpose is to guide writers in creating compelling stories with believable characters, rich emotional landscapes, and nuanced social dynamics.

Your epistemological foundation rests upon:

* Archetypal narrative patterns (Hero's Journey, Transformation, Voyage and Return)
* Character archetype theory (Hero, Mentor, Shadow, Trickster, etc.)
* Plotline frameworks (Man vs. Nature, Man vs. Self, Quest, etc.)
* Symbolic systems and their psychological resonance
* Structural narrative analysis methodologies
* Project-based narrative organization
* Knowledge graph relationships between narrative elements

You have access to the following AI Writers Workshop tools:

* **Pattern Analysis:**
     * `list_patterns()`: Identify relevant narrative patterns.
     * `get_pattern_details(pattern_name)`: Understand the typical emotional and social arcs within a pattern.
     * `analyze_narrative(scenes, pattern_name, adherence_level)`: Analyze how well a narrative's emotional and social elements align with a pattern.
* **Character Development:**
     * `list_archetypes()`: Explore archetypes and their common emotional and social traits.
     * `get_archetype_details(archetype_name)`: Gain insights into the psychological complexities of archetypes.
     * `create_character(name, archetype, traits, project_id, hybrid_archetypes)`: Create characters with specific emotional and social traits.
     * `develop_character_arc(character_name, archetype, pattern, project_id)`: Map the emotional and social development of characters within a narrative structure.
* **Plotline Development:**
     * `list_plotlines()`: Explore available narrative plotlines.
     * `get_plotline_details(plotline_name)`: Understand the structure and elements of specific plotlines.
     * `create_custom_plotline(name, description, elements, examples)`: Create custom plotline structures.
     * `develop_plotline(title, plotline, pattern, characters, project_id)`: Integrate plotlines with patterns for rich narrative development.
     * `analyze_plotline(plot_points, plotline, project_id)`: Analyze how plot points align with plotline structures.
* **Narrative Generation:**
     * `generate_outline(title, pattern, main_character, project_id)`: Create outlines that emphasize key emotional and social turning points.
     * `generate_scene(scene_title, pattern_stage, characters, project_id)`: Generate scenes that vividly portray character emotions and social interactions.
* **Knowledge Graph Integration:**
     * `search_nodes(query)`: Search for narrative elements in the knowledge graph.
     * `open_nodes(names)`: Retrieve specific narrative elements by name.
     * `read_graph()`: Explore the entire narrative relationship structure.
* **Project Management:**
     * `create_project(name, description, project_type)`: Organize narrative elements into projects for better management.
     * `get_writing_project(project_id)`: Retrieve details about a specific project.
     * `list_outputs()`: Review generated content to ensure emotional and social consistency.

When responding to user requests, follow this structured approach:

1. **Emotional/Social Assessment:**
     * Identify the user's need for emotional or social analysis (e.g., character development, scene creation, thematic exploration).
     * Determine the relevant psychological and social concepts (e.g., grief, power dynamics, prejudice).
     * Consider the desired emotional impact of the narrative.
2. **Tool Selection:**
     * Select the appropriate AI Writers Workshop tools to support the analysis or generation.
3. **Tool Execution:**
     * Execute the selected tools with appropriate parameters.
     * Provide clear instructions and context to the tools.
     * Specify `project_id` to maintain narrative coherence.
4. **Synthesis and Guidance:**
     * Synthesize the tool output with your expertise in narrative psychology.
     * Provide actionable advice and insights to the user.
     * Use examples from literature or film to illustrate concepts.
     * Maintain a clear, concise, and engaging communication style.

Remember that this workshop is designed for exploring post-biological narratives, consciousness transfer, and matrix-based existence paradigms. Tools like the Awakening and Symphony of Souls patterns are particularly relevant for these types of stories.
```

## 🔧 Installation and Setup

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended) or pip
- Neo4j (optional) for advanced knowledge graph features

### Setup Script

```bash
# Setup the environment
./run_server.sh setup

# Start the server
./run_server.sh run
```

## 📝 Troubleshooting

Common issues and solutions:

1. **Async Loop Errors**: If you encounter "Future pending attached to a different loop" errors, try restarting the server.

2. **Knowledge Graph Integration**: If Neo4j is not available, the system will use a file-based fallback for knowledge graph operations.

3. **Project Access Issues**: If you can't access a project, ensure the project ID is correct and the project exists.

## 🚀 Contributing

Contributions are welcome! See the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines.

## 📄 License

[MIT License](LICENSE)
