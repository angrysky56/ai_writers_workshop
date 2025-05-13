"""
Character Management Component for AI Writers Workshop

Handles character creation and development with archetypal frameworks.
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

class CharacterManager:
    """Manages character creation and development with archetypal frameworks."""
    
    def __init__(self, project_manager, base_dir: Union[str, Path] = "output"):
        """
        Initialize the character manager.
        
        Args:
            project_manager: ProjectManager instance for project interactions
            base_dir: Base directory for all outputs
        """
        self.base_dir = Path(base_dir)
        self.project_manager = project_manager
        
        # Set up library directory for archetypes
        self.archetypes_dir = self.base_dir / "library" / "archetypes"
        self.archetypes_dir.mkdir(exist_ok=True, parents=True)
        
        # Load default archetypes
        self.archetypes = self._load_default_archetypes()
    
    def _load_default_archetypes(self) -> Dict[str, Dict[str, Any]]:
        """Load default character archetypes."""
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
        
        # Save default archetypes to library
        for archetype_id, archetype_data in archetypes.items():
            archetype_path = self.archetypes_dir / f"{archetype_id}.json"
            if not archetype_path.exists():
                with open(archetype_path, "w") as f:
                    json.dump(archetype_data, f, indent=2)
        
        return archetypes
    
    def list_archetypes(self) -> Dict[str, Dict[str, str]]:
        """
        List all available character archetypes.
        
        Returns:
            Dictionary with list of archetypes and basic information
        """
        archetypes_summary = {}
        
        # List archetypes from library directory
        for archetype_path in self.archetypes_dir.glob("*.json"):
            with open(archetype_path, "r") as f:
                archetype_data = json.load(f)
            
            archetype_id = archetype_path.stem
            archetypes_summary[archetype_id] = {
                "name": archetype_data.get("name", archetype_id),
                "description": archetype_data.get("description", "No description available")
            }
        
        # If no archetypes found in library, use default ones
        if not archetypes_summary:
            for archetype_id, archetype_data in self.archetypes.items():
                archetypes_summary[archetype_id] = {
                    "name": archetype_data.get("name", archetype_id),
                    "description": archetype_data.get("description", "No description available")
                }
        
        return {"archetypes": archetypes_summary}
    
    def get_archetype_details(self, archetype_name: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific character archetype.
        
        Args:
            archetype_name: Name of the archetype (e.g., "hero", "mentor")
            
        Returns:
            Dictionary with detailed archetype information
        """
        # Check library directory first
        archetype_path = self.archetypes_dir / f"{archetype_name.lower()}.json"
        
        if archetype_path.exists():
            with open(archetype_path, "r") as f:
                archetype_data = json.load(f)
            return {"archetype": archetype_data}
        
        # Then check default archetypes
        if archetype_name.lower() in self.archetypes:
            return {"archetype": self.archetypes[archetype_name.lower()]}
        
        # If not found, return error
        return {
            "error": f"Archetype '{archetype_name}' not found",
            "available_archetypes": list(self.archetypes.keys())
        }
    
    def create_character(self, name: str, archetype: str, traits: Optional[List[str]] = None,
                        project_id: Optional[str] = None, hybrid_archetypes: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        """
        Create a character based on an archetype.
        
        Args:
            name: Character name
            archetype: Base archetype (e.g., "hero", "mentor")
            traits: Optional list of specific traits
            project_id: Optional project to associate with
            hybrid_archetypes: Optional dictionary of archetype_id:weight for hybrid characters
            
        Returns:
            Dictionary with character information
        """
        # If using hybrid archetypes, validate them
        if hybrid_archetypes:
            for archetype_id in hybrid_archetypes:
                archetype_details = self.get_archetype_details(archetype_id)
                if "error" in archetype_details:
                    return archetype_details
            
            # Create hybrid description
            archetype_names = []
            for archetype_id, weight in sorted(hybrid_archetypes.items(), key=lambda x: x[1], reverse=True):
                archetype_details = self.get_archetype_details(archetype_id)
                archetype_names.append(f"{int(weight * 100)}% {archetype_details['archetype']['name']}")
            
            hybrid_description = f"A hybrid character combining {', '.join(archetype_names)}"
        else:
            # Get the archetype details
            archetype_details = self.get_archetype_details(archetype)
            if "error" in archetype_details:
                return archetype_details
            
            # Set single archetype description
            hybrid_description = None
        
        # Use provided traits or select from archetype traits
        if traits is None:
            if hybrid_archetypes:
                # Collect traits from all archetypes
                traits = []
                for archetype_id in hybrid_archetypes:
                    archetype_details = self.get_archetype_details(archetype_id)
                    traits.extend(archetype_details["archetype"].get("traits", [])[:2])  # Take top 2 traits from each
                traits = list(set(traits))[:4]  # Deduplicate and limit to 4 traits
            else:
                # Use traits from primary archetype
                archetype_info = archetype_details["archetype"]
                traits = archetype_info.get("traits", [])
        
        # Select shadow aspects
        if hybrid_archetypes:
            # Get primary archetype (highest weight)
            primary_archetype_id = max(hybrid_archetypes.items(), key=lambda x: x[1])[0]
            primary_archetype = self.get_archetype_details(primary_archetype_id)["archetype"]
            shadow_aspect = primary_archetype.get("shadow_aspects", ["Unknown"])[0]
        else:
            # Use shadow from primary archetype
            archetype_info = archetype_details["archetype"]
            shadow_aspect = archetype_info.get("shadow_aspects", ["Unknown"])[0] if archetype_info.get("shadow_aspects") else None
        
        # Create character data
        character = {
            "name": name,
            "archetype": archetype,
            "hybrid_archetypes": hybrid_archetypes if hybrid_archetypes else None,
            "description": hybrid_description if hybrid_description else f"{name} is a character based on the {archetype} archetype.",
            "traits": traits,
            "shadow_aspect": shadow_aspect,
            "development_potential": f"As a {archetype}, {name} has potential for growth through confronting their {shadow_aspect} tendencies."
        }
        
        # Add creation timestamp
        character["created_at"] = datetime.now().isoformat()
        
        # Save to project if specified
        if project_id:
            return self.project_manager.save_element(
                project_id=project_id,
                element_type="characters",
                element_data=character,
                element_id=self.project_manager._sanitize_name(f"{name}-{archetype}")
            )
        else:
            # Save to legacy character directory
            character_dir = self.base_dir / "characters"
            character_dir.mkdir(exist_ok=True, parents=True)
            
            sanitized_name = name.lower().replace(" ", "_").replace("-", "_")
            filename = f"{sanitized_name}-{archetype}.json"
            character_path = character_dir / filename
            
            with open(character_path, "w") as f:
                json.dump(character, f, indent=2)
            
            return {
                "character": character,
                "output_path": f"characters/{filename}"
            }
    
    def develop_character_arc(self, character_name: str, archetype: str, pattern: str,
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
        from components.pattern_manager import PatternManager
        pattern_manager = PatternManager(self.base_dir)
        
        # Get the pattern details
        pattern_details = pattern_manager.get_pattern_details(pattern)
        if "error" in pattern_details:
            return pattern_details
        
        # Get the archetype details
        archetype_details = self.get_archetype_details(archetype)
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
            "arc_stages": arc_stages,
            "created_at": datetime.now().isoformat()
        }
        
        # Save to project if specified
        if project_id:
            return self.project_manager.save_element(
                project_id=project_id,
                element_type="characters",
                element_data=character_arc,
                element_id=f"arc-{self.project_manager._sanitize_name(character_name)}-{pattern}"
            )
        else:
            # Save to legacy character directory
            character_dir = self.base_dir / "characters"
            character_dir.mkdir(exist_ok=True, parents=True)
            
            sanitized_name = character_name.lower().replace(" ", "_").replace("-", "_")
            filename = f"arc-{sanitized_name}-{pattern}.json"
            character_path = character_dir / filename
            
            with open(character_path, "w") as f:
                json.dump(character_arc, f, indent=2)
            
            return {
                **character_arc,
                "output_path": f"characters/{filename}"
            }
    
    def create_custom_archetype(self, name: str, description: str, traits: List[str],
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
        # If based on existing archetype, get its details
        if based_on:
            base_archetype = self.get_archetype_details(based_on)
            if "error" in base_archetype:
                return base_archetype
            
            # Start with base archetype and override
            archetype_data = base_archetype["archetype"].copy()
            archetype_data["name"] = name
            archetype_data["description"] = description
            archetype_data["traits"] = traits
            archetype_data["shadow_aspects"] = shadow_aspects
            if examples:
                archetype_data["examples"] = examples
        else:
            # Create new archetype from scratch
            archetype_data = {
                "name": name,
                "description": description,
                "traits": traits,
                "shadow_aspects": shadow_aspects,
                "examples": examples or []
            }
        
        # Add creation timestamp
        archetype_data["created_at"] = datetime.now().isoformat()
        
        # Save to library
        archetype_id = name.lower().replace(" ", "_").replace("-", "_")
        archetype_path = self.archetypes_dir / f"{archetype_id}.json"
        
        with open(archetype_path, "w") as f:
            json.dump(archetype_data, f, indent=2)
        
        # Update internal dictionary
        self.archetypes[archetype_id] = archetype_data
        
        return {
            "archetype": archetype_data,
            "output_path": f"library/archetypes/{archetype_id}.json"
        }
