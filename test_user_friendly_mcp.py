#!/usr/bin/env python3
"""
Test script to demonstrate user-friendly MCP improvements
"""

import asyncio
import json
from mcp_server import codebase_analyzer, codebase_visualizer

def test_user_friendly_outputs():
    """Test the improved user-friendly MCP outputs"""
    
    print("=" * 70)
    print("TESTING USER-FRIENDLY MCP IMPROVEMENTS")
    print("=" * 70)
    
    # Test 1: Codebase Analysis
    print("\n1. TESTING CODEBASE ANALYSIS OUTPUT...")
    
    try:
        # Analyze current directory (small subset for testing)
        current_path = "."
        analysis = codebase_analyzer.analyze_codebase(current_path)
        
        # Simulate the user-friendly output format
        metrics = analysis.get('metrics', {})
        summary = f"""**Codebase Analysis Complete!**

**Project Path:** {current_path}
**Analysis Results:**
• Files Analyzed: {metrics.get('total_files', 0)} files
• Classes Found: {metrics.get('total_classes', 0)} classes
• Functions Found: {metrics.get('total_functions', 0)} functions  
• Import Dependencies: {metrics.get('total_imports', 0)} imports

**Ready for Visualization:** Use this analysis to generate an interactive knowledge graph!

**Next Steps:** Ask me to "generate knowledge graph" to create an interactive visualization of this codebase structure."""
        
        print(summary)
        
        # Test 2: Knowledge Graph Generation
        print("\n" + "=" * 50)
        print("2. TESTING KNOWLEDGE GRAPH GENERATION...")
        
        # Create a simplified analysis for testing
        test_data = {
            'files': [
                {
                    'file': 'app.py',
                    'type': 'python',
                    'classes': [],
                    'functions': [{'name': 'main', 'line': 10, 'file': 'app.py'}],
                    'imports': [{'module': 'streamlit', 'alias': 'st', 'file': 'app.py', 'line': 1}]
                },
                {
                    'file': 'mcp_server.py', 
                    'type': 'python',
                    'classes': [{'name': 'CodebaseAnalyzer', 'line': 43, 'file': 'mcp_server.py', 'methods': ['analyze_codebase']}],
                    'functions': [{'name': 'handle_call_tool', 'line': 437, 'file': 'mcp_server.py'}],
                    'imports': []
                }
            ],
            'metrics': {
                'total_files': 2,
                'total_classes': 1, 
                'total_functions': 2,
                'total_imports': 1
            },
            'repo_url': 'https://github.com/mhmalvi/neuro-weave-knowledge-graph'
        }
        
        # Generate visualization
        output_file = "test_user_friendly.html"
        net = codebase_visualizer.create_codebase_graph(test_data, output_file)
        
        if net:
            import os
            abs_path = os.path.abspath(output_file)
            metrics = test_data.get('metrics', {})
            repo_name = test_data.get('repo_url', 'Your Project').split('/')[-1]
            
            summary = f"""**Knowledge Graph Generated Successfully!**

**Quick Access:**
• File Location: {abs_path}
• Open in Browser: Double-click the file or drag to your browser
• Interactive Visualization Ready

**Analysis Summary:**
• Project: {repo_name}
• Files Analyzed: {metrics.get('total_files', 0)} files
• Classes Found: {metrics.get('total_classes', 0)} classes  
• Functions Found: {metrics.get('total_functions', 0)} functions
• Dependencies: {metrics.get('total_imports', 0)} imports

**What's Available:**
• Interactive node exploration
• Zoom and pan controls
• Hover details for each component
• Visual relationship mapping

**Next Steps:** Click the file path above to explore your codebase architecture, or ask me to analyze specific components!"""
            
            print(summary)
            print(f"\nVisualization saved to: {abs_path}")
            print(f"File size: {os.path.getsize(output_file):,} bytes")
            
        else:
            print("Failed to generate visualization")
            
    except Exception as e:
        print(f"Error during testing: {e}")
    
    print("\n" + "=" * 70)
    print("USER-FRIENDLY MCP IMPROVEMENTS SUMMARY:")
    print("• Concise, readable summaries instead of raw JSON")
    print("• Clear file paths and access instructions")  
    print("• Enhanced formatting for better UX")
    print("• Step-by-step guidance for next actions")
    print("• Progress indicators and success confirmations")
    print("• Non-technical language suitable for all users")
    print("=" * 70)

if __name__ == "__main__":
    test_user_friendly_outputs()