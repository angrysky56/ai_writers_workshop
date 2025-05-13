#!/usr/bin/env python
"""
AI Writing Agency - Main Application

This is the main entry point for the AI Writing Agency application, providing
command-line interface and initialization functionality.
"""

import os
import sys
import logging
import argparse
import asyncio
import sys # Import sys
from pathlib import Path # Import Path
from typing import Dict, List, Any, Optional

# Add project root to sys.path to find the AI_writing_agency module
sys.path.append(str(Path(__file__).resolve().parent.parent))

from AI_writing_agency.components.config import config # Corrected case
from AI_writing_agency.components.core import ModuleRegistry, ProjectRegistry, initialize_modules # Corrected case
from AI_writing_agency.components.archetypal_framework import archetypal_framework # Corrected case
from AI_writing_agency.components.fast_agent_integration import fast_agent_integration # Corrected case

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.get("framework.log_level", "INFO")),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="AI Writing Agency")
    
    # Command subparsers
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Initialize command
    init_parser = subparsers.add_parser("init", help="Initialize the AI Writing Agency")
    init_parser.add_argument(
        "--config", 
        help="Path to custom configuration file"
    )
    
    # Create project command
    create_parser = subparsers.add_parser("create", help="Create a new project")
    create_parser.add_argument(
        "name",
        help="Name of the project"
    )
    create_parser.add_argument(
        "--type",
        default="story",
        choices=["story", "novel", "article", "script"],
        help="Type of project to create"
    )
    create_parser.add_argument(
        "--description",
        help="Description of the project"
    )
    
    # List projects command
    list_parser = subparsers.add_parser("list", help="List existing projects")
    
    # Run workflow command
    run_parser = subparsers.add_parser("run", help="Run a workflow on a project")
    run_parser.add_argument(
        "project",
        help="Name of the project"
    )
    run_parser.add_argument(
        "workflow",
        help="Name of the workflow to run"
    )
    run_parser.add_argument(
        "--input",
        help="Input data for the workflow (JSON format)"
    )
    
    # Start server command
    server_parser = subparsers.add_parser("server", help="Start MCP servers")
    server_parser.add_argument(
        "--all",
        action="store_true",
        help="Start all available MCP servers"
    )
    server_parser.add_argument(
        "--server",
        action="append",
        help="Specific server(s) to start"
    )
    server_parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Base port for servers (each server uses a consecutive port)"
    )
    
    # Interactive mode command
    interactive_parser = subparsers.add_parser("interactive", help="Start interactive session")
    interactive_parser.add_argument(
        "--project",
        help="Project to work with"
    )
    
    return parser.parse_args()

async def start_mcp_server(server_name: str, port: int):
    """
    Start an MCP server.
    
    Args:
        server_name: Name of the server to start
        port: Port to use for the server
    """
    logger.info(f"Starting MCP server: {server_name} on port {port}")
    
    # Import the server module
    try:
        # Corrected case for module path
        module_path = f"AI_writing_agency.servers.{server_name}"
        server_module = __import__(module_path, fromlist=["main"])
        
        # Create and start the server
        if hasattr(server_module, "main"):
            # Replace the default port if the server uses a transport that supports it
            # This is a bit hacky, but works for our initial implementation
            old_args = sys.argv
            sys.argv = [old_args[0], "--port", str(port)]
            
            await server_module.main()
            
            # Restore original args
            sys.argv = old_args
        else:
            logger.error(f"Server module {server_name} does not have a main function")
    except ImportError as e:
        logger.error(f"Failed to import server module {server_name}: {e}")
    except Exception as e:
        logger.error(f"Error starting server {server_name}: {e}")

async def start_all_mcp_servers(server_names: List[str], base_port: int):
    """
    Start multiple MCP servers.
    
    Args:
        server_names: List of server names to start
        base_port: Base port to use (each server gets a consecutive port)
    """
    tasks = []
    
    for i, server_name in enumerate(server_names):
        port = base_port + i
        tasks.append(start_mcp_server(server_name, port))
    
    await asyncio.gather(*tasks)

def init_agency(config_path: Optional[str] = None):
    """
    Initialize the AI Writing Agency.
    
    Args:
        config_path: Path to custom configuration file
    """
    logger.info("Initializing AI Writing Agency")
    
    # Load custom configuration if provided
    if config_path and os.path.exists(config_path):
        config.__init__(config_path)
    
    # Ensure archetypal framework data files exist
    archetypal_framework.create_default_files()
    
    # Initialize fast-agent integration
    if fast_agent_integration.fast_agent_available:
        fast_agent_integration.ensure_narrative_servers()
        fast_agent_integration.generate_mcp_server_files()
    else:
        logger.warning("fast-agent not available. Some features will be disabled.")
    
    # Initialize modules
    if initialize_modules():
        logger.info("Successfully initialized all modules")
    else:
        logger.warning("Some modules failed to initialize")
    
    # Discover existing projects
    projects = ProjectRegistry.discover_projects()
    logger.info(f"Discovered {len(projects)} existing projects")

