"""
AI Writing Agency - Archetypal Framework Module

This module implements the archetypal narrative patterns, character archetypes,
and symbolic systems described in the framework architecture document.
It provides the foundation for narrative development with psychological depth.
"""

import os
import json
import yaml
import logging
from typing import Dict, List, Any, Optional, Union, Tuple, Set
from pathlib import Path

from .config import config
from .core import ProcessingComponent

# Configure logging
logger = logging.getLogger(__name__)

class ArchetypalPattern:
    """
    Represents a narrative archetypal pattern.
    
    Archetypal patterns are fundamental narrative structures that appear across
    cultures and time periods, with consistent psychological functions.
    """
    
    def __init__(self, 
                 name: str,
                 structure: List[str],
                 variations: List[str],
                 psychological_functions: List[str],
                 description: str = ""):
        """
        Initialize an archetypal pattern.
        
        Args:
            name: Name of the archetypal pattern
            structure: List of structural elements in the pattern
            variations: List of common variations of the pattern
            psychological_functions: List of psychological functions the pattern serves
            description: Optional detailed description of the pattern
        """
        self.name = name
        self.structure = structure
        self.variations = variations
        self.psychological_functions = psychological_functions
        self.description = description
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the archetypal pattern to a dictionary representation.
        
        Returns:
            Dictionary representation of the pattern
        """
        return {
            "name": self.name,
            "structure": self.structure,
            "variations": self.variations,
            "psychological_functions": self.psychological_functions,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ArchetypalPattern':
        """
        Create an archetypal pattern from a dictionary representation.
        
        Args:
            data: Dictionary representation of the pattern
            
        Returns:
            An ArchetypalPattern instance
        """
        return cls(
            name=data["name"],
            structure=data["structure"],
            variations=data["variations"],
            psychological_functions=data["psychological_functions"],
            description=data.get("description", "")
        )


class CharacterArchetype:
    """
    Represents a character archetype.
    
    Character archetypes are recurring character types that appear in narratives
    across cultures, each with specific functions, traits, and shadow aspects.
    """
    
    def __init__(self,
                 name: str,
                 functions: List[str],
                 typical_traits: List[str],
                 shadow_aspects: List[str],
                 variations: List[str],
                 description: str = ""):
        """
        Initialize a character archetype.
        
        Args:
            name: Name of the character archetype
            functions: List of narrative functions this archetype serves
            typical_traits: List of traits typically associated with this archetype
            shadow_aspects: List of shadow/negative aspects of this archetype
            variations: List of common variations of this archetype
            description: Optional detailed description of the archetype
        """
        self.name = name
        self.functions = functions
        self.typical_traits = typical_traits
        self.shadow_aspects = shadow_aspects
        self.variations = variations
        self.description = description
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the character archetype to a dictionary representation.
        
        Returns:
            Dictionary representation of the archetype
        """
        return {
            "name": self.name,
            "functions": self.functions,
            "typical_traits": self.typical_traits,
            "shadow_aspects": self.shadow_aspects,
            "variations": self.variations,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CharacterArchetype':
        """
        Create a character archetype from a dictionary representation.
        
        Args:
            data: Dictionary representation of the archetype
            
        Returns:
            A CharacterArchetype instance
        """
        return cls(
            name=data["name"],
            functions=data["functions"],
            typical_traits=data["typical_traits"],
            shadow_aspects=data["shadow_aspects"],
            variations=data["variations"],
            description=data.get("description", "")
        )


class SymbolicSystem:
    """
    Represents a symbolic system used in narratives.
    
    Symbolic systems are networks of related symbols that can be used to add
    depth and resonance to narratives, often operating on subconscious levels.
    """
    
    def __init__(self,
                 name: str,
                 categories: Dict[str, Dict[str, List[str]]],
                 description: str = ""):
        """
        Initialize a symbolic system.
        
        Args:
            name: Name of the symbolic system
            categories: Mapping of categories to symbols and their associations
            description: Optional detailed description of the symbolic system
        """
        self.name = name
        self.categories = categories
        self.description = description
    
    def get_symbols_for_concept(self, concept: str) -> List[Tuple[str, str, float]]:
        """
        Find symbols that represent a given concept or theme.
        
        Args:
            concept: Concept or theme to find symbols for
            
        Returns:
            List of tuples containing (category, symbol, relevance_score)
        """
        results = []
        for category, symbols in self.categories.items():
            for symbol, associations in symbols.items():
                # Calculate relevance score based on whether the concept
                # or related terms appear in the symbol's associations
                score = 0.0
                for association in associations:
                    if concept.lower() in association.lower():
                        score = 1.0
                        break
                    elif any(word in association.lower() for word in concept.lower().split()):
                        score = max(score, 0.5)
                
                if score > 0:
                    results.append((category, symbol, score))
        
        # Sort by relevance score in descending order
        results.sort(key=lambda x: x[2], reverse=True)
        return results
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the symbolic system to a dictionary representation.
        
        Returns:
            Dictionary representation of the symbolic system
        """
        return {
            "name": self.name,
            "categories": self.categories,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SymbolicSystem':
        """
        Create a symbolic system from a dictionary representation.
        
        Args:
            data: Dictionary representation of the symbolic system
            
        Returns:
            A SymbolicSystem instance
        """
        return cls(
            name=data["name"],
            categories=data["categories"],
            description=data.get("description", "")
        )


class ArchetypalFramework:
    """
    The central framework for working with archetypal patterns, character archetypes,
    and symbolic systems in narrative development.
    """
    
    def __init__(self):
        """Initialize the archetypal framework."""
        self.patterns: Dict[str, ArchetypalPattern] = {}
        self.character_archetypes: Dict[str, CharacterArchetype] = {}
        self.symbolic_systems: Dict[str, SymbolicSystem] = {}
        self._load_default_data()
    
    def _load_default_data(self) -> None:
        """Load default archetypal data from the configuration."""
        # Load archetypal framework configuration
        archetypal_config = config.load_archetypal_framework()
        
        # Load patterns
        for name, data in archetypal_config.get("patterns", {}).items():
            pattern = ArchetypalPattern.from_dict({"name": name, **data})
            self.patterns[name] = pattern
        
        # Load character archetypes
        for name, data in archetypal_config.get("character_archetypes", {}).items():
            archetype = CharacterArchetype.from_dict({"name": name, **data})
            self.character_archetypes[name] = archetype
        
        # Load symbolic systems
        for name, data in archetypal_config.get("symbols", {}).items():
            system = SymbolicSystem.from_dict({"name": name, **data})
            self.symbolic_systems[name] = system
        
        logger.info(f"Loaded {len(self.patterns)} patterns, {len(self.character_archetypes)} character archetypes, and {len(self.symbolic_systems)} symbolic systems")
    
    def create_default_files(self, directory: str = "./archetypes") -> None:
        """
        Create default archetypal framework files if they don't exist.
        
        Args:
            directory: Directory to create files in
        """
        os.makedirs(directory, exist_ok=True)
        
        # Create default patterns file
        patterns_file = os.path.join(directory, "patterns.yaml")
        if not os.path.exists(patterns_file):
            default_patterns = {
                "Hero's Journey": {
                    "structure": [
                        "Ordinary World",
                        "Call to Adventure",
                        "Refusal of Call",
                        "Meeting the Mentor",
                        "Crossing the Threshold",
                        "Tests, Allies, Enemies",
                        "Approach to Inmost Cave",
                        "Ordeal",
                        "Reward (Seizing the Sword)",
                        "The Road Back",
                        "Resurrection",
                        "Return with Elixir"
                    ],
                    "variations": [
                        "Classical Hero",
                        "Reluctant Hero",
                        "Anti-Hero",
                        "Tragic Hero",
                        "Ensemble Heroes"
                    ],
                    "psychological_functions": [
                        "Identity formation",
                        "Individuation process",
                        "Community integration",
                        "Value transmission"
                    ],
                    "description": "The Hero's Journey is the most well-known archetypal pattern, popularized by Joseph Campbell's work on comparative mythology."
                },
                "Transformation": {
                    "structure": [
                        "Status Quo",
                        "Inciting Incident",
                        "Awakening to Limitations",
                        "Experimental Action",
                        "Negative Consequences",
                        "Learning from Failure",
                        "New Understanding",
                        "Integration of Shadow",
                        "Transformed State"
                    ],
                    "variations": [
                        "Physical Transformation",
                        "Psychological Transformation",
                        "Social Transformation",
                        "Spiritual Transformation",
                        "Technological Transformation"
                    ],
                    "psychological_functions": [
                        "Personal growth modeling",
                        "Adaptive resilience",
                        "Change normalization",
                        "Self-actualization pathway"
                    ],
                    "description": "The Transformation archetype deals with fundamental change, either physical, psychological, or spiritual."
                }
            }
            
            with open(patterns_file, "w") as file:
                yaml.dump(default_patterns, file, default_flow_style=False)
            
            logger.info(f"Created default patterns file at {patterns_file}")
        
        # Create default character archetypes file
        archetypes_file = os.path.join(directory, "characters.yaml")
        if not os.path.exists(archetypes_file):
            default_archetypes = {
                "Hero": {
                    "functions": ["protagonist", "moral center", "audience surrogate"],
                    "typical_traits": ["courage", "conviction", "competence", "sacrifice"],
                    "shadow_aspects": ["self-righteousness", "martyrdom", "exceptionalism"],
                    "variations": ["reluctant hero", "anti-hero", "tragic hero", "everyday hero"],
                    "description": "The Hero is the central character who undertakes the journey, faces the challenges, and undergoes transformation."
                },
                "Mentor": {
                    "functions": ["guidance", "gift-giving", "motivation", "teaching"],
                    "typical_traits": ["wisdom", "patience", "perspective", "hidden knowledge"],
                    "shadow_aspects": ["manipulation", "dependency creation", "dogmatism"],
                    "variations": ["mystic mentor", "practical mentor", "false mentor", "absent mentor"],
                    "description": "The Mentor provides guidance, wisdom, and sometimes supernatural aid to the hero."
                }
            }
            
            with open(archetypes_file, "w") as file:
                yaml.dump(default_archetypes, file, default_flow_style=False)
            
            logger.info(f"Created default character archetypes file at {archetypes_file}")
        
        # Create default symbols file
        symbols_file = os.path.join(directory, "symbols.yaml")
        if not os.path.exists(symbols_file):
            default_symbols = {
                "Natural Elements": {
                    "categories": {
                        "Fire": {
                            "flame": ["transformation", "destruction", "passion", "enlightenment"],
                            "candle": ["guidance", "hope", "solitude", "fragility"],
                            "wildfire": ["chaos", "renewal", "uncontrolled power", "cleansing"]
                        },
                        "Water": {
                            "ocean": ["depth", "unconscious", "mystery", "timelessness"],
                            "river": ["journey", "time", "change", "continuity"],
                            "rain": ["renewal", "cleansing", "sorrow", "abundance"]
                        }
                    },
                    "description": "Natural elements serve as fundamental symbolic systems across cultures."
                },
                "Temporal Patterns": {
                    "categories": {
                        "Seasons": {
                            "spring": ["rebirth", "new beginning", "growth", "youth"],
                            "summer": ["abundance", "flourishing", "maturity", "fullness"],
                            "autumn": ["harvest", "decline", "wisdom", "preparation"],
                            "winter": ["dormancy", "death", "preservation", "introspection"]
                        },
                        "Day Cycle": {
                            "dawn": ["awakening", "potential", "fresh start"],
                            "noon": ["clarity", "full awareness", "direct action"],
                            "dusk": ["transition", "reflection", "liminality"],
                            "night": ["unconscious", "mystery", "dream state", "hidden work"]
                        }
                    },
                    "description": "Temporal patterns reflect the cyclical nature of life and consciousness."
                }
            }
            
            with open(symbols_file, "w") as file:
                yaml.dump(default_symbols, file, default_flow_style=False)
            
            logger.info(f"Created default symbols file at {symbols_file}")
        
        # Update the configuration to point to these files
        config.set("archetypal_framework.patterns_file", patterns_file)
        config.set("archetypal_framework.character_archetypes_file", archetypes_file)
        config.set("archetypal_framework.symbols_file", symbols_file)
        config.save()
    
    def get_pattern(self, name: str) -> Optional[ArchetypalPattern]:
        """
        Get an archetypal pattern by name.
        
        Args:
            name: Name of the pattern
            
        Returns:
            The pattern or None if not found
        """
        return self.patterns.get(name)
    
    def get_character_archetype(self, name: str) -> Optional[CharacterArchetype]:
        """
        Get a character archetype by name.
        
        Args:
            name: Name of the character archetype
            
        Returns:
            The character archetype or None if not found
        """
        return self.character_archetypes.get(name)
    
    def get_symbolic_system(self, name: str) -> Optional[SymbolicSystem]:
        """
        Get a symbolic system by name.
        
        Args:
            name: Name of the symbolic system
            
        Returns:
            The symbolic system or None if not found
        """
        return self.symbolic_systems.get(name)
    
    def find_patterns_by_theme(self, theme: str) -> List[ArchetypalPattern]:
        """
        Find archetypal patterns relevant to a given theme.
        
        Args:
            theme: Theme to find patterns for
            
        Returns:
            List of relevant patterns
        """
        relevant_patterns = []
        
        for pattern in self.patterns.values():
            # Check if the theme appears in psychological functions
            if any(theme.lower() in function.lower() for function in pattern.psychological_functions):
                relevant_patterns.append(pattern)
                continue
            
            # Check if the theme appears in variations
            if any(theme.lower() in variation.lower() for variation in pattern.variations):
                relevant_patterns.append(pattern)
                continue
            
            # Check if the theme appears in the description
            if theme.lower() in pattern.description.lower():
                relevant_patterns.append(pattern)
                continue
        
        return relevant_patterns
    
    def find_archetypes_by_traits(self, traits: List[str]) -> List[Tuple[CharacterArchetype, float]]:
        """
        Find character archetypes that match given traits.
        
        Args:
            traits: List of traits to match
            
        Returns:
            List of tuples containing (archetype, relevance_score)
        """
        results = []
        
        for archetype in self.character_archetypes.values():
            # Calculate match score between traits and archetype's typical traits
            trait_matches = sum(1 for trait in traits 
                               if any(trait.lower() in t.lower() for t in archetype.typical_traits))
            
            # Calculate a relevance score (0.0 to 1.0)
            if traits:
                relevance = trait_matches / len(traits)
                
                # Only include if there's at least some match
                if relevance > 0:
                    results.append((archetype, relevance))
        
        # Sort by relevance score in descending order
        results.sort(key=lambda x: x[1], reverse=True)
        return results
    
    def generate_symbolic_associations(self, theme: str, count: int = 5) -> List[Dict[str, Any]]:
        """
        Generate symbolic associations for a given theme.
        
        Args:
            theme: Theme to generate symbols for
            count: Maximum number of symbols to generate
            
        Returns:
            List of symbolic associations
        """
        all_symbols = []
        
        # Search across all symbolic systems
        for system in self.symbolic_systems.values():
            symbols = system.get_symbols_for_concept(theme)
            for category, symbol, score in symbols:
                all_symbols.append({
                    "system": system.name,
                    "category": category,
                    "symbol": symbol,
                    "relevance": score
                })
        
        # Sort by relevance and take top matches
        all_symbols.sort(key=lambda x: x["relevance"], reverse=True)
        return all_symbols[:count]
    
    def analyze_narrative_structure(self, scenes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze a narrative structure to identify archetypal patterns.
        
        Args:
            scenes: List of scene dictionaries with keys like "title", "description", "characters"
            
        Returns:
            Analysis results containing identified patterns and correspondences
        """
        results = {
            "identified_patterns": [],
            "structural_recommendations": [],
            "character_archetype_analysis": {},
            "symbolic_opportunities": []
        }
        
        # Extract key narrative elements
        scene_titles = [scene.get("title", "") for scene in scenes]
        scene_descriptions = [scene.get("description", "") for scene in scenes]
        characters = {}
        
        for scene in scenes:
            for character in scene.get("characters", []):
                char_name = character.get("name", "")
                if char_name:
                    if char_name not in characters:
                        characters[char_name] = {"scenes": [], "traits": set(), "actions": []}
                    
                    characters[char_name]["scenes"].append(scene.get("title", ""))
                    
                    for trait in character.get("traits", []):
                        characters[char_name]["traits"].add(trait)
                    
                    for action in character.get("actions", []):
                        characters[char_name]["actions"].append(action)
        
        # Analyze for patterns in the narrative structure
        for pattern_name, pattern in self.patterns.items():
            match_score = 0
            matching_elements = []
            
            # Look for structural elements in scene titles and descriptions
            for element in pattern.structure:
                for i, (title, description) in enumerate(zip(scene_titles, scene_descriptions)):
                    if (element.lower() in title.lower() or 
                        element.lower() in description.lower()):
                        match_score += 1
                        matching_elements.append({
                            "pattern_element": element,
                            "scene_index": i,
                            "scene_title": title
                        })
                        break
            
            # Calculate how much of the pattern is present
            coverage = match_score / len(pattern.structure)
            
            if coverage > 0.3:  # At least 30% match to be considered relevant
                results["identified_patterns"].append({
                    "pattern": pattern_name,
                    "coverage": coverage,
                    "matching_elements": matching_elements
                })
                
                # Generate recommendations for missing structural elements
                missing_elements = []
                for element in pattern.structure:
                    if not any(me["pattern_element"] == element for me in matching_elements):
                        missing_elements.append(element)
                
                if missing_elements:
                    results["structural_recommendations"].append({
                        "pattern": pattern_name,
                        "missing_elements": missing_elements,
                        "suggestion": f"Consider adding scenes that represent the following elements of the {pattern_name} pattern: {', '.join(missing_elements)}"
                    })
        
        # Analyze characters for archetypal patterns
        for char_name, char_data in characters.items():
            # Convert traits set to list for analysis
            char_traits = list(char_data["traits"])
            
            # Find matching archetypes
            archetype_matches = self.find_archetypes_by_traits(char_traits)
            
            if archetype_matches:
                results["character_archetype_analysis"][char_name] = {
                    "archetypes": [
                        {
                            "archetype": archetype.name,
                            "relevance": score,
                            "matching_traits": [
                                trait for trait in char_traits
                                if any(trait.lower() in t.lower() for t in archetype.typical_traits)
                            ],
                            "potential_traits": [
                                trait for trait in archetype.typical_traits
                                if not any(trait.lower() in t.lower() for t in char_traits)
                            ][:3]  # Suggest up to 3 new traits
                        }
                        for archetype, score in archetype_matches
                        if score > 0.2  # At least 20% match
                    ]
                }
        
        # Generate symbolic opportunities
        main_themes = self._extract_themes(scenes)
        for theme in main_themes:
            symbols = self.generate_symbolic_associations(theme)
            if symbols:
                results["symbolic_opportunities"].append({
                    "theme": theme,
                    "symbols": symbols
                })
        
        return results
    
    def _extract_themes(self, scenes: List[Dict[str, Any]]) -> List[str]:
        """
        Extract potential themes from scenes.
        
        Args:
            scenes: List of scene dictionaries
            
        Returns:
            List of potential themes
        """
        # For simplicity, extract themes from scene descriptions and explicit theme fields
        themes = set()
        
        for scene in scenes:
            if "themes" in scene and isinstance(scene["themes"], list):
                for theme in scene["themes"]:
                    themes.add(theme)
            
            # Extract keywords from description that might indicate themes
            description = scene.get("description", "")
            words = description.lower().split()
            # Filter to only include potential thematic words (nouns, adjectives)
            # This is simplistic; a real implementation would use NLP
            for word in words:
                if len(word) > 4 and word not in {"about", "these", "those", "their", "there", "where", "which"}:
                    themes.add(word)
        
        # Return the most common themes (assumed to be the ones mentioned most often)
        # A real implementation would use more sophisticated thematic analysis
        return list(themes)[:5]


class ArchetypalPatternComponent(ProcessingComponent):
    """
    Component for working with archetypal narrative patterns.
    """
    
    def __init__(self, name: str = "ArchetypalPatternComponent", **config_options):
        """
        Initialize the archetypal pattern component.
        
        Args:
            name: Component name
            **config_options: Component configuration options
        """
        super().__init__(name, **config_options)
        self.framework = ArchetypalFramework()
    
    def _initialize_state(self) -> Dict[str, Any]:
        """
        Initialize the component's state.
        
        Returns:
            Initial state dictionary
        """
        return {
            "selected_pattern": None,
            "pattern_variations": [],
            "structure_mapping": {}
        }
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the input data to apply archetypal patterns.
        
        Args:
            input_data: Input data including 'narrative_elements' and 'target_pattern'
            
        Returns:
            Processed data with archetypal pattern analysis and recommendations
        """
        # Extract the target pattern if specified
        target_pattern_name = input_data.get("target_pattern")
        narrative_elements = input_data.get("narrative_elements", {})
        
        # Initialize the output data structure
        output_data = {
            "original_elements": narrative_elements,
            "pattern_analysis": {},
            "recommendations": [],
            "structured_outline": []
        }
        
        # If a specific pattern is targeted, focus on that
        if target_pattern_name:
            pattern = self.framework.get_pattern(target_pattern_name)
            if pattern:
                # Update the component state
                self.state["selected_pattern"] = pattern.name
                self.state["pattern_variations"] = pattern.variations
                
                # Map the narrative elements to the pattern structure
                structure_mapping = self._map_to_pattern_structure(
                    narrative_elements.get("scenes", []),
                    pattern.structure
                )
                self.state["structure_mapping"] = structure_mapping
                
                # Add pattern analysis to output
                output_data["pattern_analysis"] = {
                    "pattern": pattern.name,
                    "structure": pattern.structure,
                    "mapped_elements": structure_mapping,
                    "coverage": len([v for v in structure_mapping.values() if v]) / len(pattern.structure)
                }
                
                # Generate recommendations for unmapped elements
                unmapped_elements = [
                    element for element in pattern.structure 
                    if not structure_mapping.get(element)
                ]
                
                if unmapped_elements:
                    output_data["recommendations"].append({
                        "type": "missing_elements",
                        "message": "Consider adding the following structural elements to complete the pattern",
                        "elements": unmapped_elements
                    })
                
                # Generate a structured outline based on the pattern
                output_data["structured_outline"] = self._generate_structured_outline(
                    pattern, structure_mapping, narrative_elements.get("scenes", [])
                )
            else:
                output_data["recommendations"].append({
                    "type": "pattern_not_found",
                    "message": f"Pattern '{target_pattern_name}' not found. Available patterns: {', '.join(self.framework.patterns.keys())}"
                })
        else:
            # If no specific pattern is targeted, analyze the narrative for patterns
            scenes = narrative_elements.get("scenes", [])
            if scenes:
                analysis = self.framework.analyze_narrative_structure(scenes)
                output_data["pattern_analysis"] = analysis["identified_patterns"]
                output_data["recommendations"] = analysis["structural_recommendations"]
                
                # If patterns were identified, use the strongest match for structured outline
                if analysis["identified_patterns"]:
                    best_match = max(analysis["identified_patterns"], key=lambda p: p["coverage"])
                    pattern = self.framework.get_pattern(best_match["pattern"])
                    if pattern:
                        # Convert matching_elements to structure_mapping format
                        structure_mapping = {
                            element["pattern_element"]: element["scene_index"]
                            for element in best_match["matching_elements"]
                        }
                        self.state["structure_mapping"] = structure_mapping
                        
                        output_data["structured_outline"] = self._generate_structured_outline(
                            pattern, structure_mapping, scenes
                        )
            else:
                output_data["recommendations"].append({
                    "type": "insufficient_data",
                    "message": "Insufficient narrative elements to analyze. Please provide scenes or select a specific pattern."
                })
        
        return output_data
    
    def _map_to_pattern_structure(self, scenes: List[Dict[str, Any]], structure: List[str]) -> Dict[str, int]:
        """
        Map scenes to pattern structure elements.
        
        Args:
            scenes: List of scene dictionaries
            structure: List of structural elements from the pattern
            
        Returns:
            Mapping of structure elements to scene indices or None if no match
        """
        mapping = {}
        
        for element in structure:
            best_match = None
            best_score = 0
            
            for i, scene in enumerate(scenes):
                score = 0
                
                # Check title for matches
                if "title" in scene and element.lower() in scene["title"].lower():
                    score += 2
                
                # Check description for matches
                if "description" in scene and element.lower() in scene["description"].lower():
                    score += 1
                
                # Check themes for matches
                if "themes" in scene and isinstance(scene["themes"], list):
                    if any(element.lower() in theme.lower() for theme in scene["themes"]):
                        score += 1
                
                if score > best_score:
                    best_score = score
                    best_match = i
            
            # Only map if we found a reasonable match
            mapping[element] = best_match if best_score > 0 else None
        
        return mapping
    
    def _generate_structured_outline(
        self, pattern: ArchetypalPattern, 
        structure_mapping: Dict[str, int], 
        scenes: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Generate a structured outline based on the pattern and mapping.
        
        Args:
            pattern: Archetypal pattern
            structure_mapping: Mapping of structure elements to scene indices
            scenes: List of scene dictionaries
            
        Returns:
            List of structured outline elements
        """
        outline = []
        
        for element in pattern.structure:
            scene_index = structure_mapping.get(element)
            
            if scene_index is not None and 0 <= scene_index < len(scenes):
                # Use the existing scene
                scene = scenes[scene_index]
                outline.append({
                    "element": element,
                    "title": scene.get("title", f"Scene for {element}"),
                    "description": scene.get("description", ""),
                    "status": "existing",
                    "scene_index": scene_index
                })
            else:
                # Create a placeholder for the missing element
                outline.append({
                    "element": element,
                    "title": f"[Needed: {element}]",
                    "description": f"This structural element ({element}) is missing from the current narrative.",
                    "status": "missing",
                    "scene_index": None
                })
        
        return outline


class CharacterArchetypeComponent(ProcessingComponent):
    """
    Component for working with character archetypes.
    """
    
    def __init__(self, name: str = "CharacterArchetypeComponent", **config_options):
        """
        Initialize the character archetype component.
        
        Args:
            name: Component name
            **config_options: Component configuration options
        """
        super().__init__(name, **config_options)
        self.framework = ArchetypalFramework()
    
    def _initialize_state(self) -> Dict[str, Any]:
        """
        Initialize the component's state.
        
        Returns:
            Initial state dictionary
        """
        return {
            "character_archetypes": {},
            "relationship_dynamics": [],
            "character_development_tracking": {}
        }
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the input data to apply character archetypes.
        
        Args:
            input_data: Input data including 'characters' and 'target_archetypes'
            
        Returns:
            Processed data with character archetype analysis and recommendations
        """
        characters = input_data.get("characters", [])
        target_archetypes = input_data.get("target_archetypes", {})
        
        # Initialize the output data structure
        output_data = {
            "original_characters": characters,
            "archetype_analysis": {},
            "recommendations": [],
            "enhanced_characters": []
        }
        
        # Process each character
        for character in characters:
            char_name = character.get("name", "")
            if not char_name:
                continue
            
            # Get target archetype for this character if specified
            target_archetype_name = target_archetypes.get(char_name)
            char_traits = character.get("traits", [])
            
            # If a specific archetype is targeted for this character
            if target_archetype_name:
                archetype = self.framework.get_character_archetype(target_archetype_name)
                if archetype:
                    # Analyze how well the character fits the archetype
                    matching_traits = [
                        trait for trait in char_traits
                        if any(trait.lower() in t.lower() for t in archetype.typical_traits)
                    ]
                    
                    missing_traits = [
                        trait for trait in archetype.typical_traits
                        if not any(trait.lower() in t.lower() for t in char_traits)
                    ]
                    
                    # Update the component state
                    self.state["character_archetypes"][char_name] = target_archetype_name
                    
                    # Add archetype analysis to output
                    output_data["archetype_analysis"][char_name] = {
                        "archetype": archetype.name,
                        "matching_traits": matching_traits,
                        "missing_traits": missing_traits,
                        "narrative_functions": archetype.functions,
                        "shadow_aspects": archetype.shadow_aspects,
                        "variations": archetype.variations
                    }
                    
                    # Generate recommendations for character development
                    if missing_traits:
                        output_data["recommendations"].append({
                            "type": "character_traits",
                            "character": char_name,
                            "message": f"Consider adding some of these traits to strengthen {char_name}'s {archetype.name} archetype",
                            "suggested_traits": missing_traits[:3]  # Suggest up to 3 traits
                        })
                    
                    # Add shadow aspect recommendations for character depth
                    output_data["recommendations"].append({
                        "type": "character_depth",
                        "character": char_name,
                        "message": f"To add depth to {char_name}, consider incorporating these shadow aspects of the {archetype.name} archetype",
                        "shadow_aspects": archetype.shadow_aspects
                    })
                    
                    # Create enhanced version of the character
                    enhanced_char = character.copy()
                    enhanced_char["archetype"] = archetype.name
                    enhanced_char["functions"] = archetype.functions
                    enhanced_char["suggested_traits"] = missing_traits[:3]
                    enhanced_char["shadow_aspects"] = archetype.shadow_aspects
                    
                    output_data["enhanced_characters"].append(enhanced_char)
                else:
                    output_data["recommendations"].append({
                        "type": "archetype_not_found",
                        "character": char_name,
                        "message": f"Archetype '{target_archetype_name}' not found for character {char_name}. Available archetypes: {', '.join(self.framework.character_archetypes.keys())}"
                    })
                    
                    # Still include the original character
                    output_data["enhanced_characters"].append(character)
            else:
                # If no specific archetype is targeted, analyze the character for possible matches
                if char_traits:
                    archetype_matches = self.framework.find_archetypes_by_traits(char_traits)
                    
                    if archetype_matches:
                        # Get the best matching archetype
                        best_match, score = archetype_matches[0]
                        
                        # Update the component state
                        self.state["character_archetypes"][char_name] = best_match.name
                        
                        # Add archetype analysis to output
                        output_data["archetype_analysis"][char_name] = {
                            "archetype": best_match.name,
                            "match_score": score,
                            "matching_traits": [
                                trait for trait in char_traits
                                if any(trait.lower() in t.lower() for t in best_match.typical_traits)
                            ],
                            "other_potential_archetypes": [
                                {
                                    "archetype": archetype.name,
                                    "score": s
                                }
                                for archetype, s in archetype_matches[1:3]  # Next 2 best matches
                            ] if len(archetype_matches) > 1 else []
                        }
                        
                        # Create enhanced version of the character
                        enhanced_char = character.copy()
                        enhanced_char["archetype"] = best_match.name
                        enhanced_char["functions"] = best_match.functions
                        enhanced_char["match_score"] = score
                        
                        # Suggest additional traits
                        suggested_traits = [
                            trait for trait in best_match.typical_traits
                            if not any(trait.lower() in t.lower() for t in char_traits)
                        ]
                        enhanced_char["suggested_traits"] = suggested_traits[:3]
                        
                        output_data["enhanced_characters"].append(enhanced_char)
                    else:
                        # No good archetype matches found
                        output_data["recommendations"].append({
                            "type": "no_archetype_match",
                            "character": char_name,
                            "message": f"No clear archetype match found for {char_name}. Consider reviewing traits or manually assigning an archetype."
                        })
                        
                        # Still include the original character
                        output_data["enhanced_characters"].append(character)
                else:
                    # Not enough traits to match
                    output_data["recommendations"].append({
                        "type": "insufficient_traits",
                        "character": char_name,
                        "message": f"Not enough traits defined for {char_name} to match an archetype. Add more traits for better analysis."
                    })
                    
                    # Still include the original character
                    output_data["enhanced_characters"].append(character)
        
        # Check for missing archetypal dynamics
        self._check_for_missing_archetypes(output_data)
        
        return output_data
    
    def _check_for_missing_archetypes(self, output_data: Dict[str, Any]) -> None:
        """
        Check if any important archetypal roles are missing from the cast.
        
        Args:
            output_data: The output data to update with recommendations
        """
        present_archetypes = set()
        for character_analysis in output_data["archetype_analysis"].values():
            present_archetypes.add(character_analysis.get("archetype", ""))
        
        # Important archetypes to check for
        key_archetypes = ["Hero", "Mentor", "Shadow", "Threshold Guardian", "Trickster"]
        missing_archetypes = [a for a in key_archetypes if a not in present_archetypes]
        
        if missing_archetypes:
            output_data["recommendations"].append({
                "type": "missing_archetypes",
                "message": "Consider adding characters with these archetypal roles for a more complete narrative",
                "missing_archetypes": missing_archetypes
            })


class SymbolicSystemComponent(ProcessingComponent):
    """
    Component for working with symbolic systems in narratives.
    """
    
    def __init__(self, name: str = "SymbolicSystemComponent", **config_options):
        """
        Initialize the symbolic system component.
        
        Args:
            name: Component name
            **config_options: Component configuration options
        """
        super().__init__(name, **config_options)
        self.framework = ArchetypalFramework()
    
    def _initialize_state(self) -> Dict[str, Any]:
        """
        Initialize the component's state.
        
        Returns:
            Initial state dictionary
        """
        return {
            "active_symbolic_systems": [],
            "theme_symbol_mappings": {},
            "symbolic_progressions": []
        }
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the input data to apply symbolic systems.
        
        Args:
            input_data: Input data including 'themes', 'scenes', and 'target_symbols'
            
        Returns:
            Processed data with symbolic system analysis and recommendations
        """
        themes = input_data.get("themes", [])
        scenes = input_data.get("scenes", [])
        target_symbols = input_data.get("target_symbols", {})
        
        # Initialize the output data structure
        output_data = {
            "original_themes": themes,
            "symbolic_analysis": {},
            "recommendations": [],
            "enhanced_scenes": []
        }
        
        # First, process explicit themes if provided
        if themes:
            # Update active symbolic systems based on themes
            active_systems = set()
            theme_symbols = {}
            
            for theme in themes:
                # Generate symbolic associations for the theme
                symbol_associations = self.framework.generate_symbolic_associations(theme)
                
                if symbol_associations:
                    theme_symbols[theme] = symbol_associations
                    
                    # Track which symbolic systems are being used
                    for symbol in symbol_associations:
                        active_systems.add(symbol["system"])
            
            # Update the component state
            self.state["active_symbolic_systems"] = list(active_systems)
            self.state["theme_symbol_mappings"] = theme_symbols
            
            # Add symbolic analysis to output
            output_data["symbolic_analysis"]["theme_symbols"] = theme_symbols
            output_data["symbolic_analysis"]["active_systems"] = list(active_systems)
            
            # Generate recommendations for symbolic integration
            for theme, symbols in theme_symbols.items():
                if symbols:
                    output_data["recommendations"].append({
                        "type": "symbolic_integration",
                        "theme": theme,
                        "message": f"Consider integrating these symbols to reinforce the theme of '{theme}'",
                        "symbols": [
                            {
                                "system": symbol["system"],
                                "category": symbol["category"],
                                "symbol": symbol["symbol"]
                            }
                            for symbol in symbols[:3]  # Top 3 symbols
                        ]
                    })
        
        # Process scenes to enhance with symbolic elements
        if scenes:
            enhanced_scenes = []
            
            for scene in scenes:
                enhanced_scene = scene.copy()
                scene_themes = scene.get("themes", [])
                
                # Start with existing symbols or initialize empty list
                if "symbols" not in enhanced_scene:
                    enhanced_scene["symbols"] = []
                
                # Add symbolic suggestions based on scene themes
                symbolic_suggestions = []
                
                for theme in scene_themes:
                    # Try to find symbols for this theme
                    symbols = self.framework.generate_symbolic_associations(theme)
                    if symbols:
                        for symbol in symbols[:2]:  # Top 2 symbols per theme
                            symbolic_suggestions.append({
                                "theme": theme,
                                "system": symbol["system"],
                                "category": symbol["category"],
                                "symbol": symbol["symbol"],
                                "relevance": symbol["relevance"]
                            })
                
                if symbolic_suggestions:
                    enhanced_scene["symbolic_suggestions"] = symbolic_suggestions
                
                enhanced_scenes.append(enhanced_scene)
            
            output_data["enhanced_scenes"] = enhanced_scenes
            
            # Track symbolic progressions across scenes
            if themes and enhanced_scenes:
                # Pick the primary theme (first in the list)
                if themes:
                    primary_theme = themes[0]
                    # Find symbols for this theme
                    symbols = self.state["theme_symbol_mappings"].get(primary_theme, [])
                    
                    if symbols and len(symbols) > 0:
                        # Get the top symbol
                        top_symbol = symbols[0]
                        
                        # Create a symbolic progression
                        progression = {
                            "theme": primary_theme,
                            "symbol": top_symbol["symbol"],
                            "system": top_symbol["system"],
                            "category": top_symbol["category"],
                            "progression": []
                        }
                        
                        # Design a progression across scenes
                        num_scenes = len(enhanced_scenes)
                        if num_scenes >= 3:
                            # Beginning: Introduction
                            progression["progression"].append({
                                "stage": "Introduction",
                                "scene_index": 0,
                                "description": f"Introduce the {top_symbol['symbol']} symbol subtly, establishing its connection to {primary_theme}"
                            })
                            
                            # Middle: Development
                            middle_index = num_scenes // 2
                            progression["progression"].append({
                                "stage": "Development",
                                "scene_index": middle_index,
                                "description": f"Develop the {top_symbol['symbol']} symbol further, showing its transformation as the theme of {primary_theme} evolves"
                            })
                            
                            # End: Culmination
                            progression["progression"].append({
                                "stage": "Culmination",
                                "scene_index": num_scenes - 1,
                                "description": f"Bring the {top_symbol['symbol']} symbol to its culmination, representing the resolution of the {primary_theme} theme"
                            })
                            
                            # Add to state and output
                            self.state["symbolic_progressions"].append(progression)
                            output_data["symbolic_analysis"]["symbolic_progression"] = progression
        
        return output_data


# Create a global instance of the archetypal framework
archetypal_framework = ArchetypalFramework()

# Ensure default archetypal files exist
archetypal_framework.create_default_files()
