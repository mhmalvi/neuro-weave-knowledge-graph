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

# Enhanced analysis components (serverless-compatible)
def analyze_github_repo_contents(repo_url: str, max_files: int = 50) -> Dict[str, Any]:
    """Enhanced GitHub repository analysis with file contents"""
    try:
        # Extract owner/repo from URL
        parsed = urlparse(repo_url)
        path_parts = parsed.path.strip("/").split("/")
        if len(path_parts) < 2:
            raise ValueError("Invalid GitHub repository URL")
        
        owner, repo = path_parts[0], path_parts[1]
        
        # Use GitHub API to get repository information
        api_url = f"https://api.github.com/repos/{owner}/{repo}"
        headers = {"Accept": "application/vnd.github.v3+json"}
        
        github_token = os.getenv("GITHUB_TOKEN")
        if github_token:
            headers["Authorization"] = f"token {github_token}"
        
        response = requests.get(api_url, headers=headers, timeout=10)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch repo info: {response.text}")
        
        repo_info = response.json()
        
        # Get repository contents (tree)
        tree_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{repo_info.get('default_branch', 'main')}?recursive=1"
        tree_response = requests.get(tree_url, headers=headers, timeout=15)
        
        files = []
        classes = []
        functions = []
        imports = []
        
        if tree_response.status_code == 200:
            tree_data = tree_response.json()
            file_count = 0
            
            for item in tree_data.get("tree", []):
                if file_count >= max_files:
                    break
                    
                if item["type"] == "blob" and item["path"].endswith(('.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rs')):
                    files.append({
                        "path": item["path"],
                        "size": item.get("size", 0),
                        "type": "file",
                        "language": item["path"].split('.')[-1] if '.' in item["path"] else "unknown"
                    })
                    file_count += 1
        
        analysis = {
            "repo_info": repo_info,
            "files": files,
            "classes": classes,
            "functions": functions,
            "imports": imports,
            "metrics": {
                "total_files": len(files),
                "total_classes": len(classes),
                "total_functions": len(functions),
                "total_imports": len(imports),
                "language": repo_info.get("language", "Unknown"),
                "stars": repo_info.get("stargazers_count", 0),
                "forks": repo_info.get("forks_count", 0),
                "size_kb": repo_info.get("size", 0),
                "open_issues": repo_info.get("open_issues_count", 0)
            },
            "analysis_type": "serverless_github_api"
        }
        
        return analysis
        
    except Exception as e:
        raise Exception(f"Error analyzing repository: {str(e)}")

def analyze_codebase_enhanced_serverless(repo_url: str) -> Dict[str, Any]:
    """Serverless-compatible enhanced codebase analysis via GitHub API"""
    try:
        # Use the enhanced GitHub analysis
        analysis = analyze_github_repo_contents(repo_url, max_files=100)
        
        # Add enhanced metrics and patterns detection (simplified for serverless)
        file_extensions = {}
        total_size = 0
        
        for file_info in analysis["files"]:
            ext = file_info.get("language", "unknown")
            file_extensions[ext] = file_extensions.get(ext, 0) + 1
            total_size += file_info.get("size", 0)
        
        # Simple pattern detection based on file structure
        patterns = []
        if "js" in file_extensions or "ts" in file_extensions:
            if any("component" in f["path"].lower() for f in analysis["files"]):
                patterns.append("React/Component Pattern")
            if any("test" in f["path"].lower() for f in analysis["files"]):
                patterns.append("Test-Driven Development")
        
        if "py" in file_extensions:
            if any("models" in f["path"].lower() for f in analysis["files"]):
                patterns.append("Model-View Architecture")
            if any("__init__.py" in f["path"] for f in analysis["files"]):
                patterns.append("Python Package Structure")
        
        # Enhanced analysis result
        enhanced_result = {
            **analysis,
            "enhanced_metrics": {
                "file_extensions": file_extensions,
                "total_size_bytes": total_size,
                "patterns_detected": patterns,
                "directory_structure": len(set(f["path"].split("/")[0] for f in analysis["files"] if "/" in f["path"])),
                "analysis_depth": "serverless_enhanced"
            },
            "semantic_clusters": [
                {
                    "name": f"{ext.upper()} Files",
                    "count": count,
                    "percentage": round((count / len(analysis["files"])) * 100, 1) if analysis["files"] else 0
                }
                for ext, count in file_extensions.items()
            ]
        }
        
        return enhanced_result
        
    except Exception as e:
        raise Exception(f"Error performing enhanced serverless analysis: {str(e)}")

