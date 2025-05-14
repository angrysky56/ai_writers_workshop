"""
AI Writers Workshop - Prompts Module

This module implements reusable prompt templates for the AI Writers Workshop MCP server.
Prompts are user-controlled templates that can be discovered and selected by clients.
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional, Union
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ai_writers_workshop.prompts")

# Store registered prompts
REGISTERED_PROMPTS: Dict[str, Dict[str, Any]] = {}

def register_prompt(
    name: str,
    description: str,
    arguments: Optional[List[Dict[str, Any]]] = None,
    template_func=None
):
    """
    Register a prompt template with the prompts module.
    
    Args:
        name: Unique identifier for the prompt
        description: Human-readable description
        arguments: Optional list of arguments with name, description, and required flags
        template_func: Function that generates the prompt content
    """
    if name in REGISTERED_PROMPTS:
        logger.warning(f"Overwriting existing prompt: {name}")
    
    REGISTERED_PROMPTS[name] = {
        "name": name,
        "description": description,
        "arguments": arguments or [],
        "template_func": template_func
    }
    
    logger.info(f"Registered prompt: {name}")
    return template_func

def get_prompt_schema(name: str) -> Dict[str, Any]:
    """
    Get the schema for a registered prompt (without the template function).
    
    Args:
        name: Prompt name
        
    Returns:
        Prompt schema
    """
    if name not in REGISTERED_PROMPTS:
        raise ValueError(f"Prompt not found: {name}")
    
    prompt = REGISTERED_PROMPTS[name].copy()
    prompt.pop("template_func", None)  # Remove the function, not needed in schema
    return prompt

def get_all_prompts() -> List[Dict[str, Any]]:
    """
    Get schemas for all registered prompts.
    
    Returns:
        List of prompt schemas
    """
    return [get_prompt_schema(name) for name in REGISTERED_PROMPTS]

def generate_prompt_content(name: str, arguments: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Generate the content for a prompt based on the provided arguments.
    
    Args:
        name: Prompt name
        arguments: Arguments to pass to the template function
        
    Returns:
        Generated prompt content
    """
    if name not in REGISTERED_PROMPTS:
        raise ValueError(f"Prompt not found: {name}")
    
    prompt = REGISTERED_PROMPTS[name]
    template_func = prompt["template_func"]
    
    if template_func is None:
        raise ValueError(f"Prompt {name} has no template function")
    
    arguments = arguments or {}
    
    # Validate required arguments
    for arg in prompt["arguments"]:
        if arg.get("required", False) and arg["name"] not in arguments:
            raise ValueError(f"Missing required argument: {arg['name']}")
    
    # Generate content using the template function
    return template_func(**arguments)

# ---- Register Prompt Templates ----

@register_prompt(
    name="character_creation",
    description="Create a character based on an archetype with enhanced flexibility",
    arguments=[
        {
            "name": "character_name",
            "description": "Name for the character",
            "required": True
        },
        {
            "name": "archetype",
            "description": "Base archetype (e.g., 'hero', 'mentor', 'shadow')",
            "required": True
        },
        {
            "name": "project_id",
            "description": "Optional project to associate with",
            "required": False
        },
        {
            "name": "traits",
            "description": "Comma-separated list of character traits",
            "required": False
        }
    ]
)
def character_creation_prompt(
    character_name: str,
    archetype: str,
    project_id: Optional[str] = None,
    traits: Optional[str] = None
) -> Dict[str, Any]:
    """Character creation prompt template."""
    traits_list = [t.strip() for t in traits.split(",")] if traits else []
    
    project_context = f"for the project '{project_id}'" if project_id else ""
    traits_text = ", ".join(traits_list) if traits_list else "to be determined based on the archetype"
    
    messages = [
        {
            "role": "user",
            "content": {
                "type": "text",
                "text": f"I want to create a character named '{character_name}' based on the '{archetype}' archetype {project_context}. The character should have the following traits: {traits_text}."
            }
        },
        {
            "role": "assistant",
            "content": {
                "type": "text",
                "text": f"I'll help you create the character '{character_name}' as a {archetype} archetype. First, let me get some details about the {archetype} archetype from our system."
            }
        },
        {
            "role": "user",
            "content": {
                "type": "resource",
                "resource": {
                    "uri": f"file://characters/{archetype}",
                    "mimeType": "application/json"
                }
            }
        },
        {
            "role": "assistant",
            "content": {
                "type": "text",
                "text": "Now I can create your character with this archetype information. Let me know if you want to adjust any aspects of the character after I create it."
            }
        }
    ]
    
    return {
        "description": f"Create character '{character_name}' based on the {archetype} archetype",
        "messages": messages
    }

