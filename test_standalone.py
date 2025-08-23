#!/usr/bin/env python3
"""
Standalone test for codebase analysis and visualization (without MCP dependencies)
"""

import json
import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from codebase_visualizer import CodebaseVisualizer

# Simple codebase analyzer without MCP dependencies
class SimpleCodebaseAnalyzer:
    """Simplified analyzer for testing without MCP dependencies"""
    
    def __init__(self):
        self.supported_extensions = {'.py', '.js', '.ts', '.jsx', '.tsx', '.java'}
    
    def analyze_codebase(self, path: str):
        """Basic codebase analysis"""
        analysis = {
            'files': [],
            'classes': [],
            'functions': [],
            'imports': [],
            'metrics': {}
        }
        
        # Walk through directory
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
            
            for file in files:
                if any(file.endswith(ext) for ext in self.supported_extensions):
                    file_path = os.path.join(root, file)
                    file_info = {
                        'file': file_path,
                        'type': 'python' if file.endswith('.py') else 'javascript',
                        'classes': [],
                        'functions': [],
                        'imports': []
                    }
                    
                    # Simple analysis (just file info for demo)
                    if file.endswith('.py'):
                        file_info['functions'] = [{'name': f'function_in_{file}', 'line': 1}]
                        file_info['imports'] = [{'module': 'os', 'file': file_path}]
                    
                    analysis['files'].append(file_info)
        
        # Calculate metrics
        analysis['metrics'] = {
            'total_files': len(analysis['files']),
            'total_classes': 0,
            'total_functions': sum(len(f.get('functions', [])) for f in analysis['files']),
            'total_imports': sum(len(f.get('imports', [])) for f in analysis['files'])
        }
        
        return analysis

def test_visualization():
    """Test the codebase visualization"""
    print("Testing Codebase Knowledge Graph Visualization")
    print("=" * 50)
    
    # Create sample analysis data
    sample_analysis = {
        "repo_url": "https://github.com/example/knowledge-graph-llms",
        "files": [
            {
                "file": "./app.py",
                "type": "python",
                "classes": [],
                "functions": [
                    {"name": "main", "line": 10, "args": []},
                    {"name": "setup_streamlit", "line": 25, "args": ["config"]}
                ],
                "imports": [
                    {"module": "streamlit", "file": "./app.py", "line": 2},
                    {"module": "generate_knowledge_graph", "file": "./app.py", "line": 4}
                ]
            },
            {
                "file": "./generate_knowledge_graph.py", 
                "type": "python",
                "classes": [],
                "functions": [
                    {"name": "extract_graph_data", "line": 22, "args": ["text"]},
                    {"name": "visualize_graph", "line": 37, "args": ["graph_documents"]},
                    {"name": "generate_knowledge_graph", "line": 331, "args": ["text"]}
                ],
                "imports": [
                    {"module": "langchain_experimental.graph_transformers", "file": "./generate_knowledge_graph.py", "line": 1},
                    {"module": "pyvis.network", "file": "./generate_knowledge_graph.py", "line": 4}
                ]
            },
            {
                "file": "./mcp_server.py",
                "type": "python", 
                "classes": [
                    {
                        "name": "CodebaseAnalyzer",
                        "line": 42,
                        "bases": [],
                        "methods": ["__init__", "analyze_codebase", "_analyze_file"]
                    },
                    {
                        "name": "GitHubAnalyzer", 
                        "line": 280,
                        "bases": [],
                        "methods": ["__init__", "clone_or_update_repo", "get_repo_info"]
                    },
                    {
                        "name": "CodebaseVisualizer",
                        "line": 320,
                        "bases": [],
                        "methods": ["__init__", "create_codebase_graph", "_add_node"]
                    }
                ],
                "functions": [
                    {"name": "handle_list_resources", "line": 400, "args": []},
                    {"name": "handle_call_tool", "line": 450, "args": ["name", "arguments"]},
                    {"name": "main", "line": 600, "args": []}
                ],
                "imports": [
                    {"module": "mcp.server", "file": "./mcp_server.py", "line": 21},
                    {"module": "generate_knowledge_graph", "file": "./mcp_server.py", "line": 32}
                ]
            },
            {
                "file": "./codebase_visualizer.py",
                "type": "python",
                "classes": [
                    {
                        "name": "CodebaseVisualizer",
                        "line": 15,
                        "bases": [],
                        "methods": ["__init__", "create_codebase_graph", "_add_node", "_configure_network"]
                    }
                ],
                "functions": [],
                "imports": [
                    {"module": "pyvis.network", "file": "./codebase_visualizer.py", "line": 10},
                    {"module": "os", "file": "./codebase_visualizer.py", "line": 8}
                ]
            }
        ],
        "classes": [],
        "functions": [],
        "imports": [],
        "metrics": {
            "total_files": 4,
            "total_classes": 4, 
            "total_functions": 8,
            "total_imports": 8
        }
    }
    
    # Populate flattened arrays
    for file_info in sample_analysis["files"]:
        sample_analysis["classes"].extend(file_info.get("classes", []))
        sample_analysis["functions"].extend(file_info.get("functions", []))
        sample_analysis["imports"].extend(file_info.get("imports", []))
    
    print(f"Sample Analysis Data:")
    print(f"   - Files: {sample_analysis['metrics']['total_files']}")
    print(f"   - Classes: {sample_analysis['metrics']['total_classes']}")
    print(f"   - Functions: {sample_analysis['metrics']['total_functions']}")
    print(f"   - Imports: {sample_analysis['metrics']['total_imports']}")
    
    # Generate visualization
    print("\nGenerating codebase knowledge graph...")
    visualizer = CodebaseVisualizer()
    
    try:
        net = visualizer.create_codebase_graph(sample_analysis, "demo_codebase_graph.html")
        
        if net:
            print("Knowledge graph generated successfully!")
            print("Open 'demo_codebase_graph.html' in your browser to view the interactive visualization")
            
            # Check if file was created
            if os.path.exists("demo_codebase_graph.html"):
                file_size = os.path.getsize("demo_codebase_graph.html")
                print(f"File size: {file_size:,} bytes")
            else:
                print("HTML file not found after generation")
                
        else:
            print("Failed to generate visualization")
            
    except Exception as e:
        print(f"Error generating visualization: {e}")
        import traceback
        traceback.print_exc()

def test_simple_analysis():
    """Test simple codebase analysis on current directory"""
    print("\nTesting simple codebase analysis...")
    
    analyzer = SimpleCodebaseAnalyzer()
    
    try:
        analysis = analyzer.analyze_codebase(".")
        print(f"Analyzed current directory")
        print(f"Found {analysis['metrics']['total_files']} files")
        
        # Show some files
        print("Sample files found:")
        for file_info in analysis['files'][:5]:
            print(f"   - {file_info['file']}")
            
    except Exception as e:
        print(f"Error in analysis: {e}")

def main():
    """Main test function"""
    print("NeuroWeave Codebase Knowledge Graph - Standalone Test")
    print("=" * 60)
    
    test_simple_analysis()
    test_visualization()
    
    print("\n" + "=" * 60)
    print("Standalone test completed!")
    print("\nNext steps:")
    print("1. Install MCP dependencies: pip install mcp")
    print("2. Configure Claude Desktop with the MCP server")
    print("3. Use the MCP tools through Claude to analyze real codebases")
    print("\nTip: Check out 'demo_codebase_graph.html' for an example visualization!")

if __name__ == "__main__":
    main()