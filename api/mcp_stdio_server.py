#!/usr/bin/env python3
"""
STDIO MCP Server for codebase knowledge graph analysis
Implements Model Context Protocol over STDIO for Claude Code CLI
"""

import json
import sys
import os
from urllib.parse import urlparse
import requests
from typing import Dict, Any, Optional, List

# Import enhanced analysis components
try:
    import sys
    import os
    # Add parent directory to path for enhanced imports
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, parent_dir)
    
    from enhanced_ecological_analyzer import EnhancedEcologicalAnalyzer
    from enhanced_knowledge_graph_generator import EnhancedKnowledgeGraphGenerator
    ENHANCED_AVAILABLE = True
except ImportError as e:
    ENHANCED_AVAILABLE = False
    import sys
    print(f"Enhanced import error: {e}", file=sys.stderr)

# Current MCP Protocol version
MCP_VERSION = "2025-06-18"

class MCPJsonRpcError:
    """JSON-RPC 2.0 Error codes"""
    PARSE_ERROR = -32700
    INVALID_REQUEST = -32600
    METHOD_NOT_FOUND = -32601
    INVALID_PARAMS = -32602
    INTERNAL_ERROR = -32603

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

def analyze_github_repo(repo_url: str) -> Dict[str, Any]:
    """Analyze GitHub repository via API (for STDIO)"""
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

def analyze_codebase_enhanced(path: str) -> Dict[str, Any]:
    """Perform enhanced ecological analysis on local codebase"""
    if not ENHANCED_AVAILABLE:
        raise Exception("Enhanced analysis components not available. Install required dependencies.")
    
    try:
        analyzer = EnhancedEcologicalAnalyzer()
        analysis_result = analyzer.analyze_codebase(path)
        
        # Generate interactive visualization
        generator = EnhancedKnowledgeGraphGenerator()
        html_file = generator.generate_enhanced_graph(analysis_result, f"enhanced_analysis_{hash(path) % 10000}.html")
        
        return {
            "analysis": analysis_result,
            "visualization_file": html_file,
            "summary": {
                "files_analyzed": len(analysis_result.get('files', [])),
                "classes_found": len(analysis_result.get('classes', [])),
                "functions_found": len(analysis_result.get('functions', [])),
                "patterns_detected": len(analysis_result.get('patterns', {}).get('design_patterns', [])),
                "clusters_created": len(analysis_result.get('semantic_clusters', [])),
                "concerns_identified": len(analysis_result.get('cross_cutting_concerns', []))
            }
        }
    except Exception as e:
        raise Exception(f"Error performing enhanced analysis: {str(e)}")

def generate_codebase_graph(analysis_data: dict, output_file: str = None) -> Dict[str, Any]:
    """Generate interactive knowledge graph from codebase analysis data"""
    if not ENHANCED_AVAILABLE:
        raise Exception("Enhanced analysis components not available. Install required dependencies.")
    
    try:
        generator = EnhancedKnowledgeGraphGenerator()
        if output_file is None:
            output_file = f"codebase_graph_{hash(str(analysis_data)) % 10000}.html"
        
        html_file = generator.generate_enhanced_graph(analysis_data, output_file)
        
        return {
            "visualization_file": html_file,
            "nodes_count": len(analysis_data.get('files', [])) + len(analysis_data.get('classes', [])) + len(analysis_data.get('functions', [])),
            "edges_count": len(analysis_data.get('imports', [])),
            "output_path": os.path.abspath(html_file)
        }
    except Exception as e:
        raise Exception(f"Error generating codebase graph: {str(e)}")

def handle_mcp_request(request_data: dict) -> Optional[dict]:
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
        
        # Add enhanced analysis tools if available
        if ENHANCED_AVAILABLE:
            tools.extend([
                {
                    "name": "analyze_codebase_enhanced",
                    "description": "Perform comprehensive enhanced ecological analysis on local codebase with patterns, relationships, and interactive visualization",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string", 
                                "description": "Local path to codebase directory"
                            }
                        },
                        "required": ["path"]
                    }
                },
                {
                    "name": "generate_codebase_graph",
                    "description": "Generate interactive knowledge graph from codebase analysis data",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "analysis_data": {
                                "type": "object",
                                "description": "Codebase analysis data (from analyze_codebase_enhanced or similar)"
                            },
                            "output_file": {
                                "type": "string",
                                "description": "Optional output HTML filename"
                            }
                        },
                        "required": ["analysis_data"]
                    }
                }
            ])
        
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