@register_prompt(
    name="scene_generation",
    description="Generate a scene based on pattern elements with enhanced customization",
    arguments=[
        {
            "name": "scene_title",
            "description": "Title of the scene",
            "required": True
        },
        {
            "name": "pattern_name",
            "description": "Name of the narrative pattern to use",
            "required": True
        },
        {
            "name": "pattern_stage",
            "description": "The pattern stage this scene represents",
            "required": True
        },
        {
            "name": "characters",
            "description": "Comma-separated list of characters in the scene",
            "required": True
        },
        {
            "name": "project_id",
            "description": "Optional project to associate with",
            "required": False
        },
        {
            "name": "setting",
            "description": "Description of the scene setting",
            "required": False
        },
        {
            "name": "conflict",
            "description": "Description of the conflict in the scene",
            "required": False
        }
    ]
)
def scene_generation_prompt(
    scene_title: str,
    pattern_name: str,
    pattern_stage: str,
    characters: str,
    project_id: Optional[str] = None,
    setting: Optional[str] = None,
    conflict: Optional[str] = None
) -> Dict[str, Any]:
    """Scene generation prompt template."""
    character_list = [c.strip() for c in characters.split(",")]
    
    project_context = f"for the project '{project_id}'" if project_id else ""
    setting_text = f"set in: {setting}" if setting else "with a setting to be determined"
    conflict_text = f"with conflict: {conflict}" if conflict else "with a conflict to be determined"
    
    messages = [
        {
            "role": "user",
            "content": {
                "type": "text",
                "text": f"I want to generate a scene titled '{scene_title}' {project_context} based on the '{pattern_name}' pattern, specifically the '{pattern_stage}' stage. The scene should include the following characters: {', '.join(character_list)}. The scene should be {setting_text}. {conflict_text}"
            }
        },
        {
            "role": "assistant",
            "content": {
                "type": "text",
                "text": f"I'll help you generate a scene titled '{scene_title}' for the {pattern_stage} stage of the {pattern_name} pattern. First, let me get details about this narrative pattern."
            }
        },
        {
            "role": "user",
            "content": {
                "type": "resource",
                "resource": {
                    "uri": f"file://patterns/{pattern_name}",
                    "mimeType": "application/json"
                }
            }
        },
        {
            "role": "assistant",
            "content": {
                "type": "text",
                "text": "Now I'll create your scene using this pattern information. I'll generate a scene that fits the pattern stage and includes all the specified characters."
            }
        }
    ]
    
    return {
        "description": f"Generate scene '{scene_title}' for {pattern_name} pattern, {pattern_stage} stage",
        "messages": messages
    }

@register_prompt(
    name="story_outline",
    description="Generate a story outline based on a pattern",
    arguments=[
        {
            "name": "title",
            "description": "Story title",
            "required": True
        },
        {
            "name": "pattern",
            "description": "Narrative pattern to use",
            "required": True
        },
        {
            "name": "project_id",
            "description": "Optional project to associate with",
            "required": False
        },
        {
            "name": "theme",
            "description": "Main theme of the story",
            "required": False
        },
        {
            "name": "main_character",
            "description": "Name of the main character",
            "required": False
        }
    ]
)
def story_outline_prompt(
    title: str,
    pattern: str,
    project_id: Optional[str] = None,
    theme: Optional[str] = None,
    main_character: Optional[str] = None
) -> Dict[str, Any]:
    """Story outline prompt template."""
    project_context = f"for the project '{project_id}'" if project_id else ""
    theme_text = f"with the theme of '{theme}'" if theme else "with a theme to be determined"
    character_text = f"featuring {main_character} as the main character" if main_character else "with characters to be determined"
    
    messages = [
        {
            "role": "user",
            "content": {
                "type": "text",
                "text": f"I want to generate an outline for a story titled '{title}' {project_context} based on the '{pattern}' narrative pattern. The story should be {theme_text} and {character_text}."
            }
        },
        {
            "role": "assistant",
            "content": {
                "type": "text",
                "text": f"I'll help you generate an outline for '{title}' using the {pattern} pattern. Let me first get the details of this narrative pattern."
            }
        },
        {
            "role": "user",
            "content": {
                "type": "resource",
                "resource": {
                    "uri": f"file://patterns/{pattern}",
                    "mimeType": "application/json"
                }
            }
        },
        {
            "role": "assistant",
            "content": {
                "type": "text",
                "text": "Now I can create an outline for your story using this pattern structure. I'll generate a complete outline with all the key stages."
            }
        }
    ]
    
    return {
        "description": f"Generate outline for '{title}' based on {pattern} pattern",
        "messages": messages
    }

