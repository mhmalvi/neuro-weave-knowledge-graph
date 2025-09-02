#!/usr/bin/env python3
"""
Main MCP API endpoint for Vercel deployment
Handles all MCP protocol requests
"""

import asyncio
import json
import os
import sys
import logging
from typing import Any, Dict, List, Optional

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

try:
    from fastapi import FastAPI, HTTPException, Request
    from fastapi.responses import JSONResponse
    
    # Import our MCP components (simplified for serverless)
    import ast
    import subprocess
    from urllib.parse import urlparse
    import requests
    import time
    
except ImportError as e:
    logging.error(f"Import error: {e}")

# Simplified analyzer for serverless environment
class ServerlessCodebaseAnalyzer:
    def __init__(self):
        self.supported_extensions = {".py", ".js", ".ts", ".java", ".cpp", ".c", ".h"}
    
    def analyze_github_repo(self, repo_url: str) -> Dict[str, Any]:
        """Analyze GitHub repository via API (no cloning in serverless)"""
        try:
            # Extract owner/repo from URL
            parsed = urlparse(repo_url)
            path_parts = parsed.path.strip("/").split("/")
            if len(path_parts) < 2:
                raise ValueError("Invalid GitHub repository URL")
            
            owner, repo = path_parts[0], path_parts[1]
            
            # Use GitHub API to get repository information
            api_url = f"https://api.github.com/repos/{owner}/{repo}"
            headers = {}
            
            github_token = os.getenv("GITHUB_TOKEN")
            if github_token:
                headers["Authorization"] = f"token {github_token}"
            
            response = requests.get(api_url, headers=headers, timeout=10)
            if response.status_code != 200:
                raise Exception(f"Failed to fetch repo info: {response.text}")
            
            repo_info = response.json()
            
            # Get repository contents
            contents_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
            contents_response = requests.get(contents_url, headers=headers, timeout=10)
            
            analysis = {
                "repo_info": repo_info,
                "files": [],
                "classes": [],
                "functions": [],
                "imports": [],
                "metrics": {
                    "total_files": repo_info.get("size", 0),
                    "total_classes": 0,
                    "total_functions": 0, 
                    "total_imports": 0,
                    "language": repo_info.get("language", "Unknown"),
                    "stars": repo_info.get("stargazers_count", 0),
                    "forks": repo_info.get("forks_count", 0)
                }
            }
            
            return analysis
            
        except Exception as e:
            raise Exception(f"Error analyzing repository: {str(e)}")

app = FastAPI()
analyzer = ServerlessCodebaseAnalyzer()

async def handle_mcp_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Handle MCP protocol requests"""
    method = request_data.get("method")
    params = request_data.get("params", {})
    
    if method == "initialize":
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {},
                "resources": {}
            },
            "serverInfo": {
                "name": "codebase-knowledge-graph",
                "version": "1.0.0"
            }
        }
    
    elif method == "tools/list":
        return {
            "tools": [
                {
                    "name": "analyze_github_repo",
                    "description": "Analyze a GitHub repository structure and metadata",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "repo_url": {
                                "type": "string",
                                "description": "GitHub repository URL"
                            }
                        },
                        "required": ["repo_url"]
                    }
                },
                {
                    "name": "get_repo_info",
                    "description": "Get basic information about a GitHub repository",
                    "inputSchema": {
                        "type": "object", 
                        "properties": {
                            "repo_url": {
                                "type": "string",
                                "description": "GitHub repository URL"
                            }
                        },
                        "required": ["repo_url"]
                    }
                }
            ]
        }
    
    elif method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name == "analyze_github_repo":
            repo_url = arguments.get("repo_url")
            if not repo_url:
                raise HTTPException(status_code=400, detail="repo_url is required")
            
            try:
                analysis = analyzer.analyze_github_repo(repo_url)
                
                summary = f"""🔍 **GitHub Repository Analysis Complete!**

🌐 **Repository:** {analysis["repo_info"].get("name", "Unknown")}
🔗 **URL:** {repo_url}
⭐ **Stars:** {analysis["metrics"]["stars"]}
🍴 **Forks:** {analysis["metrics"]["forks"]}
📝 **Language:** {analysis["metrics"]["language"]}

📈 **Repository Stats:**
• **Size:** {analysis["metrics"]["total_files"]} KB
• **Last Updated:** {analysis["repo_info"].get("updated_at", "Unknown")}
• **License:** {analysis["repo_info"].get("license", {}).get("name", "None") if analysis["repo_info"].get("license") else "None"}

🚀 **Repository analyzed successfully via GitHub API!**

📊 **Note:** This is a serverless analysis using GitHub API. For full codebase analysis with file-level details, use the local MCP server."""
                
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": summary
                        }
                    ]
                }
            except Exception as e:
                return {
                    "content": [
                        {
                            "type": "text", 
                            "text": f"❌ Error analyzing repository: {str(e)}"
                        }
                    ]
                }
        
        elif tool_name == "get_repo_info":
            repo_url = arguments.get("repo_url")
            if not repo_url:
                raise HTTPException(status_code=400, detail="repo_url is required")
            
            try:
                analysis = analyzer.analyze_github_repo(repo_url)
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(analysis["repo_info"], indent=2, default=str)
                        }
                    ]
                }
            except Exception as e:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"❌ Error getting repository info: {str(e)}"
                        }
                    ]
                }
        
        else:
            raise HTTPException(status_code=400, detail=f"Unknown tool: {tool_name}")
    
    else:
        raise HTTPException(status_code=400, detail=f"Unknown method: {method}")

@app.post("/mcp")
async def mcp_endpoint(request: Request):
    """Main MCP endpoint"""
    try:
        body = await request.json()
        result = await handle_mcp_request(body)
        return result
    except Exception as e:
        logging.error(f"MCP endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# For Vercel
def handler(request):
    import json
    from fastapi.responses import JSONResponse
    
    try:
        if request.method == "POST":
            body = json.loads(request.body.decode())
            
            # Create event loop for async handling
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                result = loop.run_until_complete(handle_mcp_request(body))
                return JSONResponse(content=result)
            finally:
                loop.close()
        else:
            return JSONResponse(content={"error": "Method not allowed"}, status_code=405)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)