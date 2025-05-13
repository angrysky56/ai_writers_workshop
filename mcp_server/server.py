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

# Define output directory paths
OUTPUT_DIR = project_root / "output"
CHARACTER_DIR = OUTPUT_DIR / "characters"
PROJECT_DIR = OUTPUT_DIR / "projects"
SCENE_DIR = OUTPUT_DIR / "scenes"
ANALYSIS_DIR = OUTPUT_DIR / "analyses"
OUTLINE_DIR = OUTPUT_DIR / "outlines"
SYMBOL_DIR = OUTPUT_DIR / "symbols"

# Ensure output directories exist
for directory in [OUTPUT_DIR, CHARACTER_DIR, PROJECT_DIR, SCENE_DIR, ANALYSIS_DIR, OUTLINE_DIR, SYMBOL_DIR]:
    directory.mkdir(exist_ok=True, parents=True)

# Helper function to save outputs
def save_output(data: Dict[str, Any], directory: Path, filename: str) -> str:
    """
    Save output data to a JSON file.
    
    Args:
        data: Data to save
        directory: Directory to save to
        filename: Filename to save as
        
    Returns:
        Path to saved file
    """
    # Add timestamp to data
    if isinstance(data, dict):
        data["created_at"] = datetime.datetime.now().isoformat()
    
    # Ensure filename ends with .json
    if not filename.endswith(".json"):
        filename += ".json"
    
    # Full path to save file
    filepath = directory / filename
    
    # Save data
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    
    logger.info(f"Saved output to {filepath}")
    return str(filepath)

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
    patterns_dir = project_root / "resources"
    pattern_path = patterns_dir / f"{pattern_name}.json"
    
    if not pattern_path.exists():
        # Return list of available patterns if requested pattern doesn't exist
        available = [p.stem for p in patterns_dir.glob("*.json")]
        return f"Pattern '{pattern_name}' not found. Available patterns: {', '.join(available)}"
    
    with open(pattern_path, "r") as f:
        return f.read()

@mcp.resource("file://characters/{archetype_name}")
def get_character_archetype(archetype_name: str) -> str:
    """
    Get information about a character archetype.
    
    Args:
        archetype_name: Name of the archetype (e.g., "hero", "mentor")
        
    Returns:
        Detailed information about the archetype
    """
    # This would be populated with real data in a full implementation
    archetypes = {
        "hero": {
            "name": "Hero",
            "description": "The main protagonist who embarks on a journey of growth and transformation.",
            "traits": ["Brave", "Determined", "Selfless", "Growth-oriented"],
            "shadow_aspects": ["Egotism", "Martyrdom", "Hubris"],
            "examples": ["Luke Skywalker", "Frodo", "Harry Potter"]
        },
        "mentor": {
            "name": "Mentor",
            "description": "A wise guide who provides advice, tools, or special knowledge to the hero.",
            "traits": ["Wise", "Experienced", "Protective", "Instructive"],
            "shadow_aspects": ["Manipulative", "Withholding", "Dogmatic"],
            "examples": ["Obi-Wan Kenobi", "Gandalf", "Dumbledore"]
        },
        "threshold_guardian": {
            "name": "Threshold Guardian",
            "description": "A character who tests the hero's commitment and readiness to enter the special world.",
            "traits": ["Challenging", "Testing", "Protective", "Gatekeeping"],
            "shadow_aspects": ["Blocking", "Inflexible", "Judgmental"],
            "examples": ["The Doorman in The Wizard of Oz", "The Three-Headed Dog in Harry Potter"]
        }
    }
    
    if archetype_name.lower() not in archetypes:
        available = list(archetypes.keys())
        return f"Archetype '{archetype_name}' not found. Available archetypes: {', '.join(available)}"
    
    import json
    return json.dumps(archetypes[archetype_name.lower()], indent=2)

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

## Available Resources

- `file://patterns/{pattern_name}` - Get information about narrative patterns
  Example patterns: heroes_journey, transformation