@register_prompt(
    name="character_arc",
    description="Develop a character arc within a narrative pattern",
    arguments=[
        {
            "name": "character_name",
            "description": "Character name",
            "required": True
        },
        {
            "name": "archetype",
            "description": "Character's archetype",
            "required": True
        },
        {
            "name": "pattern",
            "description": "Narrative pattern to use",
            "required": True
        },
        {
            "name": "project_id",
            "description": "Optional project to associate with",
            "required": False
        }
    ]
)
def character_arc_prompt(
    character_name: str,
    archetype: str,
    pattern: str,
    project_id: Optional[str] = None
) -> Dict[str, Any]:
    """Character arc prompt template."""
    project_context = f"for the project '{project_id}'" if project_id else ""
    
    messages = [
        {
            "role": "user",
            "content": {
                "type": "text",
                "text": f"I want to develop a character arc for '{character_name}', a {archetype} archetype, using the '{pattern}' narrative pattern {project_context}."
            }
        },
        {
            "role": "assistant",
            "content": {
                "type": "text",
                "text": f"I'll help you develop an arc for {character_name} as a {archetype} within the {pattern} pattern. Let me gather information about both the archetype and pattern."
            }
        },
        {
            "role": "user",
            "content": {
                "type": "resource",
                "resource": {
                    "uri": f"file://characters/{archetype}",
                    "mimeType": "application/json"
                }
            }
        },
        {
            "role": "user",
            "content": {
                "type": "resource",
                "resource": {
                    "uri": f"file://patterns/{pattern}",
                    "mimeType": "application/json"
                }
            }
        },
        {
            "role": "assistant",
            "content": {
                "type": "text",
                "text": "Now I can develop a full character arc that integrates both the archetype's characteristics and the pattern's structure."
            }
        }
    ]
    
    return {
        "description": f"Develop arc for '{character_name}' ({archetype}) using {pattern}",
        "messages": messages
    }

@register_prompt(
    name="symbolic_theme",
    description="Find symbolic connections for a theme",
    arguments=[
        {
            "name": "theme",
            "description": "Theme to find symbols for",
            "required": True
        },
        {
            "name": "count",
            "description": "Number of symbols to find",
            "required": False
        },
        {
            "name": "project_id",
            "description": "Optional project to associate with",
            "required": False
        }
    ]
)
def symbolic_theme_prompt(
    theme: str,
    count: Optional[str] = None,
    project_id: Optional[str] = None
) -> Dict[str, Any]:
    """Symbolic theme prompt template."""
    count_num = int(count) if count and count.isdigit() else 3
    project_context = f"for the project '{project_id}'" if project_id else ""
    
    messages = [
        {
            "role": "user",
            "content": {
                "type": "text",
                "text": f"I want to explore symbolic connections for the theme of '{theme}' {project_context}. Please find {count_num} symbols that connect to this theme."
            }
        },
        {
            "role": "assistant",
            "content": {
                "type": "text",
                "text": f"I'll help you find symbolic connections for the theme of '{theme}'. I'll identify {count_num} symbols with their meanings and connections to your theme."
            }
        }
    ]
    
    return {
        "description": f"Find symbolic connections for '{theme}'",
        "messages": messages
    }

