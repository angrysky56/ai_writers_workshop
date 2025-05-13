"""
AI Writing Agency - Core Module

This module provides the foundational classes and abstractions for the AI Writing Agency
framework, implementing the core architecture defined in the framework documentation.
"""

import os
import sys
import logging
import inspect
import importlib
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Callable, Type, Union, TypeVar, Generic

from .config import config

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, config.get("framework.log_level", "INFO")))

# Type variables for generic typing
T = TypeVar('T')
InputType = TypeVar('InputType')
OutputType = TypeVar('OutputType')
StateType = TypeVar('StateType')

class ProcessingComponent(ABC, Generic[InputType, OutputType, StateType]):
    """
    Abstract base class for all processing components in the AI Writing Agency.
    
    Implements the standard interface defined in the framework architecture document,
    providing a consistent pattern for component implementation.
    """
    
    def __init__(self, name: str = None, **config_options):
        """
        Initialize the processing component.
        
        Args:
            name: Optional component name override
            **config_options: Component-specific configuration options
        """
        self.name = name or self.__class__.__name__
        self.config_options = config_options
        self.state: StateType = self._initialize_state()
        logger.debug(f"Initialized component: {self.name}")
    
    @abstractmethod
    def _initialize_state(self) -> StateType:
        """
        Initialize the component's internal state.
        
        Returns:
            Initial state object
        """
        pass
    
    @abstractmethod
    def process(self, input_data: InputType) -> OutputType:
        """
        Process the input data according to the component's purpose.
        
        Args:
            input_data: Input data to process
            
        Returns:
            Processing result
        """
        pass
    
    def validate_input(self, input_data: InputType) -> bool:
        """
        Validate that the input data meets the component's requirements.
        
        Args:
            input_data: Input data to validate
            
        Returns:
            Boolean indicating if the input is valid
        """
        # Default implementation always validates
        return True
    
    def get_state(self) -> StateType:
        """
        Get the current state of the component.
        
        Returns:
            Current state
        """
        return self.state
    
    def set_state(self, state: StateType) -> None:
        """
        Set the state of the component.
        
        Args:
            state: New state to set
        """
        self.state = state
    
    def reset(self) -> None:
        """Reset the component to its initial state."""
        self.state = self._initialize_state()


class Module(ABC):
    """
    Base class for modules in the AI Writing Agency.
    
    Modules are collections of related components that work together
    to implement a specific aspect of the writing process.
    """
    
    def __init__(self, name: str = None, **config_options):
        """
        Initialize the module.
        
        Args:
            name: Optional module name override
            **config_options: Module-specific configuration options
        """
        self.name = name or self.__class__.__name__
        self.config_options = config_options
        self.components: Dict[str, ProcessingComponent] = {}
        
        # Register this module with the module registry
        ModuleRegistry.register_module(self)
        
        logger.info(f"Initialized module: {self.name}")
    
    @abstractmethod
    def initialize(self) -> bool:
        """
        Initialize the module and its components.
        
        Returns:
            Boolean indicating successful initialization
        """
        pass
    
    def add_component(self, component: ProcessingComponent) -> None:
        """
        Add a component to the module.
        
        Args:
            component: Component to add
        """
        self.components[component.name] = component
        logger.debug(f"Added component {component.name} to module {self.name}")
    
    def get_component(self, name: str) -> Optional[ProcessingComponent]:
        """
        Get a component by name.
        
        Args:
            name: Name of the component to get
            
        Returns:
            The component or None if not found
        """
        return self.components.get(name)
    
    def remove_component(self, name: str) -> None:
        """
        Remove a component from the module.
        
        Args:
            name: Name of the component to remove
        """
        if name in self.components:
            del self.components[name]
            logger.debug(f"Removed component {name} from module {self.name}")