def create_project(name: str, project_type: str, description: str = ""):
    """
    Create a new project.
    
    Args:
        name: Name of the project
        project_type: Type of the project
        description: Description of the project
    """
    from AI_writing_agency.components.core import Project # Corrected case
    
    # Check if project already exists
    existing_project = ProjectRegistry.get_project(name)
    if existing_project:
        logger.error(f"Project '{name}' already exists")
        return False
    
    # Create the project
    project = Project(
        name=name,
        project_type=project_type,
        description=description
    )
    
    # Save the project
    try:
        project_path = project.save()
        logger.info(f"Created project '{name}' at {project_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to create project '{name}': {e}")
        return False

def list_projects():
    """List all existing projects."""
    projects = ProjectRegistry.discover_projects()
    
    if not projects:
        print("No projects found")
        return
    
    print(f"Found {len(projects)} project(s):")
    for project in projects:
        print(f"  - {project.name} ({project.project_type}): {project.description}")

def run_workflow(project_name: str, workflow_name: str, input_data: Optional[str] = None):
    """
    Run a workflow on a project.
    
    Args:
        project_name: Name of the project
        workflow_name: Name of the workflow to run
        input_data: Input data for the workflow (JSON format)
    """
    import json
    
    # Find the project
    projects = ProjectRegistry.discover_projects()
    project = next((p for p in projects if p.name == project_name), None)
    
    if not project:
        logger.error(f"Project '{project_name}' not found")
        return
    
    # Check if the workflow exists
    if workflow_name not in project.pipelines:
        logger.error(f"Workflow '{workflow_name}' not found in project '{project_name}'")
        return
    
    # Parse input data
    parsed_input = {}
    if input_data:
        try:
            parsed_input = json.loads(input_data)
        except json.JSONDecodeError:
            logger.error("Failed to parse input data as JSON")
            return
    
    # Run the workflow
    try:
        result = project.run_pipeline(workflow_name, parsed_input)
        logger.info(f"Workflow '{workflow_name}' completed successfully")
        
        # Print the result
        print("Workflow result:")
        print(json.dumps(result, indent=2))
    except Exception as e:
        logger.error(f"Error running workflow '{workflow_name}': {e}")

