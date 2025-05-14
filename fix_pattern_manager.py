#!/usr/bin/env python3
"""
Script to fix analyze_narrative directly through the MCQ API.
"""

import os
import json
import shutil
from pathlib import Path

# Path to the pattern_manager.py file
pattern_manager_path = "/home/ty/Repositories/ai_workspace/ai_writers_workshop/mcp_server/components/pattern_manager.py"

# Create a backup of the original file
backup_path = pattern_manager_path + ".bak"
shutil.copy2(pattern_manager_path, backup_path)
print(f"Created backup at {backup_path}")

# Fixed content for the pattern_manager.py file
fixed_content = """
\"\"\"
Pattern Management Component for AI Writers Workshop

Handles narrative patterns and their application to story structures.
\"\"\"

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

class PatternManager:
    \"\"\"Manages narrative patterns and their application to story structures.\"\"\"
    
    def __init__(self, base_dir: Union[str, Path] = "output"):
        \"\"\"
        Initialize the pattern manager.
        
        Args:
            base_dir: Base directory for all outputs
        \"\"\"
        self.base_dir = Path(base_dir)
        
        # Set up library directory for patterns
        self.patterns_dir = self.base_dir / "library" / "patterns"
        self.patterns_dir.mkdir(exist_ok=True, parents=True)
        
        # Load default patterns
        self.patterns = self._load_default_patterns()
    
    def _load_default_patterns(self) -> Dict[str, Dict[str, Any]]:
        \"\"\"Load default narrative patterns.\"\"\"
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
        
        # Save default patterns to library
        for pattern_id, pattern_data in patterns.items():
            pattern_path = self.patterns_dir / f"{pattern_id}.json"
            if not pattern_path.exists():
                with open(pattern_path, "w") as f:
                    json.dump(pattern_data, f, indent=2)
        
        return patterns
    
    def list_patterns(self) -> Dict[str, Dict[str, Any]]:
        \"\"\"
        List available narrative patterns.
        
        Returns:
            Dictionary with list of patterns and basic information
        \"\"\"
        patterns_summary = {}
        
        # List patterns from library directory
        for pattern_path in self.patterns_dir.glob("*.json"):
            with open(pattern_path, "r") as f:
                pattern_data = json.load(f)
            
            pattern_id = pattern_path.stem
            patterns_summary[pattern_id] = {
                "name": pattern_data.get("name", pattern_id),
                "description": pattern_data.get("description", "No description available"),
                "stages": len(pattern_data.get("stages", []))
            }
        
        # If no patterns found in library, use default ones
        if not patterns_summary:
            for pattern_id, pattern_data in self.patterns.items():
                patterns_summary[pattern_id] = {
                    "name": pattern_data.get("name", pattern_id),
                    "description": pattern_data.get("description", "No description available"),
                    "stages": len(pattern_data.get("stages", []))
                }
        
        return {"patterns": patterns_summary}
    
    def get_pattern_details(self, pattern_name: str) -> Dict[str, Any]:
        \"\"\"
        Get detailed information about a specific narrative pattern.
        
        Args:
            pattern_name: Name of the pattern (e.g., "heroes_journey", "transformation")
            
        Returns:
            Dictionary with detailed pattern information
        \"\"\"
        # Check library directory first
        pattern_path = self.patterns_dir / f"{pattern_name.lower()}.json"
        
        if pattern_path.exists():
            with open(pattern_path, "r") as f:
                pattern_data = json.load(f)
            return {"pattern": pattern_data}
        
        # Then check default patterns
        if pattern_name.lower() in self.patterns:
            return {"pattern": self.patterns[pattern_name.lower()]}
        
        # If not found, return error
        return {
            "error": f"Pattern '{pattern_name}' not found",
            "available_patterns": list(self.patterns.keys())
        }
    
    def create_custom_pattern(self, name: str, description: str, stages: List[str],
                             psychological_functions: Optional[List[str]] = None,
                             examples: Optional[List[str]] = None,
                             based_on: Optional[str] = None) -> Dict[str, Any]:
        \"\"\"
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
        \"\"\"
        # If based on existing pattern, get its details
        if based_on:
            base_pattern = self.get_pattern_details(based_on)
            if "error" in base_pattern:
                return base_pattern
            
            # Start with base pattern and override
            pattern_data = base_pattern["pattern"].copy()
            pattern_data["name"] = name
            pattern_data["description"] = description
            pattern_data["stages"] = stages
            if psychological_functions:
                pattern_data["psychological_functions"] = psychological_functions
            if examples:
                pattern_data["examples"] = examples
        else:
            # Create new pattern from scratch
            pattern_data = {
                "name": name,
                "description": description,
                "stages": stages,
                "psychological_functions": psychological_functions or [],
                "examples": examples or []
            }
        
        # Add creation timestamp
        pattern_data["created_at"] = datetime.now().isoformat()
        
        # Save to library
        pattern_id = name.lower().replace(" ", "_").replace("-", "_")
        pattern_path = self.patterns_dir / f"{pattern_id}.json"
        
        with open(pattern_path, "w") as f:
            json.dump(pattern_data, f, indent=2)
        
        # Update internal dictionary
        self.patterns[pattern_id] = pattern_data
        
        return {
            "pattern": pattern_data,
            "output_path": f"library/patterns/{pattern_id}.json"
        }
    
    def create_hybrid_pattern(self, name: str, description: str, 
                            patterns: Dict[str, float],
                            custom_stages: Optional[List[str]] = None) -> Dict[str, Any]:
        \"\"\"
        Create a hybrid pattern from multiple existing patterns.
        
        Args:
            name: Pattern name
            description: Pattern description
            patterns: Dictionary of pattern_name:weight pairs
            custom_stages: Optional custom stage list (if None, will be auto-generated)
            
        Returns:
            Dictionary with pattern information
        \"\"\"
        # Validate all patterns exist
        pattern_data_list = []
        for pattern_name in patterns:
            pattern_details = self.get_pattern_details(pattern_name)
            if "error" in pattern_details:
                return pattern_details
            pattern_data_list.append((pattern_name, pattern_details["pattern"], patterns[pattern_name]))
        
        # Sort by weight descending
        pattern_data_list.sort(key=lambda x: x[2], reverse=True)
        
        # If custom stages provided, use those
        if custom_stages:
            stages = custom_stages
        else:
            # Auto-generate stages based on weighted patterns
            stages = []
            # Take proportional number of stages from each pattern based on weight
            total_stages = sum(len(p[1]["stages"]) for p in pattern_data_list)
            target_stages = min(12, total_stages)  # Cap at 12 stages
            
            for pattern_name, pattern_data, weight in pattern_data_list:
                # Calculate how many stages to take from this pattern
                num_stages = max(1, round(weight * target_stages))
                pattern_stages = pattern_data["stages"]
                
                # Take evenly spaced stages
                if num_stages >= len(pattern_stages):
                    stages.extend(pattern_stages)
                else:
                    indices = [int(i * (len(pattern_stages) - 1) / (num_stages - 1)) for i in range(num_stages)]
                    stages.extend([pattern_stages[i] for i in indices])
            
            # Ensure we don't exceed target stage count
            stages = stages[:target_stages]
        
        # Combine psychological functions and examples
        psychological_functions = []
        examples = []
        
        for _, pattern_data, _ in pattern_data_list:
            psychological_functions.extend(pattern_data.get("psychological_functions", []))
            examples.extend(pattern_data.get("examples", [])[:2])  # Take up to 2 examples from each
        
        # Deduplicate
        psychological_functions = list(dict.fromkeys(psychological_functions))
        examples = list(dict.fromkeys(examples))
        
        # Create hybrid pattern
        hybrid_pattern = {
            "name": name,
            "description": description,
            "hybrid": True,
            "component_patterns": {p[0]: p[2] for p in pattern_data_list},
            "stages": stages,
            "psychological_functions": psychological_functions,
            "examples": examples,
            "created_at": datetime.now().isoformat()
        }
        
        # Save to library
        pattern_id = name.lower().replace(" ", "_").replace("-", "_")
        pattern_path = self.patterns_dir / f"{pattern_id}.json"
        
        with open(pattern_path, "w") as f:
            json.dump(hybrid_pattern, f, indent=2)
        
        # Update internal dictionary
        self.patterns[pattern_id] = hybrid_pattern
        
        return {
            "pattern": hybrid_pattern,
            "output_path": f"library/patterns/{pattern_id}.json"
        }
    
    def analyze_narrative(self, scenes: List[Dict[str, str]], pattern_name: str,
                        project_id: Optional[str] = None, adherence_level: float = 1.0) -> Dict[str, Any]:
        \"\"\"
        Analyze a narrative structure using a specific pattern with flexible matching.
        
        Args:
            scenes: List of scene dictionaries
            pattern_name: Name of the pattern to analyze against
            project_id: Optional project to associate with
            adherence_level: How strictly to apply pattern (0.0-1.0)
            
        Returns:
            Dictionary with analysis results
        \"\"\"
        # Get the pattern details
        pattern_details = self.get_pattern_details(pattern_name)
        if "error" in pattern_details:
            return pattern_details
        
        pattern = pattern_details["pattern"]
        stages = pattern["stages"]
        
        # Apply adherence level - lower adherence means fewer required stages
        required_stage_count = max(1, round(len(stages) * adherence_level))
        
        # Analysis algorithm with flexible matching
        matched_stages = []
        missing_stages = []
        
        for stage in stages:
            found = False
            matched_scene = None
            
            for scene in scenes:
                # Extract all text fields from the scene for analysis
                scene_text_fields = []
                
                # Handle various field name conventions
                title = scene.get("title", scene.get("scene_title", ""))
                scene_text_fields.append(title)
                
                description = scene.get("description", "")
                scene_text_fields.append(description)
                
                # Check pattern_stage field explicitly
                pattern_stage = scene.get("pattern_stage", "")
                scene_text_fields.append(pattern_stage)
                
                # Add other narrative fields
                for field in ["conflict", "goal", "outcome", "notes"]:
                    if field in scene:
                        scene_text_fields.append(scene[field])
                
                # Join all text fields for comprehensive matching
                scene_text = " ".join(scene_text_fields).lower()
                
                # Check for exact stage name match
                if stage.lower() in scene_text:
                    matched_stages.append({
                        "stage": stage,
                        "scene": title,
                        "match_quality": "exact"
                    })
                    matched_scene = scene
                    found = True
                    break
                
                # Check for direct pattern_stage match
                if pattern_stage.lower() == stage.lower():
                    matched_stages.append({
                        "stage": stage,
                        "scene": title,
                        "match_quality": "exact"
                    })
                    matched_scene = scene
                    found = True
                    break
            
            # If no exact match, try semantic and keyword matching
            if not found:
                # Look for thematic or keyword matches
                best_match = None
                best_score = 0
                
                for scene in scenes:
                    # Extract all text fields again
                    scene_text_fields = []
                    
                    title = scene.get("title", scene.get("scene_title", ""))
                    scene_text_fields.append(title)
                    
                    description = scene.get("description", "")
                    scene_text_fields.append(description)
                    
                    pattern_stage = scene.get("pattern_stage", "")
                    scene_text_fields.append(pattern_stage)
                    
                    for field in ["conflict", "goal", "outcome", "notes"]:
                        if field in scene:
                            scene_text_fields.append(scene[field])
                    
                    scene_text = " ".join(scene_text_fields).lower()
                    
                    # Enhanced keyword matching with stemming
                    score = 0
                    stage_words = stage.lower().split()
                    
                    # For each word in the stage
                    for word in stage_words:
                        if len(word) > 3:  # Only consider significant words
                            if word in scene_text:
                                score += 2  # Full word match
                            else:
                                # Check for word stems/roots (simple implementation)
                                for content_word in scene_text.split():
                                    if content_word.startswith(word[:4]) and len(content_word) >= len(word):
                                        score += 1
                                        break
                    
                    # Semantic similarity based on theme words
                    theme_mappings = {
                        "beginning": ["start", "initiation", "genesis", "birth"],
                        "journey": ["path", "voyage", "travel", "adventure"],
                        "transformation": ["change", "evolution", "metamorphosis"],
                        "challenge": ["test", "trial", "difficulty", "obstacle"],
                        "awakening": ["realization", "discovery", "enlightenment"],
                        "integration": ["unification", "harmony", "balance"],
                        "transcendence": ["ascension", "elevation", "enlightenment"]
                    }
                    
                    # Check for semantic matches
                    for theme, related_words in theme_mappings.items():
                        if theme in stage.lower():
                            for word in related_words:
                                if word in scene_text:
                                    score += 1
                    
                    if score > best_score:
                        best_score = score
                        best_match = scene
                
                # Use a more lenient threshold to match scenes with stages
                min_score_threshold = 1  # Accept any semantic/keyword match
                
                if best_score >= min_score_threshold and best_match:
                    title = best_match.get("title", best_match.get("scene_title", ""))
                    matched_stages.append({
                        "stage": stage,
                        "scene": title,
                        "match_quality": "semantic",
                        "match_score": best_score
                    })
                    matched_scene = best_match
                    found = True
            
            if not found:
                missing_stages.append(stage)
        
        # Calculate match score based on required stages
        match_score = len(matched_stages) / required_stage_count if required_stage_count > 0 else 0
        
        # Provide more detailed match information
        match_quality = {}
        for match in matched_stages:
            quality = match["match_quality"]
            match_quality[quality] = match_quality.get(quality, 0) + 1
            
        match_quality_text = ", ".join([f"{count} {quality}" for quality, count in match_quality.items()])
        if not match_quality_text:
            match_quality_text = "no matches"
        
        # Adaptive analysis based on adherence level
        if adherence_level < 1.0:
            analysis_text = (
                f"The narrative matches {int(match_score * 100)}% of the required stages "
                f"with {len(matched_stages)} of {required_stage_count} required stages matched "
                f"({match_quality_text})."
            )
        else:
            analysis_text = (
                f"The narrative matches {int(match_score * 100)}% of the {pattern_name} pattern stages "
                f"with {len(matched_stages)} of {len(stages)} stages matched "
                f"({match_quality_text})."
            )
            
        # Add match details for each matched stage
        match_details = []
        for match in matched_stages:
            match_details.append({
                "stage": match["stage"],
                "scene": match["scene"],
                "match_quality": match["match_quality"],
                "score": match.get("match_score", None)
            })
        
        analysis_result = {
            "pattern": pattern_name,
            "adherence_level": adherence_level,
            "required_stages": required_stage_count,
            "matched_stages": match_details,
            "missing_stages": missing_stages,
            "match_score": match_score,
            "analysis": analysis_text,
            "created_at": datetime.now().isoformat()
        }
        
        # Save to project if specified
        if project_id:
            from components.project_manager import ProjectManager
            project_manager = ProjectManager(self.base_dir)
            
            # Fix to handle both title and scene_title fields
            first_scene_title = "unnamed"
            if scenes:
                first_scene = scenes[0]
                first_scene_title = first_scene.get("title", first_scene.get("scene_title", "unnamed"))
            
            sanitized_title = first_scene_title.lower().replace(" ", "_")
            
            return project_manager.save_element(
                project_id=project_id,
                element_type="analyses",
                element_data=analysis_result,
                element_id=f"analysis-{sanitized_title}-{pattern_name}"
            )
        else:
            # Save to legacy analysis directory
            analysis_dir = self.base_dir / "analyses"
            analysis_dir.mkdir(exist_ok=True, parents=True)
            
            # Fix to handle both title and scene_title fields
            first_scene_title = "unnamed"
            if scenes:
                first_scene = scenes[0]
                first_scene_title = first_scene.get("title", first_scene.get("scene_title", "unnamed"))
            
            sanitized_title = first_scene_title.lower().replace(" ", "_")
            filename = f"analysis-{sanitized_title}-{pattern_name}.json"
            analysis_path = analysis_dir / filename
            
            with open(analysis_path, "w") as f:
                json.dump(analysis_result, f, indent=2)
            
            return {
                **analysis_result,
                "output_path": f"analyses/{filename}"
            }
"""

# Write the fixed content to the file
with open(pattern_manager_path, "w") as f:
    f.write(fixed_content)

print(f"Successfully updated {pattern_manager_path}")
print("Restart the server to apply changes")
