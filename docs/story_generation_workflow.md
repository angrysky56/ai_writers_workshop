# Story Generation Workflow

This document explains how to use the automated story generation workflow to create complete stories from AI Writers Workshop projects.

## Overview

The story generation workflow uses FastAgent integration with local language models (via Ollama or LM Studio) to generate complete, cohesive stories from project components created using the AI Writers Workshop. This allows you to:

1. Develop your story structure, characters, scenes, and symbolic elements using the AI Writers Workshop
2. Generate a complete, literary-quality narrative from these components in a single process
3. Run the generation process overnight or in the background while you do other things

## Prerequisites

- Ollama installed and running (https://ollama.ai/)
- The `ai-writer-toolkit-qwen3:30b-a3b` model or another suitable creative writing model
- An existing project created with AI Writers Workshop

## Using the Workflow

### Option 1: Use the provided script for post-biological existence

To generate a story for the "post_biological_existence" project:

```bash
./generate_post_biological_story.sh
```

This script:
- Checks for dependencies
- Verifies that Ollama is running
- Launches the story generation process with the specialized post-biological writer agent
- Saves the output to the project's drafts directory

### Option 2: Generate a story for any project

You can generate a story for any project using the `generate_story.py` script:

```bash
python generate_story.py <project_id> [--model MODEL_NAME] [--output OUTPUT_FILE]
```

For example:
```bash
python generate_story.py the_quantum_gardener --model qwen3:14b
```

### Arguments:

- `project_id`: The ID of the project to generate a story from (required)
- `--model`: The name of the Ollama model to use (optional, defaults to "mistral")
- `--output`: Path to save the generated story (optional, defaults to the project's drafts directory)

## Available Agent Scripts

1. **story_generator**: General-purpose story generation agent
2. **post_biological_writer**: Specialized agent for post-biological existence narratives

## Creating Custom Agent Scripts

You can create custom agent scripts for specific genres or narrative styles by:

1. Creating a new JSON file in the `mcp_server/fastagent_integration/agent_definitions` directory
2. Defining the instruction, model, and tools for your custom agent
3. Using the agent with the `--agent` argument

## How the Story Generation Works

1. The agent retrieves the project details using `get_writing_project`
2. It compiles the existing scenes and components using `compile_narrative`
3. The agent then generates a cohesive, polished narrative that integrates all project elements
4. The completed story is saved to the specified output location

## Tips for Better Results

- Create comprehensive character profiles, scene descriptions, and outlines for best results
- Use symbolic elements to add thematic depth to your story
- Use specialized models like `ai-writer-toolkit-qwen3:30b-a3b` that are fine-tuned for creative writing
- For long, complex stories, consider breaking the generation into chapters or sections

## Troubleshooting

- If Ollama is not running, start it with `ollama serve`
- If the generation process seems slow, try a smaller model like `qwen3:0.6b` for quicker results
- If you encounter memory issues, reduce the context size in your Ollama configuration

## Extending the Workflow

You can extend the story generation workflow by:

1. Creating custom agent scripts for specific genres or writing styles
2. Modifying the `generate_story.py` script to add additional processing steps
3. Integrating with other tools or services for further refinement

## Example Usage

```bash
# Generate a story for the post_biological_existence project
./generate_post_biological_story.sh

# Generate a story for a different project with a custom model
python generate_story.py philosophical_narrative_inquiry --model qwen3:14b

# Save the output to a specific file
python generate_story.py the_quantum_gardener --output my_quantum_story.md
```
