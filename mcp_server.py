#!/usr/bin/env python3
"""
MCP Server for Codebase Knowledge Graph Visualization

This MCP server provides tools for analyzing codebases and generating
interactive knowledge graph visualizations of code architecture, dependencies,
and relationships.
"""

import asyncio
import json
import os
import ast
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import logging
from urllib.parse import urlparse
import webbrowser
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
import socket

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)
import mcp.types as types

# Import our existing knowledge graph functionality
from codebase_visualizer import CodebaseVisualizer
from enterprise_cyberpunk_generator import EnterpriseCyberpunkGenerator
from enhanced_ecological_analyzer import EnhancedEcologicalAnalyzer
from pyvis.network import Network
import requests

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("codebase-kg-mcp")

app = Server("codebase-knowledge-graph")

class CodebaseAnalyzer:
    """Analyzes codebase structure and generates knowledge graphs"""
    
    def __init__(self):
        self.supported_extensions = {
            '.py': self._analyze_python,
            '.js': self._analyze_javascript,
            '.ts': self._analyze_typescript,
            '.jsx': self._analyze_javascript,
            '.tsx': self._analyze_typescript,
            '.java': self._analyze_java,
            '.cpp': self._analyze_cpp,
            '.c': self._analyze_cpp,
            '.h': self._analyze_cpp,
            '.cs': self._analyze_csharp,
            '.go': self._analyze_go,
            '.rs': self._analyze_rust,
        }
    
    def analyze_codebase(self, path: str) -> Dict[str, Any]:
        """Analyze a codebase and extract structural information"""
        if not os.path.exists(path):
            raise FileNotFoundError(f"Path does not exist: {path}")
        
        analysis = {
            'files': [],
            'classes': [],
            'functions': [],
            'imports': [],
            'dependencies': [],
            'structure': {},
            'metrics': {}
        }
        
        # Walk through the directory
        for root, dirs, files in os.walk(path):
            # Skip common non-code directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'build', 'dist', 'target']]
            
            for file in files:
                file_path = os.path.join(root, file)
                ext = os.path.splitext(file)[1].lower()
                
                if ext in self.supported_extensions:
                    try:
                        file_analysis = self._analyze_file(file_path)
                        if file_analysis:
                            analysis['files'].append(file_analysis)
                            analysis['classes'].extend(file_analysis.get('classes', []))
                            analysis['functions'].extend(file_analysis.get('functions', []))
                            analysis['imports'].extend(file_analysis.get('imports', []))
                    except Exception as e:
                        logger.warning(f"Error analyzing file {file_path}: {e}")
        
        # Calculate metrics
        analysis['metrics'] = {
            'total_files': len(analysis['files']),
            'total_classes': len(analysis['classes']),
            'total_functions': len(analysis['functions']),
            'total_imports': len(analysis['imports'])
        }
        
        return analysis
    
    def _analyze_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Analyze a single file"""
        ext = os.path.splitext(file_path)[1].lower()
        analyzer = self.supported_extensions.get(ext)
        
        if analyzer:
            return analyzer(file_path)
        return None
    
    def _analyze_python(self, file_path: str) -> Dict[str, Any]:
        """Analyze Python files"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return {'file': file_path, 'error': 'Syntax error in file'}
        
        analysis = {
            'file': file_path,
            'type': 'python',
            'classes': [],
            'functions': [],
            'imports': []
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                analysis['classes'].append({
                    'name': node.name,
                    'line': node.lineno,
                    'file': file_path,
                    'bases': [base.id for base in node.bases if isinstance(base, ast.Name)],
                    'methods': [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                })
            elif isinstance(node, ast.FunctionDef):
                analysis['functions'].append({
                    'name': node.name,
                    'line': node.lineno,
                    'file': file_path,
                    'args': [arg.arg for arg in node.args.args]
                })
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    analysis['imports'].append({
                        'module': alias.name,
                        'alias': alias.asname,
                        'file': file_path,
                        'line': node.lineno
                    })
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for alias in node.names:
                    analysis['imports'].append({
                        'module': f"{module}.{alias.name}" if module else alias.name,
                        'alias': alias.asname,
                        'from': module,
                        'file': file_path,
                        'line': node.lineno
                    })
        
        return analysis
    
    def _analyze_javascript(self, file_path: str) -> Dict[str, Any]:
        """Basic JavaScript analysis"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Simple regex-based analysis for JS/JSX
        import re
        
        analysis = {
            'file': file_path,
            'type': 'javascript',
            'functions': [],
            'classes': [],
            'imports': []
        }
        
        # Find function declarations
        func_pattern = r'function\s+(\w+)\s*\('
        for match in re.finditer(func_pattern, content):
            analysis['functions'].append({
                'name': match.group(1),
                'file': file_path,
                'type': 'function'
            })
        
        # Find class declarations
        class_pattern = r'class\s+(\w+)'
        for match in re.finditer(class_pattern, content):
            analysis['classes'].append({
                'name': match.group(1),
                'file': file_path
            })
        
        # Find imports
        import_pattern = r'import\s+.*?from\s+["\']([^"\']+)["\']'
        for match in re.finditer(import_pattern, content):
            analysis['imports'].append({
                'module': match.group(1),
                'file': file_path
            })
        
        return analysis
    
    def _analyze_typescript(self, file_path: str) -> Dict[str, Any]:
        """Basic TypeScript analysis (similar to JavaScript for now)"""
        return self._analyze_javascript(file_path)
    
    def _analyze_java(self, file_path: str) -> Dict[str, Any]:
        """Basic Java analysis"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        import re
        
        analysis = {
            'file': file_path,
            'type': 'java',
            'classes': [],
            'functions': [],
            'imports': []
        }
        
        # Find class declarations
        class_pattern = r'class\s+(\w+)'
        for match in re.finditer(class_pattern, content):
            analysis['classes'].append({
                'name': match.group(1),
                'file': file_path
            })
        
        # Find method declarations
        method_pattern = r'(public|private|protected)?\s*\w+\s+(\w+)\s*\('
        for match in re.finditer(method_pattern, content):
            analysis['functions'].append({
                'name': match.group(2),
                'file': file_path,
                'visibility': match.group(1) or 'default'
            })
        
        # Find imports
        import_pattern = r'import\s+([^;]+);'
        for match in re.finditer(import_pattern, content):
            analysis['imports'].append({
                'module': match.group(1).strip(),
                'file': file_path
            })
        
        return analysis
    
    def _analyze_cpp(self, file_path: str) -> Dict[str, Any]:
        """Basic C++ analysis"""
        return {'file': file_path, 'type': 'cpp', 'classes': [], 'functions': [], 'imports': []}
    
    def _analyze_csharp(self, file_path: str) -> Dict[str, Any]:
        """Basic C# analysis"""
        return {'file': file_path, 'type': 'csharp', 'classes': [], 'functions': [], 'imports': []}
    
    def _analyze_go(self, file_path: str) -> Dict[str, Any]:
        """Basic Go analysis"""
        return {'file': file_path, 'type': 'go', 'classes': [], 'functions': [], 'imports': []}
    
    def _analyze_rust(self, file_path: str) -> Dict[str, Any]:
        """Basic Rust analysis"""
        return {'file': file_path, 'type': 'rust', 'classes': [], 'functions': [], 'imports': []}

class GitHubAnalyzer:
    """Handles GitHub repository analysis"""
    
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
    
    def clone_or_update_repo(self, repo_url: str, target_dir: str) -> str:
        """Clone or update a GitHub repository"""
        if os.path.exists(target_dir):
            # Update existing repo
            result = subprocess.run(['git', 'pull'], cwd=target_dir, capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(f"Failed to update repo: {result.stderr}")
        else:
            # Clone new repo
            result = subprocess.run(['git', 'clone', repo_url, target_dir], capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(f"Failed to clone repo: {result.stderr}")
        
        return target_dir
    
    def get_repo_info(self, repo_url: str) -> Dict[str, Any]:
        """Get repository information from GitHub API"""
        parsed = urlparse(repo_url)
        if 'github.com' not in parsed.netloc:
            raise ValueError("Only GitHub repositories are supported")
        
        # Extract owner/repo from URL
        path_parts = parsed.path.strip('/').split('/')
        if len(path_parts) < 2:
            raise ValueError("Invalid GitHub repository URL")
        
        owner, repo = path_parts[0], path_parts[1]
        
        api_url = f"https://api.github.com/repos/{owner}/{repo}"
        headers = {}
        
        if self.github_token:
            headers['Authorization'] = f"token {self.github_token}"
        
        response = requests.get(api_url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch repo info: {response.text}")
        
        return response.json()

# Global instances
codebase_analyzer = CodebaseAnalyzer()
github_analyzer = GitHubAnalyzer()
codebase_visualizer = CodebaseVisualizer()
enterprise_cyberpunk_generator = EnterpriseCyberpunkGenerator()
enhanced_analyzer = EnhancedEcologicalAnalyzer()

@app.list_resources()
async def handle_list_resources() -> list[Resource]:
    """List available resources"""
    return [
        Resource(
            uri="codebase://analysis",
            name="Codebase Analysis Results",
            description="Results from codebase structure analysis",
            mimeType="application/json",
        ),
        Resource(
            uri="codebase://graph",
            name="Knowledge Graph Visualization",
            description="Interactive knowledge graph of codebase structure",
            mimeType="text/html",
        ),
    ]

@app.read_resource()
async def handle_get_resource(uri: types.AnyUrl) -> str:
    """Handle resource requests"""
    if uri == "codebase://analysis":
        # Return latest analysis results
        # This would be populated by the analyze_codebase tool
        return json.dumps({"message": "Run analyze_codebase tool first"})
    elif uri == "codebase://graph":
        # Return the generated knowledge graph HTML
        graph_file = "enterprise_cyberpunk_neural_graph.html"
        if os.path.exists(graph_file):
            with open(graph_file, 'r', encoding='utf-8') as f:
                return f.read()
        return "<html><body><h1>No graph generated yet. Run generate_enterprise_cyberpunk_graph tool first.</h1></body></html>"
    else:
        raise ValueError(f"Unknown resource: {uri}")

@app.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="analyze_codebase",
            description="Analyze a local codebase and extract structural information including classes, functions, imports, and dependencies",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the codebase directory to analyze"
                    }
                },
                "required": ["path"]
            }
        ),
        Tool(
            name="analyze_github_repo",
            description="Clone and analyze a GitHub repository",
            inputSchema={
                "type": "object",
                "properties": {
                    "repo_url": {
                        "type": "string",
                        "description": "GitHub repository URL (e.g., https://github.com/user/repo)"
                    },
                    "target_dir": {
                        "type": "string",
                        "description": "Local directory to clone/store the repository (optional)"
                    }
                },
                "required": ["repo_url"]
            }
        ),
        Tool(
            name="generate_codebase_graph",
            description="Generate an interactive knowledge graph visualization of codebase structure and relationships",
            inputSchema={
                "type": "object",
                "properties": {
                    "analysis_data": {
                        "type": "object",
                        "description": "Codebase analysis data (from analyze_codebase or analyze_github_repo)"
                    },
                    "output_file": {
                        "type": "string",
                        "description": "Output HTML file path (default: neural_map.html)"
                    }
                },
                "required": ["analysis_data"]
            }
        ),
        Tool(
            name="analyze_codebase_enhanced",
            description="Perform comprehensive enhanced ecological analysis on local codebase with patterns, relationships, and interactive visualization",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Local path to codebase directory"
                    }
                },
                "required": ["path"]
            }
        ),
        Tool(
            name="generate_enterprise_cyberpunk_graph",
            description="Generate enterprise-grade cyberpunk neural network knowledge graph with professional hierarchical information architecture, semantic clustering, quality analytics, and advanced interactive controls",
            inputSchema={
                "type": "object",
                "properties": {
                    "analysis_data": {
                        "type": "object",
                        "description": "Codebase analysis data (from analyze_codebase_enhanced or similar)"
                    },
                    "output_file": {
                        "type": "string",
                        "description": "Optional output HTML filename (default: enterprise_cyberpunk_neural_graph.html)"
                    }
                },
                "required": ["analysis_data"]
            }
        ),
        Tool(
            name="get_repo_info",
            description="Get information about a GitHub repository using the GitHub API",
            inputSchema={
                "type": "object",
                "properties": {
                    "repo_url": {
                        "type": "string",
                        "description": "GitHub repository URL"
                    }
                },
                "required": ["repo_url"]
            }
        )
    ]