- `file://characters/{archetype_name}` - Get information about character archetypes
  Example archetypes: hero, mentor, threshold_guardian

## Available Tools

### Pattern Tools
- `list_patterns` - List available narrative patterns
- `get_pattern_details` - Get detailed information about a specific pattern
- `analyze_narrative` - Analyze a narrative against a pattern

### Character Tools
- `list_archetypes` - List available character archetypes
- `get_archetype_details` - Get detailed information about an archetype
- `create_character` - Create a character based on archetypes
- `develop_character_arc` - Develop a character arc within a narrative pattern

### Story Generation Tools
- `generate_outline` - Generate a story outline based on a pattern
- `generate_scene` - Generate a scene based on pattern elements
- `find_symbolic_connections` - Find symbolic connections for themes
"""

@mcp.resource("file://outputs")
def get_outputs() -> str:
    """
    Get a list of available outputs.
    
    Returns:
        List of outputs as JSON
    """
    outputs = {
        "characters": [p.stem for p in CHARACTER_DIR.glob("*.json")],
        "projects": [p.stem for p in PROJECT_DIR.glob("*.json")],
        "scenes": [p.stem for p in SCENE_DIR.glob("*.json")],
        "analyses": [p.stem for p in ANALYSIS_DIR.glob("*.json")],
        "outlines": [p.stem for p in OUTLINE_DIR.glob("*.json")],
        "symbols": [p.stem for p in SYMBOL_DIR.glob("*.json")]
    }
    
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
    # Map output type to directory
    output_dirs = {
        "characters": CHARACTER_DIR,
        "projects": PROJECT_DIR,
        "scenes": SCENE_DIR,
        "analyses": ANALYSIS_DIR,
        "outlines": OUTLINE_DIR,
        "symbols": SYMBOL_DIR
    }
    
    if output_type not in output_dirs:
        return f"Output type '{output_type}' not found. Available types: {', '.join(output_dirs.keys())}"
    
    # Ensure output_name ends with .json
    if not output_name.endswith(".json"):
        output_name += ".json"
    
    output_path = output_dirs[output_type] / output_name
    
    if not output_path.exists():
        available = [p.stem for p in output_dirs[output_type].glob("*.json")]
        return f"Output '{output_name}' not found in {output_type}. Available outputs: {', '.join(available)}"
    
    with open(output_path, "r") as f:
        return f.read()

# ---- Tools ----

@mcp.tool()
def list_patterns() -> Dict[str, Any]:
    """
    List available narrative patterns.
    
    Returns:
        Dictionary with list of patterns and basic information
    """
    patterns = {
        "heroes_journey": {
            "name": "Hero's Journey",
            "description": "The classic monomyth structure identified by Joseph Campbell",
            "stages": 12
        },
        "transformation": {
            "name": "Transformation",
            "description": "A pattern focused on character or societal change and growth",
            "stages": 7
        },
        "voyage_and_return": {
            "name": "Voyage and Return",
            "description": "A journey to an unfamiliar place, followed by a return with new perspective",
            "stages": 5
        }
    }
    
    return {"patterns": patterns}

@mcp.tool()
def get_pattern_details(pattern_name: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific narrative pattern.
    
    Args:
        pattern_name: Name of the pattern (e.g., "heroes_journey", "transformation")
        
    Returns:
        Dictionary with detailed pattern information
    """
    patterns = {
        "heroes_journey": {
            "name": "Hero's Journey",
            "description": "The classic monomyth structure identified by Joseph Campbell",
            "stages": [
                "Ordinary World",
                "Call to Adventure",
                "Refusal of the Call",
                "Meeting the Mentor",
                "Crossing the Threshold",
                "Tests, Allies, Enemies",
                "Approach to the Inmost Cave",
                "Ordeal",
                "Reward",
                "The Road Back",
                "Resurrection",
                "Return with the Elixir"
            ],
            "psychological_functions": [
                "Self-discovery",
                "Integration of shadow aspects",
                "Individuation"
            ],
            "examples": [
                "Star Wars: A New Hope",
                "The Lord of the Rings",
                "The Matrix"
            ]
        },
        "transformation": {
            "name": "Transformation",
            "description": "A pattern focused on character or societal change and growth",
            "stages": [
                "Status Quo",
                "Disruption",
                "Resistance",
                "Struggle",
                "Discovery",
                "Integration",
                "New Normal"
            ],
            "psychological_functions": [
                "Personal growth",
                "Acceptance of change",
                "Evolution of identity"
            ],
            "examples": [
                "A Christmas Carol",
                "Jane Eyre",
                "Groundhog Day"
            ]
        }
    }
    
    if pattern_name not in patterns:
        return {
            "error": f"Pattern '{pattern_name}' not found",
            "available_patterns": list(patterns.keys())
        }
    
    return {"pattern": patterns[pattern_name]}

