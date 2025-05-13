"""
AI Writing Agency - Fast Agent Integration Module

This module provides integration with the fast-agent framework, connecting the AI
Writing Agency's archetypal narrative capabilities with fast-agent's powerful agent-based
and workflow capabilities through the Message Context Protocol (MCP).
"""

import os
import yaml
import asyncio
import logging
import importlib.util
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable, Union, Tuple
import archetypal_framework

from .config import config
from .core import ProcessingComponent

def _check_fast_agent_available() -> bool:
    """
    Check if the fast-agent package is available.

    Returns:
        Boolean indicating availability
    """
    try:
        import mcp_agent
        return True
    except ImportError:
        logger.warning("fast-agent package (mcp_agent) not found. Some features will be unavailable.")
        return False

FAST_AGENT_AVAILABLE = _check_fast_agent_available()
FastAgent = None
fast = None

if FAST_AGENT_AVAILABLE:
    try:
        from mcp_agent.core.fastagent import FastAgent
        # Create a global FastAgent instance for the AI Writing Agency
        fast = FastAgent("AI Writing Agency")
        logger.info("Successfully initialized fast-agent integration")
    except Exception as e:
        logger.error(f"Error initializing fast-agent: {e}")
        FAST_AGENT_AVAILABLE = False
        fast = None

# --- Agent/Workflow Definitions (using the global 'fast' instance) --- #

if FAST_AGENT_AVAILABLE and fast:

    # --- Base Agents --- #

    @fast.agent(
        name="concept_developer",
        instruction="""
        You are a concept development specialist. Your job is to help writers develop
        compelling story concepts, generate ideas, and identify core themes.
        """
    )
    async def concept_developer_agent(): pass

    @fast.agent(
        name="narrative_architect",
        instruction="""
        You are a narrative architect with expertise in story structure, archetypal
        patterns, and plot development. Your job is to help writers create strong,
        coherent story structures based on archetypal foundations.
        """,
        servers=["archetypal_patterns"] # Assumes this MCP server is defined/available
    )
    async def narrative_architect_agent(): pass

    @fast.agent(
        name="character_developer",
        instruction="""
        You are a character development specialist with expertise in character archetypes,
        psychology, and character arcs. Your job is to help writers create psychologically
        deep and compelling characters.
        """,
        servers=["character_engine"] # Assumes this MCP server is defined/available
    )
    async def character_developer_agent(): pass

    @fast.agent(
        name="prose_generator",
        instruction="""
        You are a prose generation specialist. Your job is to help writers create
        high-quality prose for their stories, focusing on description, dialogue,
        and narrative voice.
        """
    )
    async def prose_generator_agent(): pass

    @fast.agent(
        name="editor",
        instruction="""
        You are an editor with expertise in refining stories for clarity, coherence,
        impact, and style. Your job is to help writers polish their work to a
        professional standard.
        """
    )
    async def editor_agent(): pass

    @fast.agent(
        name="story_generator",
        instruction="""
        You are a creative story generator with expertise in narrative development.
        Your job is to generate story content based on the provided instructions,
        incorporating archetypal patterns and psychological depth.
        """,
        # Assumes these MCP servers are defined/available
        servers=["narrative_engine", "archetypal_patterns", "symbolic_system"]
    )
    async def story_generator_agent(): pass

    @fast.agent(
        name="story_evaluator",
        instruction="""
        You are a literary critic and story consultant with expertise in narrative theory,
        character development, and prose style. Your job is to evaluate story content
        and provide specific, actionable feedback for improvement.

        When evaluating content, use the following rating scale:
        - EXCELLENT: The content excels in all areas and needs no significant changes.
        - GOOD: The content is effective but could benefit from minor improvements.
        - FAIR: The content has potential but needs substantial revisions.
        - POOR: The content has fundamental issues that require major reworking.

        Always begin your evaluation with your rating in ALL CAPS, followed by a
        detailed explanation and specific suggestions for improvement.
        """
    )
    async def story_evaluator_agent(): pass

    @fast.agent(
        name="narrative_assistant",
        # Default instruction, can be overridden at runtime if API supports it
        instruction="""
        You are a narrative development assistant with expertise in archetypal patterns,
        character archetypes, and symbolic systems. Help writers create psychologically
        resonant stories by applying these frameworks.
        """,
        # Assumes these MCP servers are defined/available
        servers=["narrative_engine", "character_engine", "archetypal_patterns", "symbolic_system"]
    )
    async def narrative_assistant_agent(): pass

    # --- Workflows --- #

    @fast.chain(
        name="writing_workflow",
        sequence=[
            "concept_developer",
            "narrative_architect",
            "character_developer",
            "prose_generator",
            "editor"
        ],
        instruction="""
        This workflow takes a story idea through the complete development process,
        from concept to final edited prose.
        """
    )
    async def writing_workflow(): pass

    @fast.evaluator_optimizer(
        name="story_refinement",
        generator="story_generator",
        evaluator="story_evaluator",
        min_rating="EXCELLENT",
        max_refinements=5
    )
    async def story_refinement_workflow(): pass