@app.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Handle tool calls"""
    try:
        if name == "analyze_codebase":
            path = arguments["path"]
            analysis = codebase_analyzer.analyze_codebase(path)
            
            # Create user-friendly summary instead of raw JSON
            metrics = analysis.get('metrics', {})
            summary = f"""🔍 **Codebase Analysis Complete!**

📁 **Project Path:** {path}
📈 **Analysis Results:**
• **Files Analyzed:** {metrics.get('total_files', 0)} files
• **Classes Found:** {metrics.get('total_classes', 0)} classes
• **Functions Found:** {metrics.get('total_functions', 0)} functions  
• **Import Dependencies:** {metrics.get('total_imports', 0)} imports

🚀 **Ready for Visualization:** Use this analysis to generate an interactive knowledge graph!

📊 **Next Steps:** Ask me to "generate knowledge graph" to create an interactive visualization of this codebase structure."""
            
            return [
                types.TextContent(
                    type="text",
                    text=summary
                )
            ]
        
        elif name == "analyze_github_repo":
            repo_url = arguments["repo_url"]
            target_dir = arguments.get("target_dir")
            
            if not target_dir:
                # Generate target directory from repo URL
                parsed = urlparse(repo_url)
                repo_name = parsed.path.strip('/').split('/')[-1]
                target_dir = f"./repos/{repo_name}"
            
            # Clone/update repo
            local_path = github_analyzer.clone_or_update_repo(repo_url, target_dir)
            
            # Analyze the cloned repository
            analysis = codebase_analyzer.analyze_codebase(local_path)
            analysis['repo_url'] = repo_url
            analysis['local_path'] = local_path
            
            # Create user-friendly summary
            metrics = analysis.get('metrics', {})
            repo_name = repo_url.split('/')[-1]
            summary = f"""🔍 **GitHub Repository Analysis Complete!**

