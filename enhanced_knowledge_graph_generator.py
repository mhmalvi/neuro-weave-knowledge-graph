#!/usr/bin/env python3
"""
Enhanced Multi-Dimensional Knowledge Graph Generator

Creates comprehensive interactive visualizations showing multiple levels
of ecological relationships in codebases including:
- Structural relationships (inheritance, composition, aggregation)
- Functional relationships (call graphs, data flows)
- Semantic relationships (clusters, patterns)
- Quality relationships (complexity, coupling, cohesion)
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple
from pyvis.network import Network
import colorsys
import hashlib
import math

class EnhancedKnowledgeGraphGenerator:
    """Generates multi-dimensional interactive knowledge graphs"""
    
    def __init__(self):
        self.network = None
        self.node_id_counter = 0
        self.node_registry = {}
        
        # Cyberpunk color schemes for different relationship types (default style)
        self.node_colors = {
            'file': '#FF00FF',           # Magenta
            'class': '#39FF14',          # Neon Green  
            'function': '#00FFFF',       # Cyan
            'method': '#FF1493',         # Deep Pink
            'import': '#9400D3',         # Violet
            'module': '#FF4500',         # Orange Red
            'pattern': '#FFD700',        # Gold
            'cluster': '#C0C0C0',        # Silver
            'concern': '#ADFF2F',        # Green Yellow
            'dependency': '#00CED1',     # Dark Turquoise
            'data_flow': '#FF6347',      # Tomato
            'inheritance': '#1E90FF',    # Dodger Blue
            'composition': '#32CD32',    # Lime Green
        }
        
        self.edge_colors = {
            'contains': '#808080',       # Gray
            'inherits': '#FF0000',       # Red
            'calls': '#00FF00',          # Green  
            'imports': '#0000FF',        # Blue
            'depends_on': '#FFA500',     # Orange
            'composes': '#8A2BE2',       # Blue Violet
            'flows_to': '#20B2AA',       # Light Sea Green
            'clusters_with': '#FF1493',  # Deep Pink
            'implements': '#ADFF2F',     # Green Yellow
            'associates': '#00BFFF',     # Deep Sky Blue
        }
        
        self.edge_styles = {
            'contains': 'solid',
            'inherits': 'arrows',
            'calls': 'dashed',
            'imports': 'dotted',
            'depends_on': 'solid',
            'composes': 'arrows',
            'flows_to': 'arrows',
            'clusters_with': 'dashed',
            'implements': 'arrows',
            'associates': 'dotted',
        }
    
    def generate_enhanced_graph(self, analysis_data: Dict[str, Any], output_file: str = "enhanced_codebase_graph.html") -> str:
        """Generate comprehensive multi-dimensional knowledge graph"""
        
        # Initialize network with cyberpunk theme
        self.network = Network(
            height="100vh",
            width="100%", 
            bgcolor="#0a0a0a",  # Darker background for cyberpunk feel
            font_color="#00FFFF",  # Cyan text
            directed=True
        )
        
        # Configure advanced physics for better layout
        self.network.set_options("""
        {
          "physics": {
            "enabled": true,
            "stabilization": {"iterations": 100},
            "barnesHut": {
              "gravitationalConstant": -8000,
              "centralGravity": 0.3,
              "springLength": 95,
              "springConstant": 0.04,
              "damping": 0.09,
              "avoidOverlap": 1
            }
          },
          "interaction": {
            "hover": true,
            "tooltipDelay": 200,
            "hideEdgesOnDrag": true,
            "hideNodesOnDrag": true
          },
          "nodes": {
            "borderWidth": 2,
            "borderWidthSelected": 4,
            "font": {"size": 14, "color": "white"},
            "shadow": {"enabled": true}
          },
          "edges": {
            "width": 2,
            "shadow": {"enabled": true},
            "smooth": {"type": "continuous"}
          }
        }
        """)
        
        # Step 1: Add structural nodes (files, classes, functions)
        self._add_structural_nodes(analysis_data)
        
        # Step 2: Add relationship edges 
        self._add_relationship_edges(analysis_data)
        
        # Step 3: Add semantic clusters
        self._add_semantic_clusters(analysis_data)
        
        # Step 4: Add architectural patterns
        self._add_architectural_patterns(analysis_data)
        
        # Step 5: Add cross-cutting concerns
        self._add_cross_cutting_concerns(analysis_data)
        
        # Step 6: Add quality metrics visualization
        self._add_quality_metrics(analysis_data)
        
        # Generate enhanced HTML with custom controls
        html_content = self._generate_enhanced_html(analysis_data)
        
        # Save the visualization
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_file
    
    def _add_structural_nodes(self, analysis_data: Dict[str, Any]):
        """Add nodes for files, classes, and functions"""
        
        for file_data in analysis_data.get('files', []):
            file_path = file_data['file']
            
            # Add file node
            file_id = self._get_node_id(f"file:{file_path}")
            complexity_score = file_data.get('complexity', 0)
            size_factor = min(max(file_data.get('lines', 1) / 100, 0.5), 3.0)
            
            self.network.add_node(
                file_id,
                label=Path(file_path).name,
                title=f"File: {file_path}<br/>Lines: {file_data.get('lines', 0)}<br/>Complexity: {complexity_score}",
                color=self._adjust_color_intensity(self.node_colors['file'], complexity_score / 10),
                size=20 * size_factor,
                shape='box',
                group='files'
            )
            
            # Add class nodes
            for class_data in file_data.get('classes', []):
                class_id = self._get_node_id(f"class:{class_data['name']}:{file_path}")
                method_count = len(class_data.get('methods', []))
                
                self.network.add_node(
                    class_id,
                    label=class_data['name'],
                    title=f"Class: {class_data['name']}<br/>File: {file_path}<br/>Methods: {method_count}<br/>Line: {class_data.get('line', 0)}",
                    color=self._adjust_color_intensity(self.node_colors['class'], method_count / 10),
                    size=15 + method_count * 2,
                    shape='triangle',
                    group='classes'
                )
                
                # Connect class to file
                self.network.add_edge(
                    file_id, class_id,
                    color=self.edge_colors['contains'],
                    width=2,
                    title="contains"
                )
                
                # Add method nodes
                for method_data in class_data.get('methods', []):
                    method_id = self._get_node_id(f"method:{method_data['name']}:{class_data['name']}:{file_path}")
                    method_complexity = method_data.get('complexity', 1)
                    
                    self.network.add_node(
                        method_id,
                        label=method_data['name'],
                        title=f"Method: {method_data['name']}<br/>Class: {class_data['name']}<br/>Complexity: {method_complexity}<br/>Args: {len(method_data.get('args', []))}",
                        color=self._adjust_color_intensity(self.node_colors['method'], method_complexity / 5),
                        size=8 + method_complexity * 2,
                        shape='diamond',
                        group='methods'
                    )
                    
                    # Connect method to class
                    self.network.add_edge(
                        class_id, method_id,
                        color=self.edge_colors['contains'],
                        width=1,
                        title="contains"
                    )
            
            # Add function nodes (top-level functions)
            for func_data in file_data.get('functions', []):
                func_id = self._get_node_id(f"function:{func_data['name']}:{file_path}")
                func_complexity = func_data.get('complexity', 1)
                
                self.network.add_node(
                    func_id,
                    label=func_data['name'],
                    title=f"Function: {func_data['name']}<br/>File: {file_path}<br/>Complexity: {func_complexity}<br/>Args: {len(func_data.get('args', []))}",
                    color=self._adjust_color_intensity(self.node_colors['function'], func_complexity / 5),
                    size=10 + func_complexity * 2,
                    shape='dot',
                    group='functions'
                )
                
                # Connect function to file
                self.network.add_edge(
                    file_id, func_id,
                    color=self.edge_colors['contains'],
                    width=1,
                    title="contains"
                )
    
    def _add_relationship_edges(self, analysis_data: Dict[str, Any]):
        """Add edges for various relationships"""
        
        relationships = analysis_data.get('relationships', {})
        
        # Inheritance relationships
        for rel in relationships.get('inheritance', []):
            parent_id = self._find_class_node_id(rel['parent'])
            child_id = self._find_class_node_id(rel['child'])
            
            if parent_id and child_id:
                self.network.add_edge(
                    child_id, parent_id,
                    color=self.edge_colors['inherits'],
                    width=3,
                    title=f"{rel['child']} inherits from {rel['parent']}",
                    arrows='to'
                )
        
        # Dependency relationships
        for rel in relationships.get('dependency', []):
            source_id = self._find_file_node_id(rel['source'])
            
            # Try to find target as file or module
            target_id = self._find_file_node_id(rel['target'])
            if not target_id:
                # Create module node if it doesn't exist
                target_id = self._get_node_id(f"module:{rel['target']}")
                if target_id not in self.node_registry:
                    self.network.add_node(
                        target_id,
                        label=rel['target'],
                        title=f"Module: {rel['target']}",
                        color=self.node_colors['module'],
                        size=12,
                        shape='ellipse',
                        group='modules'
                    )
                    self.node_registry[target_id] = True
            
            if source_id and target_id:
                edge_style = 'dotted' if rel.get('import_type') == 'from_import' else 'solid'
                self.network.add_edge(
                    source_id, target_id,
                    color=self.edge_colors['depends_on'],
                    width=1,
                    title=f"depends on {rel['target']}",
                    dashes=edge_style == 'dotted'
                )
        
        # Call graph relationships
        for rel in relationships.get('call_graph', []):
            caller_id = self._find_function_node_id(rel['caller'])
            callee_id = self._find_function_node_id(rel['callee'])
            
            if caller_id and callee_id:
                self.network.add_edge(
                    caller_id, callee_id,
                    color=self.edge_colors['calls'],
                    width=1,
                    title=f"{rel['caller']} calls {rel['callee']}",
                    dashes=True
                )
        
        # Data flow relationships
        for rel in relationships.get('data_flow', []):
            func_id = self._find_function_node_id(rel['function'])
            if func_id and rel.get('flow'):
                # Create data flow visualization
                for flow_item in rel['flow']:
                    if ' -> ' in flow_item:
                        # Create data node and connect
                        data_id = self._get_node_id(f"data:{flow_item}")
                        self.network.add_node(
                            data_id,
                            label=flow_item.split(' -> ')[-1],
                            title=f"Data flow: {flow_item}",
                            color=self.node_colors['data_flow'],
                            size=6,
                            shape='dot',
                            group='data_flow'
                        )
                        
                        self.network.add_edge(
                            func_id, data_id,
                            color=self.edge_colors['flows_to'],
                            width=1,
                            title=flow_item,
                            arrows='to'
                        )
    
    def _add_semantic_clusters(self, analysis_data: Dict[str, Any]):
        """Add semantic clusters as special nodes"""
        
        for cluster in analysis_data.get('semantic_clusters', []):
            cluster_id = self._get_node_id(f"cluster:{cluster['name']}")
            cohesion_score = cluster.get('cohesion_score', 0.5)
            
            self.network.add_node(
                cluster_id,
                label=f"📦 {cluster['name']}",
                title=f"Cluster: {cluster['name']}<br/>Type: {cluster.get('type', 'unknown')}<br/>Files: {len(cluster.get('files', []))}<br/>Cohesion: {cohesion_score:.2f}",
                color=self._adjust_color_intensity(self.node_colors['cluster'], cohesion_score),
                size=20 + len(cluster.get('files', [])) * 2,
                shape='hexagon',
                group='clusters'
            )
            
            # Connect cluster to its files
            for file_path in cluster.get('files', []):
                file_id = self._find_file_node_id(file_path)
                if file_id:
                    self.network.add_edge(
                        cluster_id, file_id,
                        color=self.edge_colors['clusters_with'],
                        width=2,
                        title=f"clusters with {Path(file_path).name}",
                        dashes=True
                    )
    
    def _add_architectural_patterns(self, analysis_data: Dict[str, Any]):
        """Add architectural patterns as special nodes"""
        
        patterns = analysis_data.get('patterns', {})
        all_patterns = (patterns.get('design_patterns', []) + 
                       patterns.get('architectural_patterns', []))
        
        for pattern in all_patterns:
            pattern_id = self._get_node_id(f"pattern:{pattern}")
            
            self.network.add_node(
                pattern_id,
                label=f"🏗️ {pattern}",
                title=f"Pattern: {pattern}<br/>Type: Architectural/Design Pattern",
                color=self.node_colors['pattern'],
                size=25,
                shape='star',
                group='patterns'
            )
    
    def _add_cross_cutting_concerns(self, analysis_data: Dict[str, Any]):
        """Add cross-cutting concerns as special nodes"""
        
        concern_files = {}
        for concern_data in analysis_data.get('cross_cutting_concerns', []):
            for concern in concern_data.get('concerns', []):
                if concern not in concern_files:
                    concern_files[concern] = []
                concern_files[concern].append(concern_data['file'])
        
        for concern, files in concern_files.items():
            concern_id = self._get_node_id(f"concern:{concern}")
            
            self.network.add_node(
                concern_id,
                label=f"⚡ {concern}",
                title=f"Cross-cutting Concern: {concern}<br/>Affects {len(files)} files",
                color=self.node_colors['concern'],
                size=15 + len(files) * 2,
                shape='triangle',
                group='concerns'
            )
            
            # Connect to affected files
            for file_path in files:
                file_id = self._find_file_node_id(file_path)
                if file_id:
                    self.network.add_edge(
                        concern_id, file_id,
                        color=self.edge_colors['associates'],
                        width=1,
                        title=f"affects {Path(file_path).name}",
                        dashes=True
                    )
    
    def _add_quality_metrics(self, analysis_data: Dict[str, Any]):
        """Enhance nodes with quality metrics visualization"""
        
        metrics = analysis_data.get('metrics', {})
        
        # Add complexity indicators
        complexity_data = metrics.get('complexity', {})
        for file_path, complexity_info in complexity_data.items():
            file_id = self._find_file_node_id(file_path)
            if file_id and file_id in self.network.nodes:
                # Update node with complexity visualization
                node = next(n for n in self.network.nodes if n['id'] == file_id)
                cyclomatic = complexity_info.get('cyclomatic', 0)
                
                # Add complexity indicator to title
                current_title = node.get('title', '')
                node['title'] = f"{current_title}<br/>🧮 Cyclomatic Complexity: {cyclomatic}"
                
                # Adjust border based on complexity
                if cyclomatic > 10:
                    node['borderWidth'] = 5
                    node['color'] = {'border': '#ff0000', 'background': node['color']}
        
        # Add coupling indicators
        coupling_data = metrics.get('coupling', {})
        for file_path, coupling_info in coupling_data.items():
            file_id = self._find_file_node_id(file_path)
            if file_id and file_id in self.network.nodes:
                node = next(n for n in self.network.nodes if n['id'] == file_id)
                instability = coupling_info.get('instability', 0)
                
                # Add coupling info to title
                current_title = node.get('title', '')
                node['title'] = f"{current_title}<br/>🔗 Instability: {instability:.2f}"
    
    def _generate_enhanced_html(self, analysis_data: Dict[str, Any]) -> str:
        """Generate enhanced HTML with custom controls and statistics"""
        
        # Get basic HTML from pyvis
        basic_html = self.network.generate_html()
        
        # Calculate statistics
        stats = self._calculate_graph_statistics(analysis_data)
        
        # Inject custom controls and dashboard
        enhanced_html = basic_html.replace(
            '<body>',
            f'''<body>
            <div id="dashboard" style="position: fixed; top: 10px; left: 10px; background: rgba(0,0,0,0.8); color: white; padding: 15px; border-radius: 10px; font-family: Arial, sans-serif; z-index: 1000; max-width: 300px;">
                <h3>📊 Codebase Analytics</h3>
                <div style="font-size: 12px; line-height: 1.4;">
                    <b>Files:</b> {stats['files']}<br/>
                    <b>Classes:</b> {stats['classes']}<br/>
                    <b>Functions:</b> {stats['functions']}<br/>
                    <b>Dependencies:</b> {stats['dependencies']}<br/>
                    <b>Patterns:</b> {stats['patterns']}<br/>
                    <b>Clusters:</b> {stats['clusters']}<br/>
                    <b>Concerns:</b> {stats['concerns']}<br/>
                    <hr style="margin: 8px 0;">
                    <b>🎯 Legend:</b><br/>
                    <span style="color: #1f77b4;">📄 Files</span><br/>
                    <span style="color: #ff7f0e;">🔺 Classes</span><br/>
                    <span style="color: #2ca02c;">🔴 Functions</span><br/>
                    <span style="color: #9467bd;">📦 Modules</span><br/>
                    <span style="color: #7f7f7f;">⬡ Clusters</span><br/>
                    <span style="color: #e377c2;">⭐ Patterns</span><br/>
                    <span style="color: #bcbd22;">⚡ Concerns</span><br/>
                </div>
            </div>
            
            <div id="controls" style="position: fixed; top: 10px; right: 10px; background: rgba(0,0,0,0.8); color: white; padding: 15px; border-radius: 10px; z-index: 1000;">
                <h4>🎮 Controls</h4>
                <button onclick="network.fit()" style="margin: 2px; padding: 5px; background: #4CAF50; color: white; border: none; border-radius: 3px; cursor: pointer;">🔍 Fit View</button><br/>
                <button onclick="togglePhysics()" style="margin: 2px; padding: 5px; background: #2196F3; color: white; border: none; border-radius: 3px; cursor: pointer;">⚡ Toggle Physics</button><br/>
                <button onclick="exportGraph()" style="margin: 2px; padding: 5px; background: #FF9800; color: white; border: none; border-radius: 3px; cursor: pointer;">💾 Export</button><br/>
            </div>
            '''
        )
        
        # Add custom JavaScript
        enhanced_html = enhanced_html.replace(
            '</body>',
            '''
            <script>
            let physicsEnabled = true;
            
            function togglePhysics() {
                physicsEnabled = !physicsEnabled;
                network.setOptions({physics: {enabled: physicsEnabled}});
            }
            
            function exportGraph() {
                // Basic export functionality
                const dataString = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(network.body.data));
                const downloadAnchorNode = document.createElement('a');
                downloadAnchorNode.setAttribute("href", dataString);
                downloadAnchorNode.setAttribute("download", "codebase_graph_data.json");
                document.body.appendChild(downloadAnchorNode);
                downloadAnchorNode.click();
                downloadAnchorNode.remove();
            }
            
            // Enhanced tooltip functionality
            network.on("hoverNode", function(params) {
                const nodeId = params.node;
                const node = network.body.data.nodes.get(nodeId);
                console.log("Hovering over:", node);
            });
            
            // Clustering functionality
            network.on("doubleClick", function(params) {
                if (params.nodes.length > 0) {
                    const nodeId = params.nodes[0];
                    network.focus(nodeId, {scale: 1.5, animation: true});
                }
            });
            </script>
            </body>'''
        )
        
        return enhanced_html
    
    def _calculate_graph_statistics(self, analysis_data: Dict[str, Any]) -> Dict[str, int]:
        """Calculate statistics for the dashboard"""
        
        files = len(analysis_data.get('files', []))
        classes = sum(len(f.get('classes', [])) for f in analysis_data.get('files', []))
        functions = sum(len(f.get('functions', [])) for f in analysis_data.get('files', []))
        
        relationships = analysis_data.get('relationships', {})
        dependencies = len(relationships.get('dependency', []))
        
        patterns = len(analysis_data.get('patterns', {}).get('design_patterns', []) + 
                      analysis_data.get('patterns', {}).get('architectural_patterns', []))
        
        clusters = len(analysis_data.get('semantic_clusters', []))
        concerns = len(set(concern for concern_data in analysis_data.get('cross_cutting_concerns', []) 
                          for concern in concern_data.get('concerns', [])))
        
        return {
            'files': files,
            'classes': classes, 
            'functions': functions,
            'dependencies': dependencies,
            'patterns': patterns,
            'clusters': clusters,
            'concerns': concerns
        }
    
    # Helper methods
    def _get_node_id(self, identifier: str) -> str:
        """Get or create a unique node ID"""
        if identifier not in self.node_registry:
            self.node_registry[identifier] = f"node_{self.node_id_counter}"
            self.node_id_counter += 1
        return self.node_registry[identifier]
    
    def _find_file_node_id(self, file_path: str) -> str:
        """Find node ID for a file"""
        identifier = f"file:{file_path}"
        return self.node_registry.get(identifier)
    
    def _find_class_node_id(self, class_name: str) -> str:
        """Find node ID for a class (searches across files)"""
        for key, node_id in self.node_registry.items():
            if key.startswith(f"class:{class_name}:"):
                return node_id
        return None
    
    def _find_function_node_id(self, function_name: str) -> str:
        """Find node ID for a function (searches across files)"""
        for key, node_id in self.node_registry.items():
            if (key.startswith(f"function:{function_name}:") or 
                key.startswith(f"method:{function_name}:")):
                return node_id
        return None
    
    def _adjust_color_intensity(self, base_color: str, intensity: float) -> str:
        """Adjust color intensity based on a metric"""
        # Convert hex to RGB
        base_color = base_color.lstrip('#')
        rgb = tuple(int(base_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Adjust intensity (0.0 to 1.0)
        intensity = max(0.0, min(1.0, intensity))
        adjusted_rgb = tuple(int(c * (0.5 + intensity * 0.5)) for c in rgb)
        
        # Convert back to hex
        return f"#{adjusted_rgb[0]:02x}{adjusted_rgb[1]:02x}{adjusted_rgb[2]:02x}"


def main():
    """Generate enhanced knowledge graph from analysis data"""
    
    # Load the enhanced analysis
    with open("enhanced_ecological_analysis.json", "r") as f:
        analysis_data = json.load(f)
    
    # Generate the enhanced knowledge graph
    generator = EnhancedKnowledgeGraphGenerator()
    output_file = generator.generate_enhanced_graph(analysis_data)
    
    print(f"Enhanced multi-dimensional knowledge graph generated: {output_file}")
    print(f"Graph contains:")
    print(f"   * {len(analysis_data.get('files', []))} files")
    print(f"   * {sum(len(f.get('classes', [])) for f in analysis_data.get('files', []))} classes")
    print(f"   * {sum(len(f.get('functions', [])) for f in analysis_data.get('files', []))} functions")
    print(f"   * {len(analysis_data.get('relationships', {}).get('dependency', []))} dependencies")
    print(f"   * {len(analysis_data.get('semantic_clusters', []))} semantic clusters")
    print(f"   * {len(analysis_data.get('cross_cutting_concerns', []))} cross-cutting concerns")


if __name__ == "__main__":
    main()