@register_prompt(
    name="narrative_analysis",
    description="Analyze a narrative structure using a specific pattern",
    arguments=[
        {
            "name": "pattern_name",
            "description": "Name of the pattern to analyze against",
            "required": True
        },
        {
            "name": "project_id",
            "description": "Project ID to analyze",
            "required": False
        },
        {
            "name": "adherence_level",
            "description": "How strictly to apply the pattern (0.0-1.0)",
            "required": False
        }
    ]
)
def narrative_analysis_prompt(
    pattern_name: str,
    project_id: Optional[str] = None,
    adherence_level: Optional[str] = None
) -> Dict[str, Any]:
    """Narrative analysis prompt template."""
    adherence = float(adherence_level) if adherence_level and adherence_level.replace('.', '', 1).isdigit() else 1.0
    adherence_text = f"with an adherence level of {adherence}" if adherence_level else "with standard adherence"
    
    if project_id:
        content_text = f"I want to analyze the narrative structure of project '{project_id}' against the '{pattern_name}' pattern {adherence_text}."
    else:
        content_text = f"I want to analyze a narrative against the '{pattern_name}' pattern {adherence_text}. I'll provide the scenes to analyze."
    
    messages = [
        {
            "role": "user",
            "content": {
                "type": "text",
                "text": content_text
            }
        },
        {
            "role": "assistant",
            "content": {
                "type": "text",
                "text": f"I'll help you analyze your narrative against the {pattern_name} pattern. First, let me get the details of this pattern."
            }
        },
        {
            "role": "user",
            "content": {
                "type": "resource",
                "resource": {
                    "uri": f"file://patterns/{pattern_name}",
                    "mimeType": "application/json"
                }
            }
        },
        {
            "role": "assistant",
            "content": {
                "type": "text",
                "text": "Now I can analyze your narrative against this pattern. Please provide the scenes you want to analyze, or if you've specified a project ID, I'll retrieve the scenes from that project."
            }
        }
    ]
    
    return {
        "description": f"Analyze narrative using {pattern_name} pattern",
        "messages": messages
    }

@register_prompt(
    name="project_creation",
    description="Create a new writing project with structure",
    arguments=[
        {
            "name": "name",
            "description": "Project name",
            "required": True
        },
        {
            "name": "description",
            "description": "Project description",
            "required": True
        },
        {
            "name": "project_type",
            "description": "Type of project (story, novel, article, script)",
            "required": False
        }
    ]
)
def project_creation_prompt(
    name: str,
    description: str,
    project_type: Optional[str] = None
) -> Dict[str, Any]:
    """Project creation prompt template."""
    type_text = project_type if project_type else "story"
    
    messages = [
        {
            "role": "user",
            "content": {
                "type": "text",
                "text": f"I want to create a new {type_text} project titled '{name}' with the following description: {description}"
            }
        },
        {
            "role": "assistant",
            "content": {
                "type": "text",
                "text": f"I'll help you create a new {type_text} project titled '{name}'. Let me set that up for you."
            }
        }
    ]
    
    return {
        "description": f"Create new {type_text} project '{name}'",
        "messages": messages
    }

# ---- Register Workflow Prompts ----

@register_prompt(
    name="complete_story_workflow",
    description="A complete workflow for creating a story from concept to final scenes",
    arguments=[
        {
            "name": "title",
            "description": "Story title",
            "required": True
        },
        {
            "name": "premise",
            "description": "Basic premise or concept for the story",
            "required": True
        },
        {
            "name": "pattern",
            "description": "Narrative pattern to use",
            "required": True
        },
        {
            "name": "main_character_name",
            "description": "Name of the main character",
            "required": True
        },
        {
            "name": "main_character_archetype",
            "description": "Archetype for the main character",
            "required": True
        }
    ]
)
def complete_story_workflow_prompt(
    title: str,
    premise: str,
    pattern: str,
    main_character_name: str,
    main_character_archetype: str
) -> Dict[str, Any]:
    """Complete story workflow prompt template."""
    messages = [
        {
            "role": "user",
            "content": {
                "type": "text",
                "text": f"I want to create a complete story titled '{title}' with the premise: {premise}. I'd like to use the '{pattern}' narrative pattern with '{main_character_name}' as the main character, based on the '{main_character_archetype}' archetype."
            }
        },
        {
            "role": "assistant",
            "content": {
                "type": "text",
                "text": f"I'll guide you through a complete workflow to create your story '{title}'. We'll follow these steps:\n\n1. Create a new project\n2. Define your main character based on the {main_character_archetype} archetype\n3. Develop a story outline using the {pattern} pattern\n4. Generate key scenes based on the pattern stages\n5. Explore symbolic connections for your themes\n\nLet's start with creating a new project."
            }
        },
        {
            "role": "user",
            "content": {
                "type": "text",
                "text": "Please proceed with the workflow steps."
            }
        },
        {
            "role": "assistant",
            "content": {
                "type": "text",
                "text": "Step 1: Let's create the project."
            }
        },
        {
            "role": "assistant",
            "content": {
                "type": "text",
                "text": "Step 2: Now let's define your main character. First, I need information about the archetype."
            }
        },
        {
            "role": "user",
            "content": {
                "type": "resource",
                "resource": {
                    "uri": f"file://characters/{main_character_archetype}",
                    "mimeType": "application/json"
                }
            }
        },
        {
            "role": "assistant",
            "content": {
                "type": "text",
                "text": "Step 3: Now let's develop a story outline. I need details about the pattern structure."
            }
        },
        {
            "role": "user",
            "content": {
                "type": "resource",
                "resource": {
                    "uri": f"file://patterns/{pattern}",
                    "mimeType": "application/json"
                }
            }
        },
        {
            "role": "assistant",
            "content": {
                "type": "text",
                "text": "Step 4: Now let's generate key scenes for each major stage of the pattern."
            }
        },
        {
            "role": "assistant",
            "content": {
                "type": "text",
                "text": "Step 5: Finally, let's explore symbolic connections for the main themes of your story."
            }
        }
    ]
    
    return {
        "description": f"Complete story workflow for '{title}'",
        "messages": messages
    }

