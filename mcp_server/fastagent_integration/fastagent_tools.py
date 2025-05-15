"""
AI Writers Workshop - Fast Agent Integration

This module provides integration with Fast Agent for the AI Writers Workshop MCP server.
Fast Agent is a framework for creating autonomous AI agents that can use tools and
make decisions independently. This integration allows using Ollama or LM Studio
models as the backend for AI assistants that leverage the AI Writers Workshop tools.
"""

import os
import sys
import logging
import asyncio
import json
import subprocess
import socket
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Callable

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ai_writers_workshop.fastagent")

# Add project root to path for imports
script_path = Path(__file__).resolve()
project_root = script_path.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))
    logger.info(f"Added {project_root} to sys.path")

# Try to import components from the AI Writers Workshop
try:
    from mcp_server.components.project_manager import ProjectManager
    from mcp_server.components.character_manager import CharacterManager
    from mcp_server.components.pattern_manager import PatternManager
    from mcp_server.components.narrative_generator import NarrativeGenerator
    from mcp_server.components.symbolic_manager import SymbolicManager
    from mcp_server.components.plotline_manager import PlotlineManager
    logger.info("Successfully imported AI Writers Workshop components")
except ImportError as e:
    logger.warning(f"Could not import AI Writers Workshop components: {e}")

# Configuration
CONFIG = {
    "output_dir": project_root / "output",
    "ollama_base_url": os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434"),
    "default_model": os.environ.get("DEFAULT_OLLAMA_MODEL", "mistral"),
    "agent_definitions_dir": script_path.parent / "agent_definitions",
}

# Ensure output directory exists
CONFIG["output_dir"].mkdir(parents=True, exist_ok=True)

# Ensure agent definitions directory exists
CONFIG["agent_definitions_dir"].mkdir(parents=True, exist_ok=True)

def check_ollama_available() -> bool:
    """
    Check if Ollama is available at the configured URL.
    
    Returns:
        Boolean indicating availability
    """
    import requests
    try:
        # Try to connect to Ollama API
        response = requests.get(f"{CONFIG['ollama_base_url']}/api/tags", timeout=5)
        if response.status_code == 200:
            logger.info(f"Ollama is available at {CONFIG['ollama_base_url']}")
            return True
        else:
            logger.warning(f"Ollama responded with status code {response.status_code}")
            return False
    except Exception as e:
        logger.warning(f"Error checking Ollama availability: {e}")
        return False

def check_lm_studio_available() -> bool:
    """
    Check if LM Studio server is available.
    
    Returns:
        Boolean indicating availability
    """
    import requests
    try:
        # Default LM Studio server URL
        lm_studio_url = "http://localhost:1234/v1/models"
        response = requests.get(lm_studio_url, timeout=5)
        if response.status_code == 200:
            logger.info("LM Studio server is available")
            return True
        else:
            logger.warning(f"LM Studio server responded with status code {response.status_code}")
            return False
    except Exception as e:
        logger.warning(f"Error checking LM Studio availability: {e}")
        return False

# Check backend availability
OLLAMA_AVAILABLE = check_ollama_available()
LM_STUDIO_AVAILABLE = check_lm_studio_available()
BACKEND_AVAILABLE = OLLAMA_AVAILABLE or LM_STUDIO_AVAILABLE

if not BACKEND_AVAILABLE:
    logger.warning("Neither Ollama nor LM Studio is available. Fast Agent will not function properly.")
    logger.warning("Please make sure either Ollama or LM Studio is running.")

