"""
Initialization script for AI Writers Workshop

This script ensures that the necessary directory structure and default content
is set up before the server starts.
"""

import os
import json
from pathlib import Path
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("ai_writers_workshop.init")

def initialize_directory_structure(base_dir: Path) -> None:
    """
    Initialize the directory structure for AI Writers Workshop.
    
    Args:
        base_dir: Base directory for all outputs
    """
    logger.info(f"Initializing directory structure in {base_dir}")
    
    # Create main directories
    os.makedirs(base_dir, exist_ok=True)
    
    # Create hierarchical structure
    library_dir = base_dir / "library"
    projects_dir = base_dir / "projects"
    
    os.makedirs(library_dir, exist_ok=True)
    os.makedirs(projects_dir, exist_ok=True)
    
    # Create library subdirectories
    archetypes_dir = library_dir / "archetypes"
    patterns_dir = library_dir / "patterns"
    symbols_dir = library_dir / "symbols"
    
    os.makedirs(archetypes_dir, exist_ok=True)
    os.makedirs(patterns_dir, exist_ok=True)
    os.makedirs(symbols_dir, exist_ok=True)
    
    # Create legacy directories for backward compatibility
    legacy_dirs = ["characters", "scenes", "outlines", "analyses", "symbols"]
    for dir_name in legacy_dirs:
        os.makedirs(base_dir / dir_name, exist_ok=True)
    
    logger.info(f"Directory structure initialized successfully")

def initialize_default_archetypes(archetypes_dir: Path) -> None:
    """
    Initialize default archetypes.
    
    Args:
        archetypes_dir: Directory for archetype definitions
    """
    logger.info(f"Initializing default archetypes in {archetypes_dir}")
    
    default_archetypes = {
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
        },
        "herald": {
            "name": "Herald",
            "description": "A character who announces the call to adventure or significant change.",
            "traits": ["Messenger", "Catalyst", "Announcer", "Signal"],
            "shadow_aspects": ["Deceptive", "Manipulative", "Fear-inducing"],
            "examples": ["R2-D2 in Star Wars", "The White Rabbit in Alice in Wonderland"]
        },
        "shapeshifter": {
            "name": "Shapeshifter",
            "description": "A character whose loyalty or identity is uncertain or changing.",
            "traits": ["Mysterious", "Changeable", "Unpredictable", "Ambiguous"],
            "shadow_aspects": ["Treacherous", "Inconsistent", "Untrustworthy"],
            "examples": ["Severus Snape in Harry Potter", "Catwoman in Batman"]
        },
        "shadow": {
            "name": "Shadow",
            "description": "The antagonist or representation of the hero's inner darkness.",
            "traits": ["Opposing", "Threatening", "Powerful", "Dark mirror"],
            "shadow_aspects": ["Destructive", "Corrupt", "Tyrannical"],
            "examples": ["Darth Vader in Star Wars", "Sauron in Lord of the Rings"]
        },
        "trickster": {
            "name": "Trickster",
            "description": "A character who brings humor, mischief, or chaos.",
            "traits": ["Playful", "Disruptive", "Clever", "Unpredictable"],
            "shadow_aspects": ["Malicious", "Destructive", "Cruel"],
            "examples": ["Loki in Norse mythology/Marvel", "The Joker in Batman"]
        }
    }
    
    # Save default archetypes
    for archetype_id, archetype_data in default_archetypes.items():
        archetype_path = archetypes_dir / f"{archetype_id}.json"
        if not archetype_path.exists():
            with open(archetype_path, "w") as f:
                json.dump(archetype_data, f, indent=2)
    
    logger.info(f"Default archetypes initialized successfully")

def initialize_default_patterns(patterns_dir: Path) -> None:
    """
    Initialize default narrative patterns.
    
    Args:
        patterns_dir: Directory for pattern definitions
    """
    logger.info(f"Initializing default patterns in {patterns_dir}")
    
    default_patterns = {
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
        },
        "voyage_and_return": {
            "name": "Voyage and Return",
            "description": "A journey to an unfamiliar place, followed by a return with new perspective",
            "stages": [
                "The Ordinary World",
                "The Journey Begins",
                "The Strange New World",
                "The Challenge",
                "The Return"
            ],
            "psychological_functions": [
                "Expanding perspective",
                "Appreciating home/origins",
                "Adapting to new environments"
            ],
            "examples": [
                "The Wizard of Oz",
                "Alice in Wonderland",
                "The Hobbit"
            ]
        }
    }
    
    # Save default patterns
    for pattern_id, pattern_data in default_patterns.items():
        pattern_path = patterns_dir / f"{pattern_id}.json"
        if not pattern_path.exists():
            with open(pattern_path, "w") as f:
                json.dump(pattern_data, f, indent=2)
    
    logger.info(f"Default patterns initialized successfully")