📊 **Note:** This is a STDIO MCP server analysis. For web-based access, use the HTTP endpoint."""
                
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
            if not ENHANCED_AVAILABLE:
                return create_json_rpc_response(id_val, {
                    "content": [
                        {
                            "type": "text",
                            "text": "Enhanced analysis not available. Missing dependencies: enhanced_ecological_analyzer, enhanced_knowledge_graph_generator"
                        }
                    ]
                })
            
            path = arguments.get("path")
            if not path:
                return create_json_rpc_response(
                    id_val,
                    error=create_json_rpc_error(MCPJsonRpcError.INVALID_PARAMS, "path is required")
                )
            
            try:
                result = analyze_codebase_enhanced(path)
                summary = result["summary"]
                
                enhanced_summary = f"""🔬 **Enhanced Ecological Analysis Complete!**

📁 **Path:** {path}
📊 **Files Analyzed:** {summary['files_analyzed']}
🏗️ **Classes Found:** {summary['classes_found']}
⚙️ **Functions Found:** {summary['functions_found']}

🧬 **Advanced Insights:**
• **Design Patterns:** {summary['patterns_detected']} detected
• **Semantic Clusters:** {summary['clusters_created']} created  
• **Cross-cutting Concerns:** {summary['concerns_identified']} identified

📈 **Interactive Visualization:** {result['visualization_file']}

🎯 **Enhanced ecological analysis provides deep insights into:**
• Architectural patterns and relationships
• Code quality metrics and maintainability
• Semantic clustering and cross-cutting concerns
• Interactive multi-dimensional knowledge graphs"""
                
                return create_json_rpc_response(id_val, {
                    "content": [
                        {
                            "type": "text",
                            "text": enhanced_summary
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
            if not ENHANCED_AVAILABLE:
                return create_json_rpc_response(id_val, {
                    "content": [
                        {
                            "type": "text",
                            "text": "Enhanced graph generation not available. Missing dependencies: enhanced_ecological_analyzer, enhanced_knowledge_graph_generator"
                        }
                    ]
                })
            
            analysis_data = arguments.get("analysis_data")
            if not analysis_data:
                return create_json_rpc_response(
                    id_val,
                    error=create_json_rpc_error(MCPJsonRpcError.INVALID_PARAMS, "analysis_data is required")
                )
            
            output_file = arguments.get("output_file")
            
            try:
                result = generate_codebase_graph(analysis_data, output_file)
                
                graph_summary = f"""🕸️ **Interactive Knowledge Graph Generated!**

📊 **Graph Statistics:**
• **Nodes:** {result['nodes_count']} (files, classes, functions)
• **Edges:** {result['edges_count']} (imports, relationships)
• **Visualization File:** {result['visualization_file']}
• **Full Path:** {result['output_path']}

🎯 **Graph Features:**
• Interactive node exploration
• Hierarchical relationships visualization
• Code structure mapping
• Dependency analysis
• Pattern recognition visual aids

🚀 **Open the HTML file in your browser to explore the interactive knowledge graph!**"""
                
                return create_json_rpc_response(id_val, {
                    "content": [
                        {
                            "type": "text",
                            "text": graph_summary
                        }
                    ]
                })
                
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

def main():
    """Main STDIO MCP server loop"""
    # Log to stderr to avoid polluting the JSON-RPC stdout
    def log(message):
        print(f"[MCP] {message}", file=sys.stderr)
    
    log("Starting codebase-knowledge-graph MCP server...")
    sys.stderr.flush()
    
    try:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
                
            try:
                # Parse the JSON-RPC request
                request_data = json.loads(line)
                log(f"Received: {request_data.get('method', 'unknown')}")
                
                # Handle the request
                response = handle_mcp_request(request_data)
                
                # Send response (if any)
                if response is not None:
                    response_json = json.dumps(response, ensure_ascii=False)
                    print(response_json, flush=True)
                    log(f"Sent: {response.get('result', {}).get('content', 'response')}")
                
            except json.JSONDecodeError as e:
                # Send parse error response
                error_response = create_json_rpc_response(
                    None,
                    error=create_json_rpc_error(MCPJsonRpcError.PARSE_ERROR, f"Invalid JSON: {str(e)}")
                )
                print(json.dumps(error_response), flush=True)
                log(f"Parse error: {e}")
                
            except Exception as e:
                # Send internal error response
                error_response = create_json_rpc_response(
                    None,
                    error=create_json_rpc_error(MCPJsonRpcError.INTERNAL_ERROR, f"Internal error: {str(e)}")
                )
                print(json.dumps(error_response), flush=True)
                log(f"Internal error: {e}")
                
    except KeyboardInterrupt:
        log("MCP server shutting down...")
    except Exception as e:
        log(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()