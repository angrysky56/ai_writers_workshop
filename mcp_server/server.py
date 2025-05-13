#!/usr/bin/env python
"""
AI Writers Workshop - MCP Server

A Model Context Protocol (MCP) server that provides narrative, character, and
archetypal storytelling tools to AI assistants via the MCP standard.
"""

import os
import sys
import logging
import json
import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List, Union, Tuple

# Configure logging to stderr for Claude Desktop debugging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("ai_writers_workshop.mcp")

try:
    from mcp.server.fastmcp import FastMCP, Context, Image
    logger.info("Successfully imported FastMCP")
except ImportError as e:
    logger.error(f"Error importing MCP package: {e}")
    sys.stderr.write(f"Error importing MCP package: {e}\n")
    sys.exit(1)

# Add the project root to path for imports
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

# Import component managers
from components.project_manager import ProjectManager
from components.character_manager import CharacterManager
from components.pattern_manager import PatternManager
from components.narrative_generator import NarrativeGenerator
from components.symbolic_manager import SymbolicManager
from components.knowledge_graph.graph_manager import KnowledgeGraphManager
from components.plotline_manager import PlotlineManager

# Define output directory 
OUTPUT_DIR = project_root / "output"

# Initialize component managers
project_manager = ProjectManager(OUTPUT_DIR)
pattern_manager = PatternManager(OUTPUT_DIR)
character_manager = CharacterManager(project_manager, OUTPUT_DIR)
narrative_generator = NarrativeGenerator(project_manager, pattern_manager, OUTPUT_DIR)
symbolic_manager = SymbolicManager(project_manager, OUTPUT_DIR)
knowledge_graph = KnowledgeGraphManager(OUTPUT_DIR)
plotline_manager = PlotlineManager(project_manager, pattern_manager, OUTPUT_DIR)

# Create MCP Server
mcp = FastMCP(
    name="AI Writers Workshop",
    description="Narrative and character development tools through MCP"
)
logger.info("Created FastMCP server instance")

# ---- Resources ----

# In MCP 1.7, use file:// scheme instead of custom schemes
@mcp.resource("file://patterns/{pattern_name}")
def get_pattern(pattern_name: str) -> str:
    """
    Get information about a specific narrative pattern.
    
    Args:
        pattern_name: Name of the pattern (e.g., "heroes_journey", "transformation")
        
    Returns:
        Detailed information about the pattern
    """
    # Delegate to pattern manager
    pattern_details = pattern_manager.get_pattern_details(pattern_name)
    
    if "error" in pattern_details:
        return json.dumps(pattern_details, indent=2)
    
    return json.dumps(pattern_details["pattern"], indent=2)

@mcp.resource("file://characters/{archetype_name}")
def get_character_archetype(archetype_name: str) -> str:
    """
    Get information about a character archetype.
    
    Args:
        archetype_name: Name of the archetype (e.g., "hero", "mentor")
        
    Returns:
        Detailed information about the archetype
    """
    # Delegate to character manager
    archetype_details = character_manager.get_archetype_details(archetype_name)
    
    if "error" in archetype_details:
        return json.dumps(archetype_details, indent=2)
    
    return json.dumps(archetype_details["archetype"], indent=2)

