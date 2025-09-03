from http.server import BaseHTTPRequestHandler
import json
import os
import sys
from urllib.parse import urlparse
import requests
from typing import Dict, Any, Optional, List

# Current MCP Protocol version
MCP_VERSION = "2025-06-18"

def create_json_rpc_response(id_val: Any, result: Any = None, error: Optional[Dict] = None) -> Dict[str, Any]:
    """Create a JSON-RPC 2.0 response"""
    response = {
        "jsonrpc": "2.0",
        "id": id_val
    }
    
    if error:
        response["error"] = error
    else:
        response["result"] = result
    
    return response

def create_json_rpc_error(code: int, message: str, data: Any = None) -> Dict[str, Any]:
    """Create a JSON-RPC 2.0 error object"""
    error = {
        "code": code,
        "message": message
    }
    if data is not None:
        error["data"] = data
    return error

class MCPJsonRpcError:
    """JSON-RPC 2.0 Error codes"""
    PARSE_ERROR = -32700
    INVALID_REQUEST = -32600
    METHOD_NOT_FOUND = -32601
    INVALID_PARAMS = -32602
    INTERNAL_ERROR = -32603

def analyze_github_repo(repo_url: str) -> Dict[str, Any]:
    """Analyze GitHub repository via API (serverless)"""
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

def handle_mcp_request(request_data: dict) -> dict:
    """Handle MCP protocol requests with proper JSON-RPC 2.0 format"""
    
    # Validate JSON-RPC format
    if not isinstance(request_data, dict):
        return create_json_rpc_response(
            None, 
            error=create_json_rpc_error(MCPJsonRpcError.INVALID_REQUEST, "Request must be a JSON object")
        )
    
    jsonrpc = request_data.get("jsonrpc")
    if jsonrpc != "2.0":
        return create_json_rpc_response(
            request_data.get("id"),
            error=create_json_rpc_error(MCPJsonRpcError.INVALID_REQUEST, "JSON-RPC version must be 2.0")
        )
    
    id_val = request_data.get("id")
    method = request_data.get("method")
    params = request_data.get("params", {})
    
    if not method:
        return create_json_rpc_response(
            id_val,
            error=create_json_rpc_error(MCPJsonRpcError.INVALID_REQUEST, "Method is required")
        )
    
    # Handle MCP lifecycle methods
    if method == "initialize":
        client_info = params.get("clientInfo", {})
        protocol_version = params.get("protocolVersion", MCP_VERSION)
        
        # Validate protocol version compatibility
        if protocol_version != MCP_VERSION:
            return create_json_rpc_response(
                id_val,
                error=create_json_rpc_error(
                    MCPJsonRpcError.INVALID_PARAMS, 
                    f"Unsupported protocol version. Expected {MCP_VERSION}, got {protocol_version}"
                )
            )
        
        result = {
            "protocolVersion": MCP_VERSION,
            "capabilities": {
                "tools": {
                    "listChanged": False
                },
                "resources": {
                    "subscribe": False,
                    "listChanged": False
                },
                "prompts": {
                    "listChanged": False
                },
                "logging": {}
            },
            "serverInfo": {
                "name": "codebase-knowledge-graph",
                "version": "1.0.0"
            },
            "instructions": "Use analyze_github_repo to analyze GitHub repositories for codebase insights."
        }
        
        return create_json_rpc_response(id_val, result)
    
    elif method == "notifications/initialized":
        # Client acknowledges successful initialization - no response for notifications
        return None
    
    elif method == "ping":
        return create_json_rpc_response(id_val, {})
    
    elif method == "tools/list":
        tools = [
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
        
        return create_json_rpc_response(id_val, {"tools": tools})
    
    elif method == "resources/list":
        # No resources for this server
        return create_json_rpc_response(id_val, {"resources": []})
    
    elif method == "prompts/list":
        # No prompts for this server
        return create_json_rpc_response(id_val, {"prompts": []})
    
    elif method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if not tool_name:
            return create_json_rpc_response(
                id_val,
                error=create_json_rpc_error(MCPJsonRpcError.INVALID_PARAMS, "Tool name is required")
            )
        
        if tool_name == "analyze_github_repo":
            repo_url = arguments.get("repo_url")
            if not repo_url:
                return create_json_rpc_response(
                    id_val,
                    error=create_json_rpc_error(MCPJsonRpcError.INVALID_PARAMS, "repo_url is required")
                )
            
            try:
                analysis = analyze_github_repo(repo_url)
                
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
                
                return create_json_rpc_response(id_val, {
                    "content": [
                        {
                            "type": "text",
                            "text": summary
                        }
                    ]
                })
                
            except Exception as e:
                return create_json_rpc_response(id_val, {
                    "content": [
                        {
                            "type": "text",
                            "text": f"❌ Error analyzing repository: {str(e)}"
                        }
                    ]
                })
        
        elif tool_name == "get_repo_info":
            repo_url = arguments.get("repo_url")
            if not repo_url:
                return create_json_rpc_response(
                    id_val,
                    error=create_json_rpc_error(MCPJsonRpcError.INVALID_PARAMS, "repo_url is required")
                )
            
            try:
                analysis = analyze_github_repo(repo_url)
                return create_json_rpc_response(id_val, {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(analysis["repo_info"], indent=2, default=str)
                        }
                    ]
                })
            except Exception as e:
                return create_json_rpc_response(id_val, {
                    "content": [
                        {
                            "type": "text",
                            "text": f"❌ Error getting repository info: {str(e)}"
                        }
                    ]
                })
        
        else:
            return create_json_rpc_response(
                id_val,
                error=create_json_rpc_error(MCPJsonRpcError.METHOD_NOT_FOUND, f"Unknown tool: {tool_name}")
            )
    
    else:
        return create_json_rpc_response(
            id_val,
            error=create_json_rpc_error(MCPJsonRpcError.METHOD_NOT_FOUND, f"Unknown method: {method}")
        )

class handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        """Handle GET requests - now returns 200 JSON for Claude health probe"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS, GET')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        
        health_response = {
            "ok": True,
            "service": "mcp", 
            "transport": "http",
            "endpoints": ["POST /api/mcp"],
            "version": "1.0.0",
            "server": "codebase-knowledge-graph",
            "protocol": MCP_VERSION,
            "timestamp": json.dumps({"$date": {"$numberLong": str(int(__import__("time").time() * 1000))}})
        }
        self.wfile.write(json.dumps(health_response).encode())
    
    def do_POST(self):
        """Handle POST requests for MCP calls"""
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self._send_error_response(400, MCPJsonRpcError.INVALID_REQUEST, "Empty request body")
                return
            
            body = self.rfile.read(content_length).decode('utf-8')
            
            # Parse JSON
            try:
                request_data = json.loads(body)
            except json.JSONDecodeError as e:
                self._send_error_response(400, MCPJsonRpcError.PARSE_ERROR, f"Invalid JSON: {str(e)}")
                return
            
            # Handle MCP request
            result = handle_mcp_request(request_data)
            
            # Handle notifications (no response)
            if result is None:
                self.send_response(200)
                self.send_header('Content-Length', '0')
                self.end_headers()
                return
            
            # Send JSON-RPC response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS, GET')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
            self.end_headers()
            
            response_json = json.dumps(result, ensure_ascii=False)
            self.wfile.write(response_json.encode('utf-8'))
            
        except Exception as e:
            self._send_error_response(500, MCPJsonRpcError.INTERNAL_ERROR, f"Internal server error: {str(e)}")
    
    def do_OPTIONS(self):
        """Handle preflight CORS requests - returns 204"""
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS, GET')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Access-Control-Max-Age', '86400')
        self.end_headers()
    
    def _send_error_response(self, http_status: int, error_code: int, error_message: str):
        """Send a JSON-RPC error response"""
        error_response = create_json_rpc_response(
            None,
            error=create_json_rpc_error(error_code, error_message)
        )
        
        self.send_response(http_status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response_json = json.dumps(error_response)
        self.wfile.write(response_json.encode('utf-8'))
    
    def log_message(self, format, *args):
        """Override to reduce noise in Vercel logs"""
        # Only log errors, not every request
        if "Error" in str(args) or "error" in str(args):
            super().log_message(format, *args)