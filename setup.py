#!/usr/bin/env python
"""
AI Writers Workshop - Setup

This module provides the setup configuration for the AI Writers Workshop package.
"""

from setuptools import setup, find_packages

setup(
    name="ai_writers_workshop",
    version="0.1.0",
    description="Model Context Protocol (MCP) server for narrative and character development",
    author="angrysky56",
    author_email="",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "mcp[cli]==1.7.0",  # Pin to 1.7.0 for fast-agent-mcp compatibility
        "pyyaml>=6.0",
        "anyio>=4.0.0",
        "typing_extensions>=4.7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-anyio>=0.0.0",
            "black>=23.7.0",
        ],
        "fastagent": [
            "fast_agent_mcp>=0.2.23",
        ],
    },
    entry_points={
        "console_scripts": [
            "ai-writers-workshop=mcp_server.server:main",
        ],
    },
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