def generate_codebase_graph_serverless(analysis_data: dict, format_type: str = "json") -> Dict[str, Any]:
    """Generate a serverless-compatible knowledge graph representation"""
    try:
        files = analysis_data.get("files", [])
        metrics = analysis_data.get("metrics", {})
        
        # Create nodes and edges for the graph
        nodes = []
        edges = []
        
        # Add file nodes
        for i, file_info in enumerate(files[:50]):  # Limit for performance
            nodes.append({
                "id": f"file_{i}",
                "label": file_info["path"].split("/")[-1],
                "type": "file",
                "language": file_info.get("language", "unknown"),
                "size": file_info.get("size", 0),
                "path": file_info["path"]
            })
        
        # Add language cluster nodes
        file_extensions = analysis_data.get("enhanced_metrics", {}).get("file_extensions", {})
        for ext, count in file_extensions.items():
            nodes.append({
                "id": f"lang_{ext}",
                "label": f"{ext.upper()} ({count} files)",
                "type": "language_cluster",
                "count": count
            })
        
        # Create edges between files and language clusters
        for i, file_info in enumerate(files[:50]):
            ext = file_info.get("language", "unknown")
            edges.append({
                "from": f"file_{i}",
                "to": f"lang_{ext}",
                "type": "belongs_to"
            })
        
        # Generate simple HTML representation
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Codebase Knowledge Graph</title>
            <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
        </head>
        <body>
            <div id="graph" style="height: 600px;"></div>
            <script>
                const nodes = new vis.DataSet({json.dumps(nodes)});
                const edges = new vis.DataSet({json.dumps(edges)});
                const container = document.getElementById('graph');
                const data = {{ nodes: nodes, edges: edges }};
                const options = {{
                    nodes: {{ shape: 'dot', size: 10 }},
                    physics: {{ stabilization: false }}
                }};
                const network = new vis.Network(container, data, options);
            </script>
        </body>
        </html>
        """
        
        graph_result = {
            "nodes": nodes,
            "edges": edges,
            "statistics": {
                "total_nodes": len(nodes),
                "total_edges": len(edges),
                "file_nodes": len([n for n in nodes if n["type"] == "file"]),
                "cluster_nodes": len([n for n in nodes if n["type"] == "language_cluster"])
            },
            "html_visualization": html_content if format_type == "html" else None,
            "format": format_type
        }
        
        return graph_result
        
    except Exception as e:
        raise Exception(f"Error generating serverless codebase graph: {str(e)}")

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
            },
            {
                "name": "analyze_codebase_enhanced",
                "description": "Perform comprehensive enhanced analysis on GitHub repository with patterns, relationships, and file structure (serverless version)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "repo_url": {
                            "type": "string",
                            "description": "GitHub repository URL for enhanced serverless analysis"
                        }
                    },
                    "required": ["repo_url"]
                }
            },
            {
                "name": "generate_codebase_graph",
                "description": "Generate interactive knowledge graph from GitHub repository analysis data (serverless version)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "repo_url": {
                            "type": "string",
                            "description": "GitHub repository URL to analyze and generate graph from"
                        },
                        "format": {
                            "type": "string",
                            "description": "Output format: 'json' or 'html'",
                            "enum": ["json", "html"],
                            "default": "json"
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
        
        elif tool_name == "analyze_codebase_enhanced":
            repo_url = arguments.get("repo_url")
            if not repo_url:
                return create_json_rpc_response(
                    id_val,
                    error=create_json_rpc_error(MCPJsonRpcError.INVALID_PARAMS, "repo_url is required")
                )
            
            try:
                analysis = analyze_codebase_enhanced_serverless(repo_url)
                
                summary = f"""🔬 **Enhanced Serverless Codebase Analysis Complete!**

