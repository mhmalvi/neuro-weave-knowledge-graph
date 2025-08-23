#!/usr/bin/env python3
"""
Test script for the Codebase Knowledge Graph MCP Server
"""

import json
import asyncio
from mcp_server import codebase_analyzer, codebase_visualizer

async def test_analyze_current_codebase():
    """Test analyzing the current codebase"""
    print("🧠 Testing codebase analysis...")
    
    try:
        # Analyze the current directory
        analysis = codebase_analyzer.analyze_codebase(".")
        
        print(f"✅ Analysis completed!")
        print(f"📊 Metrics:")
        print(f"   - Files: {analysis['metrics']['total_files']}")
        print(f"   - Classes: {analysis['metrics']['total_classes']}")
        print(f"   - Functions: {analysis['metrics']['total_functions']}")
        print(f"   - Imports: {analysis['metrics']['total_imports']}")
        
        # Generate visualization
        print("\n🎨 Generating codebase visualization...")
        net = codebase_visualizer.create_codebase_graph(analysis, "test_codebase_graph.html")
        
        if net:
            print("✅ Visualization generated successfully!")
            print("🌐 Open 'test_codebase_graph.html' in your browser to view the interactive graph")
        else:
            print("❌ Failed to generate visualization")
            
        return analysis
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_sample_analysis():
    """Test with sample analysis data"""
    print("\n🧪 Testing with sample analysis data...")
    
    sample_analysis = {
        "files": [
            {
                "file": "./app.py",
                "type": "python",
                "classes": [],
                "functions": [
                    {"name": "main", "line": 10, "args": []},
                    {"name": "setup_app", "line": 25, "args": ["config"]}
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
                        "methods": ["__init__", "analyze_codebase", "_analyze_file", "_analyze_python"]
                    },
                    {
                        "name": "GitHubAnalyzer", 
                        "line": 280,
                        "bases": [],
                        "methods": ["__init__", "clone_or_update_repo", "get_repo_info"]
                    }
                ],
                "functions": [
                    {"name": "handle_list_resources", "line": 328, "args": []},
                    {"name": "handle_call_tool", "line": 398, "args": ["name", "arguments"]},
                    {"name": "main", "line": 548, "args": []}
                ],
                "imports": [
                    {"module": "mcp.server", "file": "./mcp_server.py", "line": 21},
                    {"module": "generate_knowledge_graph", "file": "./mcp_server.py", "line": 32}
                ]
            }
        ],
        "classes": [],
        "functions": [],
        "imports": [],
        "metrics": {
            "total_files": 3,
            "total_classes": 2, 
            "total_functions": 8,
            "total_imports": 6
        }
    }
    
    # Populate the flattened arrays
    for file_info in sample_analysis["files"]:
        sample_analysis["classes"].extend(file_info.get("classes", []))
        sample_analysis["functions"].extend(file_info.get("functions", []))
        sample_analysis["imports"].extend(file_info.get("imports", []))
    
    print("🎨 Generating sample visualization...")
    net = codebase_visualizer.create_codebase_graph(sample_analysis, "sample_codebase_graph.html")
    
    if net:
        print("✅ Sample visualization generated!")
        print("🌐 Open 'sample_codebase_graph.html' in your browser to view the interactive graph")
    else:
        print("❌ Failed to generate sample visualization")

async def main():
    """Main test function"""
    print("🧠 NeuroWeave Codebase Knowledge Graph MCP Server - Test Suite")
    print("=" * 60)
    
    # Test current codebase analysis
    analysis = await test_analyze_current_codebase()
    
    # Test with sample data
    test_sample_analysis()
    
    print("\n" + "=" * 60)
    print("🎉 Test suite completed!")
    print("\nNext steps:")
    print("1. Install the MCP server: pip install -e .")
    print("2. Configure Claude with the MCP server using mcp_config.json")
    print("3. Use the MCP tools to analyze and visualize codebases")

if __name__ == "__main__":
    asyncio.run(main())