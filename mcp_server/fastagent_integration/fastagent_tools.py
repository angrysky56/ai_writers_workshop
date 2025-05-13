"""
AI Writers Workshop - Fast Agent Integration

This module provides integration with Fast Agent for the AI Writers Workshop MCP server.
"""

import os
import sys
import logging
import asyncio
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Union

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ai_writers_workshop.fastagent")

def _check_fastagent_available() -> bool:
    """
    Check if Fast Agent is available.
    
    Returns:
        Boolean indicating availability
    """
    try:
        import fast_agent_mcp
        return True
    except ImportError:
        logger.warning("Fast Agent package not found")
        return False
    except Exception as e:
        logger.warning(f"Error checking Fast Agent availability: {e}")
        return False

# Check Fast Agent availability
FASTAGENT_AVAILABLE = _check_fastagent_available()

# Initialize Fast Agent if available
fast_agent = None
if FASTAGENT_AVAILABLE:
    try:
        import fast_agent_mcp
        from fast_agent_mcp.core import FastAgent
        
        # Create a global FastAgent instance
        fast_agent = FastAgent("AI Writers Workshop")
        logger.info("Successfully initialized Fast Agent integration")
        
        # Define narrative agent
        @fast_agent.agent(
            name="narrative_assistant",
            instruction="""
            You are a narrative development assistant with expertise in archetypal patterns,
            character archetypes, and symbolic systems. Help writers create psychologically
            resonant stories by applying these frameworks.
            
            When assisting with story development, consider:
            1. The archetypal patterns (Hero's Journey, Transformation, etc.)
            2. Character archetypes and their psychological functions
            3. Symbolic systems and their connection to themes
            4. The internal/external character arcs
            
            Provide specific, actionable guidance based on narrative theory and psychological depth.
            """
        )
        async def narrative_assistant_agent():
            """Narrative assistant agent definition."""
            pass
        
        # Define character development agent
        @fast_agent.agent(
            name="character_developer",
            instruction="""
            You are a character development specialist with expertise in character archetypes,
            psychology, and character arcs. Your job is to help writers create psychologically
            deep and compelling characters.
            
            When developing characters, consider:
            1. The character's underlying archetype
            2. Their shadow aspects and internal conflicts
            3. Their growth and transformation arc
            4. Their symbolic associations and psychological dimensions
            
            Create characters with depth, internal consistency, and growth potential.
            """
        )
        async def character_developer_agent():
            """Character developer agent definition."""
            pass
        
        logger.info("Successfully registered Fast Agent agents")
    except Exception as e:
        logger.error(f"Error initializing Fast Agent: {e}")
        FASTAGENT_AVAILABLE = False
        fast_agent = None

def list_scripts() -> List[Dict[str, Any]]:
    """
    List available Fast Agent scripts.
    
    Returns:
        List of script information dictionaries
    """
    if not FASTAGENT_AVAILABLE or not fast_agent:
        logger.error("Fast Agent not available")
        raise RuntimeError("Fast Agent not available")
    
    try:
        # In a real implementation, this would use the Fast Agent API
        # This is a mock implementation
        return [
            {
                "name": "narrative_assistant", 
                "type": "agent",
                "description": "Narrative development assistant"
            },
            {
                "name": "character_developer", 
                "type": "agent",
                "description": "Character development specialist"
            },
            {
                "name": "writing_workflow", 
                "type": "workflow",
                "description": "Complete writing workflow from concept to editing"
            }
        ]
    except Exception as e:
        logger.error(f"Error listing Fast Agent scripts: {e}")
        raise

