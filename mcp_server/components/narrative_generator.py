"""
Narrative Generation Component for AI Writers Workshop

Handles scene generation, story outlines, and narrative compilation.
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

class NarrativeGenerator:
    """Manages scene generation, story outlines, and narrative compilation."""
    
    def __init__(self, project_manager, pattern_manager, base_dir: Union[str, Path] = "output"):
        """
        Initialize the narrative generator.
        
        Args:
            project_manager: ProjectManager instance for project interactions
            pattern_manager: PatternManager instance for pattern access
            base_dir: Base directory for all outputs
        """
        self.base_dir = Path(base_dir)
        self.project_manager = project_manager
        self.pattern_manager = pattern_manager
        
        # Ensure legacy directories exist for backward compatibility
        self.scenes_dir = self.base_dir / "scenes"
        self.outlines_dir = self.base_dir / "outlines"
        self.scenes_dir.mkdir(exist_ok=True, parents=True)
        self.outlines_dir.mkdir(exist_ok=True, parents=True)
    
    def generate_outline(self, title: str, pattern: str, main_character: Optional[Dict[str, Any]] = None,
                       project_id: Optional[str] = None, custom_sections: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Generate a story outline based on a pattern.
        
        Args:
            title: Story title
            pattern: Narrative pattern to use
            main_character: Optional character information
            project_id: Optional project to associate with
            custom_sections: Optional list of custom outline sections
            
        Returns:
            Dictionary with outline information
        """
        # Get the pattern details
        pattern_details = self.pattern_manager.get_pattern_details(pattern)
        if "error" in pattern_details:
            return pattern_details
        
        pattern_info = pattern_details["pattern"]
        
        # Use custom sections if provided, otherwise generate from pattern
        if custom_sections:
            outline = custom_sections
        else:
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
            "outline": outline,
            "created_at": datetime.now().isoformat()
        }
        
        # Save to project if specified
        if project_id:
            return self.project_manager.save_element(
                project_id=project_id,
                element_type="outlines",
                element_data=outline_data,
                element_id=f"outline-{self.project_manager._sanitize_name(title)}"
            )
        else:
            # Save to legacy outline directory
            sanitized_title = title.lower().replace(" ", "_").replace("-", "_")
            filename = f"outline-{sanitized_title}.json"
            outline_path = self.outlines_dir / filename
            
            with open(outline_path, "w") as f:
                json.dump(outline_data, f, indent=2)
            
            return {
                **outline_data,
                "output_path": f"outlines/{filename}"
            }
    
    def generate_scene(self, scene_title: str, pattern_stage: str, characters: List[str],
                     project_id: Optional[str] = None, setting: Optional[str] = None,
                     conflict: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a scene based on pattern elements.
        
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
        # Use provided setting/conflict or generate defaults
        scene_setting = setting or f"The setting for the '{scene_title}' scene"
        scene_conflict = conflict or f"The conflict in this scene involves {', '.join(characters)}"
        
        scene_data = {
            "scene_title": scene_title,
            "pattern_stage": pattern_stage,
            "characters": characters,
            "setting": scene_setting,
            "goal": f"The goal of this scene is to demonstrate the '{pattern_stage}' stage",
            "conflict": scene_conflict,
            "outcome": f"The outcome of this scene moves the story forward by...",
            "notes": f"This scene is a key moment in the {pattern_stage} stage of the story.",
            "created_at": datetime.now().isoformat()
        }
        
        # Save to project if specified
        if project_id:
            return self.project_manager.save_element(
                project_id=project_id,
                element_type="scenes",
                element_data=scene_data,
                element_id=f"scene-{self.project_manager._sanitize_name(scene_title)}"
            )
        else:
            # Save to legacy scene directory
            sanitized_title = scene_title.lower().replace(" ", "_").replace("-", "_")
            filename = f"scene-{sanitized_title}.json"
            scene_path = self.scenes_dir / filename
            
            with open(scene_path, "w") as f:
                json.dump(scene_data, f, indent=2)
            
            return {
                **scene_data,
                "output_path": f"scenes/{filename}"
            }
    
    def compile_narrative(self, project_id: str, title: Optional[str] = None,
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
        # Get project details
        project = self.project_manager.get_project(project_id)
        if "error" in project:
            return project
        
        # Get scenes from project
        scenes_list = self.project_manager.list_project_elements(project_id, "scenes")
        if "error" in scenes_list:
            return scenes_list
        
        scenes = []
        if "scenes" in scenes_list:
            scene_ids = scenes_list["scenes"]
            
            # If scene_order specified, reorder scenes
            if scene_order:
                ordered_ids = []
                for scene_id in scene_order:
                    matching = [s for s in scene_ids if s["id"] == scene_id]
                    if matching:
                        ordered_ids.extend(matching)
                
                # Add any scenes that weren't in the order list at the end
                remaining = [s for s in scene_ids if s["id"] not in scene_order]
                ordered_ids.extend(remaining)
                scene_ids = ordered_ids
            
            # Get full scene data
            for scene_info in scene_ids:
                scene_id = scene_info["id"]
                scene_data = self.project_manager.get_element(project_id, "scenes", scene_id)
                if "error" not in scene_data:
                    scenes.append(scene_data)
        
        # Get characters if requested
        characters = []
        if include_character_descriptions:
            characters_list = self.project_manager.list_project_elements(project_id, "characters")
            if "characters" in characters_list:
                for char_info in characters_list["characters"]:
                    char_id = char_info["id"]
                    char_data = self.project_manager.get_element(project_id, "characters", char_id)
                    if "error" not in char_data and "arc_stages" not in char_data:  # Skip character arcs
                        characters.append(char_data)
        
        # Use project title if none provided
        narrative_title = title or project.get("name", f"Project {project_id}")
        
        # Compile narrative based on format
        if format.lower() == "markdown":
            narrative_content = self._compile_markdown(narrative_title, characters, scenes)
        elif format.lower() == "html":
            narrative_content = self._compile_html(narrative_title, characters, scenes)
        else:
            # Default to JSON format
            narrative_content = {
                "title": narrative_title,
                "characters": characters,
                "scenes": scenes
            }
        
        # Create compilation data
        compilation = {
            "title": narrative_title,
            "project_id": project_id,
            "format": format,
            "character_count": len(characters),
            "scene_count": len(scenes),
            "compiled_at": datetime.now().isoformat(),
            "content": narrative_content
        }
        
        # Save to project drafts directory
        return self.project_manager.save_element(
            project_id=project_id,
            element_type="drafts",
            element_data=compilation,
            element_id=f"draft-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        )
    
    def _compile_markdown(self, title: str, characters: List[Dict[str, Any]], 
                         scenes: List[Dict[str, Any]]) -> str:
        """Compile narrative in Markdown format."""
        md = f"# {title}\n\n"
        
        # Add character descriptions
        if characters:
            md += "## Characters\n\n"
            for char in characters:
                md += f"### {char.get('name', 'Unnamed Character')}\n\n"
                md += f"{char.get('description', 'No description available.')}\n\n"
                if "traits" in char and char["traits"]:
                    md += "**Traits:** " + ", ".join(char["traits"]) + "\n\n"
        
        # Add scenes
        if scenes:
            md += "## Story\n\n"
            for i, scene in enumerate(scenes):
                md += f"### {i+1}. {scene.get('scene_title', f'Scene {i+1}')}\n\n"
                md += f"**Setting:** {scene.get('setting', 'No setting described.')}\n\n"
                md += f"**Characters:** {', '.join(scene.get('characters', []))}\n\n"
                md += f"**Conflict:** {scene.get('conflict', 'No conflict described.')}\n\n"
                md += f"**Outcome:** {scene.get('outcome', 'No outcome described.')}\n\n"
        
        return md
    
    def _compile_html(self, title: str, characters: List[Dict[str, Any]], 
                     scenes: List[Dict[str, Any]]) -> str:
        """Compile narrative in HTML format."""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; }}
        h1 {{ color: #2c3e50; }}
        h2 {{ color: #3498db; border-bottom: 1px solid #eee; padding-bottom: 10px; }}
        h3 {{ color: #2980b9; }}
        .character {{ margin-bottom: 20px; background-color: #f8f9fa; padding: 15px; border-radius: 5px; }}
        .scene {{ margin-bottom: 30px; background-color: #f0f7ff; padding: 15px; border-radius: 5px; }}
        .trait {{ display: inline-block; background-color: #e1f5fe; padding: 3px 10px; margin-right: 8px; border-radius: 15px; font-size: 0.9em; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
"""
        
        # Add character descriptions
        if characters:
            html += "    <h2>Characters</h2>\n"
            for char in characters:
                html += '    <div class="character">\n'
                html += f'        <h3>{char.get("name", "Unnamed Character")}</h3>\n'
                html += f'        <p>{char.get("description", "No description available.")}</p>\n'
                if "traits" in char and char["traits"]:
                    html += '        <div>\n'
                    for trait in char["traits"]:
                        html += f'            <span class="trait">{trait}</span>\n'
                    html += '        </div>\n'
                html += '    </div>\n'
        
        # Add scenes
        if scenes:
            html += "    <h2>Story</h2>\n"
            for i, scene in enumerate(scenes):
                html += '    <div class="scene">\n'
                html += f'        <h3>{i+1}. {scene.get("scene_title", f"Scene {i+1}")}</h3>\n'
                html += f'        <p><strong>Setting:</strong> {scene.get("setting", "No setting described.")}</p>\n'
                html += f'        <p><strong>Characters:</strong> {", ".join(scene.get("characters", []))}</p>\n'
                html += f'        <p><strong>Conflict:</strong> {scene.get("conflict", "No conflict described.")}</p>\n'
                html += f'        <p><strong>Outcome:</strong> {scene.get("outcome", "No outcome described.")}</p>\n'
                html += '    </div>\n'
        
        html += """</body>
</html>"""
        
        return html
