#!/usr/bin/env python3

import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from enhanced_ecological_analyzer import EnhancedEcologicalAnalyzer

def main():
    # Focus on main project files only
    main_files = [
        "app.py",
        "codebase_visualizer.py", 
        "mcp_server.py",
        "generate_knowledge_graph.py",
        "demo_mcp.py",
        "test_mcp.py",
        "test_standalone.py",
        "enhanced_ecological_analyzer.py"
    ]
    
    analyzer = EnhancedEcologicalAnalyzer()
    
    # Override the analyze_structure method to focus on specific files
    def focused_analyze_structure(root: Path):
        for file_name in main_files:
            py_file = root / file_name
            if py_file.exists():
                try:
                    with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    import ast
                    tree = ast.parse(content, filename=str(py_file))
                    file_analysis = analyzer._analyze_python_file_deep(py_file, tree, content)
                    analyzer.analysis_data['files'].append(file_analysis)
                    
                except Exception as e:
                    print(f"Error analyzing {py_file}: {e}")
    
    # Replace the method
    analyzer._analyze_structure = focused_analyze_structure
    
    # Run the analysis
    result = analyzer.analyze_codebase(".")
    
    # Save results
    import json
    with open("enhanced_ecological_analysis.json", "w") as f:
        json.dump(result, f, indent=2)
    
    print(f"Enhanced ecological analysis complete!")
    print(f"Analyzed {len(result['files'])} files")
    print(f"Found {len(result['classes'])} classes")
    print(f"Found {len(result['functions'])} functions")
    print(f"Discovered {len(result['relationships']['inheritance'])} inheritance relationships")
    print(f"Discovered {len(result['relationships']['dependency'])} dependency relationships")
    print(f"Detected {len(result['patterns']['design_patterns'])} design patterns")
    print(f"Identified {len(result['cross_cutting_concerns'])} cross-cutting concerns")
    print(f"Created {len(result['semantic_clusters'])} semantic clusters")

if __name__ == "__main__":
    main()