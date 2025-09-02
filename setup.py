#!/usr/bin/env python3
"""
Setup script for codebase-knowledge-graph MCP server
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="codebase-knowledge-graph-mcp",
    version="1.0.0",
    author="Neuro-weave-KG",
    description="MCP server for codebase knowledge graph analysis and visualization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=['mcp_server', 'codebase_visualizer', 'generate_knowledge_graph'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "codebase-kg-mcp=mcp_server:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.py", "*.html", "*.js", "*.css"],
    },
)