@register_prompt(
    name="character_development_workflow",
    description="A workflow for deeply developing a character from archetype to arc",
    arguments=[
        {
            "name": "character_name",
            "description": "Character name",
            "required": True
        },
        {
            "name": "archetype",
            "description": "Base archetype for the character",
            "required": True
        },
        {
            "name": "project_id",
            "description": "Project to associate with",
            "required": False
        },
        {
            "name": "pattern",
            "description": "Narrative pattern for character arc",
            "required": False
        }
    ]
)
def character_development_workflow_prompt(
    character_name: str,
    archetype: str,
    project_id: Optional[str] = None,
    pattern: Optional[str] = None
) -> Dict[str, Any]:
    """Character development workflow prompt template."""
    project_context = f"for project '{project_id}'" if project_id else ""
    pattern_text = f"using the {pattern} pattern" if pattern else "using an appropriate pattern"
    
    messages = [
        {
            "role": "user",
            "content": {
                "type": "text",
                "text": f"I want to develop a detailed character named '{character_name}' based on the '{archetype}' archetype {project_context}. Please guide me through a complete character development workflow {pattern_text}."
            }
        },
        {
            "role": "assistant",
            "content": {
                "type": "text",
                "text": f"I'll guide you through a comprehensive character development workflow for {character_name}. We'll follow these steps:\n\n1. Understand the {archetype} archetype deeply\n2. Create the basic character\n3. Develop the character's arc {pattern_text}\n4. Explore symbolic connections\n5. Define key scenes for character growth\n\nLet's start with understanding the archetype."
            }
        },
        {
            "role": "user",
            "content": {
                "type": "resource",
                "resource": {
                    "uri": f"file://characters/{archetype}",
                    "mimeType": "application/json"
                }
            }
        },
        {
            "role": "assistant",
            "content": {
                "type": "text",
                "text": "Step 1: Now that we understand the archetype, let's create the basic character."
            }
        },
        {
            "role": "assistant",
            "content": {
                "type": "text",
                "text": "Step 2: Next, let's develop the character's arc. First, I need information about the pattern."
            }
        },
        {
            "role": "user",
            "content": {
                "type": "resource",
                "resource": {
                    "uri": f"file://patterns/{pattern or 'heroes_journey'}",
                    "mimeType": "application/json"
                }
            }
        },
        {
            "role": "assistant",
            "content": {
                "type": "text",
                "text": "Step 3: Now let's explore symbolic connections for this character."
            }
        },
        {
            "role": "assistant",
            "content": {
                "type": "text",
                "text": "Step 4: Finally, let's define key scenes for this character's growth throughout the story."
            }
        }
    ]
    
    return {
        "description": f"Character development workflow for '{character_name}'",
        "messages": messages
    }

