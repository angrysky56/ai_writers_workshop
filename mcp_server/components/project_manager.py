"""
Project Manager Component for AI Writers Workshop

Handles project creation, organization, and management with a hierarchical structure.
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

class ProjectManager:
    """Manages narrative projects with hierarchical organization."""
    
    def __init__(self, base_dir: Union[str, Path] = "output"):
        """
        Initialize the project manager.
        
        Args:
            base_dir: Base directory for all outputs
        """
        self.base_dir = Path(base_dir)
        
        # Set up main directory structure
        self.projects_dir = self.base_dir / "projects"
        self.library_dir = self.base_dir / "library"
        
        # Create directory structure if it doesn't exist
        self.projects_dir.mkdir(exist_ok=True, parents=True)
        self.library_dir.mkdir(exist_ok=True, parents=True)
        
        # Create library subdirectories
        (self.library_dir / "archetypes").mkdir(exist_ok=True)
        (self.library_dir / "patterns").mkdir(exist_ok=True)
        (self.library_dir / "symbols").mkdir(exist_ok=True)
        
        # Legacy directories for backward compatibility
        self.legacy_dirs = {
            "characters": self.base_dir / "characters",
            "scenes": self.base_dir / "scenes",
            "outlines": self.base_dir / "outlines",
            "analyses": self.base_dir / "analyses",
            "symbols": self.base_dir / "symbols"
        }
        
        # Create legacy directories for backward compatibility
        for dir_path in self.legacy_dirs.values():
            dir_path.mkdir(exist_ok=True, parents=True)
    
    def create_project(self, name: str, description: str, project_type: str = "story") -> Dict[str, Any]:
        """
        Create a new project with hierarchical directory structure.
        
        Args:
            name: Project name
            description: Project description
            project_type: Type of project (story, novel, article, script)
            
        Returns:
            Dictionary with project information
        """
        # Create safe project directory name
        dir_name = self._sanitize_name(name)
        project_dir = self.projects_dir / dir_name
        
        # Create project directory structure
        project_dir.mkdir(exist_ok=True)
        
        # Create project subdirectories
        subdirs = ["characters", "scenes", "outlines", "analyses", "symbols", "drafts"]
        for subdir in subdirs:
            (project_dir / subdir).mkdir(exist_ok=True)
        
        # Create project metadata
        creation_time = datetime.now().isoformat()
        metadata = {
            "name": name,
            "description": description,
            "type": project_type,
            "created_at": creation_time,
            "modified_at": creation_time,
            "primary_pattern": None,
            "themes": [],
            "main_characters": [],
            "secondary_characters": [],
            "word_count": 0,
            "status": "in_progress",
            "notes": "",
            "elements": {
                "characters": [],
                "scenes": [],
                "outlines": [],
                "analyses": [],
                "symbols": [],
                "drafts": []
            }
        }
        
        # Save metadata to project directory
        metadata_path = project_dir / "metadata.json"
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)
        
        # Create notes file
        with open(project_dir / "notes.md", "w") as f:
            f.write(f"# {name}\n\n{description}\n\n## Notes\n\n")
        
        return {
            **metadata,
            "output_path": str(metadata_path.relative_to(self.base_dir)),
            "project_dir": str(project_dir.relative_to(self.base_dir))
        }
    
    def get_project(self, project_id: str) -> Dict[str, Any]:
        """
        Get project details by project ID.
        
        Args:
            project_id: Project ID (directory name)
            
        Returns:
            Dictionary with project information
        """
        # Get project directory
        project_dir = self.projects_dir / project_id
        
        if not project_dir.exists():
            return {
                "error": f"Project {project_id} not found",
                "available_projects": self.list_projects()["projects"]
            }
        
        # Load metadata
        metadata_path = project_dir / "metadata.json"
        if metadata_path.exists():
            with open(metadata_path, "r") as f:
                metadata = json.load(f)
        else:
            metadata = {
                "name": project_id,
                "error": "Metadata file not found"
            }
        
        return {
            **metadata,
            "output_path": str(metadata_path.relative_to(self.base_dir)),
            "project_dir": str(project_dir.relative_to(self.base_dir))
        }
    
    def update_project(self, project_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update project metadata.
        
        Args:
            project_id: Project ID (directory name)
            updates: Dictionary with fields to update
            
        Returns:
            Dictionary with updated project information
        """
        # Get project details
        project = self.get_project(project_id)
        if "error" in project:
            return project
        
        # Update fields
        project_dir = self.projects_dir / project_id
        metadata_path = project_dir / "metadata.json"
        
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
        
        # Update metadata with new values
        for key, value in updates.items():
            if key in metadata:
                metadata[key] = value
        
        # Always update modified time
        metadata["modified_at"] = datetime.now().isoformat()
        
        # Save updated metadata
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)
        
        return {
            **metadata,
            "output_path": str(metadata_path.relative_to(self.base_dir)),
            "project_dir": str(project_dir.relative_to(self.base_dir))
        }
    
    def add_project_element(self, project_id: str, element_type: str, 
                           element_id: str, element_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add an element reference to project metadata.
        
        Args:
            project_id: Project ID (directory name)
            element_type: Type of element (character, scene, etc.)
            element_id: Element ID
            element_data: Element data for reference
            
        Returns:
            Dictionary with updated project information
        """
        # Get project details
        project = self.get_project(project_id)
        if "error" in project:
            return project
        
        # Update project metadata
        project_dir = self.projects_dir / project_id
        metadata_path = project_dir / "metadata.json"
        
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
        
        # Create reference object
        reference = {
            "id": element_id,
            "name": element_data.get("name", "") or element_data.get("title", "") or element_id,
            "path": f"projects/{project_id}/{element_type}/{element_id}.json",
            "created_at": element_data.get("created_at", datetime.now().isoformat())
        }
        
        # Add element reference to project elements
        if "elements" not in metadata:
            metadata["elements"] = {}
        
        if element_type not in metadata["elements"]:
            metadata["elements"][element_type] = []
        
        # Check if element already exists
        existing = next((e for e in metadata["elements"][element_type] if e["id"] == element_id), None)
        if existing:
            # Update existing reference
            existing.update(reference)
        else:
            # Add new reference
            metadata["elements"][element_type].append(reference)
        
        # Update modified time
        metadata["modified_at"] = datetime.now().isoformat()
        
        # Save updated metadata
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)
        
        return {
            **metadata,
            "output_path": str(metadata_path.relative_to(self.base_dir)),
            "project_dir": str(project_dir.relative_to(self.base_dir))
        }
    
    def save_element(self, project_id: str, element_type: str, 
                    element_data: Dict[str, Any], element_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Save an element to the project directory.
        
        Args:
            project_id: Project ID (directory name)
            element_type: Type of element (character, scene, etc.)
            element_data: Element data to save
            element_id: Optional element ID (will be generated if not provided)
            
        Returns:
            Dictionary with element information including path
        """
        # Get project details
        project = self.get_project(project_id)
        if "error" in project:
            return project
        
        # Get or create element ID
        if not element_id:
            name = element_data.get("name", "") or element_data.get("title", "")
            if name:
                element_id = self._sanitize_name(name)
            else:
                element_id = f"{element_type}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Save to project directory
        project_dir = self.projects_dir / project_id
        element_dir = project_dir / element_type
        element_dir.mkdir(exist_ok=True)
        
        # Add creation timestamp if not present
        if "created_at" not in element_data:
            element_data["created_at"] = datetime.now().isoformat()
        
        # Save element data
        element_path = element_dir / f"{element_id}.json"
        with open(element_path, "w") as f:
            json.dump(element_data, f, indent=2)
        
        # Add element reference to project metadata
        self.add_project_element(project_id, element_type, element_id, element_data)
        
        # Also save to legacy directory for backward compatibility
        if element_type in self.legacy_dirs:
            with open(self.legacy_dirs[element_type] / f"{element_id}.json", "w") as f:
                json.dump(element_data, f, indent=2)
        
        # Return element data with path information
        return {
            **element_data,
            "id": element_id,
            "output_path": f"projects/{project_id}/{element_type}/{element_id}.json"
        }
    
    def list_projects(self) -> Dict[str, List[str]]:
        """
        List all available projects.
        
        Returns:
            Dictionary with list of projects
        """
        project_dirs = [d.name for d in self.projects_dir.glob("*") if d.is_dir()]
        projects = []
        
        for project_id in project_dirs:
            metadata_path = self.projects_dir / project_id / "metadata.json"
            if metadata_path.exists():
                with open(metadata_path, "r") as f:
                    metadata = json.load(f)
                projects.append({
                    "id": project_id,
                    "name": metadata.get("name", project_id),
                    "description": metadata.get("description", ""),
                    "type": metadata.get("type", "unknown"),
                    "status": metadata.get("status", "unknown"),
                    "modified_at": metadata.get("modified_at", "")
                })
        
        return {"projects": projects}
    
    def list_writing_projects(self) -> Dict[str, List[Dict[str, str]]]:
        """
        List all writing projects with basic information.
        
        This is a simplified version of list_projects() that returns
        only essential project information without requiring metadata or names.
        
        Returns:
            Dictionary with list of projects containing minimal info
        """
        project_dirs = [d.name for d in self.projects_dir.glob("*") if d.is_dir()]
        projects = []
        
        for project_id in project_dirs:
            metadata_path = self.projects_dir / project_id / "metadata.json"
            if metadata_path.exists():
                try:
                    with open(metadata_path, "r") as f:
                        metadata = json.load(f)
                    
                    # Include only essential information
                    project_info = {
                        "id": project_id,
                        "name": metadata.get("name", project_id),
                        "type": metadata.get("type", "unknown"),
                    }
                    
                    # Add project to list
                    projects.append(project_info)
                except Exception:
                    # If metadata file is corrupt or missing fields, include minimal info
                    projects.append({
                        "id": project_id,
                        "name": project_id,
                        "type": "unknown"
                    })
            else:
                # If no metadata file, include minimal directory info
                projects.append({
                    "id": project_id,
                    "name": project_id,
                    "type": "unknown"
                })
        
        return {"projects": projects}
    
    def list_project_elements(self, project_id: str, element_type: Optional[str] = None) -> Dict[str, Any]:
        """
        List elements in a project.
        
        Args:
            project_id: Project ID (directory name)
            element_type: Optional type of elements to list
            
        Returns:
            Dictionary with list of elements
        """
        # Get project details
        project = self.get_project(project_id)
        if "error" in project:
            return project
        
        # Get project elements
        if element_type:
            # List specific element type
            element_dir = self.projects_dir / project_id / element_type
            if not element_dir.exists():
                return {
                    "error": f"Element type {element_type} not found in project {project_id}",
                    "available_types": [d.name for d in (self.projects_dir / project_id).glob("*") if d.is_dir()]
                }
            
            elements = []
            for element_path in element_dir.glob("*.json"):
                with open(element_path, "r") as f:
                    element_data = json.load(f)
                elements.append({
                    "id": element_path.stem,
                    "name": element_data.get("name", "") or element_data.get("title", "") or element_path.stem,
                    "path": f"projects/{project_id}/{element_type}/{element_path.name}"
                })
            
            return {element_type: elements}
        else:
            # List all element types
            elements = {}
            for element_dir in (self.projects_dir / project_id).glob("*"):
                if element_dir.is_dir() and element_dir.name not in ["metadata"]:
                    elements[element_dir.name] = []
                    for element_path in element_dir.glob("*.json"):
                        with open(element_path, "r") as f:
                            element_data = json.load(f)
                        elements[element_dir.name].append({
                            "id": element_path.stem,
                            "name": element_data.get("name", "") or element_data.get("title", "") or element_path.stem,
                            "path": f"projects/{project_id}/{element_dir.name}/{element_path.name}"
                        })
            
            return {"elements": elements}
    
    def get_element(self, project_id: str, element_type: str, element_id: str) -> Dict[str, Any]:
        """
        Get a specific element from a project.
        
        Args:
            project_id: Project ID (directory name)
            element_type: Type of element (character, scene, etc.)
            element_id: Element ID
            
        Returns:
            Dictionary with element data
        """
        # Get project details
        project = self.get_project(project_id)
        if "error" in project:
            return project
        
        # Get element data
        element_path = self.projects_dir / project_id / element_type / f"{element_id}.json"
        if not element_path.exists():
            return {
                "error": f"Element {element_id} not found in project {project_id}",
                "available_elements": self.list_project_elements(project_id, element_type)
            }
        
        with open(element_path, "r") as f:
            element_data = json.load(f)
        
        return {
            **element_data,
            "id": element_id,
            "output_path": f"projects/{project_id}/{element_type}/{element_id}.json"
        }
    
    def list_outputs(self) -> Dict[str, Any]:
        """
        List all available outputs in hierarchical structure.
        
        Returns:
            Dictionary with lists of outputs by type
        """
        # Get all projects
        projects = self.list_projects()["projects"]
        
        # Get legacy outputs
        legacy_outputs = {
            key: [p.stem for p in directory.glob("*.json")]
            for key, directory in self.legacy_dirs.items()
        }
        
        return {
            "projects": projects,
            "legacy": legacy_outputs
        }
    
    def _sanitize_name(self, name: str) -> str:
        """Convert a name to a safe directory/file name."""
        return name.lower().replace(" ", "_").replace("-", "_").replace("'", "").replace('"', "")
