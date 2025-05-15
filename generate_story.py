#!/usr/bin/env python
"""
Story Generator Workflow

This script automates the process of generating a complete story from a project
by using FastAgent integration with local LLMs.
"""

import sys
import os
import asyncio
import json
import argparse
from pathlib import Path

# Add the parent directory to sys.path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

from mcp_server.fastagent_integration.fastagent_tools import (
    run_agent, 
    send_message,
    close_session
)

async def generate_story(project_id: str, model: str = None, output_file: str = None):
    """
    Generate a complete story from a project using FastAgent.
    
    Args:
        project_id: ID of the project to generate a story from
        model: Optional name of the Ollama model to use
        output_file: Optional file to save the story to
    """
    print(f"Generating story for project '{project_id}'...")
    
    # Determine which agent script to use
    agent_script = "post_biological_writer" if project_id == "post_biological_existence" else "story_generator"
    
    # Initial prompt for the agent
    prompt = f"""
    Please generate a complete story based on the project '{project_id}'.

    Follow these steps:
    1. First, get the project details using get_writing_project(project_id="{project_id}")
    2. Then, compile the narrative using compile_narrative(project_id="{project_id}", format="markdown")
    3. Finally, use the compiled information to generate a complete, polished narrative
    
    Take your time to create a high-quality narrative that integrates all the project components
    into a cohesive and engaging story.
    """
    
    try:
        # Run the agent with the prompt
        print(f"Starting agent '{agent_script}'...")
        result = await run_agent(
            script_name=agent_script,
            prompt=prompt, 
            model=model
        )
        
        session_id = result["session_id"]
        response_content = result["response"]["content"]
        
        print(f"Initial response received. Session ID: {session_id}")
        print(f"Agent is working on the story...")
        
        # Save the story to a file
        if output_file:
            output_path = Path(output_file)
        else:
            # Default output path
            output_dir = project_root / "output" / "projects" / project_id / "drafts"
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"{project_id}_generated_story.md"
        
        with open(output_path, "w") as f:
            f.write(response_content)
        
        print(f"Story generated and saved to {output_path}")
        
        # Close the session
        close_result = close_session(session_id)
        print(f"Session closed: {close_result['status']}")
        
        return output_path
    
    except Exception as e:
        print(f"Error generating story: {e}")
        raise

def main():
    """Main entry point for the story generator workflow."""
    parser = argparse.ArgumentParser(description="Generate a complete story from a project")
    parser.add_argument("project_id", help="ID of the project to generate a story from")
    parser.add_argument("--model", help="Name of the Ollama model to use")
    parser.add_argument("--output", help="File to save the story to")
    
    args = parser.parse_args()
    
    # Run the story generator
    asyncio.run(generate_story(args.project_id, args.model, args.output))

if __name__ == "__main__":
    main()
