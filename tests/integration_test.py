"""
Integration test script for AI Writers Workshop

This script tests the basic functionality of the AI Writers Workshop by:
1. Creating a project
2. Creating characters in the project
3. Generating scenes
4. Analyzing the narrative
5. Compiling the narrative

Run this after setup to verify everything is working correctly.
"""

import os
import sys
import json
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from mcp_server.components.project_manager import ProjectManager
from mcp_server.components.character_manager import CharacterManager
from mcp_server.components.pattern_manager import PatternManager
from mcp_server.components.narrative_generator import NarrativeGenerator
from mcp_server.components.symbolic_manager import SymbolicManager

# Define output directory
OUTPUT_DIR = project_root / "output"

def run_integration_test():
    """Run a basic integration test of all components."""
    print("Starting AI Writers Workshop integration test...")
    
    # Initialize component managers
    project_manager = ProjectManager(OUTPUT_DIR)
    pattern_manager = PatternManager(OUTPUT_DIR)
    character_manager = CharacterManager(project_manager, OUTPUT_DIR)
    narrative_generator = NarrativeGenerator(project_manager, pattern_manager, OUTPUT_DIR)
    symbolic_manager = SymbolicManager(project_manager, OUTPUT_DIR)
    
    # 1. Create a test project
    print("\n1. Creating test project...")
    project = project_manager.create_project(
        name="Test Project",
        description="A test project for integration testing",
        project_type="story"
    )
    print(f"Project created: {project['name']}")
    project_id = project_manager._sanitize_name("Test Project")
    
    # 2. Create characters
    print("\n2. Creating characters...")
    hero = character_manager.create_character(
        name="Test Hero",
        archetype="hero",
        traits=["Brave", "Smart", "Kind"],
        project_id=project_id
    )
    print(f"Character created: {hero.get('name', 'Unknown')}")
    
    mentor = character_manager.create_character(
        name="Test Mentor",
        archetype="mentor",
        traits=["Wise", "Mysterious", "Knowledgeable"],
        project_id=project_id
    )
    print(f"Character created: {mentor.get('name', 'Unknown')}")
    
    # Create a hybrid character
    hybrid = character_manager.create_character(
        name="Hybrid Character",
        archetype="hero",
        hybrid_archetypes={"hero": 0.6, "trickster": 0.4},
        project_id=project_id
    )
    print(f"Hybrid character created: {hybrid.get('name', 'Unknown')}")
    
    # 3. Generate scenes
    print("\n3. Generating scenes...")
    scenes = []
    
    scene1 = narrative_generator.generate_scene(
        scene_title="The Beginning",
        pattern_stage="Ordinary World",
        characters=["Test Hero"],
        project_id=project_id,
        setting="A small village at the edge of a great forest"
    )
    scenes.append(scene1)
    print(f"Scene created: {scene1.get('scene_title', 'Unknown')}")
    
    scene2 = narrative_generator.generate_scene(
        scene_title="The Meeting",
        pattern_stage="Meeting the Mentor",
        characters=["Test Hero", "Test Mentor"],
        project_id=project_id,
        setting="An ancient library hidden deep in the forest"
    )
    scenes.append(scene2)
    print(f"Scene created: {scene2.get('scene_title', 'Unknown')}")
    
    scene3 = narrative_generator.generate_scene(
        scene_title="The Adventure Begins",
        pattern_stage="Crossing the Threshold",
        characters=["Test Hero", "Test Mentor", "Hybrid Character"],
        project_id=project_id,
        setting="A mysterious portal at the heart of the ancient library"
    )
    scenes.append(scene3)
    print(f"Scene created: {scene3.get('scene_title', 'Unknown')}")
    
    # 4. Analyze the narrative
    print("\n4. Analyzing the narrative...")
    scene_data = [
        {"title": scene1.get("scene_title", ""), "description": scene1.get("setting", "")},
        {"title": scene2.get("scene_title", ""), "description": scene2.get("setting", "")},
        {"title": scene3.get("scene_title", ""), "description": scene3.get("setting", "")}
    ]
    
    analysis = pattern_manager.analyze_narrative(
        scenes=scene_data,
        pattern_name="heroes_journey",
        project_id=project_id,
        adherence_level=0.5  # Only require 50% adherence
    )
    
    print(f"Analysis completed: {analysis.get('analysis', 'Unknown')}")
    print(f"Match score: {analysis.get('match_score', 0)}")
    
    # 5. Apply symbolic themes
    print("\n5. Applying symbolic themes...")
    symbols = symbolic_manager.find_symbolic_connections(
        theme="journey",
        count=3,
        project_id=project_id
    )
    print(f"Symbols found for 'journey': {len(symbols.get('symbols', []))}")
    
    applied = symbolic_manager.apply_symbolic_theme(
        project_id=project_id,
        theme="journey",
        element_types=["scenes"]
    )
    print(f"Symbols applied to elements: {applied.get('applied_to', {})}")
    
    # 6. Compile the narrative
    print("\n6. Compiling the narrative...")
    compilation = narrative_generator.compile_narrative(
        project_id=project_id,
        title="Test Narrative",
        include_character_descriptions=True,
        format="markdown"
    )
    
    print(f"Narrative compiled: {compilation.get('title', 'Unknown')}")
    print(f"Character count: {compilation.get('character_count', 0)}")
    print(f"Scene count: {compilation.get('scene_count', 0)}")
    
    # 7. Report success
    print("\nIntegration test completed successfully!")
    print(f"Project directory: {OUTPUT_DIR}/projects/{project_id}")
    print("You can now run the MCP server to access these components and data.")

if __name__ == "__main__":
    run_integration_test()