# Initialize component managers
try:
    # These are initialized lazily to avoid circular imports
    _project_manager = None
    _pattern_manager = None 
    _character_manager = None
    _narrative_generator = None
    _symbolic_manager = None
    _plotline_manager = None
    
    def _get_project_manager():
        global _project_manager
        if _project_manager is None:
            _project_manager = ProjectManager(CONFIG["output_dir"])
        return _project_manager
    
    def _get_pattern_manager():
        global _pattern_manager
        if _pattern_manager is None:
            _pattern_manager = PatternManager(CONFIG["output_dir"])
        return _pattern_manager
    
    def _get_character_manager():
        global _character_manager
        if _character_manager is None:
            _character_manager = CharacterManager(_get_project_manager(), CONFIG["output_dir"])
        return _character_manager
    
    def _get_narrative_generator():
        global _narrative_generator
        if _narrative_generator is None:
            _narrative_generator = NarrativeGenerator(
                _get_project_manager(), 
                _get_pattern_manager(), 
                CONFIG["output_dir"]
            )
        return _narrative_generator
    
    def _get_symbolic_manager():
        global _symbolic_manager
        if _symbolic_manager is None:
            _symbolic_manager = SymbolicManager(_get_project_manager(), CONFIG["output_dir"])
        return _symbolic_manager
    
    def _get_plotline_manager():
        global _plotline_manager
        if _plotline_manager is None:
            _plotline_manager = PlotlineManager(
                _get_project_manager(), 
                _get_pattern_manager(), 
                CONFIG["output_dir"]
            )
        return _plotline_manager
        
    logger.info("Component manager getters initialized")
except Exception as e:
    logger.error(f"Error setting up component managers: {e}")

class FastAgentScript:
    """
    Represents a Fast Agent script that can be run with Ollama or LM Studio.
    """
    
    def __init__(
        self, 
        name: str, 
        script_type: str,
        instruction: str,
        model: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        system_prompt: Optional[str] = None
    ):
        """
        Initialize a Fast Agent script.
        
        Args:
            name: Name for the script
            script_type: Type of script ("agent", "workflow", "chain", "router")
            instruction: Base instruction for the agent
            model: Optional model to use
            tools: Optional list of tools available to the agent
            system_prompt: Optional system prompt override
        """
        self.name = name
        self.script_type = script_type
        self.instruction = instruction
        self.model = model or CONFIG["default_model"]
        self.tools = tools or []
        self.system_prompt = system_prompt or instruction
        
        # Save the script definition
        self._save_definition()
    
    def _save_definition(self) -> None:
        """Save script definition to disk."""
        script_path = CONFIG["agent_definitions_dir"] / f"{self.name}.json"
        
        script_def = {
            "name": self.name,
            "type": self.script_type,
            "instruction": self.instruction,
            "model": self.model,
            "tools": self.tools,
            "system_prompt": self.system_prompt
        }
        
        with open(script_path, "w") as f:
            json.dump(script_def, f, indent=2)
        
        logger.info(f"Saved script definition to {script_path}")
    
    @classmethod
    def load(cls, name: str) -> "FastAgentScript":
        """
        Load a script from disk.
        
        Args:
            name: Name of the script to load
            
        Returns:
            Loaded FastAgentScript
        """
        script_path = CONFIG["agent_definitions_dir"] / f"{name}.json"
        
        if not script_path.exists():
            raise FileNotFoundError(f"Script definition not found: {script_path}")
        
        with open(script_path, "r") as f:
            script_def = json.load(f)
        
        return cls(
            name=script_def["name"],
            script_type=script_def["type"],
            instruction=script_def["instruction"],
            model=script_def.get("model"),
            tools=script_def.get("tools", []),
            system_prompt=script_def.get("system_prompt")
        )
    
    @classmethod
    def list_scripts(cls) -> List[str]:
        """
        List available script names.
        
        Returns:
            List of script names
        """
        scripts = []
        for script_file in CONFIG["agent_definitions_dir"].glob("*.json"):
            scripts.append(script_file.stem)
        return scripts

