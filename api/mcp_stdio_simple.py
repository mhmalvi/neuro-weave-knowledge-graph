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
                                    'description': 'Clone and analyze a GitHub repository structure (basic analysis without cloning for now)',
                                    'inputSchema': {
                                        'type': 'object',
                                        'properties': {
                                            'repo_url': {'type': 'string', 'description': 'GitHub repository URL'},
                                            'clone_for_analysis': {'type': 'boolean', 'description': 'Whether to clone repo for detailed analysis (experimental)', 'default': False}
                                        },
                                        'required': ['repo_url']
                                    }
                                },
                                {
                                    'name': 'analyze_codebase',
                                    'description': 'Analyze a local codebase directory and extract structural information',
                                    'inputSchema': {
                                        'type': 'object',
                                        'properties': {
                                            'path': {'type': 'string', 'description': 'Path to the codebase directory to analyze'}
                                        },
                                        'required': ['path']
                                    }
                                },
                                {
                                    'name': 'get_repo_info',
                                    'description': 'Get detailed JSON information about a GitHub repository',
                                    'inputSchema': {
                                        'type': 'object',
                                        'properties': {
                                            'repo_url': {'type': 'string', 'description': 'GitHub repository URL'}
                                        },
                                        'required': ['repo_url']
                                    }
                                },
                                {
                                    'name': 'generate_codebase_graph',
                                    'description': 'Generate a text-based knowledge graph visualization of code structure',
                                    'inputSchema': {
                                        'type': 'object',
                                        'properties': {
                                            'path': {'type': 'string', 'description': 'Path to codebase directory to visualize'}
                                        },
                                        'required': ['path']
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
                        clone_for_analysis = args.get('clone_for_analysis', False)
                        
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
                                        
                                        # Extended analysis with cloning option
                                        if clone_for_analysis:
                                            try:
                                                import subprocess
                                                import tempfile
                                                import shutil
                                                
                                                # Clone to temp directory
                                                with tempfile.TemporaryDirectory() as temp_dir:
                                                    clone_result = subprocess.run(['git', 'clone', '--depth', '1', repo_url, temp_dir], 
                                                                                capture_output=True, text=True, timeout=30)
                                                    
                                                    if clone_result.returncode == 0:
                                                        # Quick analysis of cloned repo
                                                        files_count = 0
                                                        py_files = 0
                                                        
                                                        for root, dirs, files in os.walk(temp_dir):
                                                            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in {'node_modules', '__pycache__'}]
                                                            for file in files:
                                                                if not file.startswith('.'):
                                                                    files_count += 1
                                                                    if file.endswith('.py'):
                                                                        py_files += 1
                                                        
                                                        summary = f"""🔍 **GitHub Repository Analysis (with Cloning)**

🌐 **Repository:** {repo_info.get("name", "Unknown")}
⭐ **Stars:** {repo_info.get("stargazers_count", 0)}
🍴 **Forks:** {repo_info.get("forks_count", 0)}
📝 **Language:** {repo_info.get("language", "Unknown")}
📈 **Size:** {repo_info.get("size", 0)} KB

📁 **Cloned Analysis:**
• **Total Files:** {files_count}
• **Python Files:** {py_files}
• **Clone Status:** ✅ Successfully cloned and analyzed

✅ **Extended analysis complete via GitHub API + Git Clone!**

💡 **Tip:** Use analyze_codebase on the cloned directory for detailed structure analysis."""
                                                    else:
                                                        summary = f"""🔍 **GitHub Repository Analysis**

🌐 **Repository:** {repo_info.get("name", "Unknown")}
⭐ **Stars:** {repo_info.get("stargazers_count", 0)}
🍴 **Forks:** {repo_info.get("forks_count", 0)}
📝 **Language:** {repo_info.get("language", "Unknown")}
📈 **Size:** {repo_info.get("size", 0)} KB

⚠️ **Clone Failed:** {clone_result.stderr[:200] if clone_result.stderr else 'Git clone failed'}

✅ Analysis complete via GitHub API only!"""
                                            except Exception as e:
                                                summary = f"""🔍 **GitHub Repository Analysis**

🌐 **Repository:** {repo_info.get("name", "Unknown")}
⭐ **Stars:** {repo_info.get("stargazers_count", 0)}
🍴 **Forks:** {repo_info.get("forks_count", 0)}
📝 **Language:** {repo_info.get("language", "Unknown")}
📈 **Size:** {repo_info.get("size", 0)} KB

⚠️ **Clone Error:** {str(e)[:100]}

✅ Analysis complete via GitHub API only!"""
                                        else:
                                            summary = f"""🔍 **GitHub Repository Analysis**

🌐 **Repository:** {repo_info.get("name", "Unknown")}
⭐ **Stars:** {repo_info.get("stargazers_count", 0)}
🍴 **Forks:** {repo_info.get("forks_count", 0)}
📝 **Language:** {repo_info.get("language", "Unknown")}
📈 **Size:** {repo_info.get("size", 0)} KB

✅ Analysis complete via GitHub API!

💡 **Tip:** Add `"clone_for_analysis": true` for extended analysis with git clone."""
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
                        
                    elif tool_name == 'analyze_codebase':
                        path = args.get('path', '')
                        if not path:
                            response = {
                                'jsonrpc': '2.0',
                                'id': req_id,
                                'error': {
                                    'code': -32602,
                                    'message': 'path is required'
                                }
                            }
                        else:
                            try:
                                import os
                                import ast
                                from pathlib import Path
                                
                                # Analyze local codebase
                                analysis_result = {
                                    'files': [],
                                    'classes': [],
                                    'functions': [],
                                    'imports': [],
                                    'metrics': {
                                        'total_files': 0,
                                        'total_lines': 0,
                                        'languages': {},
                                        'file_types': {}
                                    }
                                }
                                
                                if os.path.exists(path) and os.path.isdir(path):
                                    # Supported file extensions
                                    extensions = {'.py', '.js', '.ts', '.java', '.cpp', '.c', '.h', '.hpp', '.go', '.rs', '.rb', '.php'}
                                    
                                    for root, dirs, files in os.walk(path):
                                        # Skip common ignore directories
                                        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in {'node_modules', '__pycache__', 'target', 'build', 'dist'}]
                                        
                                        for file in files:
                                            file_path = Path(root) / file
                                            if file_path.suffix in extensions:
                                                analysis_result['files'].append(str(file_path))
                                                analysis_result['metrics']['total_files'] += 1
                                                
                                                # Count file types
                                                ext = file_path.suffix
                                                analysis_result['metrics']['file_types'][ext] = analysis_result['metrics']['file_types'].get(ext, 0) + 1
                                                
                                                # Analyze Python files with AST
                                                if ext == '.py':
                                                    try:
                                                        with open(file_path, 'r', encoding='utf-8') as f:
                                                            content = f.read()
                                                            analysis_result['metrics']['total_lines'] += len(content.splitlines())
                                                            
                                                            tree = ast.parse(content)
                                                            for node in ast.walk(tree):
                                                                if isinstance(node, ast.ClassDef):
                                                                    analysis_result['classes'].append({
                                                                        'name': node.name,
                                                                        'file': str(file_path),
                                                                        'line': node.lineno
                                                                    })
                                                                elif isinstance(node, ast.FunctionDef):
                                                                    analysis_result['functions'].append({
                                                                        'name': node.name,
                                                                        'file': str(file_path),
                                                                        'line': node.lineno
                                                                    })
                                                                elif isinstance(node, ast.Import):
                                                                    for alias in node.names:
                                                                        analysis_result['imports'].append({
                                                                            'module': alias.name,
                                                                            'file': str(file_path),
                                                                            'line': node.lineno
                                                                        })
                                                                elif isinstance(node, ast.ImportFrom):
                                                                    module = node.module or ''
                                                                    for alias in node.names:
                                                                        analysis_result['imports'].append({
                                                                            'module': f"{module}.{alias.name}" if module else alias.name,
                                                                            'file': str(file_path),
                                                                            'line': node.lineno
                                                                        })
                                                    except Exception as e:
                                                        # Skip files that can't be parsed
                                                        pass
                                                else:
                                                    # Count lines for other file types
                                                    try:
                                                        with open(file_path, 'r', encoding='utf-8') as f:
                                                            analysis_result['metrics']['total_lines'] += len(f.readlines())
                                                    except:
                                                        pass
                                    
                                    # Generate summary
                                    total_classes = len(analysis_result['classes'])
                                    total_functions = len(analysis_result['functions'])
                                    total_imports = len(analysis_result['imports'])
                                    
                                    summary = f"""📁 **Codebase Analysis Complete!**

🗂️ **Path:** {path}
📊 **Files:** {analysis_result['metrics']['total_files']} files
📝 **Lines:** {analysis_result['metrics']['total_lines']:,} lines of code

🏗️ **Structure:**
• **Classes:** {total_classes}
• **Functions:** {total_functions}
• **Imports:** {total_imports}

📂 **File Types:**
{chr(10).join([f'• **{ext}**: {count} files' for ext, count in analysis_result['metrics']['file_types'].items()])}

✅ **Local codebase analysis complete!**

📊 Use generate_codebase_graph to create an interactive visualization."""
                                    
                                    response = {
                                        'jsonrpc': '2.0',
                                        'id': req_id,
                                        'result': {
                                            'content': [{'type': 'text', 'text': summary}]
                                        }
                                    }
                                else:
                                    response = {
                                        'jsonrpc': '2.0',
                                        'id': req_id,
                                        'result': {
                                            'content': [{'type': 'text', 'text': f"❌ Path not found or not a directory: {path}"}]
                                        }
                                    }
                                    
                            except Exception as e:
                                response = {
                                    'jsonrpc': '2.0',
                                    'id': req_id,
                                    'result': {
                                        'content': [{'type': 'text', 'text': f"❌ Error analyzing codebase: {str(e)}"}]
                                    }
                                }
                        print(json.dumps(response), flush=True)
                        
                    elif tool_name == 'get_repo_info':
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
                                        # Return raw JSON data
                                        response = {
                                            'jsonrpc': '2.0',
                                            'id': req_id,
                                            'result': {
                                                'content': [{'type': 'text', 'text': json.dumps(repo_info, indent=2)}]
                                            }
                                        }
                                    else:
                                        response = {
                                            'jsonrpc': '2.0',
                                            'id': req_id,
                                            'result': {
                                                'content': [{'type': 'text', 'text': f"❌ Failed to fetch repository info: HTTP {resp.status_code}"}]
                                            }
                                        }
                                else:
                                    response = {
                                        'jsonrpc': '2.0',
                                        'id': req_id,
                                        'result': {
                                            'content': [{'type': 'text', 'text': "❌ Invalid GitHub repository URL"}]
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
                        
                    elif tool_name == 'generate_codebase_graph':
                        path = args.get('path', '')
                        if not path:
                            response = {
                                'jsonrpc': '2.0',
                                'id': req_id,
                                'error': {
                                    'code': -32602,
                                    'message': 'path is required'
                                }
                            }
                        else:
                            try:
                                import os
                                import ast
                                from pathlib import Path
                                
                                # Analyze and generate graph representation
                                if os.path.exists(path) and os.path.isdir(path):
                                    files_data = {}
                                    graph_lines = []
                                    
                                    # First pass: collect all files and their contents
                                    for root, dirs, files in os.walk(path):
                                        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in {'node_modules', '__pycache__', 'target', 'build', 'dist'}]
                                        
                                        for file in files:
                                            if file.endswith('.py'):
                                                file_path = Path(root) / file
                                                relative_path = file_path.relative_to(Path(path))
                                                
                                                try:
                                                    with open(file_path, 'r', encoding='utf-8') as f:
                                                        content = f.read()
                                                        tree = ast.parse(content)
                                                        
                                                        files_data[str(relative_path)] = {
                                                            'classes': [],
                                                            'functions': [],
                                                            'imports': []
                                                        }
                                                        
                                                        for node in ast.walk(tree):
                                                            if isinstance(node, ast.ClassDef):
                                                                files_data[str(relative_path)]['classes'].append(node.name)
                                                            elif isinstance(node, ast.FunctionDef):
                                                                files_data[str(relative_path)]['functions'].append(node.name)
                                                            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                                                                if isinstance(node, ast.Import):
                                                                    for alias in node.names:
                                                                        files_data[str(relative_path)]['imports'].append(alias.name)
                                                                else:
                                                                    module = node.module or 'relative'
                                                                    files_data[str(relative_path)]['imports'].append(module)
                                                except Exception:
                                                    pass
                                    
                                    # Generate ASCII graph representation
                                    graph_lines.append("🕸️  **CODEBASE KNOWLEDGE GRAPH**")
                                    graph_lines.append("=" * 50)
                                    graph_lines.append("")
                                    
                                    for file_path, data in files_data.items():
                                        graph_lines.append(f"📁 **{file_path}**")
                                        
                                        # Show classes
                                        if data['classes']:
                                            graph_lines.append(f"  └─ 🏛️  Classes ({len(data['classes'])})")
                                            for cls in data['classes'][:5]:  # Limit display
                                                graph_lines.append(f"      ├─ {cls}")
                                            if len(data['classes']) > 5:
                                                graph_lines.append(f"      └─ ... and {len(data['classes']) - 5} more")
                                        
                                        # Show functions  
                                        if data['functions']:
                                            graph_lines.append(f"  └─ ⚙️  Functions ({len(data['functions'])})")
                                            for func in data['functions'][:5]:  # Limit display
                                                graph_lines.append(f"      ├─ {func}")
                                            if len(data['functions']) > 5:
                                                graph_lines.append(f"      └─ ... and {len(data['functions']) - 5} more")
                                        
                                        # Show key imports
                                        if data['imports']:
                                            unique_imports = list(set(data['imports']))
                                            graph_lines.append(f"  └─ 📦 Imports ({len(unique_imports)})")
                                            for imp in unique_imports[:3]:  # Limit display
                                                graph_lines.append(f"      ├─ {imp}")
                                            if len(unique_imports) > 3:
                                                graph_lines.append(f"      └─ ... and {len(unique_imports) - 3} more")
                                        
                                        graph_lines.append("")
                                    
                                    # Summary statistics
                                    total_files = len(files_data)
                                    total_classes = sum(len(data['classes']) for data in files_data.values())
                                    total_functions = sum(len(data['functions']) for data in files_data.values())
                                    total_imports = sum(len(set(data['imports'])) for data in files_data.values())
                                    
                                    graph_lines.append("📊 **GRAPH STATISTICS**")
                                    graph_lines.append("=" * 30)
                                    graph_lines.append(f"📁 Files: {total_files}")
                                    graph_lines.append(f"🏛️  Classes: {total_classes}")
                                    graph_lines.append(f"⚙️  Functions: {total_functions}")
                                    graph_lines.append(f"📦 Import Statements: {total_imports}")
                                    graph_lines.append("")
                                    graph_lines.append("✅ **Knowledge graph generated successfully!**")
                                    
                                    graph_text = "\n".join(graph_lines)
                                    
                                    response = {
                                        'jsonrpc': '2.0',
                                        'id': req_id,
                                        'result': {
                                            'content': [{'type': 'text', 'text': graph_text}]
                                        }
                                    }
                                else:
                                    response = {
                                        'jsonrpc': '2.0',
                                        'id': req_id,
                                        'result': {
                                            'content': [{'type': 'text', 'text': f"❌ Path not found or not a directory: {path}"}]
                                        }
                                    }
                                    
                            except Exception as e:
                                response = {
                                    'jsonrpc': '2.0',
                                    'id': req_id,
                                    'result': {
                                        'content': [{'type': 'text', 'text': f"❌ Error generating graph: {str(e)}"}]
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