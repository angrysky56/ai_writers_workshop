"""
AI Writing Agency - Configuration Module

This module provides the core configuration infrastructure for the AI Writing Agency
framework, handling settings for different components, modules, and integrations.
"""

import os
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AgencyConfig:
    """
    Central configuration manager for the AI Writing Agency.
    
    Handles loading configuration from files, environment variables,
    and runtime settings, with appropriate precedence rules.
    """
    
    DEFAULT_CONFIG = {
        "framework": {
            "version": "0.1.0",
            "log_level": "INFO",
            "workspace_dir": "./workspace",
            "default_language_model": "claude-3-7-sonnet-latest"
        },
        "modules": {
            "enabled": [
                "concept_development",
                "narrative_architecture",
                "character_development",
                "prose_generation",
                "content_editing"
            ]
        },
        "language_models": {
            "anthropic": {
                "enabled": True,
                "config_key": "ANTHROPIC_API_KEY",
                "models": ["claude-3-haiku", "claude-3-sonnet", "claude-3-opus"]
            },
            "openai": {
                "enabled": True,
                "config_key": "OPENAI_API_KEY",
                "models": ["gpt-4o", "gpt-4-turbo"]
            },
            "local": {
                "enabled": True,
                "endpoint": "http://localhost:11434",
                "models": ["llama3", "mistral"]
            }
        },
        "fast_agent": {
            "enabled": True,
            "config_path": "./mcp_server/fastagent.config.yaml" # Corrected path relative to repo root
        },
        "archetypal_framework": {
            "enabled": True,
            "patterns_file": "./archetypes/patterns.yaml",
            "character_archetypes_file": "./archetypes/characters.yaml",
            "symbols_file": "./archetypes/symbols.yaml"
        }
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the configuration manager.
        
        Args:
            config_path: Path to the configuration file (optional)
        """
        self.config = self.DEFAULT_CONFIG.copy()
        self.config_path = config_path
        
        # Load configuration in the correct order of precedence
        self._load_config_from_file()
        self._load_config_from_env()
        
        # Ensure workspace directory exists
        self._ensure_workspace()
        
        logger.info(f"Configuration initialized with {len(self.config)} top-level settings")
    
    def _load_config_from_file(self) -> None:
        """Load configuration from the specified YAML file if it exists."""
        if not self.config_path:
            config_paths = [
                Path("./agency_config.yaml"),
                Path("./config/agency_config.yaml"),
                Path(os.path.expanduser("~/.ai_writing_agency/config.yaml"))
            ]
            
            for path in config_paths:
                if path.exists():
                    self.config_path = str(path)
                    break
        
        if self.config_path and os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as file:
                    file_config = yaml.safe_load(file)
                    if file_config:
                        # Deep merge the configurations
                        self._deep_merge(self.config, file_config)
                logger.info(f"Loaded configuration from {self.config_path}")
            except Exception as e:
                logger.error(f"Error loading configuration from {self.config_path}: {e}")
    
    def _load_config_from_env(self) -> None:
        """Load configuration from environment variables."""
        # Handle API keys
        for provider in self.config.get("language_models", {}):
            provider_config = self.config["language_models"][provider]
            env_key = provider_config.get("config_key")
            if env_key and env_key in os.environ:
                provider_config["api_key"] = os.environ[env_key]
        
        # Handle general framework config overrides
        if "AGENCY_LOG_LEVEL" in os.environ:
            self.config["framework"]["log_level"] = os.environ["AGENCY_LOG_LEVEL"]
        
        if "AGENCY_WORKSPACE_DIR" in os.environ:
            self.config["framework"]["workspace_dir"] = os.environ["AGENCY_WORKSPACE_DIR"]
    
    def _deep_merge(self, target: Dict, source: Dict) -> None:
        """
        Recursively merge source dictionary into target dictionary.
        
        Args:
            target: Target dictionary to merge into
            source: Source dictionary to merge from
        """
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._deep_merge(target[key], value)
            else:
                target[key] = value
    
    def _ensure_workspace(self) -> None:
        """Ensure that the workspace directory exists."""
        workspace_dir = Path(self.config["framework"]["workspace_dir"])
        try:
            workspace_dir.mkdir(parents=True, exist_ok=True)
            
            # Create subdirectories
            for subdir in ["projects", "templates", "archives", "resources"]:
                (workspace_dir / subdir).mkdir(exist_ok=True)
                
            logger.info(f"Workspace directory initialized at {workspace_dir}")
        except Exception as e:
            logger.error(f"Failed to create workspace directory: {e}")
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get a configuration value using a dot-notation path.
        
        Args:
            key_path: Dot-notation path to the configuration value
            default: Default value to return if the path doesn't exist
            
        Returns:
            The configuration value or the default value
        """
        parts = key_path.split('.')
        current = self.config
        
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return default
        
        return current
    
    def set(self, key_path: str, value: Any) -> None:
        """
        Set a configuration value using a dot-notation path.
        
        Args:
            key_path: Dot-notation path to the configuration value
            value: Value to set
        """
        parts = key_path.split('.')
        current = self.config
        
        # Navigate to the parent of the target key
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        
        # Set the value at the target key
        current[parts[-1]] = value
    
    def save(self, config_path: Optional[str] = None) -> None:
        """
        Save the current configuration to a YAML file.
        
        Args:
            config_path: Path to save the configuration to (optional)
        """
        save_path = config_path or self.config_path
        if not save_path:
            save_path = "./agency_config.yaml"
        
        try:
            with open(save_path, 'w') as file:
                yaml.dump(self.config, file, default_flow_style=False)
            logger.info(f"Configuration saved to {save_path}")
        except Exception as e:
            logger.error(f"Error saving configuration to {save_path}: {e}")
    
    def load_archetypal_framework(self) -> Dict[str, Any]:
        """
        Load the archetypal framework configuration files.
        
        Returns:
            Dictionary containing the archetypal framework configuration
        """
        framework = {
            "patterns": {},
            "character_archetypes": {},
            "symbols": {}
        }
        
        if not self.config["archetypal_framework"]["enabled"]:
            logger.info("Archetypal framework is disabled")
            return framework
        
        # Load patterns
        patterns_file = self.config["archetypal_framework"]["patterns_file"]
        if os.path.exists(patterns_file):
            try:
                with open(patterns_file, 'r') as file:
                    framework["patterns"] = yaml.safe_load(file) or {}
                logger.info(f"Loaded archetypal patterns from {patterns_file}")
            except Exception as e:
                logger.error(f"Error loading archetypal patterns: {e}")
        
        # Load character archetypes
        characters_file = self.config["archetypal_framework"]["character_archetypes_file"]
        if os.path.exists(characters_file):
            try:
                with open(characters_file, 'r') as file:
                    framework["character_archetypes"] = yaml.safe_load(file) or {}
                logger.info(f"Loaded character archetypes from {characters_file}")
            except Exception as e:
                logger.error(f"Error loading character archetypes: {e}")
        
        # Load symbols
        symbols_file = self.config["archetypal_framework"]["symbols_file"]
        if os.path.exists(symbols_file):
            try:
                with open(symbols_file, 'r') as file:
                    framework["symbols"] = yaml.safe_load(file) or {}
                logger.info(f"Loaded symbolic systems from {symbols_file}")
            except Exception as e:
                logger.error(f"Error loading symbolic systems: {e}")
        
        return framework
    
    def setup_fast_agent_integration(self) -> bool:
        """
        Set up integration with the fast-agent framework.
        
        Returns:
            Boolean indicating success or failure
        """
        if not self.config["fast_agent"]["enabled"]:
            logger.info("Fast-agent integration is disabled")
            return False
        
        config_path = self.config["fast_agent"]["config_path"]
        if not os.path.exists(config_path):
            # Create default fast-agent config
            default_config = {
                "default_model": self.config["framework"]["default_language_model"],
                "mcp": {
                    "servers": {
                        "narrative_engine": {
                            "command": "python",
                            "args": ["-m", "ai_writing_agency.servers.narrative_engine"]
                        },
                        "character_engine": {
                            "command": "python",
                            "args": ["-m", "ai_writing_agency.servers.character_engine"]
                        }
                    }
                }
            }
            
            try:
                os.makedirs(os.path.dirname(config_path), exist_ok=True)
                with open(config_path, 'w') as file:
                    yaml.dump(default_config, file, default_flow_style=False)
                logger.info(f"Created default fast-agent configuration at {config_path}")
                return True
            except Exception as e:
                logger.error(f"Error creating fast-agent configuration: {e}")
                return False
        
        return True


# Create a global configuration instance with default settings
# This can be overridden by modules that need specific configurations
config = AgencyConfig()
