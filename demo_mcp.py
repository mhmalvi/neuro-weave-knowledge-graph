#!/usr/bin/env python3
"""
Demo script showing MCP server functionality
"""

import os
import json
from pathlib import Path
from codebase_visualizer import CodebaseVisualizer

def demo_codebase_analysis():
    """Demonstrate codebase analysis functionality"""
    
    print("=" * 60)
    print("MCP SERVER DEMO - CODEBASE ANALYSIS")
    print("=" * 60)
    
    # Initialize visualizer
    visualizer = CodebaseVisualizer()
    
    # Analyze current directory
    print("\n1. ANALYZING CURRENT CODEBASE...")
    current_dir = Path(".")
    
    # Get file statistics
    python_files = list(current_dir.glob("*.py"))
    js_files = list(current_dir.glob("*.js")) 
    html_files = list(current_dir.glob("*.html"))
    
    print(f"   Python files: {len(python_files)}")
    print(f"   JavaScript files: {len(js_files)}")  
    print(f"   HTML files: {len(html_files)}")
    
    # Show sample files
    print(f"\n2. SAMPLE FILES FOUND:")
    all_files = python_files + js_files + html_files
    for file in all_files[:8]:
        print(f"   - {file.name}")
    
    # Analyze Python files for structure
    print(f"\n3. ANALYZING CODE STRUCTURE...")
    total_functions = 0
    total_classes = 0
    
    for py_file in python_files:
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple parsing for demo
            functions = content.count('def ')
            classes = content.count('class ')
            imports = content.count('import ') + content.count('from ')
            
            total_functions += functions
            total_classes += classes
            
            if functions > 0 or classes > 0:
                print(f"   {py_file.name}: {functions} functions, {classes} classes")
                
        except Exception as e:
            continue
    
    print(f"\n4. SUMMARY STATISTICS:")
    print(f"   Total files analyzed: {len(all_files)}")
    print(f"   Total functions found: {total_functions}")
    print(f"   Total classes found: {total_classes}")
    
    # Generate visualization
    print(f"\n5. GENERATING KNOWLEDGE GRAPH...")
    
    # Create sample data for visualization
    sample_data = {
        'files': [{'name': f.name, 'type': 'file'} for f in all_files[:6]],
        'functions': [{'name': f'function_{i}', 'file': python_files[0].name if python_files else 'app.py'} for i in range(min(total_functions, 5))],
        'classes': [{'name': f'Class_{i}', 'file': python_files[0].name if python_files else 'app.py'} for i in range(min(total_classes, 3))]
    }
    
    # Generate graph
    output_file = "mcp_demo_graph.html"
    try:
        visualizer.generate_codebase_graph(sample_data, output_file)
        file_size = os.path.getsize(output_file)
        print(f"   Knowledge graph saved to: {output_file}")
        print(f"   File size: {file_size:,} bytes")
    except Exception as e:
        print(f"   Error generating graph: {e}")
    
    print(f"\n6. MCP TOOLS AVAILABLE:")
    print("   - analyze_codebase: Analyze local directories")
    print("   - analyze_github_repo: Clone and analyze GitHub repos")  
    print("   - generate_codebase_graph: Create interactive visualizations")
    print("   - get_repo_info: Fetch GitHub repository metadata")
    
    print(f"\n7. INTEGRATION READY:")
    print("   - Claude Desktop: Add to claude_desktop_config.json")
    print("   - Custom MCP clients: Use standard MCP protocol")
    print("   - Python applications: Direct module import")
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    
    return {
        'files_analyzed': len(all_files),
        'functions_found': total_functions, 
        'classes_found': total_classes,
        'visualization_created': output_file if os.path.exists(output_file) else None
    }

if __name__ == "__main__":
    demo_codebase_analysis()