@register_prompt(
    name="narrative_analysis_workflow",
    description="A workflow for analyzing, refining, and enhancing a narrative structure",
    arguments=[
        {
            "name": "project_id",
            "description": "Project to analyze",
            "required": True
        },
        {
            "name": "pattern",
            "description": "Narrative pattern to use for analysis",
            "required": True
        }
    ]
)
def narrative_analysis_workflow_prompt(
    project_id: str,
    pattern: str
) -> Dict[str, Any]:
    """Narrative analysis workflow prompt template."""
    messages = [
        {
            "role": "user",
            "content": {
                "type": "text",
                "text": f"I want to analyze and enhance the narrative structure of project '{project_id}' using the '{pattern}' pattern. Please guide me through a complete narrative analysis workflow."
            }
        },
        {
            "role": "assistant",
            "content": {
                "type": "text",
                "text": f"I'll guide you through a complete narrative analysis workflow for project '{project_id}' using the {pattern} pattern. We'll follow these steps:\n\n1. Review the project and pattern structure\n2. Analyze how well the existing narrative aligns with the pattern\n3. Identify gaps and opportunities for enhancement\n4. Suggest specific improvements for each stage\n5. Identify symbolic connections to strengthen\n\nLet's start by reviewing the project and pattern structure."
            }
        },
        {
            "role": "user",
            "content": {
                "type": "resource",
                "resource": {
                    "uri": f"file://patterns/{pattern}",
                    "mimeType": "application/json"
                }
            }
        },
        {
            "role": "assistant",
            "content": {
                "type": "text",
                "text": "Step 1: Now, let's analyze how the existing narrative aligns with this pattern."
            }
        },
        {
            "role": "assistant",
            "content": {
                "type": "text",
                "text": "Step 2: Based on our analysis, I'll identify gaps and opportunities for enhancement."
            }
        },
        {
            "role": "assistant",
            "content": {
                "type": "text",
                "text": "Step 3: Now, let's suggest specific improvements for each stage of the pattern."
            }
        },
        {
            "role": "assistant",
            "content": {
                "type": "text",
                "text": "Step 4: Finally, let's identify symbolic connections that could be strengthened or added to enhance the narrative."
            }
        }
    ]
    
    return {
        "description": f"Narrative analysis workflow for project '{project_id}'",
        "messages": messages
    }

@register_prompt(
    name="symbolic_exploration_workflow",
    description="A workflow for deeply exploring symbolic connections in a story",
    arguments=[
        {
            "name": "theme",
            "description": "Main theme to explore",
            "required": True
        },
        {
            "name": "project_id",
            "description": "Project to associate with",
            "required": False
        },
        {
            "name": "secondary_themes",
            "description": "Comma-separated list of secondary themes",
            "required": False
        }
    ]
)
def symbolic_exploration_workflow_prompt(
    theme: str,
    project_id: Optional[str] = None,
    secondary_themes: Optional[str] = None
) -> Dict[str, Any]:
    """Symbolic exploration workflow prompt template."""
    project_context = f"for project '{project_id}'" if project_id else ""
    secondary_themes_list = [t.strip() for t in secondary_themes.split(",")] if secondary_themes else []
    secondary_themes_text = f" and secondary themes of {', '.join(secondary_themes_list)}" if secondary_themes_list else ""
    
    messages = [
        {
            "role": "user",
            "content": {
                "type": "text",
                "text": f"I want to explore symbolic connections for the main theme of '{theme}'{secondary_themes_text} {project_context}. Please guide me through a complete symbolic exploration workflow."
            }
        },
        {
            "role": "assistant",
            "content": {
                "type": "text",
                "text": f"I'll guide you through a comprehensive symbolic exploration workflow for the theme of '{theme}'{secondary_themes_text}. We'll follow these steps:\n\n1. Explore primary symbolic connections for the main theme\n2. Identify contrasting and complementary symbols\n3. Create a symbolic system connecting all themes\n4. Suggest ways to integrate symbols into narrative elements\n5. Develop a symbolic progression throughout the story\n\nLet's start with exploring primary symbolic connections."
            }
        },
        {
            "role": "assistant",
            "content": {
                "type": "text",
                "text": "Step 1: Let's identify the primary symbolic connections for your main theme."
            }
        },
        {
            "role": "assistant",
            "content": {
                "type": "text",
                "text": "Step 2: Now, let's explore contrasting and complementary symbols."
            }
        }
    ]
    
    # Add sections for secondary themes if provided
    if secondary_themes_list:
        for i, sec_theme in enumerate(secondary_themes_list):
            messages.append({
                "role": "assistant",
                "content": {
                    "type": "text",
                    "text": f"Let's also explore symbolic connections for the secondary theme of '{sec_theme}'."
                }
            })
    
    messages.extend([
        {
            "role": "assistant",
            "content": {
                "type": "text",
                "text": "Step 3: Now, let's create a coherent symbolic system connecting all themes."
            }
        },
        {
            "role": "assistant",
            "content": {
                "type": "text",
                "text": "Step 4: Let's suggest ways to integrate these symbols into narrative elements like characters, settings, and objects."
            }
        },
        {
            "role": "assistant",
            "content": {
                "type": "text",
                "text": "Step 5: Finally, let's develop a symbolic progression that evolves throughout the story."
            }
        }
    ])
    
    return {
        "description": f"Symbolic exploration workflow for '{theme}'",
        "messages": messages
    }