@mcp.tool()
def analyze_narrative(scenes: List[Dict[str, str]], pattern_name: Optional[str] = "heroes_journey") -> Dict[str, Any]:
    """
    Analyze a narrative structure using a specific pattern.
    
    Args:
        scenes: List of scene dictionaries, each with 'title' and 'description'
        pattern_name: Name of the pattern to analyze against
        
    Returns:
        Dictionary with analysis results
    """
    # Get the pattern details to compare against
    pattern_details = get_pattern_details(pattern_name)
    if "error" in pattern_details:
        return pattern_details
    
    pattern = pattern_details["pattern"]
    stages = pattern["stages"]
    
    # Very simple analysis algorithm for demonstration purposes
    matched_stages = []
    missing_stages = []
    
    for stage in stages:
        found = False
        for scene in scenes:
            title = scene.get("title", "")
            description = scene.get("description", "")
            
            # Check if the stage is mentioned in the title or description
            if (stage.lower() in title.lower() or
                stage.lower() in description.lower()):
                matched_stages.append({
                    "stage": stage,
                    "scene": title
                })
                found = True
                break
        
        if not found:
            missing_stages.append(stage)
    
    # Calculate a simple match score
    match_score = len(matched_stages) / len(stages)
    
    analysis_result = {
        "pattern": pattern_name,
        "match_score": match_score,
        "matched_stages": matched_stages,
        "missing_stages": missing_stages,
        "analysis": f"The narrative matches {int(match_score * 100)}% of the {pattern_name} pattern stages."
    }
    
    # Save analysis to output directory
    first_scene_title = scenes[0]["title"] if scenes else "unnamed"
    sanitized_title = first_scene_title.lower().replace(" ", "_")
    filename = f"analysis-{sanitized_title}-{pattern_name}.json"
    save_output(analysis_result, ANALYSIS_DIR, filename)
    
    analysis_result["output_path"] = f"analyses/{filename}"
    return analysis_result

@mcp.tool()
def list_archetypes() -> Dict[str, Any]:
    """
    List available character archetypes.
    
    Returns:
        Dictionary with list of archetypes and basic information
    """
    archetypes = {
        "hero": {
            "name": "Hero",
            "description": "The main protagonist who embarks on a journey of growth"
        },
        "mentor": {
            "name": "Mentor",
            "description": "A wise guide who provides advice and special knowledge"
        },
        "threshold_guardian": {
            "name": "Threshold Guardian",
            "description": "A character who tests the hero's commitment and readiness"
        },
        "herald": {
            "name": "Herald",
            "description": "A character who announces the call to adventure"
        },
        "shapeshifter": {
            "name": "Shapeshifter",
            "description": "A character whose loyalty or identity is uncertain"
        },
        "shadow": {
            "name": "Shadow",
            "description": "The antagonist or representation of the hero's inner darkness"
        },
        "trickster": {
            "name": "Trickster",
            "description": "A character who brings humor, mischief, or chaos"
        }
    }
    
    return {"archetypes": archetypes}