@mcp.resource("file://guide")
def get_guide() -> str:
    """
    Get a guide on how to use the AI Writers Workshop tools.
    
    Returns:
        Basic guide text
    """
    return """
# AI Writers Workshop - Usage Guide

This server provides access to narrative development tools through the Model Context Protocol (MCP).

## Project-Based Organization

The AI Writers Workshop now supports project-based organization. All elements (characters, scenes, etc.) 
can be associated with specific projects for better organization and management.

When using any tool, you can specify a `project_id` parameter to associate the output with a project. 
If not specified, outputs will be saved to the legacy flat structure for backward compatibility.

## Available Resources

- `file://patterns/{pattern_name}` - Get information about narrative patterns
  Example patterns: heroes_journey, transformation, voyage_and_return

- `file://characters/{archetype_name}` - Get information about character archetypes
  Example archetypes: hero, mentor, threshold_guardian, shadow, trickster

- `file://outputs` - List all available outputs

## Available Tools

### Project Management
- `create_project` - Create a new project with hierarchical structure
- `list_outputs` - List all available outputs across projects

### Pattern Tools
- `list_patterns` - List available narrative patterns
- `get_pattern_details` - Get detailed information about a specific pattern
- `analyze_narrative` - Analyze a narrative against a pattern with flexible adherence
- `create_custom_pattern` - Create a custom narrative pattern
- `create_hybrid_pattern` - Create a hybrid pattern from multiple existing patterns

### Character Tools
- `list_archetypes` - List available character archetypes
- `get_archetype_details` - Get detailed information about an archetype
- `create_character` - Create a character based on archetypes with hybrid support
- `develop_character_arc` - Develop a character arc within a narrative pattern
- `create_custom_archetype` - Create a custom character archetype

### Narrative Generation Tools
- `generate_outline` - Generate a story outline based on a pattern
- `generate_scene` - Generate a scene based on pattern elements
- `compile_narrative` - Compile a complete narrative from project elements

### Symbolic Tools
- `find_symbolic_connections` - Find symbolic connections for themes
- `create_custom_symbols` - Create custom symbolic connections for a theme
- `apply_symbolic_theme` - Apply a symbolic theme to project elements
"""

@mcp.resource("file://outputs")
def get_outputs() -> str:
    """
    Get a list of available outputs.
    
    Returns:
        List of outputs as JSON
    """
    outputs = project_manager.list_outputs()
    return json.dumps(outputs, indent=2)

@mcp.resource("file://outputs/{output_type}/{output_name}")
def get_output(output_type: str, output_name: str) -> str:
    """
    Get a specific output file.
    
    Args:
        output_type: Type of output (characters, projects, etc.)
        output_name: Name of the output file
        
    Returns:
        Output file content
    """
    # Handle project-based outputs
    if output_type == "projects" and "/" in output_name:
        # Extract project ID and element type
        parts = output_name.split("/")
        if len(parts) >= 3:
            project_id = parts[0]
            element_type = parts[1]
            element_id = "/".join(parts[2:]).replace(".json", "")
            
            element = project_manager.get_element(project_id, element_type, element_id)
            return json.dumps(element, indent=2)
    
    # Handle legacy outputs
    output_path = OUTPUT_DIR / output_type / f"{output_name}"
    if not output_path.exists() and not output_name.endswith(".json"):
        output_path = OUTPUT_DIR / output_type / f"{output_name}.json"
    
    if not output_path.exists():
        return json.dumps({
            "error": f"Output '{output_name}' not found in {output_type}",
            "outputs": project_manager.list_outputs()
        }, indent=2)
    
    with open(output_path, "r") as f:
        return f.read()

# ---- Tools ----

@mcp.tool()
def create_project(name: str, description: str, project_type: str = "story") -> Dict[str, Any]:
    """
    Create a new project with hierarchical structure.
    
    Args:
        name: Project name
        description: Project description
        project_type: Type of project (story, novel, article, script)
        
    Returns:
        Dictionary with project information
    """
    try:
        return project_manager.create_project(name, description, project_type)
    except Exception as e:
        logger.error(f"Error creating project: {e}")
        return {"error": f"Failed to create project: {str(e)}"}

