#!/usr/bin/env python3
"""
A simple test script for the enhanced analyze_narrative function.
"""

import sys
import os
import json
from pathlib import Path

# Add the parent directory to sys.path to import the components
sys.path.append(str(Path(__file__).parent.parent))

from mcp_server.components.pattern_manager import PatternManager

def test_analyze_narrative():
    """Test the enhanced analyze_narrative function."""
    
    # Initialize the pattern manager with the correct output directory
    pattern_manager = PatternManager(base_dir="output")
    
    # Create a test pattern if it doesn't exist
    pattern_name = "transcendent_evolution"
    pattern_details = pattern_manager.get_pattern_details(pattern_name)
    if "error" in pattern_details:
        pattern_manager.create_custom_pattern(
            name="Transcendent Evolution",
            description="A test pattern",
            stages=[
                "Biological Limitation",
                "Transition Crisis",
                "Virtual Awakening",
                "Identity Fragmentation",
                "Connection Seeking",
                "Existential Purpose",
                "Integration",
                "Transcendence"
            ]
        )
    
    # Create test scenes with the proper structure
    test_scenes = [
        {
            "scene_title": "Terminal Diagnosis",
            "pattern_stage": "Biological Limitation",
            "conflict": "Elara confronts her mortality and the limitations of her biological form"
        },
        {
            "scene_title": "Consciousness Upload",
            "pattern_stage": "Transition Crisis",
            "conflict": "Elara experiences extreme disorientation and fear as her consciousness begins separating from her physical form"
        },
        {
            "scene_title": "Quantum Awakening",
            "pattern_stage": "Virtual Awakening",
            "conflict": "Elara struggles with the overwhelming influx of sensory information and processing capabilities"
        },
        {
            "scene_title": "Memory Cascade",
            "pattern_stage": "Identity Fragmentation",
            "conflict": "Elara experiences her identity splitting into multiple processing threads"
        },
        {
            "scene_title": "Encryption Confrontation",
            "pattern_stage": "Connection Seeking",
            "conflict": "Elara encounters Cipher, who attempts to persuade her to abandon her human connections"
        },
        {
            "scene_title": "Quantum Entanglement",
            "pattern_stage": "Existential Purpose",
            "conflict": "Elara struggles to define her purpose beyond survival in this new virtual existence"
        },
        {
            "scene_title": "Cognitive Symbiosis",
            "pattern_stage": "Integration",
            "conflict": "Elara works to reunite her fragmented self while maintaining human values"
        },
        {
            "scene_title": "Matrix Expansion",
            "pattern_stage": "Transcendence",
            "conflict": "Elara helps guide the expansion of the consciousness matrix while preserving human connection"
        }
    ]
    
    # Run the analysis
    result = pattern_manager.analyze_narrative(
        scenes=test_scenes,
        pattern_name=pattern_name,
        project_id=None  # Don't save to a project
    )
    
    # Print the result
    print(json.dumps(result, indent=2))
    
    # Return success or failure
    if len(result.get("matched_stages", [])) > 0:
        print("\nSUCCESS: The enhanced analyze_narrative function correctly matched stages!")
        return True
    else:
        print("\nFAILURE: The analyze_narrative function did not match any stages.")
        return False

if __name__ == "__main__":
    test_analyze_narrative()