@mcp.tool()
def get_archetype_details(archetype_name: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific character archetype.
    
    Args:
        archetype_name: Name of the archetype (e.g., "hero", "mentor")
        
    Returns:
        Dictionary with detailed archetype information
    """
    archetypes = {
        "hero": {
            "name": "Hero",
            "description": "The main protagonist who embarks on a journey of growth and transformation.",
            "traits": ["Brave", "Determined", "Selfless", "Growth-oriented"],
            "shadow_aspects": ["Egotism", "Martyrdom", "Hubris"],
            "examples": ["Luke Skywalker", "Frodo", "Harry Potter"]
        },
        "mentor": {
            "name": "Mentor",
            "description": "A wise guide who provides advice, tools, or special knowledge to the hero.",
            "traits": ["Wise", "Experienced", "Protective", "Instructive"],
            "shadow_aspects": ["Manipulative", "Withholding", "Dogmatic"],
            "examples": ["Obi-Wan Kenobi", "Gandalf", "Dumbledore"]
        },
        "threshold_guardian": {
            "name": "Threshold Guardian",
            "description": "A character who tests the hero's commitment and readiness to enter the special world.",
            "traits": ["Challenging", "Testing", "Protective", "Gatekeeping"],
            "shadow_aspects": ["Blocking", "Inflexible", "Judgmental"],
            "examples": ["The Doorman in The Wizard of Oz", "The Three-Headed Dog in Harry Potter"]
        }
    }
    
    if archetype_name not in archetypes:
        return {
            "error": f"Archetype '{archetype_name}' not found",
            "available_archetypes": list(archetypes.keys())
        }
    
    return {"archetype": archetypes[archetype_name]}

@mcp.tool()
def create_character(name: str, archetype: str, traits: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Create a character based on an archetype.
    
    Args:
        name: Character name
        archetype: Base archetype (e.g., "hero", "mentor")
        traits: Optional list of specific traits
        
    Returns:
        Dictionary with character information
    """
    # Get the archetype details
    archetype_details = get_archetype_details(archetype)
    if "error" in archetype_details:
        return archetype_details
    
    archetype_info = archetype_details["archetype"]
    
    # Use provided traits or select from archetype traits
    character_traits = traits or archetype_info["traits"]
    
    # Select one shadow aspect from the archetype
    shadow_aspect = archetype_info["shadow_aspects"][0] if archetype_info["shadow_aspects"] else None
    
    character = {
        "name": name,
        "archetype": archetype,
        "description": f"{name} is a character based on the {archetype} archetype.",
        "traits": character_traits,
        "shadow_aspect": shadow_aspect,
        "development_potential": f"As a {archetype}, {name} has potential for growth through confronting their {shadow_aspect} tendencies."
    }
    
    # Save character to output directory
    sanitized_name = name.lower().replace(" ", "_")
    filename = f"{sanitized_name}-{archetype}.json"
    save_output(character, CHARACTER_DIR, filename)
    
    character_result = {"character": character}
    character_result["output_path"] = f"characters/{filename}"
    return character_result

@mcp.tool()
def develop_character_arc(character_name: str, archetype: str, pattern: str) -> Dict[str, Any]:
    """
    Develop a character arc within a narrative pattern.
    
    Args:
        character_name: Character name
        archetype: Character's archetype
        pattern: Narrative pattern to use
        
    Returns:
        Dictionary with character arc information
    """
    # Get the pattern details
    pattern_details = get_pattern_details(pattern)
    if "error" in pattern_details:
        return pattern_details
    
    # Get the archetype details
    archetype_details = get_archetype_details(archetype)
    if "error" in archetype_details:
        return archetype_details
    
    pattern_info = pattern_details["pattern"]
    archetype_info = archetype_details["archetype"]
    
    # Create character arc stages based on pattern
    arc_stages = []
    for stage in pattern_info["stages"]:
        arc_stages.append({
            "pattern_stage": stage,
            "character_development": f"{character_name}'s development during the {stage} stage.",
            "internal_change": f"Internal transformation that occurs during {stage}.",
            "external_manifestation": f"How {character_name}'s change manifests externally during {stage}."
        })
    
    character_arc = {
        "character_name": character_name,
        "archetype": archetype,
        "pattern": pattern,
        "arc_stages": arc_stages
    }
    
    # Save character arc to output directory
    sanitized_name = character_name.lower().replace(" ", "_")
    filename = f"arc-{sanitized_name}-{pattern}.json"
    save_output(character_arc, CHARACTER_DIR, filename)
    
    character_arc_result = character_arc.copy()
    character_arc_result["output_path"] = f"characters/{filename}"
    return character_arc_result

@mcp.tool()
def generate_outline(title: str, pattern: str, main_character: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Generate a story outline based on a pattern.
    
    Args:
        title: Story title
        pattern: Narrative pattern to use
        main_character: Optional character information
        
    Returns:
        Dictionary with outline information
    """
    # Get the pattern details
    pattern_details = get_pattern_details(pattern)
    if "error" in pattern_details:
        return pattern_details
    
    pattern_info = pattern_details["pattern"]
    
    # Create outline based on pattern stages
    outline = []
    for i, stage in enumerate(pattern_info["stages"]):
        outline.append({
            "section": i + 1,
            "title": f"{stage}",
            "description": f"In this section, the story addresses the '{stage}' stage of the {pattern} pattern.",
            "key_elements": [
                f"Element 1 for {stage}",
                f"Element 2 for {stage}",
                f"Element 3 for {stage}"
            ]
        })
    
    # Add character information if provided
    if main_character:
        character_info = f"The main character is {main_character.get('name', 'Unnamed')}, a {main_character.get('archetype', 'character')}."
    else:
        character_info = "No main character information provided."
    
    outline_data = {
        "title": title,
        "pattern": pattern,
        "character_info": character_info,
        "outline": outline
    }
    
    # Save outline to output directory
    sanitized_title = title.lower().replace(" ", "_")
    filename = f"outline-{sanitized_title}.json"
    save_output(outline_data, OUTLINE_DIR, filename)
    
    outline_result = outline_data.copy()
    outline_result["output_path"] = f"outlines/{filename}"
    return outline_result

@mcp.tool()
def generate_scene(scene_title: str, pattern_stage: str, characters: List[str]) -> Dict[str, Any]:
    """
    Generate a scene based on pattern elements.
    
    Args:
        scene_title: Title of the scene
        pattern_stage: The pattern stage this scene represents
        characters: List of character names in the scene
        
    Returns:
        Dictionary with scene information
    """
    scene_data = {
        "scene_title": scene_title,
        "pattern_stage": pattern_stage,
        "characters": characters,
        "setting": f"The setting for the '{scene_title}' scene",
        "goal": f"The goal of this scene is to demonstrate the '{pattern_stage}' stage",
        "conflict": f"The conflict in this scene involves {', '.join(characters)}",
        "outcome": f"The outcome of this scene moves the story forward by...",
        "notes": f"This scene is a key moment in the {pattern_stage} stage of the story."
    }
    
    # Save scene to output directory
    sanitized_title = scene_title.lower().replace(" ", "_")
    filename = f"scene-{sanitized_title}.json"
    save_output(scene_data, SCENE_DIR, filename)
    
    scene_result = scene_data.copy()
    scene_result["output_path"] = f"scenes/{filename}"
    return scene_result

@mcp.tool()
def find_symbolic_connections(theme: str, count: int = 3) -> Dict[str, Any]:
    """
    Find symbolic connections for a theme.
    
    Args:
        theme: Theme to find symbols for
        count: Number of symbols to return
        
    Returns:
        Dictionary with symbolic connections
    """
    # Simplified demonstration of symbolic connections
    symbol_systems = {
        "rebirth": [
            {"symbol": "Phoenix", "meaning": "Rising from ashes, transformation through fire"},
            {"symbol": "Spring", "meaning": "Renewal after winter, cyclical rebirth"},
            {"symbol": "Butterfly", "meaning": "Transformation from caterpillar, beauty emerging from confinement"},
            {"symbol": "Sunrise", "meaning": "New day, fresh beginnings after darkness"}
        ],
        "power": [
            {"symbol": "Lion", "meaning": "Strength, leadership, dominance"},
            {"symbol": "Crown", "meaning": "Authority, rulership, responsibility"},
            {"symbol": "Mountain", "meaning": "Permanence, solidity, overseeing from height"},
            {"symbol": "Fire", "meaning": "Transformative energy, destructive or creative force"}
        ],
        "love": [
            {"symbol": "Rose", "meaning": "Beauty with thorns, passion with pain"},
            {"symbol": "Circle", "meaning": "Eternity, completion, unbroken connection"},
            {"symbol": "Bridge", "meaning": "Connection between separate entities"},
            {"symbol": "Twin Flames", "meaning": "Two parts of a whole, complementary forces"}
        ]
    }
    
    # Find symbols for theme or return closest match
    if theme.lower() in symbol_systems:
        symbols = symbol_systems[theme.lower()][:count]
    else:
        # Suggest similar themes if exact match not found
        available_themes = list(symbol_systems.keys())
        symbols = [{"symbol": "Not found", "meaning": f"Theme '{theme}' not found. Try: {', '.join(available_themes)}"}]
    
    symbol_data = {
        "theme": theme,
        "symbols": symbols
    }
    
    # Save symbols to output directory
    sanitized_theme = theme.lower().replace(" ", "_")
    filename = f"symbols-{sanitized_theme}.json"
    save_output(symbol_data, SYMBOL_DIR, filename)
    
    symbol_result = symbol_data.copy()
    symbol_result["output_path"] = f"symbols/{filename}"
    return symbol_result

@mcp.tool()
def create_project(name: str, description: str, project_type: str = "story") -> Dict[str, Any]:
    """
    Create a new project.
    
    Args:
        name: Project name
        description: Project description
        project_type: Type of project (story, novel, article, script)
        
    Returns:
        Dictionary with project information
    """
    project_data = {
        "name": name,
        "description": description,
        "type": project_type,
        "created_at": datetime.datetime.now().isoformat(),
        "modified_at": datetime.datetime.now().isoformat(),
        "primary_pattern": None,
        "themes": [],
        "main_characters": [],
        "secondary_characters": [],
        "word_count": 0,
        "status": "in_progress",
        "notes": ""
    }
    
    # Save project to output directory
    sanitized_name = name.lower().replace(" ", "_")
    filename = f"{sanitized_name}.json"
    save_output(project_data, PROJECT_DIR, filename)
    
    # Create project directory structure
    project_dir = PROJECT_DIR / sanitized_name
    project_dir.mkdir(exist_ok=True)
    
    # Create subdirectories
    (project_dir / "characters").mkdir(exist_ok=True)
    (project_dir / "scenes").mkdir(exist_ok=True)
    
    # Save metadata to project directory
    with open(project_dir / "metadata.json", "w") as f:
        json.dump(project_data, f, indent=2)
    
    # Create notes file
    with open(project_dir / "notes.md", "w") as f:
        f.write(f"# {name}\n\n{description}\n\n## Notes\n\n")
    
    project_result = project_data.copy()
    project_result["output_path"] = f"projects/{filename}"
    project_result["project_dir"] = f"projects/{sanitized_name}"
    return project_result

@mcp.tool()
def list_outputs() -> Dict[str, Any]:
    """
    List all available outputs.
    
    Returns:
        Dictionary with lists of outputs by type
    """
    outputs = {
        "characters": [p.stem for p in CHARACTER_DIR.glob("*.json")],
        "projects": [p.stem for p in PROJECT_DIR.glob("*.json")],
        "scenes": [p.stem for p in SCENE_DIR.glob("*.json")],
        "analyses": [p.stem for p in ANALYSIS_DIR.glob("*.json")],
        "outlines": [p.stem for p in OUTLINE_DIR.glob("*.json")],
        "symbols": [p.stem for p in SYMBOL_DIR.glob("*.json")]
    }
    
    return outputs

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
