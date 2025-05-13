"""
Plotline Management Component for AI Writers Workshop

Handles plotline creation, development, and management for narrative structures.
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

class PlotlineManager:
    """Manages plotline creation, development, and analysis."""
    
    def __init__(self, project_manager, pattern_manager, base_dir: Union[str, Path] = "output"):
        """
        Initialize the plotline manager.
        
        Args:
            project_manager: ProjectManager instance for project interactions
            pattern_manager: PatternManager instance for pattern access
            base_dir: Base directory for all outputs
        """
        self.base_dir = Path(base_dir)
        self.project_manager = project_manager
        self.pattern_manager = pattern_manager
        
        # Set up library directory for plotlines
        self.plotlines_dir = self.base_dir / "library" / "plotlines"
        self.plotlines_dir.mkdir(exist_ok=True, parents=True)
        
        # Legacy directory for backward compatibility
        self.legacy_plotlines_dir = self.base_dir / "plotlines"
        self.legacy_plotlines_dir.mkdir(exist_ok=True, parents=True)
        
        # Load default plotlines
        self.plotlines = self._load_default_plotlines()
    
    def _load_default_plotlines(self) -> Dict[str, Dict[str, Any]]:
        """Load default narrative plotlines."""
        plotlines = {
            "man_vs_nature": {
                "name": "Man vs. Nature",
                "description": "A character or group struggles against natural forces.",
                "elements": [
                    "Powerful natural force (storms, wilderness, disaster)",
                    "Character with special skills or knowledge",
                    "Survival challenge",
                    "Psychological impact of isolation or danger"
                ],
                "examples": ["The Old Man and the Sea", "Cast Away", "Into the Wild"]
            },
            "man_vs_self": {
                "name": "Man vs. Self",
                "description": "A character struggles with their own internal conflicts, desires, or limitations.",
                "elements": [
                    "Internal conflict or psychological challenge",
                    "Self-destructive behavior",
                    "Moment of truth or clarity",
                    "Growth or acceptance"
                ],
                "examples": ["Hamlet", "The Bell Jar", "A Beautiful Mind"]
            },
            "man_vs_man": {
                "name": "Man vs. Man",
                "description": "A character is in direct conflict with another person or group.",
                "elements": [
                    "Protagonist with clear goals",
                    "Antagonist with opposing goals",
                    "Escalating confrontations",
                    "Final confrontation"
                ],
                "examples": ["Sherlock Holmes stories", "The Count of Monte Cristo", "Harry Potter series"]
            },
            "man_vs_society": {
                "name": "Man vs. Society",
                "description": "A character struggles against social norms, institutions, or cultural expectations.",
                "elements": [
                    "Restrictive social order or norm",
                    "Character who questions or challenges",
                    "Attempts at reform or rebellion",
                    "Consequences of challenging the status quo"
                ],
                "examples": ["1984", "The Handmaid's Tale", "The Hunger Games"]
            },
            "man_vs_technology": {
                "name": "Man vs. Technology",
                "description": "A character struggles with artificial intelligence, machines, or technological systems.",
                "elements": [
                    "Advanced technology with capabilities beyond human control",
                    "Initial benefits of technology",
                    "Unintended consequences",
                    "Ethical dilemmas regarding human vs. machine value"
                ],
                "examples": ["Frankenstein", "2001: A Space Odyssey", "The Matrix"]
            },
            "man_vs_fate": {
                "name": "Man vs. Fate",
                "description": "A character struggles against destiny or predetermined events.",
                "elements": [
                    "Prophecy or inevitability",
                    "Character's attempts to defy destiny",
                    "Signs and omens",
                    "Acceptance or transcendence"
                ],
                "examples": ["Oedipus Rex", "Macbeth", "Slaughterhouse-Five"]
            },
            "quest": {
                "name": "Quest",
                "description": "Characters journey to find an object, place, or person of significance.",
                "elements": [
                    "Clear objective or goal",
                    "Journey across challenging terrain (physical or metaphorical)",
                    "Tests and challenges that develop character",
                    "Transformation through the journey"
                ],
                "examples": ["The Lord of the Rings", "The Odyssey", "Star Wars"]
            },
            "revenge": {
                "name": "Revenge",
                "description": "A character seeks retribution for a perceived wrong.",
                "elements": [
                    "Initial harm or injustice",
                    "Planning and preparation",
                    "Moral ambiguity as revenge progresses",
                    "Price of vengeance"
                ],
                "examples": ["The Count of Monte Cristo", "Hamlet", "Kill Bill"]
            },
            "tragedy": {
                "name": "Tragedy",
                "description": "A character's flaws or choices lead to their downfall.",
                "elements": [
                    "Character with a fatal flaw",
                    "Rise in fortune or status",
                    "Critical error in judgment",
                    "Downfall and realization"
                ],
                "examples": ["Romeo and Juliet", "Macbeth", "The Great Gatsby"]
            },
            "rebirth": {
                "name": "Rebirth",
                "description": "A character undergoes a transformation and begins a new life.",
                "elements": [
                    "Character trapped in negative circumstances",
                    "Threat or crisis that forces change",
                    "Intervention or assistance from outside",
                    "Redemption and renewal"
                ],
                "examples": ["A Christmas Carol", "Beauty and the Beast", "The Shawshank Redemption"]
            }
        }
        
        # Save default plotlines to library
        for plotline_id, plotline_data in plotlines.items():
            plotline_path = self.plotlines_dir / f"{plotline_id}.json"
            if not plotline_path.exists():
                with open(plotline_path, "w") as f:
                    json.dump(plotline_data, f, indent=2)
        
        return plotlines
    
    def list_plotlines(self) -> Dict[str, Dict[str, str]]:
        """
        List all available narrative plotlines.
        
        Returns:
            Dictionary with list of plotlines and basic information
        """
        plotlines_summary = {}
        
        # List plotlines from library directory
        for plotline_path in self.plotlines_dir.glob("*.json"):
            with open(plotline_path, "r") as f:
                plotline_data = json.load(f)
            
            plotline_id = plotline_path.stem
            plotlines_summary[plotline_id] = {
                "name": plotline_data.get("name", plotline_id),
                "description": plotline_data.get("description", "No description available")
            }
        
        # If no plotlines found in library, use default ones
        if not plotlines_summary:
            for plotline_id, plotline_data in self.plotlines.items():
                plotlines_summary[plotline_id] = {
                    "name": plotline_data.get("name", plotline_id),
                    "description": plotline_data.get("description", "No description available")
                }
        
        return {"plotlines": plotlines_summary}
    
    def get_plotline_details(self, plotline_name: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific narrative plotline.
        
        Args:
            plotline_name: Name of the plotline (e.g., "man_vs_nature", "quest")
            
        Returns:
            Dictionary with detailed plotline information
        """
        # Check library directory first
        plotline_path = self.plotlines_dir / f"{plotline_name.lower()}.json"
        
        if plotline_path.exists():
            with open(plotline_path, "r") as f:
                plotline_data = json.load(f)
            return {"plotline": plotline_data}
        
        # Then check default plotlines
        if plotline_name.lower() in self.plotlines:
            return {"plotline": self.plotlines[plotline_name.lower()]}
        
        # If not found, return error
        return {
            "error": f"Plotline '{plotline_name}' not found",
            "available_plotlines": list(self.plotlines.keys())
        }
    
    def create_custom_plotline(self, name: str, description: str, elements: List[str],
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
        # If based on existing plotline, get its details
        if based_on:
            base_plotline = self.get_plotline_details(based_on)
            if "error" in base_plotline:
                return base_plotline
            
            # Start with base plotline and override
            plotline_data = base_plotline["plotline"].copy()
            plotline_data["name"] = name
            plotline_data["description"] = description
            plotline_data["elements"] = elements
            if examples:
                plotline_data["examples"] = examples
        else:
            # Create new plotline from scratch
            plotline_data = {
                "name": name,
                "description": description,
                "elements": elements,
                "examples": examples or []
            }
        
        # Add creation timestamp
        plotline_data["created_at"] = datetime.now().isoformat()
        
        # Save to library
        plotline_id = name.lower().replace(" ", "_").replace("-", "_")
        plotline_path = self.plotlines_dir / f"{plotline_id}.json"
        
        with open(plotline_path, "w") as f:
            json.dump(plotline_data, f, indent=2)
        
        # Update internal dictionary
        self.plotlines[plotline_id] = plotline_data
        
        return {
            "plotline": plotline_data,
            "output_path": f"library/plotlines/{plotline_id}.json"
        }
    
    def develop_plotline(self, title: str, plotline: str, pattern: str,
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
        # Get the plotline details
        plotline_details = self.get_plotline_details(plotline)
        if "error" in plotline_details:
            return plotline_details
        
        # Get the pattern details
        pattern_details = self.pattern_manager.get_pattern_details(pattern)
        if "error" in pattern_details:
            return pattern_details
        
        plotline_info = plotline_details["plotline"]
        pattern_info = pattern_details["pattern"]
        
        # Create plot points based on pattern stages
        plot_points = []
        for i, stage in enumerate(pattern_info["stages"]):
            plot_points.append({
                "stage": i + 1,
                "pattern_element": stage,
                "plot_point": f"Plot point for {stage}",
                "narrative_significance": f"How this advances the {plotline} plotline",
                "characters_involved": characters or ["Character A", "Character B"]
            })
        
        developed_plotline = {
            "title": title,
            "base_plotline": plotline,
            "pattern": pattern,
            "elements": plotline_info.get("elements", []),
            "plot_points": plot_points,
            "themes": [
                f"Theme derived from {plotline} plotline",
                f"Theme derived from {pattern} pattern"
            ],
            "created_at": datetime.now().isoformat()
        }
        
        # Save to project if specified
        if project_id:
            return self.project_manager.save_element(
                project_id=project_id,
                element_type="plotlines",
                element_data=developed_plotline,
                element_id=f"plotline-{self.project_manager._sanitize_name(title)}"
            )
        else:
            # Save to legacy plotline directory
            sanitized_title = title.lower().replace(" ", "_").replace("-", "_")
            filename = f"plotline-{sanitized_title}.json"
            plotline_path = self.legacy_plotlines_dir / filename
            
            with open(plotline_path, "w") as f:
                json.dump(developed_plotline, f, indent=2)
            
            return {
                **developed_plotline,
                "output_path": f"plotlines/{filename}"
            }
    
    def analyze_plotline(self, plot_points: List[Dict[str, str]], plotline: str,
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
        # Get the plotline details
        plotline_details = self.get_plotline_details(plotline)
        if "error" in plotline_details:
            return plotline_details
        
        plotline_info = plotline_details["plotline"]
        plotline_elements = plotline_info.get("elements", [])
        
        # Analyze how each plot point aligns with the plotline
        analysis = []
        for i, point in enumerate(plot_points):
            # Determine the most relevant plotline element
            relevant_element = plotline_elements[min(i, len(plotline_elements) - 1)]
            
            analysis.append({
                "plot_point": point.get("title", f"Point {i+1}"),
                "description": point.get("description", "No description provided"),
                "relevant_element": relevant_element,
                "alignment": "Strong",  # Placeholder for more sophisticated analysis
                "suggestions": f"How to strengthen this plot point within the {plotline} structure"
            })
        
        # Check for missing plotline elements
        covered_elements = set(item["relevant_element"] for item in analysis)
        missing_elements = [elem for elem in plotline_elements if elem not in covered_elements]
        
        analysis_result = {
            "plotline": plotline,
            "plotline_description": plotline_info.get("description", ""),
            "analysis": analysis,
            "missing_elements": missing_elements,
            "overall_alignment": "Strong" if not missing_elements else "Partial",
            "recommendations": f"Suggestions for better alignment with {plotline} structure",
            "created_at": datetime.now().isoformat()
        }
        
        # Save to project if specified
        if project_id:
            return self.project_manager.save_element(
                project_id=project_id,
                element_type="analyses",
                element_data=analysis_result,
                element_id=f"analysis-{plotline}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            )
        else:
            # Save to legacy analyses directory
            analyses_dir = self.base_dir / "analyses"
            analyses_dir.mkdir(exist_ok=True, parents=True)
            
            filename = f"analysis-{plotline}-{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
            analysis_path = analyses_dir / filename
            
            with open(analysis_path, "w") as f:
                json.dump(analysis_result, f, indent=2)
            
            return {
                **analysis_result,
                "output_path": f"analyses/{filename}"
            }