class FastAgentIntegration:
    """
    Manages integration with the fast-agent framework.

    This class serves as a bridge between the AI Writing Agency framework
    and the fast-agent framework, enabling the use of fast-agent's powerful
    agent-based workflow capabilities with the agency's archetypal narrative tools.
    """

    def __init__(self):
        """Initialize the fast-agent integration."""
        self.fast_agent_available = FAST_AGENT_AVAILABLE
        self.fast = fast # Use the globally initialized instance
        self.mcp_servers = {}

        if self.fast_agent_available:
            self._load_mcp_servers()

    def _load_mcp_servers(self) -> None:
        """Load MCP server configurations from fastagent.config.yaml."""
        if not self.fast_agent_available or not self.fast:
            return

        config_path = config.get("fast_agent.config_path", "./mcp_server/fastagent.config.yaml")

        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as file:
                    fast_config = yaml.safe_load(file)

                if fast_config and "mcp" in fast_config and "servers" in fast_config["mcp"]:
                    self.mcp_servers = fast_config["mcp"]["servers"]
                    logger.info(f"Loaded {len(self.mcp_servers)} MCP server configurations from {config_path}")
            except Exception as e:
                logger.error(f"Error loading fast-agent configuration from {config_path}: {e}")
        else:
             logger.warning(f"fast-agent configuration file not found at {config_path}")

    def ensure_narrative_servers(self) -> None:
        """
        Ensure that narrative-related MCP servers are configured in fastagent.config.yaml.
        """
        if not self.fast_agent_available:
            return

        config_path_str = config.get("fast_agent.config_path", "./mcp_server/fastagent.config.yaml")
        config_path = Path(config_path_str)

        default_servers = {
            # These keys should match the server names used in @fast.agent definitions
            "narrative_engine": {
                "command": "python",
                # Ensure this module path is correct relative to how it's run
                "args": ["mcp_server/server.py", "--transport", "stdio"] # Example - adjust as needed
                # Or potentially use the module structure if servers are importable:
                # "args": ["-m", "ai_writing_agency.servers.narrative_engine"]
            },
            "character_engine": {
                "command": "python",
                "args": ["mcp_server/server.py", "--transport", "stdio"] # Example - adjust as needed
                # "args": ["-m", "ai_writing_agency.servers.character_engine"]
            },
            "archetypal_patterns": {
                "command": "python",
                 "args": ["mcp_server/server.py", "--transport", "stdio"] # Example - adjust as needed
               # "args": ["-m", "ai_writing_agency.servers.archetypal_patterns"]
            },
            "symbolic_system": {
                "command": "python",
                 "args": ["mcp_server/server.py", "--transport", "stdio"] # Example - adjust as needed
                #"args": ["-m", "ai_writing_agency.servers.symbolic_system"]
            }
        }

        try:
            fast_config = {}
            if config_path.exists():
                with open(config_path, 'r') as file:
                    fast_config = yaml.safe_load(file) or {}

            if "mcp" not in fast_config:
                fast_config["mcp"] = {}
            if "servers" not in fast_config["mcp"]:
                fast_config["mcp"]["servers"] = {}

            updated = False
            current_servers = fast_config["mcp"]["servers"]
            for server_name, server_config in default_servers.items():
                if server_name not in current_servers:
                    current_servers[server_name] = server_config
                    updated = True

            if updated:
                config_path.parent.mkdir(parents=True, exist_ok=True)
                with open(config_path, 'w') as file:
                    yaml.dump(fast_config, file, default_flow_style=False)
                logger.info(f"Updated fast-agent configuration '{config_path}' with narrative servers")
                self.mcp_servers = current_servers # Reload
            else:
                 logger.info(f"Narrative servers already configured in '{config_path}'")

        except Exception as e:
            logger.error(f"Error updating fast-agent configuration '{config_path}': {e}")

    async def run_narrative_agent(self, instruction: Optional[str] = None, model: Optional[str] = None) -> Any:
        """
        Run the predefined 'narrative_assistant' agent.

        Args:
            instruction: Custom instruction (overrides default if supported by fast-agent API).
            model: Model to use (overrides default).

        Returns:
            Agent session/handle or None on error.
        """
        if not self.fast_agent_available or not self.fast:
            logger.error("Cannot run narrative agent: fast-agent not available or not initialized.")
            return None

        self.ensure_narrative_servers()

        try:
            # Runtime arguments for the agent run
            run_args = {}
            if model:
                run_args['model'] = model
            if instruction:
                 # Check fast-agent documentation for how to override instruction at runtime
                 # This might involve sending it as the first message or a specific run parameter.
                 # Placeholder: Assume it's passed via run() if supported, otherwise it uses the default.
                 # run_args['instruction'] = instruction # If supported
                 pass

            # Run the agent defined statically above
            async with self.fast.run("narrative_assistant", **run_args) as agent_session:
                # If instruction override is needed via message:
                if instruction:
                    await agent_session.send(f"Use this instruction: {instruction}") # Example
                # Return the session object for interaction
                return agent_session
        except Exception as e:
            logger.error(f"Error running narrative agent: {e}")
            return None

    async def run_writing_workflow(self, project_data: Optional[Dict[str, Any]] = None) -> Any:
        """
        Run the predefined 'writing_workflow'.

        Args:
            project_data: Initial data for the workflow.

        Returns:
            Workflow session/handle or None on error.
        """
        if not self.fast_agent_available or not self.fast:
            logger.error("Cannot run writing workflow: fast-agent not available or not initialized.")
            return None

        self.ensure_narrative_servers()

        try:
            async with self.fast.run("writing_workflow") as workflow_session:
                if project_data:
                    # Send initial data to the first agent in the chain (concept_developer)
                    # Adjust based on fast-agent API for initializing chain state
                    initial_prompt = f"Initialize project with the following data: {project_data}"
                    logger.info(f"Initializing writing workflow with: {initial_prompt[:100]}...")
                    # Assuming the session allows targeting the first agent or has an init method
                    # await workflow_session.concept_developer.send(initial_prompt)
                    await workflow_session.send(initial_prompt) # Or send to the workflow itself

                return workflow_session
        except Exception as e:
            logger.error(f"Error running writing workflow: {e}")
            return None

    async def run_evaluator_optimizer_workflow(self, initial_prompt: Optional[str] = None) -> Any:
        """
        Run the predefined 'story_refinement' evaluator-optimizer workflow.

         Args:
            initial_prompt: The initial prompt to start the generation/refinement.

        Returns:
            Workflow session/handle or None on error.
        """
        if not self.fast_agent_available or not self.fast:
            logger.error("Cannot run evaluator-optimizer workflow: fast-agent not available or not initialized.")
            return None

        self.ensure_narrative_servers()

        try:
            async with self.fast.run("story_refinement") as eo_session:
                 if initial_prompt:
                     # Send the initial prompt to start the process
                     logger.info(f"Starting story refinement with prompt: {initial_prompt[:100]}...")
                     await eo_session.send(initial_prompt)
                 else:
                     logger.warning("Running story refinement workflow without an initial prompt.")
                 return eo_session
        except Exception as e:
            logger.error(f"Error running evaluator-optimizer workflow: {e}")
            return None

    def generate_mcp_server_files(self, directory: str = "./ai_writing_agency/servers") -> None:
        """
        Generate placeholder MCP server implementation files.
        NOTE: This now generates very basic placeholders. The actual server logic
        needs to be implemented correctly in these files or in mcp_server/server.py.

        Args:
            directory: Directory to create server files in
        """
        # Removed complex generation logic as it was likely incorrect
        # and server definitions seem centralized in mcp_server/server.py
        # This function might be deprecated or simplified further.

        target_dir = Path(directory)
        target_dir.mkdir(parents=True, exist_ok=True)

        init_path = target_dir / "__init__.py"
        if not init_path.exists():
            with open(init_path, "w") as f:
                f.write('"""AI Writing Agency MCP Server implementations (Placeholders)."""\n')
            logger.info(f"Created {init_path}")

        placeholder_content = """
import asyncio
# Add necessary imports for mcp.server, mcp.transport, etc.
# Add imports for your application logic (e.g., archetypal_framework)

# Define your MCP server class here

async def main():
    print(f"Running {__name__} placeholder server...")
    # Add server initialization and run logic here

if __name__ == "__main__":
    asyncio.run(main())
"""

        # Only create placeholder files if they don't exist to avoid overwriting
        server_files = [
            "narrative_engine.py",
            "character_engine.py",
            "archetypal_patterns.py",
            "symbolic_system.py"
        ]

        for filename in server_files:
            file_path = target_dir / filename
            if not file_path.exists():
                with open(file_path, "w") as f:
                    f.write(placeholder_content.strip())
                logger.info(f"Generated placeholder server file: {file_path}")
            else:
                 logger.info(f"Server file already exists (skipping generation): {file_path}")


