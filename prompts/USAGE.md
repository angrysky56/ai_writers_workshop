# Using AI Writers Workshop Prompts

This directory contains prompt templates for the AI Writers Workshop MCP server. These prompts help guide AI assistants in creating narrative content, developing characters, and working with archetypal patterns.

## Available Prompts

### Character Creator (`character_creator.json`)

This prompt guides the creation of a character based on archetypal patterns and psychological depth.

Example invocation:
```
Use the character_creator prompt to develop a protagonist for my story.
```

### Structure Analyzer (`structure_analyzer.json`)

Analyzes narrative structure against common archetypal patterns like the Hero's Journey.

Example invocation:
```
Use the structure_analyzer prompt to analyze my story outline.
```

## Creating Custom Prompts

You can create custom prompts by adding new JSON files to this directory. Each prompt should follow this format:

```json
{
    "name": "Prompt Name",
    "description": "Brief description of the prompt's purpose",
    "messages": [
        {
            "role": "system",
            "content": "System instructions for the AI"
        },
        {
            "role": "user",
            "content": "Initial user message or instructions"
        },
        {
            "role": "assistant",
            "content": "Example assistant response"
        }
    ]
}
```

## Integration with MCP

The MCP server automatically loads prompts from this directory. To update or add prompts, simply modify the JSON files and restart the server.

## Best Practices

- Keep prompt instructions clear and specific
- Include examples of expected input and output
- Structure prompts to guide the AI's reasoning process
- Consider the archetypal patterns and narrative theory in your prompt design
