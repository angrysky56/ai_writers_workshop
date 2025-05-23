# Project Output Directory

This directory contains complete story projects with multiple components generated by the AI Writers Workshop.

## Contents

- Project metadata JSON files
- Project subdirectories containing all related content
- Project markdown summary files

## Project Structure

Each project is stored in its own subdirectory with the following structure:
```
project_name/
├── metadata.json         # Project metadata
├── characters/           # Characters in this project
├── scenes/               # Scene files
├── outline.json          # Project outline
├── analysis.json         # Narrative analysis
└── notes.md              # Additional notes
```

## Project Metadata Schema

Project metadata follows this structure:
```json
{
  "name": "Project Name",
  "created_at": "YYYY-MM-DDTHH:MM:SS",
  "modified_at": "YYYY-MM-DDTHH:MM:SS",
  "type": "story|novel|article|script",
  "description": "Project description",
  "primary_pattern": "Primary narrative pattern",
  "themes": ["Theme 1", "Theme 2"],
  "main_characters": ["Character 1", "Character 2"],
  "secondary_characters": ["Character 3", "Character 4"],
  "word_count": 0,
  "status": "in_progress|draft|complete",
  "notes": "Additional notes"
}
```

## Usage

This directory is used by:
- Full project workflows
- Project management tools
- Cross-component analyses

Projects serve as the top-level organizational unit for complex narratives with multiple characters, scenes, and structural elements.