class FastAgentComponent(ProcessingComponent):
    """
    Component for integrating with the fast-agent framework.
    """

    def __init__(self, name: str = "FastAgentComponent", **config_options):
        super().__init__(name, **config_options)
        self.integration = FastAgentIntegration()
        self.active_sessions = {}

    def _initialize_state(self) -> Dict[str, Any]:
        return {
            "initialized": self.integration.fast_agent_available,
            "last_error": None
        }

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process actions related to fast-agent integration.
        Actions: run_agent, run_workflow, send_message, close_session
        """
        if not self.integration.fast_agent_available:
            return {"error": "fast-agent integration not available", "status": "failed"}

        action = input_data.get("action")
        session_id = input_data.get("session_id")
        self.state["last_error"] = None

        try:
            if action == "run_agent":
                agent_name = input_data.get("agent_name", "narrative_assistant") # Default to narrative_assistant
                instruction = input_data.get("instruction")
                model = input_data.get("model")

                if agent_name != "narrative_assistant":
                     return {"error": f"Running agent '{agent_name}' not implemented yet.", "status": "failed"}

                session = asyncio.run(self.integration.run_narrative_agent(instruction, model))
                if session:
                    new_session_id = f"agent_session_{len(self.active_sessions)}"
                    self.active_sessions[new_session_id] = session
                    return {"session_id": new_session_id, "status": "running", "type": agent_name}
                else:
                    return {"error": "Failed to run narrative agent", "status": "failed"}

            elif action == "run_workflow":
                workflow_name = input_data.get("workflow_name")
                initial_data = input_data.get("initial_data")
                session = None

                if workflow_name == "writing_workflow":
                    session = asyncio.run(self.integration.run_writing_workflow(initial_data))
                elif workflow_name == "story_refinement":
                    session = asyncio.run(self.integration.run_evaluator_optimizer_workflow(initial_data))
                else:
                     return {"error": f"Unknown or unsupported workflow: {workflow_name}", "status": "failed"}

                if session:
                    new_session_id = f"workflow_session_{len(self.active_sessions)}"
                    self.active_sessions[new_session_id] = session
                    return {"session_id": new_session_id, "status": "running", "type": workflow_name}
                else:
                    return {"error": f"Failed to run workflow '{workflow_name}'", "status": "failed"}

            elif action == "send_message":
                if not session_id:
                    return {"error": "No session_id provided for send_message", "status": "failed"}
                session = self.active_sessions.get(session_id)
                if not session:
                    return {"error": f"Session '{session_id}' not found or inactive", "status": "failed"}
                prompt = input_data.get("prompt")
                if not prompt:
                    return {"error": "No prompt provided for send_message", "status": "failed"}

                # Assuming the session object returned by fast.run() has a send method
                result = asyncio.run(session.send(prompt))
                # The structure of 'result' depends on the fast-agent implementation
                return {"session_id": session_id, "status": "message_sent", "result": result}

            elif action == "close_session":
                 if not session_id:
                    return {"error": "No session_id provided for close_session", "status": "failed"}
                 session = self.active_sessions.pop(session_id, None)
                 if not session:
                    return {"error": f"Session '{session_id}' not found", "status": "failed"}

                 # Add logic here to properly close/clean up the fast-agent session if needed
                 # e.g., await session.close() if available
                 try:
                      # Check if the session object has an async close method
                      if hasattr(session, 'close') and asyncio.iscoroutinefunction(session.close):
                          asyncio.run(session.close())
                      # Or potentially a sync close
                      elif hasattr(session, 'close'):
                           session.close()
                      logger.info(f"Closed session {session_id}")
                 except Exception as close_err:
                     logger.warning(f"Error trying to explicitly close session {session_id}: {close_err}")

                 return {"session_id": session_id, "status": "closed"}

            else:
                return {"error": f"Unknown action: {action}", "status": "failed"}

        except Exception as e:
            logger.error(f"Error processing fast-agent action '{action}': {e}")
            self.state["last_error"] = str(e)
            return {"error": str(e), "status": "failed"}

# --- Global Instance --- #

# Initialize the integration manager (attempts to init fast-agent)
fast_agent_integration = FastAgentIntegration()

# Initialize the processing component (uses the integration manager)
fast_agent_component = FastAgentComponent()