class Pipeline:
    """
    A processing pipeline that chains multiple components together.
    
    The pipeline ensures that the output of each component is passed
    as input to the next component in the sequence.
    """
    
    def __init__(self, name: str):
        """
        Initialize the pipeline.
        
        Args:
            name: Name of the pipeline
        """
        self.name = name
        self.components: List[ProcessingComponent] = []
        logger.debug(f"Initialized pipeline: {name}")
    
    def add_component(self, component: ProcessingComponent) -> 'Pipeline':
        """
        Add a component to the pipeline.
        
        Args:
            component: Component to add
            
        Returns:
            Self for method chaining
        """
        self.components.append(component)
        logger.debug(f"Added component {component.name} to pipeline {self.name}")
        return self
    
    def process(self, initial_input: Any) -> Any:
        """
        Process data through the pipeline.
        
        Args:
            initial_input: Initial input data for the first component
            
        Returns:
            Output from the final component
        """
        if not self.components:
            logger.warning(f"Pipeline {self.name} has no components")
            return initial_input
        
        current_output = initial_input
        
        for component in self.components:
            try:
                if not component.validate_input(current_output):
                    raise ValueError(f"Input validation failed for component {component.name}")
                
                current_output = component.process(current_output)
                logger.debug(f"Processed through component {component.name} in pipeline {self.name}")
            except Exception as e:
                logger.error(f"Error in pipeline {self.name} at component {component.name}: {e}")
                raise
        
        return current_output
    
    def reset(self) -> None:
        """Reset all components in the pipeline to their initial state."""
        for component in self.components:
            component.reset()
        
        logger.debug(f"Reset all components in pipeline {self.name}")


class Project:
    """
    Represents a writing project within the AI Writing Agency.
    
    A project contains all data, metadata, and processing state
    related to a specific writing endeavor.
    """
    
    def __init__(self, 
                 name: str,
                 project_type: str,
                 description: str = "",
                 metadata: Dict[str, Any] = None):
        """
        Initialize a new project.
        
        Args:
            name: Project name
            project_type: Type of the project (e.g., novel, article, etc.)
            description: Project description
            metadata: Additional project metadata
        """
        self.name = name
        self.project_type = project_type
        self.description = description
        self.metadata = metadata or {}
        self.creation_date = self.metadata.get("creation_date", None)
        self.data: Dict[str, Any] = {}
        self.pipelines: Dict[str, Pipeline] = {}
        
        # Register with the project registry
        ProjectRegistry.register_project(self)
        
        logger.info(f"Created project: {name} ({project_type})")
    
    def add_pipeline(self, pipeline: Pipeline) -> None:
        """
        Add a processing pipeline to the project.
        
        Args:
            pipeline: Pipeline to add
        """
        self.pipelines[pipeline.name] = pipeline
        logger.debug(f"Added pipeline {pipeline.name} to project {self.name}")
    
    def run_pipeline(self, pipeline_name: str, initial_input: Any) -> Any:
        """
        Run a specific pipeline with the given input.
        
        Args:
            pipeline_name: Name of the pipeline to run
            initial_input: Initial input data for the pipeline
            
        Returns:
            Output from the pipeline
        """
        if pipeline_name not in self.pipelines:
            raise ValueError(f"Pipeline {pipeline_name} not found in project {self.name}")
        
        logger.info(f"Running pipeline {pipeline_name} in project {self.name}")
        return self.pipelines[pipeline_name].process(initial_input)
    
    def get_data(self, key: str, default: Any = None) -> Any:
        """
        Get data from the project's data store.
        
        Args:
            key: Data key
            default: Default value if key doesn't exist
            
        Returns:
            The data value or default
        """
        return self.data.get(key, default)
    
    def set_data(self, key: str, value: Any) -> None:
        """
        Set data in the project's data store.
        
        Args:
            key: Data key
            value: Data value
        """
        self.data[key] = value
    
    def save(self, path: Optional[str] = None) -> str:
        """
        Save the project to disk.
        
        Args:
            path: Optional path to save to, uses default if not provided
            
        Returns:
            Path where the project was saved
        """
        import json
        from datetime import datetime
        
        if not path:
            workspace_dir = config.get("framework.workspace_dir", "./workspace")
            project_dir = os.path.join(workspace_dir, "projects", self.name)
            os.makedirs(project_dir, exist_ok=True)
            path = os.path.join(project_dir, "project.json")
        
        # Update metadata
        self.metadata["last_saved"] = datetime.now().isoformat()
        if not self.creation_date:
            self.creation_date = self.metadata["last_saved"]
            self.metadata["creation_date"] = self.creation_date
        
        # Create serializable representation
        project_data = {
            "name": self.name,
            "project_type": self.project_type,
            "description": self.description,
            "metadata": self.metadata,
            "data": self.data
            # Note: Pipelines are not serialized as they contain complex objects
        }
        
        with open(path, 'w') as file:
            json.dump(project_data, file, indent=2)
        
        logger.info(f"Saved project {self.name} to {path}")
        return path
    
    @classmethod
    def load(cls, path: str) -> 'Project':
        """
        Load a project from disk.
        
        Args:
            path: Path to load from
            
        Returns:
            Loaded project
        """
        import json
        
        with open(path, 'r') as file:
            project_data = json.load(file)
        
        project = cls(
            name=project_data["name"],
            project_type=project_data["project_type"],
            description=project_data["description"],
            metadata=project_data["metadata"]
        )
        
        project.data = project_data["data"]
        
        logger.info(f"Loaded project {project.name} from {path}")
        return project


