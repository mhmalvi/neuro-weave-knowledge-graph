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
def analyze_github_repo_contents(repo_url: str, max_files: int = 20, analyze_content: bool = True) -> Dict[str, Any]:
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
                    file_info = {
                        "path": item["path"],
                        "size": item.get("size", 0),
                        "type": "file",
                        "language": item["path"].split('.')[-1] if '.' in item["path"] else "unknown",
                        "sha": item.get("sha")
                    }
                    
                    # Analyze file content if requested and file is small enough
                    if analyze_content and item.get("size", 0) < 50000:  # Skip large files
                        try:
                            content_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{item['path']}"
                            content_response = requests.get(content_url, headers=headers, timeout=10)
                            
                            if content_response.status_code == 200:
                                content_data = content_response.json()
                                if content_data.get("encoding") == "base64":
                                    import base64
                                    content = base64.b64decode(content_data["content"]).decode('utf-8', errors='ignore')
                                    
                                    # Simple code analysis based on language
                                    if item["path"].endswith('.py'):
                                        # Python analysis
                                        py_classes = [line.strip()[6:].split('(')[0].split(':')[0] 
                                                    for line in content.split('\n') 
                                                    if line.strip().startswith('class ')]
                                        py_functions = [line.strip()[4:].split('(')[0] 
                                                      for line in content.split('\n') 
                                                      if line.strip().startswith('def ')]
                                        py_imports = [line.strip() 
                                                    for line in content.split('\n') 
                                                    if line.strip().startswith(('import ', 'from '))]
                                        
                                        classes.extend([{"name": cls, "file": item["path"], "language": "python"} for cls in py_classes])
                                        functions.extend([{"name": func, "file": item["path"], "language": "python"} for func in py_functions])
                                        imports.extend([{"statement": imp, "file": item["path"], "language": "python"} for imp in py_imports])
                                    
                                    elif item["path"].endswith(('.js', '.ts')):
                                        # JavaScript/TypeScript analysis
                                        js_classes = [line.strip()[6:].split(' ')[0].split('{')[0] 
                                                    for line in content.split('\n') 
                                                    if 'class ' in line]
                                        js_functions = [line.strip().split('(')[0].split(' ')[-1] 
                                                      for line in content.split('\n') 
                                                      if ('function ' in line or '=>' in line) and not line.strip().startswith('//')]
                                        js_imports = [line.strip() 
                                                    for line in content.split('\n') 
                                                    if line.strip().startswith(('import ', 'const ', 'require('))]
                                        
                                        classes.extend([{"name": cls, "file": item["path"], "language": "javascript"} for cls in js_classes if cls])
                                        functions.extend([{"name": func, "file": item["path"], "language": "javascript"} for func in js_functions if func])
                                        imports.extend([{"statement": imp, "file": item["path"], "language": "javascript"} for imp in js_imports])
                                    
                                    file_info["content_analyzed"] = True
                                    file_info["lines_of_code"] = len(content.split('\n'))
                        
                        except Exception as content_error:
                            # Skip content analysis if it fails
                            file_info["content_analyzed"] = False
                            pass
                    
                    files.append(file_info)
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
        # Use the enhanced GitHub analysis with content parsing
        analysis = analyze_github_repo_contents(repo_url, max_files=50, analyze_content=True)
        
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
        classes = analysis_data.get("classes", [])
        functions = analysis_data.get("functions", [])
        imports = analysis_data.get("imports", [])
        metrics = analysis_data.get("metrics", {})
        
        # Create nodes and edges for the graph
        nodes = []
        edges = []
        
        # Add file nodes with enhanced data
        for i, file_info in enumerate(files[:30]):  # Limit for performance
            size_category = "small" if file_info.get("size", 0) < 5000 else "medium" if file_info.get("size", 0) < 20000 else "large"
            nodes.append({
                "id": f"file_{i}",
                "label": file_info["path"].split("/")[-1],
                "title": f"File: {file_info['path']}\nSize: {file_info.get('size', 0)} bytes\nLanguage: {file_info.get('language', 'unknown')}\nLines: {file_info.get('lines_of_code', 'N/A')}",
                "type": "file",
                "language": file_info.get("language", "unknown"),
                "size": file_info.get("size", 0),
                "path": file_info["path"],
                "group": file_info.get("language", "unknown"),
                "value": min(file_info.get("size", 0) / 1000, 50),  # Size-based node size
                "color": {
                    "background": "#4CAF50" if file_info.get("language") == "py" else 
                                 "#FF9800" if file_info.get("language") in ["js", "ts"] else 
                                 "#2196F3" if file_info.get("language") == "java" else "#9C27B0"
                }
            })
        
        # Add class nodes
        for i, class_info in enumerate(classes[:20]):
            nodes.append({
                "id": f"class_{i}",
                "label": class_info["name"],
                "title": f"Class: {class_info['name']}\nFile: {class_info['file']}\nLanguage: {class_info['language']}",
                "type": "class",
                "language": class_info["language"],
                "file": class_info["file"],
                "group": "classes",
                "shape": "box",
                "color": {"background": "#FF5722"}
            })
        
        # Add function nodes (top-level functions only)
        for i, func_info in enumerate(functions[:30]):
            nodes.append({
                "id": f"func_{i}",
                "label": func_info["name"],
                "title": f"Function: {func_info['name']}\nFile: {func_info['file']}\nLanguage: {func_info['language']}",
                "type": "function",
                "language": func_info["language"],
                "file": func_info["file"],
                "group": "functions",
                "shape": "triangle",
                "color": {"background": "#607D8B"}
            })
        
        # Add language cluster nodes
        file_extensions = analysis_data.get("enhanced_metrics", {}).get("file_extensions", {})
        for ext, count in file_extensions.items():
            nodes.append({
                "id": f"lang_{ext}",
                "label": f"{ext.upper()}\n({count} files)",
                "title": f"Language: {ext.upper()}\nFiles: {count}",
                "type": "language_cluster",
                "count": count,
                "group": "languages",
                "shape": "ellipse",
                "size": min(count * 3, 40),
                "color": {"background": "#FFC107"}
            })
        
        # Create enhanced edges
        file_to_lang_edges = []
        class_to_file_edges = []
        func_to_file_edges = []
        
        # Files to language clusters
        for i, file_info in enumerate(files[:30]):
            ext = file_info.get("language", "unknown")
            edges.append({
                "from": f"file_{i}",
                "to": f"lang_{ext}",
                "type": "belongs_to",
                "color": {"color": "#999999"},
                "width": 1
            })
        
        # Classes to files
        for i, class_info in enumerate(classes[:20]):
            # Find the file node
            for j, file_info in enumerate(files[:30]):
                if file_info["path"] == class_info["file"]:
                    edges.append({
                        "from": f"class_{i}",
                        "to": f"file_{j}",
                        "type": "defined_in",
                        "color": {"color": "#FF5722"},
                        "width": 2
                    })
                    break
        
        # Functions to files
        for i, func_info in enumerate(functions[:30]):
            # Find the file node
            for j, file_info in enumerate(files[:30]):
                if file_info["path"] == func_info["file"]:
                    edges.append({
                        "from": f"func_{i}",
                        "to": f"file_{j}",
                        "type": "defined_in",
                        "color": {"color": "#607D8B"},
                        "width": 1.5
                    })
                    break
        
        # Generate enhanced HTML representation
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Enhanced Codebase Knowledge Graph</title>
            <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {{ background-color: #1a1a1a; color: #ffffff; }}
                #graph {{ 
                    height: 100vh; 
                    background-color: #1a1a1a; 
                    border: 1px solid #444; 
                }}
                .controls {{ 
                    position: absolute; 
                    top: 10px; 
                    left: 10px; 
                    z-index: 1000; 
                    background: rgba(0,0,0,0.8); 
                    padding: 10px; 
                    border-radius: 5px; 
                }}
                .info-panel {{ 
                    position: absolute; 
                    top: 10px; 
                    right: 10px; 
                    z-index: 1000; 
                    background: rgba(0,0,0,0.9); 
                    padding: 15px; 
                    border-radius: 5px; 
                    max-width: 300px; 
                }}
            </style>
        </head>
        <body>
            <div class="controls">
                <button id="fitBtn" class="btn btn-sm btn-primary">Fit View</button>
                <button id="physicsBtn" class="btn btn-sm btn-secondary">Toggle Physics</button>
            </div>
            <div class="info-panel">
                <h6>Repository Analysis</h6>
                <div id="selection-info">Click a node to see details</div>
                <hr>
                <small>
                    Files: {len(files)}<br>
                    Classes: {len(classes)}<br>
                    Functions: {len(functions)}<br>
                    Languages: {len(file_extensions)}
                </small>
            </div>
            <div id="graph"></div>
            <script>
                const nodes = new vis.DataSet({json.dumps(nodes, indent=2)});
                const edges = new vis.DataSet({json.dumps(edges, indent=2)});
                const container = document.getElementById('graph');
                const data = {{ nodes: nodes, edges: edges }};
                
                const options = {{
                    nodes: {{
                        borderWidth: 2,
                        shadow: true,
                        font: {{ color: '#ffffff', size: 12 }},
                        chosen: {{ node: true }}
                    }},
                    edges: {{
                        shadow: true,
                        smooth: {{ type: 'continuous' }},
                        arrows: {{ to: {{ enabled: true, scaleFactor: 0.5 }} }}
                    }},
                    physics: {{
                        enabled: true,
                        stabilization: {{ iterations: 100 }},
                        barnesHut: {{
                            gravitationalConstant: -2000,
                            centralGravity: 0.3,
                            springLength: 95,
                            springConstant: 0.04,
                            damping: 0.09
                        }}
                    }},
                    interaction: {{
                        hover: true,
                        tooltipDelay: 200,
                        hideEdgesOnDrag: true
                    }},
                    groups: {{
                        py: {{ color: {{ background: '#4CAF50', border: '#2E7D32' }} }},
                        js: {{ color: {{ background: '#FF9800', border: '#E65100' }} }},
                        ts: {{ color: {{ background: '#FF9800', border: '#E65100' }} }},
                        java: {{ color: {{ background: '#2196F3', border: '#0D47A1' }} }},
                        classes: {{ color: {{ background: '#FF5722', border: '#BF360C' }} }},
                        functions: {{ color: {{ background: '#607D8B', border: '#37474F' }} }},
                        languages: {{ color: {{ background: '#FFC107', border: '#F57C00' }} }}
                    }}
                }};
                
                const network = new vis.Network(container, data, options);
                
                // Event handlers
                network.on('click', function(params) {{
                    const nodeId = params.nodes[0];
                    if (nodeId) {{
                        const node = nodes.get(nodeId);
                        const infoDiv = document.getElementById('selection-info');
                        infoDiv.innerHTML = `
                            <strong>${{node.label}}</strong><br>
                            Type: ${{node.type}}<br>
                            ${{node.title ? node.title.replace(/\\n/g, '<br>') : 'No details available'}}
                        `;
                    }}
                }});
                
                document.getElementById('fitBtn').addEventListener('click', function() {{
                    network.fit();
                }});
                
                let physicsEnabled = true;
                document.getElementById('physicsBtn').addEventListener('click', function() {{
                    physicsEnabled = !physicsEnabled;
                    network.setOptions({{ physics: {{ enabled: physicsEnabled }} }});
                    this.textContent = physicsEnabled ? 'Disable Physics' : 'Enable Physics';
                }});
                
                // Auto-fit after stabilization
                network.once('stabilizationIterationsDone', function() {{
                    network.fit();
                }});
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