class AgentSession:
    """
    Manages an interactive session with a Fast Agent.
    """
    
    def __init__(self, script: FastAgentScript):
        """
        Initialize an agent session.
        
        Args:
            script: FastAgentScript definition
        """
        self.script = script
        self.session_id = f"{script.name}_{id(self)}"
        self.messages = []
        self.active = True
        
    async def send_message(self, content: str) -> Dict[str, Any]:
        """
        Send a message to the agent and get a response.
        
        Args:
            content: Message content
            
        Returns:
            Response from the agent
        """
        if not self.active:
            raise RuntimeError("Session is no longer active")
        
        # Add user message to history
        self.messages.append({"role": "user", "content": content})
        
        # Get response using either Ollama or LM Studio
        response = await self._get_model_response()
        
        # Add assistant response to history
        self.messages.append({"role": "assistant", "content": response["content"]})
        
        return response
    
    async def _get_model_response(self) -> Dict[str, Any]:
        """
        Get a response from the model.
        
        Returns:
            Model response
        """
        if OLLAMA_AVAILABLE:
            return await self._get_ollama_response()
        elif LM_STUDIO_AVAILABLE:
            return await self._get_lm_studio_response()
        else:
            raise RuntimeError("Neither Ollama nor LM Studio is available")
    
    async def _get_ollama_response(self) -> Dict[str, Any]:
        """
        Get a response using Ollama.
        
        Returns:
            Ollama response
        """
        import httpx
        
        # Prepare the message history
        messages = [{"role": "system", "content": self.script.system_prompt}]
        messages.extend(self.messages)
        
        # Add tool definitions if available
        options = {}
        if self.script.tools:
            # Format depends on Ollama version, this is for newer versions
            options["tools"] = self.script.tools
            
        # Create the request payload
        payload = {
            "model": self.script.model,
            "messages": messages,
            "stream": False,
            "options": options
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{CONFIG['ollama_base_url']}/api/chat", 
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            
            # Process the response
            if "message" in data:
                return {
                    "role": data["message"]["role"],
                    "content": data["message"]["content"],
                    "model": self.script.model
                }
            else:
                # Fallback for older Ollama versions
                return {
                    "role": "assistant",
                    "content": data.get("response", "No response from model"),
                    "model": self.script.model
                }
    
    async def _get_lm_studio_response(self) -> Dict[str, Any]:
        """
        Get a response using LM Studio.
        
        Returns:
            LM Studio response
        """
        import httpx
        
        # LM Studio uses OpenAI-compatible API
        lm_studio_url = "http://localhost:1234/v1/chat/completions"
        
        # Prepare the message history
        messages = [{"role": "system", "content": self.script.system_prompt}]
        messages.extend(self.messages)
        
        # Create the request payload
        payload = {
            "model": self.script.model,
            "messages": messages,
            "temperature": 0.7,
            "stream": False
        }
        
        # Add tool definitions if available and supported by the model
        if self.script.tools:
            # OpenAI format for tools
            payload["tools"] = self.script.tools
            payload["tool_choice"] = "auto"
        
        async with httpx.AsyncClient() as client:
            response = await client.post(lm_studio_url, json=payload)
            response.raise_for_status()
            data = response.json()
            
            # Process the response
            if "choices" in data and len(data["choices"]) > 0:
                choice = data["choices"][0]
                message = choice.get("message", {})
                
                # Check for tool calls in the response
                tool_calls = message.get("tool_calls", [])
                tool_results = []
                
                # Execute any tool calls and append results
                for tool_call in tool_calls:
                    tool_result = await self._execute_tool_call(tool_call)
                    tool_results.append(tool_result)
                
                # If there were tool calls, add their results and get a final response
                if tool_results:
                    for result in tool_results:
                        self.messages.append({
                            "role": "tool",
                            "tool_call_id": result["tool_call_id"],
                            "content": result["content"]
                        })
                    
                    # Get final response after tool use
                    return await self._get_model_response()
                
                return {
                    "role": message.get("role", "assistant"),
                    "content": message.get("content", "No response from model"),
                    "model": self.script.model
                }
            else:
                return {
                    "role": "assistant",
                    "content": "No valid response from LM Studio",
                    "model": self.script.model
                }
    
    async def _execute_tool_call(self, tool_call: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool call and return the result.
        
        Args:
            tool_call: Tool call definition
            
        Returns:
            Tool call result
        """
        try:
            function_name = tool_call.get("function", {}).get("name")
            function_args_str = tool_call.get("function", {}).get("arguments", "{}")
            function_args = json.loads(function_args_str)
            
            # Get the tool handler
            tool_handler = get_tool_handler(function_name)
            if not tool_handler:
                return {
                    "tool_call_id": tool_call.get("id", "unknown"),
                    "content": f"Error: Tool '{function_name}' not found"
                }
            
            # Execute the tool
            result = tool_handler(**function_args)
            
            # Convert result to string if necessary
            if not isinstance(result, str):
                result = json.dumps(result, indent=2)
            
            return {
                "tool_call_id": tool_call.get("id", "unknown"),
                "content": result
            }
        except Exception as e:
            logger.error(f"Error executing tool call: {e}")
            return {
                "tool_call_id": tool_call.get("id", "unknown"),
                "content": f"Error executing tool: {str(e)}"
            }
    
    def close(self) -> None:
        """Close the session."""
        self.active = False
        logger.info(f"Closed session {self.session_id}")

# Dictionary to store active sessions
active_sessions: Dict[str, AgentSession] = {}

# Dictionary to map tool names to handler functions
tool_handlers: Dict[str, Callable] = {}

def get_tool_handler(tool_name: str) -> Optional[Callable]:
    """
    Get a handler function for a tool.
    
    Args:
        tool_name: Name of the tool
        
    Returns:
        Handler function or None if not found
    """
    if tool_name in tool_handlers:
        return tool_handlers[tool_name]
    
    # Check for AI Writers Workshop tools
    # These are dynamically looked up to avoid import issues
    
    # Project Management tools
    if tool_name == "create_writing_project":
        return _get_project_manager().create_project
    elif tool_name == "get_writing_project":
        return _get_project_manager().get_project
    elif tool_name == "list_outputs":
        return _get_project_manager().list_outputs
    
    # Pattern tools
    elif tool_name == "list_patterns":
        return _get_pattern_manager().list_patterns
    elif tool_name == "get_pattern_details":
        return _get_pattern_manager().get_pattern_details
    elif tool_name == "analyze_narrative":
        return _get_pattern_manager().analyze_narrative
    elif tool_name == "create_custom_pattern":
        return _get_pattern_manager().create_custom_pattern
    elif tool_name == "create_hybrid_pattern":
        return _get_pattern_manager().create_hybrid_pattern
    
    # Character tools
    elif tool_name == "list_archetypes":
        return _get_character_manager().list_archetypes
    elif tool_name == "get_archetype_details":
        return _get_character_manager().get_archetype_details
    elif tool_name == "create_character":
        return _get_character_manager().create_character
    elif tool_name == "develop_character_arc":
        return _get_character_manager().develop_character_arc
    elif tool_name == "create_custom_archetype":
        return _get_character_manager().create_custom_archetype
    
    # Narrative generation tools
    elif tool_name == "generate_outline":
        return _get_narrative_generator().generate_outline
    elif tool_name == "generate_scene":
        return _get_narrative_generator().generate_scene
    elif tool_name == "compile_narrative":
        return _get_narrative_generator().compile_narrative
    
    # Symbolic tools
    elif tool_name == "find_symbolic_connections":
        return _get_symbolic_manager().find_symbolic_connections
    elif tool_name == "create_custom_symbols":
        return _get_symbolic_manager().create_custom_symbols
    elif tool_name == "apply_symbolic_theme":
        return _get_symbolic_manager().apply_symbolic_theme
    
    # Plotline tools
    elif tool_name == "list_plotlines":
        return _get_plotline_manager().list_plotlines
    elif tool_name == "get_plotline_details":
        return _get_plotline_manager().get_plotline_details
    elif tool_name == "create_custom_plotline":
        return _get_plotline_manager().create_custom_plotline
    elif tool_name == "develop_plotline":
        return _get_plotline_manager().develop_plotline
    elif tool_name == "analyze_plotline":
        return _get_plotline_manager().analyze_plotline
    
    return None

def register_tool(name: str, handler: Callable) -> None:
    """
    Register a custom tool handler.
    
    Args:
        name: Tool name
        handler: Tool handler function
    """
    tool_handlers[name] = handler
    logger.info(f"Registered tool handler for '{name}'")

# ---- API Functions ----

def list_scripts() -> List[Dict[str, Any]]:
    """
    List available Fast Agent scripts.
    
    Returns:
        List of script information dictionaries
    """
    if not BACKEND_AVAILABLE:
        logger.error("No model backend (Ollama or LM Studio) is available")
        raise RuntimeError("No model backend available")
    
    scripts = []
    for script_name in FastAgentScript.list_scripts():
        try:
            script = FastAgentScript.load(script_name)
            scripts.append({
                "name": script.name,
                "type": script.script_type,
                "description": script.instruction[:100] + "..." if len(script.instruction) > 100 else script.instruction,
                "model": script.model
            })
        except Exception as e:
            logger.error(f"Error loading script '{script_name}': {e}")
    
    # Add default scripts if none exist
    if not scripts:
        # Create default scripts
        create_default_scripts()
        return list_scripts()  # Recursive call to get the newly created scripts
    
    return scripts

def create_script(
    name: str,
    script_type: str = "agent",
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
    if not BACKEND_AVAILABLE:
        logger.error("No model backend (Ollama or LM Studio) is available")
        raise RuntimeError("No model backend available")
    
    try:
        # Define a set of tools based on script type
        tools = []
        
        # Add writing-related tools based on script type
        if script_type == "agent":
            if "narrative" in name.lower() or "story" in name.lower():
                # Narrative-focused agent
                tools = define_narrative_tools()
            elif "character" in name.lower():
                # Character-focused agent
                tools = define_character_tools()
            else:
                # General writing agent - all tools
                tools = define_all_tools()
        
        # Create the script
        script = FastAgentScript(
            name=name,
            script_type=script_type,
            instruction=instruction,
            model=model,
            tools=tools
        )
        
        return {
            "name": script.name,
            "type": script.script_type,
            "instruction": script.instruction,
            "model": script.model,
            "status": "created",
            "tool_count": len(tools)
        }
    except Exception as e:
        logger.error(f"Error creating Fast Agent script: {e}")
        raise

def delete_script(name: str) -> Dict[str, Any]:
    """
    Delete a Fast Agent script.
    
    Args:
        name: Name of the script to delete
        
    Returns:
        Dictionary with deletion status
    """
    script_path = CONFIG["agent_definitions_dir"] / f"{name}.json"
    
    if not script_path.exists():
        return {"status": "error", "message": f"Script '{name}' not found"}
    
    try:
        script_path.unlink()
        return {"status": "success", "message": f"Script '{name}' deleted"}
    except Exception as e:
        logger.error(f"Error deleting script '{name}': {e}")
        return {"status": "error", "message": f"Error deleting script: {str(e)}"}

async def run_agent(
    script_name: str,
    prompt: str,
    model: Optional[str] = None
) -> Dict[str, Any]:
    """
    Run a Fast Agent script with a prompt.
    
    Args:
        script_name: Name of the script to run
        prompt: Initial prompt to send to the agent
        model: Optional model override
        
    Returns:
        Dictionary with agent response
    """
    if not BACKEND_AVAILABLE:
        logger.error("No model backend (Ollama or LM Studio) is available")
        raise RuntimeError("No model backend available")
    
    try:
        # Load the script
        script = FastAgentScript.load(script_name)
        
        # Override model if specified
        if model:
            script.model = model
        
        # Create a session
        session = AgentSession(script)
        
        # Store the session
        session_id = session.session_id
        active_sessions[session_id] = session
        
        # Send the initial prompt
        response = await session.send_message(prompt)
        
        return {
            "session_id": session_id,
            "response": response,
            "status": "running"
        }
    except Exception as e:
        logger.error(f"Error running agent '{script_name}': {e}")
        raise

async def send_message(
    session_id: str,
    message: str
) -> Dict[str, Any]:
    """
    Send a message to an active agent session.
    
    Args:
        session_id: ID of the session to send the message to
        message: Message content
        
    Returns:
        Dictionary with agent response
    """
    if not BACKEND_AVAILABLE:
        logger.error("No model backend (Ollama or LM Studio) is available")
        raise RuntimeError("No model backend available")
    
    if session_id not in active_sessions:
        raise ValueError(f"Session '{session_id}' not found")
    
    try:
        session = active_sessions[session_id]
        response = await session.send_message(message)
        
        return {
            "session_id": session_id,
            "response": response,
            "status": "running"
        }
    except Exception as e:
        logger.error(f"Error sending message to session '{session_id}': {e}")
        raise

def close_session(session_id: str) -> Dict[str, Any]:
    """
    Close an active agent session.
    
    Args:
        session_id: ID of the session to close
        
    Returns:
        Dictionary with closure status
    """
    if session_id not in active_sessions:
        return {
            "status": "error",
            "message": f"Session '{session_id}' not found"
        }
    
    try:
        session = active_sessions.pop(session_id)
        session.close()
        
        return {
            "status": "success",
            "message": f"Session '{session_id}' closed"
        }
    except Exception as e:
        logger.error(f"Error closing session '{session_id}': {e}")
        return {
            "status": "error",
            "message": f"Error closing session: {str(e)}"
        }

def check_fastagent_status() -> Dict[str, Any]:
    """
    Check Fast Agent status.
    
    Returns:
        Dictionary with status information
    """
    status = {
        "available": BACKEND_AVAILABLE,
        "ollama_available": OLLAMA_AVAILABLE,
        "lm_studio_available": LM_STUDIO_AVAILABLE,
        "active_sessions": len(active_sessions),
        "scripts": len(FastAgentScript.list_scripts()),
    }
    
    if not BACKEND_AVAILABLE:
        status["error"] = "No model backend available. Please install and run Ollama or LM Studio."
    
    return status

def create_default_scripts() -> None:
    """Create default Fast Agent scripts."""
    try:
        # Narrative assistant
        if "narrative_assistant" not in FastAgentScript.list_scripts():
            create_script(
                name="narrative_assistant",
                script_type="agent",
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
                """,
                model=CONFIG["default_model"]
            )
        
        # Character developer
        if "character_developer" not in FastAgentScript.list_scripts():
            create_script(
                name="character_developer",
                script_type="agent",
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
                """,
                model=CONFIG["default_model"]
            )
        
        # Story editor
        if "story_editor" not in FastAgentScript.list_scripts():
            create_script(
                name="story_editor",
                script_type="agent",
                instruction="""
                You are a skilled story editor with expertise in narrative structure, pacing,
                character development, and prose style. Your job is to help writers improve
                their stories through thoughtful feedback and suggestions.

                When editing, focus on:
                1. Narrative coherence and plot structure
                2. Character consistency and development
                3. Thematic clarity and resonance
                4. Writing quality and style

                Provide specific, actionable feedback that respects the writer's vision while
                helping them improve their work.
                """,
                model=CONFIG["default_model"]
            )
        
        logger.info("Created default Fast Agent scripts")
    except Exception as e:
        logger.error(f"Error creating default scripts: {e}")

def define_narrative_tools() -> List[Dict[str, Any]]:
    """
    Define narrative-focused tools for agents.
    
    Returns:
        List of tool definitions
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "list_patterns",
                "description": "List available narrative patterns",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_pattern_details",
                "description": "Get detailed information about a specific narrative pattern",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "pattern_name": {
                            "type": "string",
                            "description": "Name of the pattern (e.g., 'heroes_journey', 'transformation')"
                        }
                    },
                    "required": ["pattern_name"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "analyze_narrative",
                "description": "Analyze a narrative structure using a specific pattern",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "scenes": {
                            "type": "array",
                            "description": "List of scene dictionaries, each with 'title' and 'description'",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "title": {"type": "string"},
                                    "description": {"type": "string"}
                                }
                            }
                        },
                        "pattern_name": {
                            "type": "string",
                            "description": "Name of the pattern to analyze against",
                            "default": "heroes_journey"
                        },
                        "project_id": {
                            "type": "string",
                            "description": "Optional project to associate with"
                        },
                        "adherence_level": {
                            "type": "number",
                            "description": "How strictly to apply pattern (0.0-1.0)",
                            "default": 1.0
                        }
                    },
                    "required": ["scenes"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "generate_outline",
                "description": "Generate a story outline based on a pattern",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Story title"
                        },
                        "pattern": {
                            "type": "string",
                            "description": "Narrative pattern to use"
                        },
                        "main_character": {
                            "type": "object",
                            "description": "Optional character information"
                        },
                        "project_id": {
                            "type": "string",
                            "description": "Optional project to associate with"
                        }
                    },
                    "required": ["title", "pattern"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "generate_scene",
                "description": "Generate a scene based on pattern elements",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "scene_title": {
                            "type": "string",
                            "description": "Title of the scene"
                        },
                        "pattern_stage": {
                            "type": "string",
                            "description": "The pattern stage this scene represents"
                        },
                        "characters": {
                            "type": "array",
                            "description": "List of character names in the scene",
                            "items": {"type": "string"}
                        },
                        "project_id": {
                            "type": "string",
                            "description": "Optional project to associate with"
                        },
                        "setting": {
                            "type": "string",
                            "description": "Optional setting description"
                        },
                        "conflict": {
                            "type": "string",
                            "description": "Optional conflict description"
                        }
                    },
                    "required": ["scene_title", "pattern_stage", "characters"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "compile_narrative",
                "description": "Compile scenes into a complete narrative",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "project_id": {
                            "type": "string",
                            "description": "Project ID to compile"
                        },
                        "title": {
                            "type": "string",
                            "description": "Optional title for the narrative (defaults to project name)"
                        },
                        "scene_order": {
                            "type": "array",
                            "description": "Optional list of scene IDs to define order",
                            "items": {"type": "string"}
                        },
                        "include_character_descriptions": {
                            "type": "boolean",
                            "description": "Whether to include character descriptions",
                            "default": true
                        },
                        "format": {
                            "type": "string",
                            "description": "Output format (markdown, json, html)",
                            "default": "markdown"
                        }
                    },
                    "required": ["project_id"]
                }
            }
        }
    ]

