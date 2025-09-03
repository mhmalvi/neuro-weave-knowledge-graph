#!/usr/bin/env python3
"""
Fast STDIO MCP Server for Claude Code CLI
Optimized for quick health checks and responsiveness
"""

import json
import sys

def main():
    """Fast MCP server loop"""
    try:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
                
            try:
                req = json.loads(line)
                method = req.get('method')
                req_id = req.get('id')
                
                if method == 'initialize':
                    response = {
                        'jsonrpc': '2.0',
                        'id': req_id,
                        'result': {
                            'protocolVersion': '2024-11-05',
                            'serverInfo': {
                                'name': 'codebase-knowledge-graph',
                                'version': '1.0.0'
                            },
                            'capabilities': {
                                'tools': {'listChanged': False}
                            }
                        }
                    }
                    print(json.dumps(response), flush=True)
                    
                elif method == 'notifications/initialized':
                    # No response for notifications
                    continue
                    
                elif method == 'tools/list':
                    response = {
                        'jsonrpc': '2.0',
                        'id': req_id,
                        'result': {
                            'tools': [
                                {
                                    'name': 'analyze_github_repo',
                                    'description': 'Analyze a GitHub repository structure and metadata',
                                    'inputSchema': {
                                        'type': 'object',
                                        'properties': {
                                            'repo_url': {'type': 'string', 'description': 'GitHub repository URL'}
                                        },
                                        'required': ['repo_url']
                                    }
                                },
                                {
                                    'name': 'echo_test',
                                    'description': 'Simple echo test tool',
                                    'inputSchema': {
                                        'type': 'object',
                                        'properties': {
                                            'message': {'type': 'string'}
                                        },
                                        'required': ['message']
                                    }
                                }
                            ]
                        }
                    }
                    print(json.dumps(response), flush=True)
                    
                elif method == 'tools/call':
                    params = req.get('params', {})
                    tool_name = params.get('name')
                    args = params.get('arguments', {})
                    
                    if tool_name == 'analyze_github_repo':
                        repo_url = args.get('repo_url', '')
                        if not repo_url:
                            response = {
                                'jsonrpc': '2.0',
                                'id': req_id,
                                'error': {
                                    'code': -32602,
                                    'message': 'repo_url is required'
                                }
                            }
                        else:
                            try:
                                # Simple GitHub API analysis (only import when needed)
                                import requests
                                import os
                                from urllib.parse import urlparse
                                
                                parsed = urlparse(repo_url)
                                path_parts = parsed.path.strip("/").split("/")
                                if len(path_parts) >= 2:
                                    owner, repo = path_parts[0], path_parts[1]
                                    api_url = f"https://api.github.com/repos/{owner}/{repo}"
                                    
                                    headers = {}
                                    github_token = os.getenv("GITHUB_TOKEN")
                                    if github_token:
                                        headers["Authorization"] = f"token {github_token}"
                                    
                                    resp = requests.get(api_url, headers=headers, timeout=10)
                                    if resp.status_code == 200:
                                        repo_info = resp.json()
                                        summary = f"""🔍 **GitHub Repository Analysis**

🌐 **Repository:** {repo_info.get("name", "Unknown")}
⭐ **Stars:** {repo_info.get("stargazers_count", 0)}
🍴 **Forks:** {repo_info.get("forks_count", 0)}
📝 **Language:** {repo_info.get("language", "Unknown")}
📈 **Size:** {repo_info.get("size", 0)} KB

✅ Analysis complete via GitHub API!"""
                                    else:
                                        summary = f"❌ Failed to fetch repository info: HTTP {resp.status_code}"
                                else:
                                    summary = "❌ Invalid GitHub repository URL"
                                    
                                response = {
                                    'jsonrpc': '2.0',
                                    'id': req_id,
                                    'result': {
                                        'content': [{'type': 'text', 'text': summary}]
                                    }
                                }
                            except Exception as e:
                                response = {
                                    'jsonrpc': '2.0',
                                    'id': req_id,
                                    'result': {
                                        'content': [{'type': 'text', 'text': f"❌ Error: {str(e)}"}]
                                    }
                                }
                        print(json.dumps(response), flush=True)
                        
                    elif tool_name == 'echo_test':
                        response = {
                            'jsonrpc': '2.0',
                            'id': req_id,
                            'result': {
                                'content': [
                                    {
                                        'type': 'text',
                                        'text': f"Echo: {args.get('message', 'No message provided')}"
                                    }
                                ]
                            }
                        }
                        print(json.dumps(response), flush=True)
                    else:
                        # Unknown tool
                        response = {
                            'jsonrpc': '2.0',
                            'id': req_id,
                            'error': {
                                'code': -32602,
                                'message': f'Unknown tool: {tool_name}'
                            }
                        }
                        print(json.dumps(response), flush=True)
                        
                else:
                    # Unknown method
                    response = {
                        'jsonrpc': '2.0',
                        'id': req_id,
                        'error': {
                            'code': -32601,
                            'message': f'Unknown method: {method}'
                        }
                    }
                    print(json.dumps(response), flush=True)
                    
            except json.JSONDecodeError:
                # Parse error
                response = {
                    'jsonrpc': '2.0',
                    'id': None,
                    'error': {
                        'code': -32700,
                        'message': 'Parse error'
                    }
                }
                print(json.dumps(response), flush=True)
                
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()