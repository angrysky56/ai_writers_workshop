# Generating Your Post-Biological Existence Story

This guide walks you through the process of using local AI models to generate a complete story from your "Post-Biological Existence" project.

## Prerequisites

1. Make sure Ollama is installed and running:
   ```bash
   ollama serve
   ```

2. Ensure you have the necessary models:
   ```bash
   # Check available models
   ollama list
   
   # Pull the recommended model if not already installed
   ollama pull CognitiveComputations/dolphin-mistral-nemo:12b
   ```

3. Activate your Python environment:
   ```bash
   cd ./ai_writers_workshop
   source .venv/bin/activate
   ```

## Method 1: Using the One-Step Script (Recommended)

The simplest way to generate your story is to use the provided script:

```bash
# Make sure you're in the project directory
cd ./ai_writers_workshop

# Run the script
./generate_post_biological_story.sh
```

This script:
- Checks dependencies and Ollama status
- Uses the specialized post-biological writer agent
- Saves the story to the project's drafts directory

The story generation may take a significant amount of time (potentially hours for a full story) as the AI carefully crafts a coherent narrative from your project components.

## Method 2: Running the Story Generator Manually

If you want more control over the process:

```bash
# With default options:
python generate_story.py post_biological_existence

# With a specific model:
python generate_story.py post_biological_existence --model ai-writer-toolkit-qwen3:30b-a3b

# With a specific output file:
python generate_story.py post_biological_existence --output my_story.md
```

## Method 3: Using the FastAgent Tools Directly

For advanced users who want to interact directly with the agent:

1. Check the FastAgent status:
   ```bash
   python -c "from mcp_server.fastagent_integration.fastagent_tools import check_fastagent_status; print(check_fastagent_status())"
   ```

2. List available scripts:
   ```bash
   python -c "from mcp_server.fastagent_integration.fastagent_tools import list_scripts; print(list_scripts())"
   ```

3. Run the agent and get a session ID:
   ```python
   import asyncio
   from mcp_server.fastagent_integration.fastagent_tools import run_agent
   
   async def main():
       result = await run_agent(
           script_name="post_biological_writer",
           prompt="Generate a story for post_biological_existence project",
           model="ai-writer-toolkit-qwen3:30b-a3b"
       )
       print(f"Session ID: {result['session_id']}")
       print(result['response'])
   
   asyncio.run(main())
   ```

4. Send additional messages to the session if needed:
   ```python
   import asyncio
   from mcp_server.fastagent_integration.fastagent_tools import send_message
   
   async def main():
       result = await send_message(
           session_id="YOUR_SESSION_ID",
           message="Please continue the story"
       )
       print(result['response'])
   
   asyncio.run(main())
   ```

## Accessing the Generated Story

The generated story will be saved to:
```
/home/ty/Repositories/ai_workspace/ai_writers_workshop/output/projects/post_biological_existence/drafts/post_biological_existence_generated_story.md
```

You can also specify a custom output location using the `--output` parameter with the generator script.

## Tips for Better Results

1. **Model Choice**:
   - `ai-writer-toolkit-qwen3:30b-a3b` is recommended for best quality
   - Use larger models for more coherent, complex narratives
   - Use smaller models if speed is a priority

2. **System Requirements**:
   - The story generation process can be memory-intensive
   - Ensure you have enough RAM (at least 8GB for smaller models, 16GB+ for larger models)
   - If you encounter memory issues, try a smaller model like `qwen3:4b`

3. **Run Time Expectations**:
   - Generating a full story can take anywhere from 15 minutes to several hours
   - Larger models take longer but produce better results
   - The script is designed to run in the background

4. **Story Refinement**:
   - The generated story serves as a high-quality draft
   - Review and edit the output for final polishing
   - Use the agent interactively if you want to refine specific sections

## Troubleshooting

1. **Memory Issues**:
   - Error: "Failed to allocate memory"
   - Solution: Try a smaller model or reduce the Ollama context size

2. **Connection Errors**:
   - Error: "Could not connect to Ollama"
   - Solution: Make sure Ollama is running with `ollama serve`

3. **Missing Model**:
   - Error: "Model not found"
   - Solution: Install the model with `ollama pull ai-writer-toolkit-qwen3:30b-a3b`

4. **Stuck Generation**:
   - If the generation seems to hang, check Ollama's logs
   - You can restart the process with a different model

For additional help or to report issues, refer to the documentation in the `docs/` directory.