def create_script(
    name: str,
    script_type: str = "basic",
    instruction: str = "You are a narrative development assistant.",
    model: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a Fast Agent script.
    
    Args:
        name: Name for the script
        script_type: Type of script to create
        instruction: Base instruction for the agent
        model: Model to use
        
    Returns:
        Dictionary with creation results
    """
    if not FASTAGENT_AVAILABLE or not fast_agent:
        logger.error("Fast Agent not available")
        raise RuntimeError("Fast Agent not available")
    
    try:
        # In a real implementation, this would use the Fast Agent API
        # This is a mock implementation
        return {
            "name": name,
            "type": script_type,
            "instruction": instruction,
            "model": model or "default",
            "status": "created"
        }
    except Exception as e:
        logger.error(f"Error creating Fast Agent script: {e}")
        raise

async def _run_narrative_agent_async(
    prompt: str,
    instruction: Optional[str] = None,
    model: Optional[str] = None
) -> str:
    """
    Run the narrative assistant agent asynchronously.
    
    Args:
        prompt: The prompt to send to the agent
        instruction: Optional custom instruction
        model: Optional model to use
        
    Returns:
        Agent response text
    """
    if not FASTAGENT_AVAILABLE or not fast_agent:
        logger.error("Fast Agent not available")
        raise RuntimeError("Fast Agent not available")
    
    try:
        run_args = {}
        if model:
            run_args["model"] = model
            
        # Run the narrative assistant agent
        async with fast_agent.run("narrative_assistant", **run_args) as session:
            # If custom instruction is provided, send it first
            if instruction:
                await session.send(f"Use this instruction: {instruction}")
                
            # Send the main prompt
            response = await session.send(prompt)
            
            # Return the response text
            return response.content if hasattr(response, 'content') else str(response)
    except Exception as e:
        logger.error(f"Error running narrative agent: {e}")
        raise

def run_narrative_agent(
    prompt: str,
    instruction: Optional[str] = None,
    model: Optional[str] = None
) -> str:
    """
    Run the narrative assistant agent.
    
    Args:
        prompt: The prompt to send to the agent
        instruction: Optional custom instruction
        model: Optional model to use
        
    Returns:
        Agent response text
    """
    if not FASTAGENT_AVAILABLE:
        logger.error("Fast Agent not available")
        raise RuntimeError("Fast Agent not available")
    
    try:
        # In a real implementation, this would use the Fast Agent API
        # This is a mock implementation for demonstration
        return f"""
        [Narrative Assistant Response]
        
        I've analyzed your request: "{prompt}"
        
        Here's my narrative analysis and recommendations:
        
        1. Archetypal Pattern: This appears to follow the Transformation pattern
        2. Character Development: Consider deepening the protagonist's internal conflict
        3. Symbolic Elements: The recurring water imagery connects to themes of rebirth
        
        I recommend developing the threshold crossing moment more explicitly to strengthen 
        the character's commitment to their journey.
        
        Let me know if you'd like to explore any specific aspect in more depth!
        """
    except Exception as e:
        logger.error(f"Error running narrative agent: {e}")
        raise
        
def run_fastagent_workflow(
    workflow_name: str,
    input_data: Dict[str, Any],
    model: Optional[str] = None
) -> Dict[str, Any]:
    """
    Run a Fast Agent workflow.
    
    Args:
        workflow_name: Name of the workflow to run
        input_data: Input data for the workflow
        model: Optional model to use
        
    Returns:
        Workflow results
    """
    if not FASTAGENT_AVAILABLE or not fast_agent:
        logger.error("Fast Agent not available")
        raise RuntimeError("Fast Agent not available")
    
    try:
        # In a real implementation, this would use the Fast Agent API
        # This is a mock implementation
        return {
            "workflow": workflow_name,
            "status": "completed",
            "results": {
                "concept": "Developed initial concept",
                "structure": "Applied Hero's Journey structure",
                "characters": "Developed 3 primary characters",
                "scenes": "Outlined 12 key scenes",
                "draft": "Generated initial draft of key scenes"
            }
        }
    except Exception as e:
        logger.error(f"Error running Fast Agent workflow: {e}")
        raise

def check_fastagent_status() -> Dict[str, Any]:
    """
    Check Fast Agent status.
    
    Returns:
        Dictionary with status information
    """
    status = {
        "available": FASTAGENT_AVAILABLE,
        "initialized": fast_agent is not None
    }
    
    if not FASTAGENT_AVAILABLE:
        status["error"] = "Fast Agent package not found. Please install with 'uv add fast_agent_mcp'"
    elif not fast_agent:
        status["error"] = "Fast Agent initialized but failed to create agent instance"
    else:
        status["agents"] = len(list_scripts())
    
    return status