@mcp.tool()
def get_project(project_id: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific project.
    
    Args:
        project_id: ID of the project to retrieve
        
    Returns:
        Dictionary with project details
    """
    try:
        return project_manager.get_project(project_id)
    except Exception as e:
        logger.error(f"Error retrieving project: {e}")
        return {"error": f"Failed to retrieve project: {str(e)}"}

@mcp.tool()
def list_patterns() -> Dict[str, Any]:
    """
    List available narrative patterns.
    
    Returns:
        Dictionary with list of patterns and basic information
    """
    return pattern_manager.list_patterns()

@mcp.tool()
def get_pattern_details(pattern_name: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific narrative pattern.
    
    Args:
        pattern_name: Name of the pattern (e.g., "heroes_journey", "transformation")
        
    Returns:
        Dictionary with detailed pattern information
    """
    return pattern_manager.get_pattern_details(pattern_name)

@mcp.tool()
def create_custom_pattern(name: str, description: str, stages: List[str],
                        psychological_functions: Optional[List[str]] = None,
                        examples: Optional[List[str]] = None,
                        based_on: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a custom narrative pattern.
    
    Args:
        name: Pattern name
        description: Pattern description
        stages: List of pattern stages
        psychological_functions: Optional list of psychological functions
        examples: Optional list of example stories
        based_on: Optional base pattern to extend
        
    Returns:
        Dictionary with pattern information
    """
    return pattern_manager.create_custom_pattern(
        name=name,
        description=description,
        stages=stages,
        psychological_functions=psychological_functions,
        examples=examples,
        based_on=based_on
    )

@mcp.tool()
def create_hybrid_pattern(name: str, description: str, patterns: Dict[str, float],
                        custom_stages: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Create a hybrid pattern from multiple existing patterns.
    
    Args:
        name: Pattern name
        description: Pattern description
        patterns: Dictionary of pattern_name:weight pairs
        custom_stages: Optional custom stage list
        
    Returns:
        Dictionary with pattern information
    """
    return pattern_manager.create_hybrid_pattern(
        name=name,
        description=description,
        patterns=patterns,
        custom_stages=custom_stages
    )

@mcp.tool()
def analyze_narrative(scenes: List[Dict[str, str]], pattern_name: str = "heroes_journey",
                    project_id: Optional[str] = None, adherence_level: float = 1.0) -> Dict[str, Any]:
    """
    Analyze a narrative structure using a specific pattern with flexible matching.
    
    Args:
        scenes: List of scene dictionaries, each with 'title' and 'description'
        pattern_name: Name of the pattern to analyze against
        project_id: Optional project to associate with
        adherence_level: How strictly to apply pattern (0.0-1.0)
        
    Returns:
        Dictionary with analysis results
    """
    return pattern_manager.analyze_narrative(
        scenes=scenes,
        pattern_name=pattern_name,
        project_id=project_id,
        adherence_level=adherence_level
    )

@mcp.tool()
def list_archetypes() -> Dict[str, Any]:
    """
    List available character archetypes.
    
    Returns:
        Dictionary with list of archetypes and basic information
    """
    return character_manager.list_archetypes()

@mcp.tool()
def get_archetype_details(archetype_name: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific character archetype.
    
    Args:
        archetype_name: Name of the archetype (e.g., "hero", "mentor")
        
    Returns:
        Dictionary with detailed archetype information
    """
    return character_manager.get_archetype_details(archetype_name)

@mcp.tool()
def create_character(name: str, archetype: str, traits: Optional[List[str]] = None,
                    project_id: Optional[str] = None, 
                    hybrid_archetypes: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
    """
    Create a character based on an archetype with enhanced flexibility.
    
    Args:
        name: Character name
        archetype: Base archetype (e.g., "hero", "mentor")
        traits: Optional list of specific traits
        project_id: Optional project to associate with
        hybrid_archetypes: Optional dictionary of archetype_id:weight for hybrid characters
        
    Returns:
        Dictionary with character information
    """
    return character_manager.create_character(
        name=name,
        archetype=archetype,
        traits=traits,
        project_id=project_id,
        hybrid_archetypes=hybrid_archetypes
    )

@mcp.tool()
def create_custom_archetype(name: str, description: str, traits: List[str],
                          shadow_aspects: List[str], examples: Optional[List[str]] = None,
                          based_on: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a custom character archetype.
    
    Args:
        name: Archetype name
        description: Archetype description
        traits: List of typical traits
        shadow_aspects: List of shadow aspects
        examples: Optional list of example characters
        based_on: Optional base archetype to extend
        
    Returns:
        Dictionary with archetype information
    """
    return character_manager.create_custom_archetype(
        name=name,
        description=description,
        traits=traits,
        shadow_aspects=shadow_aspects,
        examples=examples,
        based_on=based_on
    )

@mcp.tool()
def develop_character_arc(character_name: str, archetype: str, pattern: str,
                         project_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Develop a character arc within a narrative pattern.
    
    Args:
        character_name: Character name
        archetype: Character's archetype
        pattern: Narrative pattern to use
        project_id: Optional project to associate with
        
    Returns:
        Dictionary with character arc information
    """
    return character_manager.develop_character_arc(
        character_name=character_name,
        archetype=archetype,
        pattern=pattern,
        project_id=project_id
    )

@mcp.tool()
def generate_outline(title: str, pattern: str, main_character: Optional[Dict[str, Any]] = None,
                    project_id: Optional[str] = None, 
                    custom_sections: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """
    Generate a story outline based on a pattern with custom sections support.
    
    Args:
        title: Story title
        pattern: Narrative pattern to use
        main_character: Optional character information
        project_id: Optional project to associate with
        custom_sections: Optional list of custom outline sections
        
    Returns:
        Dictionary with outline information
    """
    return narrative_generator.generate_outline(
        title=title,
        pattern=pattern,
        main_character=main_character,
        project_id=project_id,
        custom_sections=custom_sections
    )

@mcp.tool()
def generate_scene(scene_title: str, pattern_stage: str, characters: List[str],
                  project_id: Optional[str] = None, setting: Optional[str] = None,
                  conflict: Optional[str] = None) -> Dict[str, Any]:
    """
    Generate a scene based on pattern elements with enhanced customization.
    
    Args:
        scene_title: Title of the scene
        pattern_stage: The pattern stage this scene represents
        characters: List of character names in the scene
        project_id: Optional project to associate with
        setting: Optional setting description
        conflict: Optional conflict description
        
    Returns:
        Dictionary with scene information
    """
    return narrative_generator.generate_scene(
        scene_title=scene_title,
        pattern_stage=pattern_stage,
        characters=characters,
        project_id=project_id,
        setting=setting,
        conflict=conflict
    )

@mcp.tool()
def compile_narrative(project_id: str, title: Optional[str] = None,
                     scene_order: Optional[List[str]] = None,
                     include_character_descriptions: bool = True,
                     format: str = "markdown") -> Dict[str, Any]:
    """
    Compile scenes into a complete narrative.
    
    Args:
        project_id: Project ID to compile
        title: Optional title for the narrative (defaults to project name)
        scene_order: Optional list of scene IDs to define order
        include_character_descriptions: Whether to include character descriptions
        format: Output format ("markdown", "json", "html")
        
    Returns:
        Dictionary with compiled narrative
    """
    return narrative_generator.compile_narrative(
        project_id=project_id,
        title=title,
        scene_order=scene_order,
        include_character_descriptions=include_character_descriptions,
        format=format
    )

@mcp.tool()
def find_symbolic_connections(theme: str, count: int = 3,
                             project_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Find symbolic connections for a theme with project support.
    
    Args:
        theme: Theme to find symbols for
        count: Number of symbols to return
        project_id: Optional project to associate with
        
    Returns:
        Dictionary with symbolic connections
    """
    return symbolic_manager.find_symbolic_connections(
        theme=theme,
        count=count,
        project_id=project_id
    )

@mcp.tool()
def create_custom_symbols(theme: str, symbols: List[Dict[str, str]],
                         project_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Create custom symbols for a theme.
    
    Args:
        theme: Theme name
        symbols: List of symbol dictionaries with "symbol" and "meaning" keys
        project_id: Optional project to associate with
        
    Returns:
        Dictionary with symbol information
    """
    return symbolic_manager.create_custom_symbols(
        theme=theme,
        symbols=symbols,
        project_id=project_id
    )

@mcp.tool()
def apply_symbolic_theme(project_id: str, theme: str,
                        element_types: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Apply a symbolic theme to project elements.
    
    Args:
        project_id: Project ID to apply theme to
        theme: Theme to apply
        element_types: Optional list of element types to apply theme to
        
    Returns:
        Dictionary with application results
    """
    return symbolic_manager.apply_symbolic_theme(
        project_id=project_id,
        theme=theme,
        element_types=element_types
    )

@mcp.tool()
def list_outputs() -> Dict[str, Any]:
    """
    List all available outputs.
    
    Returns:
        Dictionary with lists of outputs by type
    """
    return project_manager.list_outputs()

# ----- Knowledge Graph Tools -----

@mcp.tool()
def search_nodes(query: str) -> Dict[str, Any]:
    """
    Search for nodes in the knowledge graph based on a query.
    
    Args:
        query: The search query to match against entity names, types, and properties
        
    Returns:
        Dictionary with search results
    """
    try:
        return knowledge_graph.search_nodes(query)
    except Exception as e:
        logger.error(f"Error searching nodes: {e}")
        return {"error": str(e), "query": query, "results": []}

@mcp.tool()
def open_nodes(names: List[str]) -> Dict[str, Any]:
    """
    Open specific nodes in the knowledge graph by their names.
    
    Args:
        names: An array of entity names to retrieve
        
    Returns:
        Dictionary with requested nodes
    """
    try:
        return knowledge_graph.open_nodes(names)
    except Exception as e:
        logger.error(f"Error opening nodes: {e}")
        return {"error": str(e), "names": names, "nodes": {}}

@mcp.tool()
def read_graph() -> Dict[str, Any]:
    """
    Read the entire knowledge graph.
    
    Returns:
        Dictionary with complete graph data
    """
    try:
        return knowledge_graph.read_graph()
    except Exception as e:
        logger.error(f"Error reading graph: {e}")
        return {"error": str(e), "nodes": [], "relations": []}

# ----- Plotline Tools -----

@mcp.tool()
def list_plotlines() -> Dict[str, Any]:
    """
    List available narrative plotlines.
    
    Returns:
        Dictionary with list of plotlines and basic information
    """
    return plotline_manager.list_plotlines()

@mcp.tool()
def get_plotline_details(plotline_name: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific narrative plotline.
    
    Args:
        plotline_name: Name of the plotline (e.g., "man_vs_nature", "quest")
        
    Returns:
        Dictionary with detailed plotline information
    """
    return plotline_manager.get_plotline_details(plotline_name)

@mcp.tool()
def create_custom_plotline(name: str, description: str, elements: List[str],
                         examples: Optional[List[str]] = None,
                         based_on: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a custom narrative plotline.
    
    Args:
        name: Plotline name
        description: Plotline description
        elements: List of key narrative elements
        examples: Optional list of example stories
        based_on: Optional base plotline to extend
        
    Returns:
        Dictionary with plotline information
    """
    return plotline_manager.create_custom_plotline(
        name=name,
        description=description,
        elements=elements,
        examples=examples,
        based_on=based_on
    )

@mcp.tool()
def develop_plotline(title: str, plotline: str, pattern: str,
                    characters: Optional[List[str]] = None,
                    project_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Develop a plotline using both a base plotline type and narrative pattern.
    
    Args:
        title: Title for the plotline
        plotline: Base plotline type (e.g., "quest", "revenge")
        pattern: Narrative pattern to structure the plotline
        characters: Optional list of character names to include
        project_id: Optional project to associate with
        
    Returns:
        Dictionary with plotline development information
    """
    return plotline_manager.develop_plotline(
        title=title,
        plotline=plotline,
        pattern=pattern,
        characters=characters,
        project_id=project_id
    )

@mcp.tool()
def analyze_plotline(plot_points: List[Dict[str, str]], plotline: str,
                   project_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Analyze how well a set of plot points aligns with a plotline structure.
    
    Args:
        plot_points: List of plot point dictionaries, each with 'title' and 'description'
        plotline: Plotline to analyze against
        project_id: Optional project to associate with
        
    Returns:
        Dictionary with analysis results
    """
    return plotline_manager.analyze_plotline(
        plot_points=plot_points,
        plotline=plotline,
        project_id=project_id
    )

def main():
    """Run the MCP server."""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Writers Workshop MCP Server")
    parser.add_argument("--transport", choices=["stdio", "sse", "streamable-http"], 
                       default="stdio", help="Transport type")
    parser.add_argument("--port", type=int, default=8000, 
                       help="Port for SSE or streamable-http transport")
    parser.add_argument("--host", default="127.0.0.1", 
                       help="Host for SSE or streamable-http transport")
    
    args = parser.parse_args()
    
    # Log server startup information
    logger.info(f"Starting AI Writers Workshop MCP Server with {args.transport} transport")
    
    try:
        if args.transport == "sse":
            mcp.run(transport="sse", host=args.host, port=args.port)
        elif args.transport == "streamable-http":
            mcp.run(transport="streamable-http", host=args.host, port=args.port)
        else:
            # Default to stdio
            mcp.run(transport="stdio")
    except Exception as e:
        logger.error(f"Error running MCP server: {e}")
        sys.stderr.write(f"Error running MCP server: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