🌐 **Repository:** {analysis["repo_info"].get("name", "Unknown")}
🔗 **URL:** {repo_url}
⭐ **Stars:** {analysis["metrics"]["stars"]}
🍴 **Forks:** {analysis["metrics"]["forks"]}

📊 **Enhanced Analysis Results:**
• **Files Analyzed:** {analysis["metrics"]["total_files"]}
• **Languages Detected:** {len(analysis.get("enhanced_metrics", {}).get("file_extensions", {}))}
• **Total Size:** {analysis.get("enhanced_metrics", {}).get("total_size_bytes", 0)} bytes
• **Directory Structure:** {analysis.get("enhanced_metrics", {}).get("directory_structure", 0)} top-level directories

🧬 **Patterns Detected:**
{chr(10).join(f'• {pattern}' for pattern in analysis.get("enhanced_metrics", {}).get("patterns_detected", []))}

📈 **Semantic Clusters:**
{chr(10).join(f'• {cluster["name"]}: {cluster["count"]} files ({cluster["percentage"]}%)' for cluster in analysis.get("semantic_clusters", []))}

🚀 **Enhanced serverless analysis provides insights into repository structure, patterns, and semantic organization!**

📊 **Note:** This is an enhanced serverless analysis using GitHub API with pattern detection and clustering."""
                
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
                            "text": f"❌ Error performing enhanced analysis: {str(e)}"
                        }
                    ]
                })
        
        elif tool_name == "generate_codebase_graph":
            repo_url = arguments.get("repo_url")
            format_type = arguments.get("format", "json")
            
            if not repo_url:
                return create_json_rpc_response(
                    id_val,
                    error=create_json_rpc_error(MCPJsonRpcError.INVALID_PARAMS, "repo_url is required")
                )
            
            try:
                # First get enhanced analysis data
                analysis = analyze_codebase_enhanced_serverless(repo_url)
                
                # Generate the knowledge graph
                graph_result = generate_codebase_graph_serverless(analysis, format_type)
                
                summary = f"""🕸️ **Interactive Knowledge Graph Generated!**

🌐 **Repository:** {analysis["repo_info"].get("name", "Unknown")}
🔗 **Source:** {repo_url}

📊 **Graph Statistics:**
• **Total Nodes:** {graph_result["statistics"]["total_nodes"]}
• **Total Edges:** {graph_result["statistics"]["total_edges"]}
• **File Nodes:** {graph_result["statistics"]["file_nodes"]}
• **Language Clusters:** {graph_result["statistics"]["cluster_nodes"]}
• **Format:** {graph_result["format"]}

🎯 **Graph Features:**
• Interactive node exploration
• Language-based clustering
• File relationship mapping
• Repository structure visualization

{"🌐 **HTML Visualization Generated!** The graph includes interactive vis.js visualization." if format_type == "html" else "📊 **JSON Data Generated!** Use the graph data for custom visualization."}

🚀 **Serverless knowledge graph provides comprehensive repository insights through interactive visualization!**"""
                
                content = [{"type": "text", "text": summary}]
                
                # Add HTML content if requested
                if format_type == "html" and graph_result["html_visualization"]:
                    content.append({
                        "type": "text",
                        "text": f"\n\n**HTML Visualization Code:**\n```html\n{graph_result['html_visualization'][:1000]}...\n```"
                    })
                
                return create_json_rpc_response(id_val, {"content": content})
                
            except Exception as e:
                return create_json_rpc_response(id_val, {
                    "content": [
                        {
                            "type": "text",
                            "text": f"❌ Error generating codebase graph: {str(e)}"
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