🌐 **Repository:** {repo_name}
🔗 **URL:** {repo_url}
📁 **Local Path:** {local_path}

📈 **Analysis Results:**
• **Files Analyzed:** {metrics.get('total_files', 0)} files
• **Classes Found:** {metrics.get('total_classes', 0)} classes
• **Functions Found:** {metrics.get('total_functions', 0)} functions  
• **Import Dependencies:** {metrics.get('total_imports', 0)} imports

🚀 **Ready for Visualization:** Repository successfully cloned and analyzed!

📊 **Next Steps:** Ask me to "generate knowledge graph" to create an interactive visualization of this repository's architecture."""
            
            return [
                types.TextContent(
                    type="text",
                    text=summary
                )
            ]
        
        elif name == "generate_codebase_graph":
            analysis_data = arguments["analysis_data"]
            output_file = arguments.get("output_file", "codebase_graph.html")
            
            # Use specialized codebase visualizer
            net = codebase_visualizer.create_codebase_graph(analysis_data, output_file)
            
            if net:
                # Get absolute path for easy access
                abs_path = os.path.abspath(output_file)
                
                # Create user-friendly summary
                metrics = analysis_data.get('metrics', {})
                repo_name = analysis_data.get('repo_url', 'Your Project').split('/')[-1] if 'repo_url' in analysis_data else 'Your Project'
                
                summary = f"""🎉 **Knowledge Graph Generated Successfully!**

🚀 **Quick Access:**
• 📁 **File Location:** `{abs_path}`
• 🌐 **Open in Browser:** Double-click the file or drag to your browser
• 📊 **Interactive Visualization Ready**

📈 **Analysis Summary:**
• **Project:** {repo_name}
• **Files Analyzed:** {metrics.get('total_files', 0)} files
• **Classes Found:** {metrics.get('total_classes', 0)} classes  
• **Functions Found:** {metrics.get('total_functions', 0)} functions
• **Dependencies:** {metrics.get('total_imports', 0)} imports

🔄 **What's Available:**
• Interactive node exploration
• Zoom and pan controls
• Hover details for each component
• Visual relationship mapping

💡 **Next Steps:** Click the link above to explore your codebase architecture, or ask me to analyze specific components!"""
                
                return [
                    types.TextContent(
                        type="text",
                        text=summary
                    )
                ]
            else:
                return [
                    types.TextContent(
                        type="text",
                        text="❌ Failed to generate knowledge graph. Please check your analysis data and try again."
                    )
                ]
        
        elif name == "analyze_codebase_enhanced":
            path = arguments["path"]
            analysis = enhanced_analyzer.analyze_codebase(path)
            
            # Create user-friendly summary for enhanced analysis
            files_count = len(analysis.get('files', []))
            classes_count = sum(len(f.get('classes', [])) for f in analysis.get('files', []))
            functions_count = sum(len(f.get('functions', [])) for f in analysis.get('files', []))
            clusters_count = len(analysis.get('semantic_clusters', []))
            patterns_count = len(analysis.get('patterns', {}).get('design_patterns', []) + 
                                analysis.get('patterns', {}).get('architectural_patterns', []))
            
            summary = f"""🧠 **Enhanced Ecological Analysis Complete!**

🎯 **Project Path:** {path}
🔬 **Deep Analysis Results:**
• **Files Analyzed:** {files_count} files
• **Neural Cores (Classes):** {classes_count} classes
• **Synapses (Functions):** {functions_count} functions
• **Semantic Clusters:** {clusters_count} clusters
• **Architectural Patterns:** {patterns_count} patterns

🌐 **Advanced Features Detected:**
• Semantic relationship mapping
• Cross-cutting concern analysis
• Architectural pattern detection
• Code complexity metrics
• Dependency flow analysis

⚡ **Ready for Enterprise Cyberpunk Visualization:** This enhanced analysis includes all the rich metadata needed for enterprise-grade neural network visualizations!

🚀 **Next Steps:** Ask me to "generate enterprise cyberpunk graph" to create an immersive enterprise-grade visualization of your codebase consciousness!"""
            
            return [
                types.TextContent(
                    type="text",
                    text=summary
                )
            ]
        
        elif name == "generate_enterprise_cyberpunk_graph":
            analysis_data = arguments["analysis_data"]
            output_file = arguments.get("output_file", "enterprise_cyberpunk_neural_graph.html")
            
            # Generate the enterprise cyberpunk visualization
            result_file = enterprise_cyberpunk_generator.generate_enterprise_graph(analysis_data, output_file)
            
            if result_file:
                # Get absolute path for easy access
                abs_path = os.path.abspath(result_file)
                
                # Calculate stats from analysis data
                files_count = len(analysis_data.get('files', []))
                classes_count = sum(len(f.get('classes', [])) for f in analysis_data.get('files', []))
                functions_count = sum(len(f.get('functions', [])) for f in analysis_data.get('files', []))
                clusters_count = len(analysis_data.get('semantic_clusters', []))
                
                # Calculate total complexity
                total_complexity = 0
                for file_data in analysis_data.get('files', []):
                    total_complexity += file_data.get('complexity', 0)
                
                # Determine activity level
                activity_level = 'LOW'
                if total_complexity > 100:
                    activity_level = 'MEDIUM'
                if total_complexity > 300:
                    activity_level = 'HIGH'
                if total_complexity > 500:
                    activity_level = 'CRITICAL'
                
                summary = f"""🌃 **Enterprise Cyberpunk Neural Network Knowledge Graph Generated!**

⚡ **Neural Matrix Status:** ONLINE
🧠 **Digital Consciousness:** ACTIVATED
🏢 **Enterprise Controls:** ENGAGED

🎮 **Quick Access:**
• 📁 **File Location:** `{abs_path}`
• 🌐 **Open in Browser:** Double-click or drag to browser
• 🎛️ **Interactive Controls:** Gravity field, node filters, pulse animations

🔬 **Neural Network Metrics:**
• **Data Crystals (Files):** {files_count}
• **Neural Cores (Classes):** {classes_count}  
• **Synapses (Functions):** {functions_count}
• **Neural Clusters:** {clusters_count}
• **Complexity Score:** {total_complexity}
• **Activity Level:** {activity_level}

✨ **Enterprise Cyberpunk Features:**
• Professional semantic color coding system
• Hierarchical information architecture
• Advanced filtering and search capabilities
• Quality analytics and metrics dashboard
• Progressive information disclosure
• Enterprise-grade performance optimization
• Responsive professional design

🚀 **Experience:** Explore your codebase through an enterprise-grade cyberpunk interface with professional analytics, hierarchical organization, and stunning neural visualizations designed for serious code analysis!

💡 **Next Steps:** Open the file to dive into your cyberpunk neural codebase matrix!"""
                
                return [
                    types.TextContent(
                        type="text",
                        text=summary
                    )
                ]
            else:
                return [
                    types.TextContent(
                        type="text",
                        text="❌ Failed to generate enterprise cyberpunk neural graph. Please check your analysis data and try again."
                    )
                ]
        
        elif name == "get_repo_info":
            repo_url = arguments["repo_url"]
            repo_info = github_analyzer.get_repo_info(repo_url)
            
            return [
                types.TextContent(
                    type="text",
                    text=json.dumps(repo_info, indent=2, default=str)
                )
            ]
        
        else:
            return [
                types.TextContent(
                    type="text",
                    text=f"Unknown tool: {name}"
                )
            ]
    
    except Exception as e:
        logger.error(f"Error in tool {name}: {e}")
        return [
            types.TextContent(
                type="text",
                text=f"Error: {str(e)}"
            )
        ]