def define_character_tools() -> List[Dict[str, Any]]:
    """
    Define character-focused tools for agents.
    
    Returns:
        List of tool definitions
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "list_archetypes",
                "description": "List available character archetypes",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_archetype_details",
                "description": "Get detailed information about a specific character archetype",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "archetype_name": {
                            "type": "string",
                            "description": "Name of the archetype (e.g., 'hero', 'mentor')"
                        }
                    },
                    "required": ["archetype_name"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "create_character",
                "description": "Create a character based on an archetype",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Character name"
                        },
                        "archetype": {
                            "type": "string",
                            "description": "Base archetype (e.g., 'hero', 'mentor')"
                        },
                        "traits": {
                            "type": "array",
                            "description": "Optional list of specific traits",
                            "items": {"type": "string"}
                        },
                        "project_id": {
                            "type": "string",
                            "description": "Optional project to associate with"
                        }
                    },
                    "required": ["name", "archetype"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "develop_character_arc",
                "description": "Develop a character arc within a narrative pattern",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "character_name": {
                            "type": "string",
                            "description": "Character name"
                        },
                        "archetype": {
                            "type": "string",
                            "description": "Character's archetype"
                        },
                        "pattern": {
                            "type": "string",
                            "description": "Narrative pattern to use"
                        },
                        "project_id": {
                            "type": "string",
                            "description": "Optional project to associate with"
                        }
                    },
                    "required": ["character_name", "archetype", "pattern"]
                }
            }
        }
    ]

def define_all_tools() -> List[Dict[str, Any]]:
    """
    Define all tools for agents.
    
    Returns:
        List of tool definitions
    """
    # Combine narrative and character tools
    tools = define_narrative_tools()
    tools.extend(define_character_tools())
    
    # Add project management tools
    tools.extend([
        {
            "type": "function",
            "function": {
                "name": "create_writing_project",
                "description": "Create a new project with hierarchical structure",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Project name"
                        },
                        "description": {
                            "type": "string",
                            "description": "Project description"
                        },
                        "project_type": {
                            "type": "string",
                            "description": "Type of project (story, novel, article, script)",
                            "default": "story"
                        }
                    },
                    "required": ["name", "description"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_writing_project",
                "description": "Get detailed information about a specific writing project",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "project_id": {
                            "type": "string",
                            "description": "ID of the project to retrieve"
                        }
                    },
                    "required": ["project_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "list_outputs",
                "description": "List all available outputs",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }
    ])
    
    # Add symbolic tools
    tools.extend([
        {
            "type": "function",
            "function": {
                "name": "find_symbolic_connections",
                "description": "Find symbolic connections for a theme",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "theme": {
                            "type": "string",
                            "description": "Theme to find symbols for"
                        },
                        "count": {
                            "type": "integer",
                            "description": "Number of symbols to return",
                            "default": 3
                        },
                        "project_id": {
                            "type": "string",
                            "description": "Optional project to associate with"
                        }
                    },
                    "required": ["theme"]
                }
            }
        }
    ])
    
    return tools

# Initialize default scripts
create_default_scripts()
