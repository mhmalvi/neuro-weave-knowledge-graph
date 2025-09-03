from http.server import BaseHTTPRequestHandler
import json
import os
from urllib.parse import urlparse
import requests
from typing import Dict, Any

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

analyzer = ServerlessCodebaseAnalyzer()

def handle_mcp_request(request_data: dict) -> dict:
    """Handle MCP protocol requests"""
    # Handle JSON-RPC format
    jsonrpc = request_data.get("jsonrpc", "2.0")
    id_val = request_data.get("id", 1)
    method = request_data.get("method")
    params = request_data.get("params", {})
    
    if method == "initialize":
        return {
            "jsonrpc": jsonrpc,
            "id": id_val,
            "result": {
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
        }
    
    elif method == "tools/list":
        return {
            "jsonrpc": jsonrpc,
            "id": id_val,
            "result": {
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
        }
    
    elif method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name == "analyze_github_repo":
            repo_url = arguments.get("repo_url")
            if not repo_url:
                return {
                    "jsonrpc": jsonrpc,
                    "id": id_val,
                    "error": {
                        "code": -32602,
                        "message": "repo_url is required"
                    }
                }
            
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
                    "jsonrpc": jsonrpc,
                    "id": id_val,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": summary
                            }
                        ]
                    }
                }
            except Exception as e:
                return {
                    "jsonrpc": jsonrpc,
                    "id": id_val,
                    "result": {
                        "content": [
                            {
                                "type": "text", 
                                "text": f"❌ Error analyzing repository: {str(e)}"
                            }
                        ]
                    }
                }
        
        elif tool_name == "get_repo_info":
            repo_url = arguments.get("repo_url")
            if not repo_url:
                return {
                    "jsonrpc": jsonrpc,
                    "id": id_val,
                    "error": {
                        "code": -32602,
                        "message": "repo_url is required"
                    }
                }
            
            try:
                analysis = analyzer.analyze_github_repo(repo_url)
                return {
                    "jsonrpc": jsonrpc,
                    "id": id_val,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(analysis["repo_info"], indent=2, default=str)
                            }
                        ]
                    }
                }
            except Exception as e:
                return {
                    "jsonrpc": jsonrpc,
                    "id": id_val,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": f"❌ Error getting repository info: {str(e)}"
                            }
                        ]
                    }
                }
        
        else:
            return {
                "jsonrpc": jsonrpc,
                "id": id_val,
                "error": {
                    "code": -32601,
                    "message": f"Unknown tool: {tool_name}"
                }
            }
    
    else:
        return {
            "jsonrpc": jsonrpc,
            "id": id_val,
            "error": {
                "code": -32601,
                "message": f"Unknown method: {method}"
            }
        }

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Main MCP endpoint"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            request_data = json.loads(body)
            
            result = handle_mcp_request(request_data)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
            
        except Exception as e:
            error_response = {"error": str(e)}
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(error_response).encode())
    
    def do_OPTIONS(self):
        """Handle preflight OPTIONS requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()