def initialize_default_symbols(symbols_dir: Path) -> None:
    """
    Initialize default symbolic connections.
    
    Args:
        symbols_dir: Directory for symbol definitions
    """
    logger.info(f"Initializing default symbols in {symbols_dir}")
    
    default_symbols = {
        "rebirth": {
            "theme": "rebirth",
            "symbols": [
                {"symbol": "Phoenix", "meaning": "Rising from ashes, transformation through fire"},
                {"symbol": "Spring", "meaning": "Renewal after winter, cyclical rebirth"},
                {"symbol": "Butterfly", "meaning": "Transformation from caterpillar, beauty emerging from confinement"},
                {"symbol": "Sunrise", "meaning": "New day, fresh beginnings after darkness"}
            ]
        },
        "power": {
            "theme": "power",
            "symbols": [
                {"symbol": "Lion", "meaning": "Strength, leadership, dominance"},
                {"symbol": "Crown", "meaning": "Authority, rulership, responsibility"},
                {"symbol": "Mountain", "meaning": "Permanence, solidity, overseeing from height"},
                {"symbol": "Fire", "meaning": "Transformative energy, destructive or creative force"}
            ]
        },
        "love": {
            "theme": "love",
            "symbols": [
                {"symbol": "Rose", "meaning": "Beauty with thorns, passion with pain"},
                {"symbol": "Circle", "meaning": "Eternity, completion, unbroken connection"},
                {"symbol": "Bridge", "meaning": "Connection between separate entities"},
                {"symbol": "Twin Flames", "meaning": "Two parts of a whole, complementary forces"}
            ]
        },
        "knowledge": {
            "theme": "knowledge",
            "symbols": [
                {"symbol": "Tree", "meaning": "Branching wisdom, deep roots of understanding"},
                {"symbol": "Book", "meaning": "Accumulated wisdom, preserved insights"},
                {"symbol": "Lantern", "meaning": "Illumination in darkness, guided insight"},
                {"symbol": "Owl", "meaning": "Wisdom, perception beyond ordinary sight"}
            ]
        },
        "journey": {
            "theme": "journey",
            "symbols": [
                {"symbol": "Road", "meaning": "Path of life, choices and direction"},
                {"symbol": "River", "meaning": "Flow of time, changing yet constant"},
                {"symbol": "Bridge", "meaning": "Transition, crossing boundaries"},
                {"symbol": "Map", "meaning": "Guidance, overview of possibilities"}
            ]
        }
    }
    
    # Save default symbols
    for theme_id, theme_data in default_symbols.items():
        theme_path = symbols_dir / f"{theme_id}.json"
        if not theme_path.exists():
            with open(theme_path, "w") as f:
                json.dump(theme_data, f, indent=2)
    
    logger.info(f"Default symbols initialized successfully")

def initialize_demo_project(projects_dir: Path) -> None:
    """
    Initialize a demo project to showcase the system.
    
    Args:
        projects_dir: Directory for projects
    """
    # Check if demo project already exists
    demo_dir = projects_dir / "demo_project"
    if demo_dir.exists():
        logger.info(f"Demo project already exists, skipping initialization")
        return
    
    logger.info(f"Initializing demo project in {demo_dir}")
    
    # Create project directory and subdirectories
    os.makedirs(demo_dir, exist_ok=True)
    subdirs = ["characters", "scenes", "outlines", "analyses", "symbols", "drafts"]
    for subdir in subdirs:
        os.makedirs(demo_dir / subdir, exist_ok=True)
    
    # Create project metadata
    metadata = {
        "name": "Demo Project",
        "description": "A demonstration project for AI Writers Workshop",
        "type": "story",
        "created_at": "2023-09-01T12:00:00",
        "modified_at": "2023-09-01T12:00:00",
        "primary_pattern": "heroes_journey",
        "themes": ["journey", "knowledge"],
        "main_characters": ["Hero", "Mentor"],
        "secondary_characters": ["Threshold Guardian"],
        "word_count": 0,
        "status": "in_progress",
        "notes": "This is a demonstration project to showcase the AI Writers Workshop system.",
        "elements": {
            "characters": [],
            "scenes": [],
            "outlines": [],
            "analyses": [],
            "symbols": [],
            "drafts": []
        }
    }
    
    # Save metadata
    metadata_path = demo_dir / "metadata.json"
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)
    
    # Create notes file
    with open(demo_dir / "notes.md", "w") as f:
        f.write(f"# Demo Project\n\nA demonstration project for AI Writers Workshop\n\n## Notes\n\nUse this project to test the various tools and features of the AI Writers Workshop system.\n")
    
    logger.info(f"Demo project initialized successfully")

def initialize_all(base_dir: Path) -> None:
    """
    Initialize all components of the AI Writers Workshop.
    
    Args:
        base_dir: Base directory for all outputs
    """
    logger.info(f"Starting initialization of AI Writers Workshop in {base_dir}")
    
    initialize_directory_structure(base_dir)
    initialize_default_archetypes(base_dir / "library" / "archetypes")
    initialize_default_patterns(base_dir / "library" / "patterns")
    initialize_default_symbols(base_dir / "library" / "symbols")
    initialize_demo_project(base_dir / "projects")
    
    logger.info(f"Initialization completed successfully")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Initialize AI Writers Workshop")
    parser.add_argument("--dir", type=str, default="output",
                       help="Base directory for all outputs")
    
    args = parser.parse_args()
    
    base_dir = Path(args.dir)
    initialize_all(base_dir)
