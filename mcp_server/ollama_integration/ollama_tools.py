"""
AI Writers Workshop - Ollama Integration

This module provides integration with Ollama LLMs for the AI Writers Workshop MCP server.
"""

import os
import sys
import logging
import json
import subprocess
from typing import Dict, List, Any, Optional, Union

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ai_writers_workshop.ollama")

def _check_ollama_available() -> bool:
    """
    Check if Ollama is available on the system.

    Returns:
        Boolean indicating availability
    """
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode == 0
    except FileNotFoundError:
        logger.warning("Ollama executable not found in PATH")
        return False
    except Exception as e:
        logger.warning(f"Error checking Ollama availability: {e}")
        return False

# Check Ollama availability
OLLAMA_AVAILABLE = _check_ollama_available()

def list_models() -> List[Dict[str, Any]]:
    """
    List available Ollama models.

    Returns:
        List of model information dictionaries
    """
    if not OLLAMA_AVAILABLE:
        logger.error("Ollama not available")
        raise RuntimeError("Ollama not available")

    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            check=True
        )

        # Parse the output (format: NAME TAG SIZE MODIFIED)
        models = []
        lines = result.stdout.strip().split('\n')

        # Skip the header line
        for line in lines[1:]:
            if not line.strip():
                continue

            parts = line.split()
            if len(parts) >= 4:
                name = parts[0]
                tag = parts[1]
                size = parts[2]

                models.append({
                    "name": name,
                    "tag": tag,
                    "size": size,
                    "model_id": f"{name}:{tag}"
                })

        return models
    except subprocess.CalledProcessError as e:
        logger.error(f"Error listing Ollama models: {e}")
        logger.error(f"STDERR: {e.stderr}")
        raise RuntimeError(f"Error listing Ollama models: {e.stderr}")
    except Exception as e:
        logger.error(f"Unexpected error listing Ollama models: {e}")
        raise

def run_prompt(
    prompt: str,
    model: str = "ai-writer-toolkit-qwen3:30b-a3b",
    temperature: float = 0.8,
    max_tokens: int = 8192
) -> str:
    """
    Run a prompt with an Ollama model.

    Args:
        prompt: The prompt to run
        model: Ollama model to use
        temperature: Sampling temperature (0-1)
        max_tokens: Maximum tokens to generate

    Returns:
        Generated text
    """
    if not OLLAMA_AVAILABLE:
        logger.error("Ollama not available")
        raise RuntimeError("Ollama not available")

    # Prepare the generate command
    try:
        # Create a JSON request body
        request = {
            "model": model,
            "prompt": prompt,
            "temperature": temperature,
            "num_predict": max_tokens
        }

        # Use the Ollama CLI for simplicity
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True,
            check=True
        )

        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running Ollama prompt: {e}")
        logger.error(f"STDERR: {e.stderr}")
        raise RuntimeError(f"Error running Ollama prompt: {e.stderr}")
    except Exception as e:
        logger.error(f"Unexpected error running Ollama prompt: {e}")
        raise

def run_prompt_streaming(
    prompt: str,
    model: str = "ai-writer-toolkit-qwen3:30b-a3b",
    temperature: float = 0.8,
    max_tokens: int = 8192
):
    """
    Run a prompt with an Ollama model in streaming mode.

    Args:
        prompt: The prompt to run
        model: Ollama model to use
        temperature: Sampling temperature (0-1)
        max_tokens: Maximum tokens to generate

    Yields:
        Generated text chunks
    """
    if not OLLAMA_AVAILABLE:
        logger.error("Ollama not available")
        raise RuntimeError("Ollama not available")

    try:
        # Use subprocess with Popen for streaming
        process = subprocess.Popen(
            ["ollama", "run", model, prompt],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Read output line by line
        for line in iter(process.stdout.readline, ''):
            yield line.strip()

        # Check for errors
        process.wait()
        if process.returncode != 0:
            stderr = process.stderr.read()
            logger.error(f"Error running Ollama prompt: {stderr}")
            raise RuntimeError(f"Error running Ollama prompt: {stderr}")

    except Exception as e:
        logger.error(f"Unexpected error running Ollama prompt: {e}")
        raise

# Helper function to format a system prompt and user prompt for Ollama
def format_combined_prompt(system_prompt: str, user_prompt: str) -> str:
    """
    Format a system prompt and user prompt for Ollama.

    Args:
        system_prompt: System instructions
        user_prompt: User query

    Returns:
        Formatted prompt
    """
    return f"<|system|>\n{system_prompt}\n<|user|>\n{user_prompt}\n<|assistant|>\n"

# Function to check if Ollama is running, and provide friendly error messages
def check_ollama_status() -> Dict[str, Any]:
    """
    Check if Ollama service is running.

    Returns:
        Dictionary with status information
    """
    if not OLLAMA_AVAILABLE:
        return {
            "running": False,
            "error": "Ollama not installed. Please install Ollama from ollama.ai",
            "install_command": "curl -fsSL https://ollama.com/install.sh | sh"
        }

    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            check=False
        )

        if result.returncode == 0:
            return {
                "running": True,
                "models": len(list_models())
            }
        else:
            return {
                "running": False,
                "error": "Ollama installed but not running or responding",
                "start_command": "ollama serve"
            }
    except Exception as e:
        return {
            "running": False,
            "error": f"Error checking Ollama status: {str(e)}",
            "start_command": "ollama serve"
        }
