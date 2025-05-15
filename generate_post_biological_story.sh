#!/bin/bash

# Generate Story for Post-Biological Existence Project
# This script runs the story generation process using the specialized agent

# Change to the project directory
cd "$(dirname "$0")"

# Activate the virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "Virtual environment activated"
fi

# Install any required dependencies
echo "Checking for dependencies..."
uv pip install -r requirements.txt

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "Error: Ollama is not running. Please start Ollama first."
    exit 1
fi

# Run the story generation script
echo "Starting story generation for post_biological_existence..."
echo "This process may take a while to complete (potentially hours for a full story)."
echo "The story will be saved in the output/projects/post_biological_existence/drafts directory."

python generate_story.py post_biological_existence --model "CognitiveComputations/dolphin-mistral-nemo:12b"

echo "Story generation process complete!"
