"""
Symbolic System Component for AI Writers Workshop

Handles symbolic connections and thematic resonance.
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

class SymbolicManager:
    """Manages symbolic connections and thematic resonance."""
    
    def __init__(self, project_manager, base_dir: Union[str, Path] = "output"):
        """
        Initialize the symbolic manager.
        
        Args:
            project_manager: ProjectManager instance for project interactions
            base_dir: Base directory for all outputs
        """
        self.base_dir = Path(base_dir)
        self.project_manager = project_manager
        
        # Set up library directory for symbols
        self.symbols_dir = self.base_dir / "library" / "symbols"
        self.symbols_dir.mkdir(exist_ok=True, parents=True)
        
        # Ensure legacy directory exists for backward compatibility
        self.legacy_symbols_dir = self.base_dir / "symbols"
        self.legacy_symbols_dir.mkdir(exist_ok=True, parents=True)
        
        # Load default symbol systems
        self.symbol_systems = self._load_default_symbol_systems()
    
    def _load_default_symbol_systems(self) -> Dict[str, List[Dict[str, str]]]:
        """Load default symbolic connections."""
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
            ],
            "knowledge": [
                {"symbol": "Tree", "meaning": "Branching wisdom, deep roots of understanding"},
                {"symbol": "Book", "meaning": "Accumulated wisdom, preserved insights"},
                {"symbol": "Lantern", "meaning": "Illumination in darkness, guided insight"},
                {"symbol": "Owl", "meaning": "Wisdom, perception beyond ordinary sight"}
            ],
            "journey": [
                {"symbol": "Road", "meaning": "Path of life, choices and direction"},
                {"symbol": "River", "meaning": "Flow of time, changing yet constant"},
                {"symbol": "Bridge", "meaning": "Transition, crossing boundaries"},
                {"symbol": "Map", "meaning": "Guidance, overview of possibilities"}
            ]
        }
        
        # Save default symbols to library
        for theme, symbols in symbol_systems.items():
            symbol_path = self.symbols_dir / f"{theme}.json"
            if not symbol_path.exists():
                with open(symbol_path, "w") as f:
                    json.dump({"theme": theme, "symbols": symbols}, f, indent=2)
        
        return symbol_systems
    
    def find_symbolic_connections(self, theme: str, count: int = 3,
                                project_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Find symbolic connections for a theme.
        
        Args:
            theme: Theme to find symbols for
            count: Number of symbols to return
            project_id: Optional project to associate with
            
        Returns:
            Dictionary with symbolic connections
        """
        # Check if theme exists in library first
        symbol_path = self.symbols_dir / f"{theme.lower()}.json"
        
        if symbol_path.exists():
            with open(symbol_path, "r") as f:
                symbol_data = json.load(f)
            symbols = symbol_data.get("symbols", [])[:count]
        elif theme.lower() in self.symbol_systems:
            # Use default symbols if not in library
            symbols = self.symbol_systems[theme.lower()][:count]
        else:
            # Suggest similar themes if exact match not found
            available_themes = list(self.symbol_systems.keys())
            symbols = [{"symbol": "Not found", "meaning": f"Theme '{theme}' not found. Try: {', '.join(available_themes)}"}]
        
        symbol_data = {
            "theme": theme,
            "symbols": symbols,
            "created_at": datetime.now().isoformat()
        }
        
        # Save to project if specified
        if project_id:
            return self.project_manager.save_element(
                project_id=project_id,
                element_type="symbols",
                element_data=symbol_data,
                element_id=f"symbols-{self.project_manager._sanitize_name(theme)}"
            )
        else:
            # Save to legacy symbols directory
            sanitized_theme = theme.lower().replace(" ", "_").replace("-", "_")
            filename = f"symbols-{sanitized_theme}.json"
            symbol_path = self.legacy_symbols_dir / filename
            
            with open(symbol_path, "w") as f:
                json.dump(symbol_data, f, indent=2)
            
            return {
                **symbol_data,
                "output_path": f"symbols/{filename}"
            }
    
    def create_custom_symbols(self, theme: str, symbols: List[Dict[str, str]],
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
        # Validate symbol structure
        for symbol in symbols:
            if not all(key in symbol for key in ["symbol", "meaning"]):
                return {"error": "Each symbol must have 'symbol' and 'meaning' keys"}
        
        symbol_data = {
            "theme": theme,
            "symbols": symbols,
            "created_at": datetime.now().isoformat()
        }
        
        # Save to library
        theme_id = theme.lower().replace(" ", "_").replace("-", "_")
        symbol_path = self.symbols_dir / f"{theme_id}.json"
        
        with open(symbol_path, "w") as f:
            json.dump(symbol_data, f, indent=2)
        
        # Update internal dictionary
        self.symbol_systems[theme_id] = symbols
        
        # Save to project if specified
        if project_id:
            return self.project_manager.save_element(
                project_id=project_id,
                element_type="symbols",
                element_data=symbol_data,
                element_id=f"symbols-{theme_id}"
            )
        
        return {
            **symbol_data,
            "output_path": f"library/symbols/{theme_id}.json"
        }
    
    def apply_symbolic_theme(self, project_id: str, theme: str,
                           element_types: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Apply symbolic theme to project elements.
        
        Args:
            project_id: Project ID to apply theme to
            theme: Theme to apply
            element_types: Optional list of element types to apply theme to
            
        Returns:
            Dictionary with application results
        """
        # Get project details
        project = self.project_manager.get_project(project_id)
        if "error" in project:
            return project
        
        # Get symbol data
        symbols_data = self.find_symbolic_connections(theme)
        if "error" in symbols_data:
            return symbols_data
        
        symbols = symbols_data.get("symbols", [])
        
        if not symbols:
            return {"error": f"No symbols found for theme '{theme}'"}
        
        # Default to all elements if not specified
        if not element_types:
            element_types = ["characters", "scenes", "outlines"]
        
        # Apply symbols to elements
        results = {
            "theme": theme,
            "project": project_id,
            "applied_to": {},
            "symbols_used": symbols
        }
        
        for element_type in element_types:
            elements = self.project_manager.list_project_elements(project_id, element_type)
            if "error" in elements:
                results["applied_to"][element_type] = {"error": elements["error"]}
                continue
            
            elements_list = elements.get(element_type, [])
            if not elements_list:
                results["applied_to"][element_type] = {"count": 0, "reason": "No elements found"}
                continue
            
            # Apply symbols to elements
            applied_count = 0
            for element_info in elements_list:
                element_id = element_info["id"]
                element = self.project_manager.get_element(project_id, element_type, element_id)
                
                if "error" in element:
                    continue
                
                # Add symbolic connections to element
                if "symbolic_themes" not in element:
                    element["symbolic_themes"] = {}
                
                element["symbolic_themes"][theme] = symbols
                element["modified_at"] = datetime.now().isoformat()
                
                # Save updated element
                self.project_manager.save_element(
                    project_id=project_id,
                    element_type=element_type,
                    element_data=element,
                    element_id=element_id
                )
                
                applied_count += 1
            
            results["applied_to"][element_type] = {"count": applied_count}
        
        # Save theme to project metadata
        project_data = self.project_manager.get_project(project_id)
        if "themes" not in project_data:
            project_data["themes"] = []
        
        if theme not in project_data["themes"]:
            project_data["themes"].append(theme)
        
        self.project_manager.update_project(project_id, {"themes": project_data["themes"]})
        
        return results