def start_interactive_session(project_name: Optional[str] = None):
    """
    Start an interactive session.
    
    Args:
        project_name: Name of the project to work with
    """
    import json
    
    print("AI Writing Agency - Interactive Session")
    print("Type 'help' for a list of commands, 'exit' to quit")
    
    # Load the project if specified
    project = None
    if project_name:
        projects = ProjectRegistry.discover_projects()
        project = next((p for p in projects if p.name == project_name), None)
        
        if project:
            print(f"Loaded project: {project.name} ({project.project_type})")
        else:
            print(f"Project '{project_name}' not found")
    
    # Interactive loop
    while True:
        try:
            command = input("\n> ").strip()
            
            if command.lower() in ("exit", "quit"):
                break
            
            if command.lower() == "help":
                print("Available commands:")
                print("  help                - Show this help message")
                print("  exit, quit          - Exit the interactive session")
                print("  list projects       - List all projects")
                print("  load project <name> - Load a project")
                print("  create project <name> [type] [description] - Create a new project")
                print("  info                - Show information about the loaded project")
                print("  run <workflow>      - Run a workflow on the loaded project")
                print("  mcp start <server>  - Start an MCP server")
                print("  agent create        - Create a fast-agent agent")
                continue
            
            if command.lower() == "list projects":
                list_projects()
                continue
            
            if command.lower().startswith("load project "):
                parts = command.split(" ", 2)
                if len(parts) < 3:
                    print("Usage: load project <name>")
                    continue
                
                project_name = parts[2]
                projects = ProjectRegistry.discover_projects()
                project = next((p for p in projects if p.name == project_name), None)
                
                if project:
                    print(f"Loaded project: {project.name} ({project.project_type})")
                else:
                    print(f"Project '{project_name}' not found")
                
                continue
            
            if command.lower().startswith("create project "):
                parts = command.split(" ", 3)
                if len(parts) < 3:
                    print("Usage: create project <name> [type] [description]")
                    continue
                
                project_name = parts[2]
                project_type = "story"
                description = ""
                
                if len(parts) > 3:
                    remaining = parts[3]
                    type_and_desc = remaining.split(" ", 1)
                    
                    if type_and_desc[0] in ("story", "novel", "article", "script"):
                        project_type = type_and_desc[0]
                        
                        if len(type_and_desc) > 1:
                            description = type_and_desc[1]
                    else:
                        description = remaining
                
                if create_project(project_name, project_type, description):
                    # Load the newly created project
                    projects = ProjectRegistry.discover_projects()
                    project = next((p for p in projects if p.name == project_name), None)
                    print(f"Created and loaded project: {project.name} ({project.project_type})")
                
                continue
            
            if command.lower() == "info":
                if not project:
                    print("No project loaded. Use 'load project <name>' to load a project.")
                    continue
                
                print(f"Project: {project.name}")
                print(f"Type: {project.project_type}")
                print(f"Description: {project.description}")
                print(f"Creation date: {project.creation_date}")
                
                if project.pipelines:
                    print("Workflows:")
                    for pipeline_name in project.pipelines:
                        print(f"  - {pipeline_name}")
                else:
                    print("No workflows defined")
                
                continue
            
            if command.lower().startswith("run "):
                if not project:
                    print("No project loaded. Use 'load project <name>' to load a project.")
                    continue
                
                parts = command.split(" ", 1)
                if len(parts) < 2:
                    print("Usage: run <workflow>")
                    continue
                
                workflow_name = parts[1]
                
                if workflow_name not in project.pipelines:
                    print(f"Workflow '{workflow_name}' not found in project '{project.name}'")
                    continue
                
                # Get input data
                print("Enter input data (JSON format, empty to use default):")
                input_data = input().strip()
                
                # Run the workflow
                try:
                    parsed_input = {}
                    if input_data:
                        parsed_input = json.loads(input_data)
                    
                    result = project.run_pipeline(workflow_name, parsed_input)
                    print("Workflow result:")
                    print(json.dumps(result, indent=2))
                except Exception as e:
                    print(f"Error running workflow: {e}")
                
                continue
            
            if command.lower().startswith("mcp start "):
                parts = command.split(" ", 2)
                if len(parts) < 3:
                    print("Usage: mcp start <server>")
                    continue
                
                server_name = parts[2]
                
                try:
                    print(f"Starting MCP server: {server_name}")
                    asyncio.run(start_mcp_server(server_name, 8000))
                except KeyboardInterrupt:
                    print("Server stopped")
                except Exception as e:
                    print(f"Error starting server: {e}")
                
                continue
            
            if command.lower() == "agent create":
                if not fast_agent_integration.fast_agent_available:
                    print("fast-agent integration not available")
                    continue
                
                print("Creating a narrative agent...")
                
                # Get instruction
                print("Enter instruction (or leave empty for default):")
                instruction = input().strip()
                
                # Get model
                print("Enter model (or leave empty for default):")
                model = input().strip()
                
                try:
                    # Updated based on previous refactoring of fast_agent_integration
                    # Use run_narrative_agent and manage sessions
                    session = asyncio.run(fast_agent_integration.run_narrative_agent(
                        instruction if instruction else None,
                        model if model else None
                    ))
                    
                    if session: # Check if session was created
                        print("Successfully started narrative agent session.")
                        # Store session maybe? Or handle interaction differently?
                        # The previous .interactive() call might not work on the session object.
                        # This part needs clarification on how interactive sessions with fast-agent are handled.
                        print("Interactive session with agent needs further implementation based on fast-agent API.")
                        # Placeholder: 
                        # agent_id = f"interactive_agent_{id(session)}"
                        # active_sessions[agent_id] = session # Requires active_sessions dict
                        # Run interaction loop here using session.send() and print results
                    else:
                        print("Failed to start narrative agent session")
                except Exception as e:
                    print(f"Error creating narrative agent: {e}")
                
                continue
            
            print(f"Unknown command: {command}")
            print("Type 'help' for a list of commands")
        
        except KeyboardInterrupt:
            print("\nUse 'exit' to quit")
            continue
        except Exception as e:
            print(f"Error: {e}")
            continue

def main():
    """Main entry point for the AI Writing Agency."""
    args = parse_arguments()
    
    if args.command == "init":
        init_agency(args.config)
    
    elif args.command == "create":
        create_project(args.name, args.type, args.description or "")
    
    elif args.command == "list":
        list_projects()
    
    elif args.command == "run":
        run_workflow(args.project, args.workflow, args.input)
    
    elif args.command == "server":
        # Determine which servers to start
        servers_to_start = []
        
        if args.all:
            # Start all available servers
            server_dir = os.path.join(os.path.dirname(__file__), "servers")
            
            if os.path.exists(server_dir):
                for filename in os.listdir(server_dir):
                    if filename.endswith(".py") and not filename.startswith("__"):
                        servers_to_start.append(filename[:-3])  # Remove .py extension
        elif args.server:
            servers_to_start = args.server
        else:
            logger.error("No servers specified. Use --all to start all servers or --server to specify individual servers.")
            return
        
        if servers_to_start:
            try:
                print(f"Starting {len(servers_to_start)} MCP server(s) on ports {args.port}-{args.port + len(servers_to_start) - 1}")
                asyncio.run(start_all_mcp_servers(servers_to_start, args.port))
            except KeyboardInterrupt:
                print("Servers stopped")
    
    elif args.command == "interactive":
        start_interactive_session(args.project)
    
    else:
        # Default to initializing if no command is provided
        init_agency()
        
        # Start interactive session
        start_interactive_session()

if __name__ == "__main__":
    main()
