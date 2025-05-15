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
        
        # Generate a meaningful outcome based on pattern stage and scene details
        outcome = self._generate_scene_outcome(scene_title, pattern_stage, characters, conflict)
        
        scene_data = {
            "scene_title": scene_title,
            "pattern_stage": pattern_stage,
            "characters": characters,
            "setting": scene_setting,
            "goal": f"The goal of this scene is to demonstrate the '{pattern_stage}' stage",
            "conflict": scene_conflict,
            "outcome": outcome,
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
    
    def write_project_story(self, project_id: str, format: str = "markdown", 
                          include_character_details: bool = True,
                          prose_style: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a complete story narrative based on project elements.
        
        This method goes beyond compile_narrative by generating polished prose
        that connects the scenes and integrates character arcs into a cohesive story.
        
        Args:
            project_id: Project ID to generate story for
            format: Output format ("markdown", "json", "html")
            include_character_details: Whether to include detailed character information
            prose_style: Optional style guide for prose (e.g., "descriptive", "concise", "literary")
            
        Returns:
            Dictionary with complete story and metadata
        """
        # Get project details
        project = self.project_manager.get_project(project_id)
        if "error" in project:
            return project
        
        # Get characters from project
        characters = []
        characters_list = self.project_manager.list_project_elements(project_id, "characters")
        if "error" not in characters_list and "characters" in characters_list:
            for char_info in characters_list["characters"]:
                char_id = char_info["id"]
                char_data = self.project_manager.get_element(project_id, "characters", char_id)
                if "error" not in char_data:
                    characters.append(char_data)
        
        # Get scenes from project
        scenes = []
        scenes_list = self.project_manager.list_project_elements(project_id, "scenes")
        if "error" not in scenes_list and "scenes" in scenes_list:
            for scene_info in scenes_list["scenes"]:
                scene_id = scene_info["id"]
                scene_data = self.project_manager.get_element(project_id, "scenes", scene_id)
                if "error" not in scene_data:
                    scenes.append(scene_data)
        
        # Verify we have scenes
        if not scenes:
            return {
                "error": f"No scenes found in project {project_id}. Create scenes before generating a story.",
                "project_id": project_id,
                "available_elements": self.project_manager.list_project_elements(project_id)
            }
        
        # Use project title or generate one
        story_title = project.get("name", f"Story - Project {project_id}")
        
        # Get project theme/pattern data to enrich the narrative
        project_patterns = []
        if "primary_pattern" in project and project["primary_pattern"]:
            pattern_data = self.pattern_manager.get_pattern_details(project["primary_pattern"])
            if "error" not in pattern_data:
                project_patterns.append(pattern_data["pattern"])
        
        # Sort scenes by logical order if possible (by pattern stage)
        if project_patterns and len(project_patterns) > 0:
            pattern_stages = project_patterns[0].get("stages", [])
            if pattern_stages:
                # Create a dictionary mapping stages to their order in the pattern
                stage_order = {stage: idx for idx, stage in enumerate(pattern_stages)}
                
                # Sort scenes based on their pattern_stage's order in the pattern
                scenes.sort(key=lambda x: stage_order.get(x.get("pattern_stage", ""), float('inf')))
        
        # Generate story sections
        story_sections = []
        
        # Add title and introduction 
        intro_text = f"# {story_title}\n\n"
        
        # Add a story prologue based on project description
        if "description" in project and project["description"]:
            intro_text += f"{project['description']}\n\n"
        
        # Add character introductions if requested
        if include_character_details and characters:
            intro_text += "## Characters\n\n"
            for char in characters:
                char_name = char.get("name", "Unnamed Character")
                intro_text += f"### {char_name}\n\n"
                
                # Add description with fallback to archetype description
                char_desc = char.get("description", "")
                if not char_desc and "archetype" in char:
                    char_desc = f"{char_name} is a character based on the {char.get('archetype', '')} archetype."
                
                intro_text += f"{char_desc}\n\n"
                
                # Add character traits with more detailed formatting
                if "traits" in char and char["traits"]:
                    intro_text += "**Traits:** " + ", ".join(char["traits"]) + "\n\n"
                    
                # Add character shadow aspects if available
                if "shadow_aspect" in char and char["shadow_aspect"]:
                    intro_text += f"**Shadow Aspect:** {char['shadow_aspect']}\n\n"
        
        story_sections.append(intro_text)
        
        # Generate story body with enhanced scene descriptions
        story_sections.append("## Story\n\n")
        
        previous_scene_setting = None
        for i, scene in enumerate(scenes):
            scene_title = scene.get("scene_title", f"Scene {i+1}")
            scene_text = f"### {scene_title}\n\n"
            
            # Enhanced setting description with more detail
            setting = scene.get("setting", "No setting described.")
            if setting != previous_scene_setting:
                scene_text += f"{setting}\n\n"
                previous_scene_setting = setting
            
            # Enhanced character descriptions and interactions
            character_names = scene.get("characters", [])
            scene_characters = []
            for name in character_names:
                matching = [c for c in characters if c.get("name") == name]
                if matching:
                    scene_characters.append(matching[0])
            
            if scene_characters:
                # Add character interactions with more variety
                char_descriptions = []
                for char in scene_characters:
                    traits = char.get("traits", [])
                    if traits:
                        # Use up to three traits for more variety
                        used_traits = traits[:min(3, len(traits))]
                        trait = used_traits[i % len(used_traits)]  # Cycle through traits for variety
                        char_descriptions.append(f"{char.get('name')} displayed their {trait} nature")
                    else:
                        char_descriptions.append(f"{char.get('name')} was present")
                
                if char_descriptions:
                    scene_text += ", ".join(char_descriptions[:-1])
                    if len(char_descriptions) > 1:
                        scene_text += f" and {char_descriptions[-1]}"
                    else:
                        scene_text += char_descriptions[0]
                    scene_text += ".\n\n"
            
            # Enhanced conflict description with pattern context
            conflict = scene.get("conflict", "No conflict described.")
            scene_text += f"{conflict}\n\n"
            
            # Replace placeholder outcome with more meaningful content
            outcome = scene.get("outcome", "")
            if outcome == "The outcome of this scene moves the story forward by..." or not outcome:
                # Generate a meaningful outcome based on pattern stage
                pattern_stage = scene.get("pattern_stage", "")
                if pattern_stage and project_patterns:
                    pattern = project_patterns[0]
                    stages = pattern.get("stages", [])
                    stage_index = -1
                    
                    try:
                        stage_index = stages.index(pattern_stage)
                    except (ValueError, IndexError):
                        pass
                    
                    if stage_index >= 0:
                        # Determine if this is beginning, middle, or end of pattern
                        if stage_index == 0:  # First stage
                            outcome = f"This pivotal moment establishes the {pattern_stage} phase, setting events in motion."
                        elif stage_index == len(stages) - 1:  # Last stage
                            outcome = f"The {pattern_stage} stage reaches its culmination, bringing significant change."
                        else:  # Middle stages
                            next_stage = stages[stage_index + 1]
                            outcome = f"This development completes the {pattern_stage} stage and transitions the narrative toward {next_stage}."
                else:
                    # Generic outcome based on scene position
                    if i == 0:
                        outcome = "This opening scene establishes the core conflict and introduces the key characters."
                    elif i == len(scenes) - 1:
                        outcome = "This final scene resolves the central tensions and brings closure to the narrative arc."
                    else:
                        outcome = f"This scene develops the narrative by intensifying conflicts and deepening character relationships."
            
            scene_text += f"{outcome}\n\n"
            
            story_sections.append(scene_text)
        
        # Add enhanced conclusion with theme resolution
        if len(scenes) > 0:
            conclusion = "## Conclusion\n\n"
            
            # Get thematic elements for conclusion
            themes = project.get("themes", [])
            theme_text = ""
            if themes:
                theme_text = f"The story explores themes of {', '.join(themes)}, "
                theme_text += "ultimately revealing deeper truths about the human condition."
            
            # Character arcs conclusion
            if characters:
                conclusion += "As our story concludes, the characters find themselves transformed by their experiences:\n\n"
                for char in characters:
                    char_name = char.get("name", "Character")
                    archetype = char.get("archetype", "")
                    shadow = char.get("shadow_aspect", "")
                    
                    # Generate meaningful character conclusion based on archetype
                    if archetype == "hero":
                        conclusion += f"- {char_name} overcame their greatest fears and limitations, embracing their role as a true hero while learning to balance ambition with humility.\n"
                    elif archetype == "mentor":
                        conclusion += f"- {char_name} imparted crucial wisdom while also discovering new perspectives, proving that teaching is its own form of learning.\n"
                    elif archetype == "shadow":
                        conclusion += f"- {char_name} embodied the darker potentialities that the other characters confronted, ultimately serving as the catalyst for profound transformation.\n"
                    else:
                        # Generic character conclusion with shadow integration
                        if shadow:
                            conclusion += f"- {char_name} confronted their {shadow} tendencies and emerged with greater self-awareness and purpose.\n"
                        else:
                            conclusion += f"- {char_name} completed a transformative journey, forever changed by the experiences and relationships formed.\n"
                
                conclusion += "\n" + theme_text if theme_text else ""
            else:
                if theme_text:
                    conclusion += theme_text + "\n\n"
                else:
                    conclusion += "The narrative reaches its conclusion, leaving echoes of meaning that resonate beyond the final scene.\n\n"
            
            story_sections.append(conclusion)
        
        # Combine all sections
        story_text = "\n".join(story_sections)
        
        # Apply prose style adjustments if specified
        if prose_style:
            if prose_style.lower() == "descriptive":
                # Add more sensory details and descriptive language
                story_text = story_text.replace("was present", "entered with purpose")
                story_text = story_text.replace("No setting described", "The scene unfolds in a setting rich with possibility")
            elif prose_style.lower() == "concise":
                # Make language more direct and economical
                story_text = story_text.replace("displayed their", "showed")
                story_text = story_text.replace("finds themselves", "becomes")
            elif prose_style.lower() == "literary":
                # Add more metaphorical and poetic language
                story_text = story_text.replace("confronted", "gazed into the abyss of")
                story_text = story_text.replace("overcame", "transcended")
        
        # Format based on requested format
        if format.lower() == "markdown":
            formatted_content = story_text
        elif format.lower() == "html":
            # Improved HTML conversion
            html_content = self._convert_markdown_to_html(story_text, story_title)
            formatted_content = html_content
        else:
            # JSON format with structured content
            formatted_sections = []
            current_section = ""
            section_type = ""
            
            for line in story_text.split("\n"):
                if line.startswith("# "):
                    if current_section:
                        formatted_sections.append({"type": section_type, "content": current_section.strip()})
                    section_type = "title"
                    current_section = line[2:] + "\n"
                elif line.startswith("## "):
                    if current_section:
                        formatted_sections.append({"type": section_type, "content": current_section.strip()})
                    section_type = "section"
                    current_section = line[3:] + "\n"
                elif line.startswith("### "):
                    if current_section:
                        formatted_sections.append({"type": section_type, "content": current_section.strip()})
                    section_type = "subsection"
                    current_section = line[4:] + "\n"
                else:
                    current_section += line + "\n"
            
            if current_section:
                formatted_sections.append({"type": section_type, "content": current_section.strip()})
            
            formatted_content = {
                "title": story_title,
                "sections": formatted_sections
            }
        
        # Create story data
        story_data = {
            "title": story_title,
            "project_id": project_id,
            "format": format,
            "word_count": len(story_text.split()) if isinstance(story_text, str) else 0,
            "character_count": len(characters),
            "scene_count": len(scenes),
            "generated_at": datetime.now().isoformat(),
            "content": formatted_content
        }
        
        # Save to project directory
        project_dir = self.project_manager.projects_dir / project_id
        stories_dir = project_dir / "stories"
        stories_dir.mkdir(exist_ok=True)
        
        # Create a unique filename
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"story-{timestamp}.json"
        story_path = stories_dir / filename
        
        with open(story_path, "w") as f:
            json.dump(story_data, f, indent=2)
        
        # Add to project elements
        self.project_manager.add_project_element(
            project_id=project_id,
            element_type="stories",
            element_id=f"story-{timestamp}",
            element_data=story_data
        )
        
        # Include path information in return data
        return {
            **story_data,
            "output_path": f"projects/{project_id}/stories/{filename}"
        }
    
    def _convert_markdown_to_html(self, markdown_text: str, title: str) -> str:
        """Convert markdown text to properly formatted HTML."""
        # Build proper HTML with better structure
        html_parts = [
            '<!DOCTYPE html>',
            '<html lang="en">',
            '<head>',
            f'    <title>{title}</title>',
            '    <meta charset="UTF-8">',
            '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
            '    <style>',
            '        body { font-family: Georgia, serif; line-height: 1.6; margin: 0; padding: 20px; max-width: 800px; margin: 0 auto; color: #333; }',
            '        h1 { color: #2c3e50; text-align: center; margin-bottom: 1.5em; }',
            '        h2 { color: #3498db; border-bottom: 1px solid #eee; padding-bottom: 10px; margin-top: 1.5em; }',
            '        h3 { color: #2980b9; margin-top: 1.2em; }',
            '        p { margin-bottom: 1em; }',
            '        .character { background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px; }',
            '        .scene { background-color: #f0f7ff; padding: 15px; border-radius: 5px; margin-bottom: 30px; }',
            '        .conclusion { background-color: #f9f0ff; padding: 15px; border-radius: 5px; margin-bottom: 30px; }',
            '        ul { padding-left: 20px; }',
            '        li { margin-bottom: 0.5em; }',
            '        strong { color: #2c3e50; }',
            '    </style>',
            '</head>',
            '<body>'
        ]
        
        # Process the markdown into proper HTML
        in_characters_section = False
        in_story_section = False
        in_conclusion_section = False
        current_div_open = False
        
        for line in markdown_text.split('\n'):
            if line.startswith('# '):
                html_parts.append(f'    <h1>{line[2:]}</h1>')
            elif line.startswith('## '):
                if current_div_open:
                    html_parts.append('    </div>')
                    current_div_open = False
                
                section_title = line[3:]
                html_parts.append(f'    <h2>{section_title}</h2>')
                
                if section_title == 'Characters':
                    in_characters_section = True
                    in_story_section = False
                    in_conclusion_section = False
                elif section_title == 'Story':
                    in_characters_section = False
                    in_story_section = True
                    in_conclusion_section = False
                elif section_title == 'Conclusion':
                    in_characters_section = False
                    in_story_section = False
                    in_conclusion_section = True
            elif line.startswith('### '):
                if current_div_open:
                    html_parts.append('    </div>')
                
                if in_characters_section:
                    html_parts.append(f'    <div class="character">')
                    html_parts.append(f'        <h3>{line[4:]}</h3>')
                elif in_story_section:
                    html_parts.append(f'    <div class="scene">')
                    html_parts.append(f'        <h3>{line[4:]}</h3>')
                elif in_conclusion_section:
                    html_parts.append(f'    <div class="conclusion">')
                    html_parts.append(f'        <h3>{line[4:]}</h3>')
                else:
                    html_parts.append(f'    <h3>{line[4:]}</h3>')
                
                current_div_open = True
            elif line.startswith('**') and line.endswith('**'):
                # Bold text
                html_parts.append(f'        <p><strong>{line[2:-2]}</strong></p>')
            elif line.startswith('- '):
                # List item
                if not any(p.strip().startswith('<ul>') for p in html_parts[-3:]):
                    html_parts.append('        <ul>')
                
                html_parts.append(f'            <li>{line[2:]}</li>')
                
                # Check if next line is not a list item to close the list
                try:
                    next_idx = markdown_text.split('\n').index(line) + 1
                    next_line = markdown_text.split('\n')[next_idx] if next_idx < len(markdown_text.split('\n')) else ""
                    if not next_line.startswith('- '):
                        html_parts.append('        </ul>')
                except:
                    html_parts.append('        </ul>')
            elif line.strip():
                # Regular paragraph
                line = line.replace('**', '<strong>', 1)
                line = line.replace('**', '</strong>', 1) if '**' in line else line
                html_parts.append(f'        <p>{line}</p>')
        
        if current_div_open:
            html_parts.append('    </div>')
        
        html_parts.append('</body>')
        html_parts.append('</html>')
        
        return '\n'.join(html_parts)
    
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
    
    def _generate_scene_outcome(self, scene_title: str, pattern_stage: str, 
                              characters: List[str], conflict: Optional[str] = None) -> str:
        """
        Generate a meaningful outcome for a scene based on its elements.
        
        Args:
            scene_title: Title of the scene
            pattern_stage: The pattern stage this scene represents
            characters: List of character names in the scene
            conflict: Optional conflict description
            
        Returns:
            A string describing the scene outcome
        """
        # Get pattern information if available to add context
        pattern_info = None
        try:
            # Try to determine what pattern this stage belongs to
            patterns = self.pattern_manager.list_patterns()
            for pattern_name, pattern_data in patterns.get("patterns", {}).items():
                if pattern_stage in pattern_data.get("stages", []):
                    pattern_details = self.pattern_manager.get_pattern_details(pattern_name)
                    if "error" not in pattern_details:
                        pattern_info = pattern_details["pattern"]
                        break
        except:
            # If we can't get pattern info, continue without it
            pass
            
        # Common outcome templates
        generic_outcomes = [
            f"Through this confrontation, {'the characters' if len(characters) > 1 else characters[0] if characters else 'the protagonist'} must face difficult truths that reshape their understanding.",
            f"The consequences of this scene reverberate through the narrative, altering relationships and creating new possibilities.",
            f"This pivotal moment forces {'a collective' if len(characters) > 1 else 'an individual'} reckoning with the central tensions of the story.",
            f"The resolution of this conflict marks a significant turning point in the character's journey through the {pattern_stage} stage."
        ]
        
        # Pattern-specific outcomes
        if pattern_info:
            stages = pattern_info.get("stages", [])
            if stages:
                try:
                    stage_index = stages.index(pattern_stage)
                    stage_count = len(stages)
                    
                    # Beginning of pattern
                    if stage_index == 0:
                        return f"This scene establishes the {pattern_stage} phase, setting in motion the transformative journey that will unfold through subsequent stages."
                    # Middle of pattern
                    elif 0 < stage_index < stage_count - 1:
                        next_stage = stages[stage_index + 1]
                        prev_stage = stages[stage_index - 1]
                        return f"Having moved beyond {prev_stage}, this scene solidifies the challenges of {pattern_stage} and begins to foreshadow the coming {next_stage} stage."
                    # End of pattern
                    elif stage_index == stage_count - 1:
                        return f"The {pattern_stage} stage reaches its culmination in this scene, bringing the narrative arc toward resolution and revealing deeper truths."
                except (ValueError, IndexError):
                    pass
        
        # Scene title-based outcomes
        if "awakening" in scene_title.lower():
            return "This awakening moment fundamentally shifts perspective, revealing new dimensions of understanding."
        elif "confrontation" in scene_title.lower():
            return "The confrontation forces a reckoning that cannot be undone, forever altering the trajectory of events."
        elif "sacrifice" in scene_title.lower():
            return f"This sacrifice represents a pivotal choice that demonstrates {'the characters' if len(characters) > 1 else characters[0] if characters else 'the protagonist'}'s true values and priorities."
        elif "transformation" in scene_title.lower():
            return "The transformation in this scene represents both an ending and a beginning, closing one chapter while opening another."
        
        # Character-based outcomes
        if len(characters) == 1:
            return f"Through this experience, {characters[0]} undergoes a significant shift in understanding that will reshape their approach to future challenges."
        elif len(characters) == 2:
            return f"The interaction between {characters[0]} and {characters[1]} fundamentally alters their relationship, creating new dynamics that will echo through the narrative."
        elif len(characters) > 2:
            return f"The collective experience shared by {', '.join(characters[:-1])} and {characters[-1]} creates bonds and divisions that will influence all future interactions."
            
        # Fall back to generic outcomes
        import random
        return random.choice(generic_outcomes)

    def _compile_html(self, title: str, characters: List[Dict[str, Any]], 
                     scenes: List[Dict[str, Any]]) -> str:
        """Compile narrative in HTML format."""
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{ font-family: Georgia, serif; line-height: 1.6; margin: 0; padding: 20px; max-width: 800px; margin: 0 auto; color: #333; }}
        h1 {{ color: #2c3e50; text-align: center; margin-bottom: 1.5em; }}
        h2 {{ color: #3498db; border-bottom: 1px solid #eee; padding-bottom: 10px; margin-top: 1.5em; }}
        h3 {{ color: #2980b9; margin-top: 1.2em; }}
        p {{ margin-bottom: 1em; }}
        .character {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .scene {{ background-color: #f0f7ff; padding: 15px; border-radius: 5px; margin-bottom: 30px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .conclusion {{ background-color: #f9f0ff; padding: 15px; border-radius: 5px; margin-bottom: 30px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .trait {{ display: inline-block; background-color: #e1f5fe; padding: 3px 10px; margin-right: 8px; border-radius: 15px; font-size: 0.9em; }}
        ul {{ padding-left: 20px; }}
        li {{ margin-bottom: 0.5em; }}
        strong {{ color: #2c3e50; }}
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
