#!/usr/bin/env python3
"""
Vercel API endpoint for MCP server root
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json

app = FastAPI()

@app.get("/")
def root():
    """Root endpoint - MCP server info"""
    return {
        "name": "NeuroWeave Knowledge Graph MCP Server",
        "version": "1.0.0", 
        "description": "Remote codebase analysis and interactive knowledge graph generation",
        "transport": "http",
        "author": "mhmalvi",
        "repository": "https://github.com/mhmalvi/neuro-weave-knowledge-graph",
        "capabilities": ["tools", "resources"],
        "tools": [
            {
                "name": "analyze_codebase",
                "description": "Analyze a local codebase structure"
            },
            {
                "name": "analyze_github_repo", 
                "description": "Clone and analyze a GitHub repository"
            },
            {
                "name": "generate_codebase_graph",
                "description": "Generate interactive knowledge graph visualization"
            },
            {
                "name": "get_repo_info",
                "description": "Get GitHub repository information"
            }
        ],
        "installation": {
            "cli": "claude mcp add --transport http codebase-kg https://neuroweave-mcp.vercel.app",
            "requirements": ["OpenAI API Key (optional for enhanced features)"]
        }
    }

# For Vercel
def handler(request):
    import json
    from fastapi.responses import JSONResponse
    
    if request.method == "GET":
        return JSONResponse(content=root())
    else:
        return JSONResponse(content={"error": "Method not allowed"}, status_code=405)

