# api/mcp.py
import json
from typing import Any, Tuple, Dict

COMMON_HEADERS = {
    "content-type": "application/json; charset=utf-8",
    "cache-control": "no-store",
    # not strictly needed for server->server, but harmless and helps OPTIONS
    "access-control-allow-origin": "*",
    "access-control-allow-methods": "POST, OPTIONS, GET",
    "access-control-allow-headers": "content-type, authorization",
}

def _json(status: int, body: Dict[str, Any], extra: Dict[str, str] | None = None) -> Tuple[int, Dict[str,str], bytes]:
    h = dict(COMMON_HEADERS)
    if extra: h.update(extra)
    return status, h, json.dumps(body).encode("utf-8")

def _no_content() -> Tuple[int, Dict[str,str], bytes]:
    return 204, {
        "access-control-allow-origin": "*",
        "access-control-allow-methods": "POST, OPTIONS, GET",
        "access-control-allow-headers": "content-type, authorization",
    }, b""

def handler(request: Any):
    method = request.method.upper()

    # 1) Claude health probe
    if method == "GET":
        return _json(200, {
            "ok": True,
            "service": "mcp",
            "transport": "http",
            "endpoints": ["POST /api/mcp"],
            "version": "0.1.0"
        })

    # 2) Preflight
    if method == "OPTIONS":
        return _no_content()

    # 3) JSON-RPC
    if method == "POST":
        try:
            req = request.json() or {}
        except Exception:
            return _json(400, {"jsonrpc":"2.0","id":None,"error":{"code":-32700,"message":"Parse error"}})

        mid = req.get("id")
        mth = req.get("method")
        params = req.get("params") or {}

        if mth == "initialize":
            return _json(200, {
                "jsonrpc":"2.0","id": mid,
                "result":{
                    "protocolVersion":"2024-11-05",
                    "serverInfo":{"name":"codebase-knowledge-graph","version":"1.0.0"},
                    "capabilities":{
                        "tools":{"listChanged": False},
                        "resources":{"subscribe": False, "listChanged": False},
                        "prompts":{"listChanged": False}
                    }
                }
            })

        if mth == "tools/list":
            return _json(200, {
                "jsonrpc":"2.0","id": mid,
                "result":{"tools":[
                    {
                        "name":"analyze_github_repo",
                        "description":"Analyze a GitHub repository structure and metadata",
                        "inputSchema":{
                            "type":"object",
                            "properties":{"repo_url":{"type":"string","description":"GitHub repository URL"}},
                            "required":["repo_url"]
                        }
                    },
                    {
                        "name":"get_repo_info",
                        "description":"Get basic information about a GitHub repository", 
                        "inputSchema":{
                            "type":"object",
                            "properties":{"repo_url":{"type":"string","description":"GitHub repository URL"}},
                            "required":["repo_url"]
                        }
                    }
                ]}
            })

        if mth == "tools/call":
            name = params.get("name")
            args = params.get("arguments") or {}
            
            if name == "analyze_github_repo":
                repo_url = args.get("repo_url")
                if not repo_url:
                    return _json(200, {"jsonrpc":"2.0","id": mid,
                        "error":{"code":-32602,"message":"repo_url is required"}})
                
                try:
                    # Simplified analysis for serverless environment
                    from urllib.parse import urlparse
                    import requests
                    import os
                    
                    parsed = urlparse(repo_url)
                    path_parts = parsed.path.strip("/").split("/")
                    if len(path_parts) < 2:
                        raise ValueError("Invalid GitHub repository URL")
                    
                    owner, repo = path_parts[0], path_parts[1]
                    
                    api_url = f"https://api.github.com/repos/{owner}/{repo}"
                    headers = {}
                    
                    github_token = os.getenv("GITHUB_TOKEN")
                    if github_token:
                        headers["Authorization"] = f"token {github_token}"
                    
                    response = requests.get(api_url, headers=headers, timeout=10)
                    if response.status_code != 200:
                        raise Exception(f"Failed to fetch repo info: {response.text}")
                    
                    repo_info = response.json()
                    
                    summary = f"""🔍 **GitHub Repository Analysis Complete!**

🌐 **Repository:** {repo_info.get("name", "Unknown")}
🔗 **URL:** {repo_url}
⭐ **Stars:** {repo_info.get("stargazers_count", 0)}
🍴 **Forks:** {repo_info.get("forks_count", 0)}
📝 **Language:** {repo_info.get("language", "Unknown")}

📈 **Repository Stats:**
• **Size:** {repo_info.get("size", 0)} KB
• **Last Updated:** {repo_info.get("updated_at", "Unknown")}
• **License:** {repo_info.get("license", {}).get("name", "None") if repo_info.get("license") else "None"}

🚀 **Repository analyzed successfully via GitHub API!**

📊 **Note:** This is a serverless analysis using GitHub API. For full codebase analysis with file-level details, use the local MCP server."""
                    
                    return _json(200, {
                        "jsonrpc":"2.0","id": mid,
                        "result":{"content":[{"type":"text","text":summary}]}
                    })
                    
                except Exception as e:
                    return _json(200, {
                        "jsonrpc":"2.0","id": mid,
                        "result":{"content":[{"type":"text","text":f"❌ Error analyzing repository: {str(e)}"}]}
                    })
            
            elif name == "get_repo_info":
                repo_url = args.get("repo_url")
                if not repo_url:
                    return _json(200, {"jsonrpc":"2.0","id": mid,
                        "error":{"code":-32602,"message":"repo_url is required"}})
                
                try:
                    from urllib.parse import urlparse
                    import requests
                    import os
                    
                    parsed = urlparse(repo_url)
                    path_parts = parsed.path.strip("/").split("/")
                    if len(path_parts) < 2:
                        raise ValueError("Invalid GitHub repository URL")
                    
                    owner, repo = path_parts[0], path_parts[1]
                    
                    api_url = f"https://api.github.com/repos/{owner}/{repo}"
                    headers = {}
                    
                    github_token = os.getenv("GITHUB_TOKEN")
                    if github_token:
                        headers["Authorization"] = f"token {github_token}"
                    
                    response = requests.get(api_url, headers=headers, timeout=10)
                    if response.status_code != 200:
                        raise Exception(f"Failed to fetch repo info: {response.text}")
                    
                    repo_info = response.json()
                    
                    return _json(200, {
                        "jsonrpc":"2.0","id": mid,
                        "result":{"content":[{"type":"text","text":json.dumps(repo_info, indent=2, default=str)}]}
                    })
                    
                except Exception as e:
                    return _json(200, {
                        "jsonrpc":"2.0","id": mid,
                        "result":{"content":[{"type":"text","text":f"❌ Error getting repository info: {str(e)}"}]}
                    })
            
            else:
                return _json(200, {"jsonrpc":"2.0","id": mid,
                    "error":{"code":-32602,"message":f"Unknown tool: {name}"}})

        # Default "method not found"
        return _json(200, {"jsonrpc":"2.0","id": mid,
            "error":{"code":-32601,"message":"Method not found"}})

    # 4) Anything else
    return _json(405, {"error":"Method not allowed"})