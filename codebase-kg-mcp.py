#!/usr/bin/env python3
"""
Global wrapper for the codebase knowledge graph MCP server
"""
import os
import sys

# Add the project directory to Python path
project_dir = r"I:\CYBERPUNK\Neuoro-weave-KG\knowledge-graph-llms"
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

# Change working directory to project directory
os.chdir(project_dir)

# Import and run the MCP server
if __name__ == "__main__":
    from mcp_server import main
    import asyncio
    asyncio.run(main())