def _find_free_port() -> int:
    """Find an available port for local server"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

def _start_local_server(html_file: str) -> int:
    """Start a local HTTP server to serve the HTML file"""
    port = _find_free_port()
    
    class CustomHandler(SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            # Suppress server logs
            pass
    
    def run_server():
        try:
            httpd = HTTPServer(('localhost', port), CustomHandler)
            # Set a timeout so server doesn't run forever
            httpd.timeout = 300  # 5 minutes
            httpd.serve_forever()
        except:
            pass  # Silently handle any server errors
    
    # Start server in background thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    return port

def format_analysis_for_llm(analysis_data: Dict[str, Any]) -> str:
    """Format codebase analysis data into a text summary for LLM processing"""
    text_parts = []
    
    # Add metadata
    if 'repo_url' in analysis_data:
        text_parts.append(f"Repository: {analysis_data['repo_url']}")
    
    if 'local_path' in analysis_data:
        text_parts.append(f"Local Path: {analysis_data['local_path']}")
    
    # Add metrics
    metrics = analysis_data.get('metrics', {})
    if metrics:
        text_parts.append(f"Codebase Metrics:")
        text_parts.append(f"- Total Files: {metrics.get('total_files', 0)}")
        text_parts.append(f"- Total Classes: {metrics.get('total_classes', 0)}")
        text_parts.append(f"- Total Functions: {metrics.get('total_functions', 0)}")
        text_parts.append(f"- Total Imports: {metrics.get('total_imports', 0)}")
    
    # Add file structure
    files = analysis_data.get('files', [])
    if files:
        text_parts.append("\nCodebase Structure:")
        for file_info in files[:20]:  # Limit to first 20 files
            file_path = file_info.get('file', '')
            file_type = file_info.get('type', 'unknown')
            text_parts.append(f"- {file_path} ({file_type})")
            
            # Add classes
            classes = file_info.get('classes', [])
            for cls in classes:
                text_parts.append(f"  - Class: {cls.get('name', 'Unknown')}")
                methods = cls.get('methods', [])
                for method in methods:
                    text_parts.append(f"    - Method: {method}")
            
            # Add functions
            functions = file_info.get('functions', [])
            for func in functions:
                text_parts.append(f"  - Function: {func.get('name', 'Unknown')}")
    
    # Add imports and dependencies
    imports = analysis_data.get('imports', [])
    if imports:
        text_parts.append("\nImports and Dependencies:")
        unique_modules = set()
        for imp in imports:
            module = imp.get('module', '')
            if module and module not in unique_modules:
                unique_modules.add(module)
                text_parts.append(f"- Import: {module}")
    
    return "\n".join(text_parts)

async def main():
    # Import here to avoid issues if mcp package is not available
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="codebase-knowledge-graph",
                server_version="0.1.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())