class ModuleRegistry:
    """Static registry for module management."""
    
    _modules: Dict[str, Module] = {}
    
    @classmethod
    def register_module(cls, module: Module) -> None:
        """
        Register a module with the registry.
        
        Args:
            module: Module to register
        """
        cls._modules[module.name] = module
        logger.debug(f"Registered module: {module.name}")
    
    @classmethod
    def get_module(cls, name: str) -> Optional[Module]:
        """
        Get a module by name.
        
        Args:
            name: Name of the module to get
            
        Returns:
            The module or None if not found
        """
        return cls._modules.get(name)
    
    @classmethod
    def get_all_modules(cls) -> Dict[str, Module]:
        """
        Get all registered modules.
        
        Returns:
            Dictionary of all modules
        """
        return cls._modules.copy()
    
    @classmethod
    def discover_modules(cls, package_name: str = "ai_writing_agency.modules") -> List[Module]:
        """
        Discover and load modules from a package.
        
        Args:
            package_name: Package to discover modules in
            
        Returns:
            List of discovered modules
        """
        discovered = []
        
        try:
            package = importlib.import_module(package_name)
            package_path = os.path.dirname(package.__file__)
            
            # Look for Python files in the package
            for filename in os.listdir(package_path):
                if filename.endswith('.py') and not filename.startswith('__'):
                    module_name = filename[:-3]  # Remove .py extension
                    full_module_name = f"{package_name}.{module_name}"
                    
                    try:
                        # Import the module
                        module = importlib.import_module(full_module_name)
                        
                        # Look for Module subclasses in the module
                        for item_name, item in inspect.getmembers(module, inspect.isclass):
                            if issubclass(item, Module) and item is not Module:
                                # Instantiate the module class
                                instance = item()
                                discovered.append(instance)
                                logger.info(f"Discovered module: {instance.name}")
                    except Exception as e:
                        logger.error(f"Error loading module {full_module_name}: {e}")
            
            logger.info(f"Discovered {len(discovered)} modules in package {package_name}")
        except ImportError:
            logger.warning(f"Package {package_name} not found")
        
        return discovered


class ProjectRegistry:
    """Static registry for project management."""
    
    _projects: Dict[str, Project] = {}
    
    @classmethod
    def register_project(cls, project: Project) -> None:
        """
        Register a project with the registry.
        
        Args:
            project: Project to register
        """
        cls._projects[project.name] = project
        logger.debug(f"Registered project: {project.name}")
    
    @classmethod
    def get_project(cls, name: str) -> Optional[Project]:
        """
        Get a project by name.
        
        Args:
            name: Name of the project to get
            
        Returns:
            The project or None if not found
        """
        return cls._projects.get(name)
    
    @classmethod
    def get_all_projects(cls) -> Dict[str, Project]:
        """
        Get all registered projects.
        
        Returns:
            Dictionary of all projects
        """
        return cls._projects.copy()
    
    @classmethod
    def discover_projects(cls, workspace_dir: Optional[str] = None) -> List[Project]:
        """
        Discover and load projects from the workspace.
        
        Args:
            workspace_dir: Optional workspace directory override
            
        Returns:
            List of discovered projects
        """
        import glob
        import json
        
        discovered = []
        
        if not workspace_dir:
            workspace_dir = config.get("framework.workspace_dir", "./workspace")
        
        # Look for project.json files
        project_files = glob.glob(os.path.join(workspace_dir, "projects", "*", "project.json"))
        
        for project_file in project_files:
            try:
                project = Project.load(project_file)
                discovered.append(project)
            except Exception as e:
                logger.error(f"Error loading project from {project_file}: {e}")
        
        logger.info(f"Discovered {len(discovered)} projects in workspace {workspace_dir}")
        return discovered


# Initialize the module system
def initialize_modules() -> bool:
    """
    Initialize the module system.
    
    Discovers and initializes all available modules.
    
    Returns:
        Boolean indicating successful initialization
    """
    # Discover available modules
    modules = ModuleRegistry.discover_modules()
    
    # Initialize each module
    success = True
    for module in modules:
        if not module.initialize():
            logger.error(f"Failed to initialize module: {module.name}")
            success = False
    
    if success:
        logger.info(f"Successfully initialized {len(modules)} modules")
    else:
        logger.warning("Some modules failed to initialize")
    
    return success
