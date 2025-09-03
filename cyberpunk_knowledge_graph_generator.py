#!/usr/bin/env python3
"""
Cyberpunk Neural Network Knowledge Graph Generator

Creates immersive cyberpunk-themed interactive visualizations showing codebase
relationships as neural networks with futuristic aesthetics and advanced controls.

This replaces the standard generator with a cyberpunk-themed version that creates
stunning visualizations perfect for exploring AI codebase consciousness.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple
import hashlib
import math

class CyberpunkKnowledgeGraphGenerator:
    """Generates cyberpunk-themed neural network knowledge graphs"""
    
    def __init__(self):
        self.node_id_counter = 0
        self.node_registry = {}
        
        # Cyberpunk color schemes for different node types
        self.cyberpunk_colors = {
            'files': {
                'background': '#FF00FF',
                'border': '#FF1493',
                'highlight': '#FF69B4',
                'shadow': '#FF00FF'
            },
            'classes': {
                'background': '#39FF14',
                'border': '#00FF00',
                'highlight': '#7FFF00',
                'shadow': '#39FF14'
            },
            'functions': {
                'background': '#00FFFF',
                'border': '#0080FF',
                'highlight': '#87CEEB',
                'shadow': '#00FFFF'
            },
            'methods': {
                'background': '#FF1493',
                'border': '#FF69B4',
                'highlight': '#FFB6C1',
                'shadow': '#FF1493'
            },
            'modules': {
                'background': '#4B0082',
                'border': '#8A2BE2',
                'highlight': '#9966CC',
                'shadow': '#4B0082'
            },
            'patterns': {
                'background': '#FF4500',
                'border': '#FF6347',
                'highlight': '#FFA500',
                'shadow': '#FF4500'
            },
            'clusters': {
                'background': '#0080FF',
                'border': '#4169E1',
                'highlight': '#6495ED',
                'shadow': '#0080FF'
            },
            'concerns': {
                'background': '#FFD700',
                'border': '#FFA500',
                'highlight': '#FFFF00',
                'shadow': '#FFD700'
            }
        }
        
        self.cyberpunk_edges = {
            'contains': {'color': '#666666', 'highlight': '#FF00FF'},
            'inherits': {'color': '#FF1493', 'highlight': '#39FF14'},
            'calls': {'color': '#00FFFF', 'highlight': '#FF4500'},
            'imports': {'color': '#39FF14', 'highlight': '#FF1493'},
            'depends_on': {'color': '#ff8800', 'highlight': '#00FFFF'},
            'composes': {'color': '#8A2BE2', 'highlight': '#39FF14'},
            'flows_to': {'color': '#00FF88', 'highlight': '#FF00FF'},
            'clusters_with': {'color': '#FF0088', 'highlight': '#00FFFF'},
            'implements': {'color': '#88FF00', 'highlight': '#FF1493'},
            'associates': {'color': '#0088FF', 'highlight': '#FFD700'},
        }
    
    def generate_cyberpunk_graph(self, analysis_data: Dict[str, Any], output_file: str = "cyberpunk_neural_graph.html") -> str:
        """Generate cyberpunk neural network knowledge graph"""
        
        # Process analysis data into cyberpunk format
        nodes, edges = self._process_analysis_data(analysis_data)
        
        # Calculate statistics
        stats = self._calculate_neural_stats(analysis_data, nodes, edges)
        
        # Generate the cyberpunk HTML
        html_content = self._generate_cyberpunk_html(nodes, edges, stats)
        
        # Save the visualization
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_file
    
    def _process_analysis_data(self, analysis_data: Dict[str, Any]) -> Tuple[List[Dict], List[Dict]]:
        """Process analysis data into cyberpunk node and edge format"""
        
        nodes = []
        edges = []
        
        # Process files and their contents
        for file_data in analysis_data.get('files', []):
            file_path = file_data['file']
            
            # Add file node
            file_id = self._get_node_id(f"file:{file_path}")
            complexity_score = file_data.get('complexity', 0)
            lines = file_data.get('lines', 1)
            size_factor = min(max(lines / 100, 0.5), 3.0) * 20
            
            file_node = {
                'id': file_id,
                'label': Path(file_path).name,
                'group': 'files',
                'shape': 'box',
                'size': size_factor,
                'title': self._create_cyberpunk_tooltip('📄 File', {
                    'File': file_path,
                    'Lines': lines,
                    'Complexity': complexity_score
                }),
                'font': {'color': '#00FFFF', 'face': 'Orbitron, monospace', 'strokeWidth': 2, 'strokeColor': '#000000'},
                'color': self._get_cyberpunk_color('files'),
                'shadow': {'enabled': True, 'color': self.cyberpunk_colors['files']['shadow'], 'size': 10},
                'borderWidth': 3,
                'borderWidthSelected': 5
            }
            nodes.append(file_node)
            
            # Process classes
            for class_data in file_data.get('classes', []):
                class_id = self._get_node_id(f"class:{class_data['name']}:{file_path}")
                method_count = len(class_data.get('methods', []))
                
                class_node = {
                    'id': class_id,
                    'label': class_data['name'],
                    'group': 'classes',
                    'shape': 'triangle',
                    'size': 15 + method_count * 3,
                    'title': self._create_cyberpunk_tooltip('🧠 Neural Core', {
                        'Class': class_data['name'],
                        'File': Path(file_path).name,
                        'Methods': method_count,
                        'Line': class_data.get('line', 0)
                    }),
                    'font': {'color': '#00FFFF', 'face': 'Orbitron, monospace', 'strokeWidth': 2, 'strokeColor': '#000000'},
                    'color': self._get_cyberpunk_color('classes'),
                    'shadow': {'enabled': True, 'color': self.cyberpunk_colors['classes']['shadow'], 'size': 10},
                    'borderWidth': 3,
                    'borderWidthSelected': 5
                }
                nodes.append(class_node)
                
                # Connect class to file
                edges.append(self._create_cyberpunk_edge(file_id, class_id, 'contains', 'neural_link', 2))
                
                # Process methods
                for method_data in class_data.get('methods', []):
                    method_id = self._get_node_id(f"method:{method_data['name']}:{class_data['name']}:{file_path}")
                    method_complexity = method_data.get('complexity', 1)
                    
                    method_node = {
                        'id': method_id,
                        'label': method_data['name'],
                        'group': 'methods',
                        'shape': 'diamond',
                        'size': 8 + method_complexity * 3,
                        'title': self._create_cyberpunk_tooltip('🔧 Processor', {
                            'Method': method_data['name'],
                            'Class': class_data['name'],
                            'Complexity': method_complexity,
                            'Args': len(method_data.get('args', []))
                        }),
                        'font': {'color': '#00FFFF', 'face': 'Orbitron, monospace', 'strokeWidth': 2, 'strokeColor': '#000000'},
                        'color': self._get_cyberpunk_color('methods'),
                        'shadow': {'enabled': True, 'color': self.cyberpunk_colors['methods']['shadow'], 'size': 10},
                        'borderWidth': 3,
                        'borderWidthSelected': 5
                    }
                    nodes.append(method_node)
                    
                    # Connect method to class
                    edges.append(self._create_cyberpunk_edge(class_id, method_id, 'contains', 'neural_pathway', 1))
            
            # Process functions
            for func_data in file_data.get('functions', []):
                func_id = self._get_node_id(f"function:{func_data['name']}:{file_path}")
                func_complexity = func_data.get('complexity', 1)
                
                func_node = {
                    'id': func_id,
                    'label': func_data['name'],
                    'group': 'functions',
                    'shape': 'dot',
                    'size': 10 + func_complexity * 3,
                    'title': self._create_cyberpunk_tooltip('⚡ Synapse', {
                        'Function': func_data['name'],
                        'File': Path(file_path).name,
                        'Complexity': func_complexity,
                        'Args': len(func_data.get('args', []))
                    }),
                    'font': {'color': '#00FFFF', 'face': 'Orbitron, monospace', 'strokeWidth': 2, 'strokeColor': '#000000'},
                    'color': self._get_cyberpunk_color('functions'),
                    'shadow': {'enabled': True, 'color': self.cyberpunk_colors['functions']['shadow'], 'size': 10},
                    'borderWidth': 3,
                    'borderWidthSelected': 5
                }
                nodes.append(func_node)
                
                # Connect function to file
                edges.append(self._create_cyberpunk_edge(file_id, func_id, 'contains', 'neural_connection', 1))
        
        # Process relationships
        relationships = analysis_data.get('relationships', {})
        
        # Inheritance relationships
        for rel in relationships.get('inheritance', []):
            parent_id = self._find_class_node_id(rel['parent'])
            child_id = self._find_class_node_id(rel['child'])
            
            if parent_id and child_id:
                edges.append(self._create_cyberpunk_edge(child_id, parent_id, 'inherits', 
                    f"{rel['child']} inherits neural patterns from {rel['parent']}", 3))
        
        # Dependency relationships
        for rel in relationships.get('dependency', []):
            source_id = self._find_file_node_id(rel['source'])
            target_id = self._find_file_node_id(rel['target'])
            
            # Create module node if target doesn't exist
            if not target_id:
                target_id = self._get_node_id(f"module:{rel['target']}")
                if target_id not in [n['id'] for n in nodes]:
                    module_node = {
                        'id': target_id,
                        'label': rel['target'],
                        'group': 'modules',
                        'shape': 'ellipse',
                        'size': 12,
                        'title': self._create_cyberpunk_tooltip('📡 Module', {'Module': rel['target']}),
                        'font': {'color': '#00FFFF', 'face': 'Orbitron, monospace', 'strokeWidth': 2, 'strokeColor': '#000000'},
                        'color': self._get_cyberpunk_color('modules'),
                        'shadow': {'enabled': True, 'color': self.cyberpunk_colors['modules']['shadow'], 'size': 10},
                        'borderWidth': 3,
                        'borderWidthSelected': 5
                    }
                    nodes.append(module_node)
            
            if source_id and target_id:
                edges.append(self._create_cyberpunk_edge(source_id, target_id, 'depends_on', 
                    f"neural dependency on {rel['target']}", 1))
        
        # Call graph relationships
        for rel in relationships.get('call_graph', []):
            caller_id = self._find_function_node_id(rel['caller'])
            callee_id = self._find_function_node_id(rel['callee'])
            
            if caller_id and callee_id:
                edges.append(self._create_cyberpunk_edge(caller_id, callee_id, 'calls', 
                    f"{rel['caller']} transmits to {rel['callee']}", 1))
        
        # Add semantic clusters
        for cluster in analysis_data.get('semantic_clusters', []):
            cluster_id = self._get_node_id(f"cluster:{cluster['name']}")
            cohesion_score = cluster.get('cohesion_score', 0.5)
            files_count = len(cluster.get('files', []))
            
            cluster_node = {
                'id': cluster_id,
                'label': f"📦 {cluster['name']}",
                'group': 'clusters',
                'shape': 'hexagon',
                'size': 20 + files_count * 3,
                'title': self._create_cyberpunk_tooltip('🌐 Neural Cluster', {
                    'Cluster': cluster['name'],
                    'Type': cluster.get('type', 'unknown'),
                    'Files': files_count,
                    'Cohesion': f"{cohesion_score:.2f}"
                }),
                'font': {'color': '#00FFFF', 'face': 'Orbitron, monospace', 'strokeWidth': 2, 'strokeColor': '#000000'},
                'color': self._get_cyberpunk_color('clusters'),
                'shadow': {'enabled': True, 'color': self.cyberpunk_colors['clusters']['shadow'], 'size': 10},
                'borderWidth': 3,
                'borderWidthSelected': 5
            }
            nodes.append(cluster_node)
            
            # Connect cluster to files
            for file_path in cluster.get('files', []):
                file_id = self._find_file_node_id(file_path)
                if file_id:
                    edges.append(self._create_cyberpunk_edge(cluster_id, file_id, 'clusters_with', 
                        f"neural cluster with {Path(file_path).name}", 2))
        
        # Add architectural patterns
        patterns = analysis_data.get('patterns', {})
        all_patterns = (patterns.get('design_patterns', []) + 
                       patterns.get('architectural_patterns', []))
        
        for pattern in all_patterns:
            pattern_id = self._get_node_id(f"pattern:{pattern}")
            
            pattern_node = {
                'id': pattern_id,
                'label': f"🏗️ {pattern}",
                'group': 'patterns',
                'shape': 'star',
                'size': 25,
                'title': self._create_cyberpunk_tooltip('⭐ Neural Pattern', {
                    'Pattern': pattern,
                    'Type': 'Architectural/Design Pattern'
                }),
                'font': {'color': '#00FFFF', 'face': 'Orbitron, monospace', 'strokeWidth': 2, 'strokeColor': '#000000'},
                'color': self._get_cyberpunk_color('patterns'),
                'shadow': {'enabled': True, 'color': self.cyberpunk_colors['patterns']['shadow'], 'size': 10},
                'borderWidth': 3,
                'borderWidthSelected': 5
            }
            nodes.append(pattern_node)
        
        # Add cross-cutting concerns
        concern_files = {}
        for concern_data in analysis_data.get('cross_cutting_concerns', []):
            for concern in concern_data.get('concerns', []):
                if concern not in concern_files:
                    concern_files[concern] = []
                concern_files[concern].append(concern_data['file'])
        
        for concern, files in concern_files.items():
            concern_id = self._get_node_id(f"concern:{concern}")
            
            concern_node = {
                'id': concern_id,
                'label': f"⚡ {concern}",
                'group': 'concerns',
                'shape': 'triangle',
                'size': 15 + len(files) * 2,
                'title': self._create_cyberpunk_tooltip('🔗 Cross-Cutting Neural Bridge', {
                    'Concern': concern,
                    'Affects': f"{len(files)} neural nodes"
                }),
                'font': {'color': '#00FFFF', 'face': 'Orbitron, monospace', 'strokeWidth': 2, 'strokeColor': '#000000'},
                'color': self._get_cyberpunk_color('concerns'),
                'shadow': {'enabled': True, 'color': self.cyberpunk_colors['concerns']['shadow'], 'size': 10},
                'borderWidth': 3,
                'borderWidthSelected': 5
            }
            nodes.append(concern_node)
            
            # Connect to affected files
            for file_path in files:
                file_id = self._find_file_node_id(file_path)
                if file_id:
                    edges.append(self._create_cyberpunk_edge(concern_id, file_id, 'associates', 
                        f"neural bridge affects {Path(file_path).name}", 1))
        
        return nodes, edges
    
    def _create_cyberpunk_tooltip(self, type_label: str, data: Dict[str, Any]) -> str:
        """Create cyberpunk-styled tooltip"""
        tooltip_parts = [type_label]
        for key, value in data.items():
            tooltip_parts.append(f"{key}: {value}")
        return "<br/>".join(tooltip_parts)
    
    def _get_cyberpunk_color(self, group: str) -> Dict[str, str]:
        """Get cyberpunk color scheme for a group"""
        colors = self.cyberpunk_colors.get(group, self.cyberpunk_colors['functions'])
        return {
            'background': colors['background'],
            'border': colors['border'],
            'highlight': {
                'background': colors['highlight'],
                'border': colors['border']
            },
            'hover': {
                'background': colors['highlight'],
                'border': colors['border']
            }
        }
    
    def _create_cyberpunk_edge(self, from_id: str, to_id: str, edge_type: str, title: str, width: int) -> Dict[str, Any]:
        """Create cyberpunk-styled edge"""
        edge_colors = self.cyberpunk_edges.get(edge_type, self.cyberpunk_edges['contains'])
        
        return {
            'from': from_id,
            'to': to_id,
            'title': title,
            'width': width,
            'color': {
                'color': edge_colors['color'],
                'highlight': edge_colors['highlight']
            },
            'shadow': {
                'enabled': True,
                'color': edge_colors['color'],
                'size': 5
            },
            'smooth': {
                'type': 'continuous',
                'forceDirection': 'none'
            },
            'arrows': 'to' if edge_type in ['inherits', 'calls', 'depends_on', 'flows_to', 'implements'] else None
        }
    
    def _calculate_neural_stats(self, analysis_data: Dict[str, Any], nodes: List[Dict], edges: List[Dict]) -> Dict[str, Any]:
        """Calculate neural network statistics"""
        
        # Count node types
        node_counts = {}
        total_complexity = 0
        
        for node in nodes:
            group = node['group']
            node_counts[group] = node_counts.get(group, 0) + 1
            
            # Extract complexity from title if available
            if 'Complexity:' in node['title']:
                try:
                    complexity_part = node['title'].split('Complexity: ')[1].split('<br/>')[0]
                    total_complexity += int(complexity_part)
                except (IndexError, ValueError):
                    pass
        
        # Determine activity level
        activity_level = 'LOW'
        if total_complexity > 100:
            activity_level = 'MEDIUM'
        if total_complexity > 300:
            activity_level = 'HIGH'
        if total_complexity > 500:
            activity_level = 'CRITICAL'
        
        return {
            'node_counts': node_counts,
            'total_nodes': len(nodes),
            'total_edges': len(edges),
            'total_complexity': total_complexity,
            'activity_level': activity_level,
            'files': node_counts.get('files', 0),
            'classes': node_counts.get('classes', 0),
            'functions': node_counts.get('functions', 0),
            'methods': node_counts.get('methods', 0)
        }
    
    def _generate_cyberpunk_html(self, nodes: List[Dict], edges: List[Dict], stats: Dict[str, Any]) -> str:
        """Generate the complete cyberpunk HTML visualization"""
        
        # Convert nodes and edges to JavaScript format
        nodes_js = json.dumps(nodes, indent=2)
        edges_js = json.dumps(edges, indent=2)
        
        return f'''<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>🌃 Cyberpunk Neural Network Knowledge Graph</title>
        
        <!-- Vis.js Network Library -->
        <script src="lib/bindings/utils.js"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/dist/dist/vis-network.min.css" integrity="sha512-WgxfT5LWjfszlPHXRmBWHkV2eceiWTOBvrKCNbdgDYTHrT2AeLCGbF4sZlZw3UMN3WtL0tGUoIAKsu8mllg/XA==" crossorigin="anonymous" referrerpolicy="no-referrer" />
        <script src="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/dist/vis-network.min.js" integrity="sha512-LnvoEWDFrqGHlHmDD2101OrLcbsfkrzoSpvtSQtxK3RMnRV0eOkhhBN2dXHKRrUU8p2DGRTk35n4O8nWSVe1mQ==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
        
        <!-- Bootstrap for UI Components -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6" crossorigin="anonymous" />
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/js/bootstrap.bundle.min.js" integrity="sha384-JEW9xMcG8R+pH31jmWH6WWP0WintQrMb4s7ZOdauHnUtxwoG2vI5DkLtS3qm9Ekf" crossorigin="anonymous"></script>

        <!-- Custom Cyberpunk Fonts -->
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap" rel="stylesheet">

        <style type="text/css">
            /* === CYBERPUNK NEURAL NETWORK STYLING === */
            
            /* Global Variables for Cyberpunk Theme */
            :root {{
                --cyber-cyan: #00FFFF;
                --cyber-magenta: #FF00FF;
                --cyber-lime: #39FF14;
                --cyber-purple: #4B0082;
                --cyber-blue: #0080FF;
                --cyber-pink: #FF1493;
                --cyber-orange: #FF4500;
                --cyber-void: #000000;
                --cyber-dark-purple: #1a0d2e;
                --cyber-darker-purple: #0d0a1a;
                --cyber-grid: rgba(0, 255, 255, 0.2);
                --cyber-glow: 0 0 20px;
            }}

            /* Main Container and Background */
            body {{
                margin: 0;
                padding: 0;
                background: radial-gradient(ellipse at center, var(--cyber-dark-purple) 0%, var(--cyber-darker-purple) 50%, var(--cyber-void) 100%);
                font-family: 'Rajdhani', 'Courier New', monospace;
                color: var(--cyber-cyan);
                overflow: hidden;
            }}

            /* Cyberpunk Background Grid */
            body::before {{
                content: '';
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-image: 
                    linear-gradient(var(--cyber-grid) 1px, transparent 1px),
                    linear-gradient(90deg, var(--cyber-grid) 1px, transparent 1px);
                background-size: 50px 50px;
                animation: gridPulse 4s ease-in-out infinite;
                pointer-events: none;
                z-index: 0;
            }}

            @keyframes gridPulse {{
                0%, 100% {{ opacity: 0.3; }}
                50% {{ opacity: 0.6; }}
            }}

            /* Floating Digital Particles */
            .cyber-particles {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
                z-index: 1;
            }}

            .particle {{
                position: absolute;
                width: 2px;
                height: 2px;
                background: var(--cyber-cyan);
                border-radius: 50%;
                opacity: 0.6;
                animation: float 20s linear infinite;
                box-shadow: var(--cyber-glow) var(--cyber-cyan);
            }}

            @keyframes float {{
                0% {{
                    transform: translateY(100vh) translateX(0);
                    opacity: 0;
                }}
                10% {{ opacity: 1; }}
                90% {{ opacity: 1; }}
                100% {{
                    transform: translateY(-10vh) translateX(100px);
                    opacity: 0;
                }}
            }}

            /* Neural Network Container */
            #mynetwork {{
                width: 100%;
                height: 100vh;
                background: transparent;
                border: none;
                position: relative;
                z-index: 2;
            }}

            /* Cyberpunk Title Styling */
            .cyber-title {{
                position: absolute;
                top: 20px;
                left: 50%;
                transform: translateX(-50%);
                z-index: 10;
                font-family: 'Orbitron', monospace;
                font-size: 2.5em;
                font-weight: 900;
                color: var(--cyber-cyan);
                text-shadow: 
                    0 0 10px var(--cyber-cyan),
                    0 0 20px var(--cyber-cyan),
                    0 0 30px var(--cyber-cyan);
                animation: titleGlitch 3s ease-in-out infinite;
                text-align: center;
            }}

            @keyframes titleGlitch {{
                0%, 90%, 100% {{ transform: translateX(-50%) translateY(0); }}
                95% {{ transform: translateX(-50%) translateY(-2px); }}
                97% {{ transform: translateX(-48%) translateY(1px); }}
                99% {{ transform: translateX(-52%) translateY(-1px); }}
            }}

            /* Cyberpunk Loading Bar */
            #loadingBar {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 520px;
                height: 60px;
                background: rgba(0, 0, 0, 0.8);
                border: 2px solid var(--cyber-cyan);
                border-radius: 10px;
                box-shadow: 
                    0 0 20px var(--cyber-cyan),
                    inset 0 0 20px rgba(0, 255, 255, 0.1);
                z-index: 15;
            }}

            #bar {{
                position: absolute;
                top: 4px;
                left: 4px;
                height: 48px;
                min-width: 20px;
                background: linear-gradient(90deg, var(--cyber-cyan), var(--cyber-magenta), var(--cyber-lime));
                border-radius: 6px;
                animation: loadingPulse 1s ease-in-out infinite;
            }}

            @keyframes loadingPulse {{
                0%, 100% {{ opacity: 0.8; }}
                50% {{ opacity: 1; }}
            }}

            #text {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                color: var(--cyber-cyan);
                font-family: 'Orbitron', monospace;
                font-size: 18px;
                font-weight: bold;
                text-shadow: 0 0 10px var(--cyber-cyan);
            }}

            /* Cyberpunk Control Panels */
            .cyber-panel {{
                position: absolute;
                background: rgba(0, 0, 0, 0.8);
                border: 1px solid var(--cyber-cyan);
                border-radius: 8px;
                padding: 15px;
                backdrop-filter: blur(10px);
                box-shadow: 
                    0 0 15px var(--cyber-cyan),
                    inset 0 0 15px rgba(0, 255, 255, 0.1);
                z-index: 5;
                font-family: 'Rajdhani', monospace;
                color: var(--cyber-cyan);
            }}

            .cyber-panel::before {{
                content: '';
                position: absolute;
                top: -1px;
                left: -1px;
                right: -1px;
                bottom: -1px;
                background: linear-gradient(45deg, var(--cyber-cyan), var(--cyber-magenta), var(--cyber-lime), var(--cyber-cyan));
                border-radius: 8px;
                z-index: -1;
                animation: borderFlow 3s linear infinite;
            }}

            @keyframes borderFlow {{
                0% {{ background-position: 0% 50%; }}
                100% {{ background-position: 100% 50%; }}
            }}

            /* Custom Node Hover Effects */
            .vis-network .vis-nodes .vis-node {{
                transition: all 0.3s ease;
            }}

            .vis-network .vis-nodes .vis-node:hover {{
                transform: scale(1.1);
            }}

            /* Legend Items */
            .legend-item {{
                display: flex;
                align-items: center;
                margin: 8px 0;
                padding: 5px;
                border-radius: 4px;
                transition: all 0.3s ease;
            }}

            .legend-item:hover {{
                background: rgba(0, 255, 255, 0.1);
                box-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
            }}

            .legend-shape {{
                width: 20px;
                height: 20px;
                margin-right: 10px;
                border: 2px solid;
                display: flex;
                align-items: center;
                justify-content: center;
            }}

            .legend-files {{ 
                background: var(--cyber-magenta);
                border-color: var(--cyber-magenta);
                box-shadow: 0 0 10px var(--cyber-magenta);
            }}

            .legend-classes {{ 
                background: var(--cyber-lime);
                border-color: var(--cyber-lime);
                box-shadow: 0 0 10px var(--cyber-lime);
                clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
            }}

            .legend-functions {{ 
                background: var(--cyber-cyan);
                border-color: var(--cyber-cyan);
                box-shadow: 0 0 10px var(--cyber-cyan);
                border-radius: 50%;
            }}

            .legend-methods {{ 
                background: var(--cyber-pink);
                border-color: var(--cyber-pink);
                box-shadow: 0 0 10px var(--cyber-pink);
                transform: rotate(45deg);
            }}

            /* Cyberpunk Scrollbar */
            ::-webkit-scrollbar {{
                width: 8px;
            }}

            ::-webkit-scrollbar-track {{
                background: var(--cyber-void);
            }}

            ::-webkit-scrollbar-thumb {{
                background: var(--cyber-cyan);
                border-radius: 4px;
                box-shadow: 0 0 5px var(--cyber-cyan);
            }}

            ::-webkit-scrollbar-thumb:hover {{
                background: var(--cyber-magenta);
                box-shadow: 0 0 10px var(--cyber-magenta);
            }}

            /* Digital Scan Lines Effect */
            .scanlines {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
                z-index: 3;
                opacity: 0.1;
                background: linear-gradient(
                    transparent 0%,
                    rgba(0, 255, 255, 0.1) 50%,
                    transparent 51%,
                    transparent 100%
                );
                background-size: 100% 4px;
                animation: scanlineMove 0.1s linear infinite;
            }}

            @keyframes scanlineMove {{
                0% {{ background-position: 0 0; }}
                100% {{ background-position: 0 4px; }}
            }}

            @keyframes activityWave {{
                0%, 100% {{ opacity: 0.3; transform: scaleY(0.5); }}
                50% {{ opacity: 1; transform: scaleY(1); }}
            }}

            @keyframes pulseExpand {{
                0% {{
                    transform: translate(-50%, -50%) scale(0);
                    opacity: 1;
                }}
                100% {{
                    transform: translate(-50%, -50%) scale(5);
                    opacity: 0;
                }}
            }}
        </style>

        <center>
            <div class="cyber-title">🌃 NEURAL CODEBASE MATRIX 🌃</div>
        </center>
    </head>

    <body>
        <!-- Cyberpunk Background Particles -->
        <div class="cyber-particles" id="particleContainer"></div>
        
        <!-- Digital Scan Lines -->
        <div class="scanlines"></div>

        <!-- Main Network Container -->
        <div id="mynetwork" class="card-body"></div>

        <!-- Cyberpunk Control Panel -->
        <div class="cyber-panel control-panel" style="top: 80px; left: 20px; width: 280px;">
            <h5 style="margin-bottom: 15px; color: var(--cyber-lime); font-family: 'Orbitron', monospace;">
                🎛️ NEURAL CONTROLS 🎛️
            </h5>
            
            <!-- Search Interface -->
            <div style="margin-bottom: 15px;">
                <input type="text" id="nodeSearch" placeholder="SEARCH NEURAL NODES..." 
                       style="width: 100%; padding: 8px; background: rgba(0,0,0,0.8); border: 1px solid var(--cyber-cyan); 
                              border-radius: 4px; color: var(--cyber-cyan); font-family: 'Rajdhani', monospace; 
                              box-shadow: 0 0 10px rgba(0,255,255,0.3);">
            </div>

            <!-- Physics Controls -->
            <div style="margin-bottom: 15px;">
                <label style="color: var(--cyber-magenta); font-size: 12px; margin-bottom: 5px; display: block;">GRAVITY FIELD</label>
                <input type="range" id="gravitySlider" min="-15000" max="-2000" value="-8000" 
                       style="width: 100%; accent-color: var(--cyber-magenta);">
                <span id="gravityValue" style="color: var(--cyber-cyan); font-size: 11px;">-8000</span>
            </div>

            <!-- Node Filters -->
            <div style="margin-bottom: 15px;">
                <label style="color: var(--cyber-lime); font-size: 12px; margin-bottom: 8px; display: block;">NODE FILTERS</label>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 5px;">
                    <label style="display: flex; align-items: center; font-size: 11px; color: var(--cyber-cyan);">
                        <input type="checkbox" id="showFiles" checked style="margin-right: 5px; accent-color: var(--cyber-magenta);">
                        Files
                    </label>
                    <label style="display: flex; align-items: center; font-size: 11px; color: var(--cyber-cyan);">
                        <input type="checkbox" id="showClasses" checked style="margin-right: 5px; accent-color: var(--cyber-lime);">
                        Classes
                    </label>
                    <label style="display: flex; align-items: center; font-size: 11px; color: var(--cyber-cyan);">
                        <input type="checkbox" id="showFunctions" checked style="margin-right: 5px; accent-color: var(--cyber-cyan);">
                        Functions
                    </label>
                    <label style="display: flex; align-items: center; font-size: 11px; color: var(--cyber-cyan);">
                        <input type="checkbox" id="showMethods" checked style="margin-right: 5px; accent-color: var(--cyber-pink);">
                        Methods
                    </label>
                </div>
            </div>

            <!-- Animation Controls -->
            <div style="margin-bottom: 15px;">
                <button id="pulseBtn" style="width: 48%; padding: 8px 4px; margin-right: 4%; background: linear-gradient(45deg, var(--cyber-cyan), var(--cyber-blue)); 
                                           border: none; border-radius: 4px; color: black; font-family: 'Orbitron', monospace; 
                                           font-size: 10px; font-weight: bold; cursor: pointer; box-shadow: 0 0 15px var(--cyber-cyan);">
                    PULSE
                </button>
                <button id="resetBtn" style="width: 48%; padding: 8px 4px; background: linear-gradient(45deg, var(--cyber-magenta), var(--cyber-pink)); 
                                           border: none; border-radius: 4px; color: black; font-family: 'Orbitron', monospace; 
                                           font-size: 10px; font-weight: bold; cursor: pointer; box-shadow: 0 0 15px var(--cyber-magenta);">
                    RESET
                </button>
            </div>
        </div>

        <!-- Cyberpunk Legend Panel -->
        <div class="cyber-panel legend-panel" style="top: 80px; right: 20px; min-width: 250px;">
            <h5 style="margin-bottom: 15px; color: var(--cyber-lime); font-family: 'Orbitron', monospace;">
                ⚡ NODE TYPES ⚡
            </h5>
            <div class="legend-item">
                <div class="legend-shape legend-files"></div>
                <span>Files (Data Crystals)</span>
            </div>
            <div class="legend-item">
                <div class="legend-shape legend-classes"></div>
                <span>Classes (Neural Cores)</span>
            </div>
            <div class="legend-item">
                <div class="legend-shape legend-functions"></div>
                <span>Functions (Synapses)</span>
            </div>
            <div class="legend-item">
                <div class="legend-shape legend-methods"></div>
                <span>Methods (Processors)</span>
            </div>
        </div>

        <!-- Neural Activity Stats Panel -->
        <div class="cyber-panel stats-panel" style="bottom: 20px; left: 20px; min-width: 300px;">
            <h5 style="margin-bottom: 15px; color: var(--cyber-lime); font-family: 'Orbitron', monospace;">
                📊 NEURAL METRICS 📊
            </h5>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; font-size: 12px;">
                <div>
                    <span style="color: var(--cyber-magenta);">TOTAL NODES:</span>
                    <span id="nodeCount" style="color: var(--cyber-cyan); font-weight: bold;">{stats['total_nodes']}</span>
                </div>
                <div>
                    <span style="color: var(--cyber-lime);">CONNECTIONS:</span>
                    <span id="edgeCount" style="color: var(--cyber-cyan); font-weight: bold;">{stats['total_edges']}</span>
                </div>
                <div>
                    <span style="color: var(--cyber-pink);">COMPLEXITY:</span>
                    <span id="totalComplexity" style="color: var(--cyber-cyan); font-weight: bold;">{stats['total_complexity']}</span>
                </div>
                <div>
                    <span style="color: var(--cyber-orange);">ACTIVITY:</span>
                    <span id="networkActivity" style="color: var(--cyber-lime); font-weight: bold;">{stats['activity_level']}</span>
                </div>
            </div>
            
            <!-- Real-time Activity Graph -->
            <div style="margin-top: 15px; height: 40px; background: rgba(0,0,0,0.5); border: 1px solid var(--cyber-cyan); 
                        border-radius: 4px; position: relative; overflow: hidden;">
                <div style="position: absolute; bottom: 0; left: 0; width: 100%; height: 100%; 
                           background: linear-gradient(to top, transparent 60%, var(--cyber-cyan) 80%, transparent 100%); 
                           animation: activityWave 2s ease-in-out infinite;"></div>
                <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); 
                           color: var(--cyber-cyan); font-size: 10px; font-family: 'Orbitron', monospace; font-weight: bold;">
                    NEURAL ACTIVITY
                </div>
            </div>
        </div>

        <!-- Loading Bar -->
        <div id="loadingBar">
            <div class="outerBorder">
                <div id="text">INITIALIZING NEURAL MATRIX...</div>
                <div id="bar"></div>
            </div>
        </div>

        <script type="text/javascript">
            // === CYBERPUNK PARTICLE SYSTEM ===
            function createParticleSystem() {{
                const particleContainer = document.getElementById('particleContainer');
                
                function createParticle() {{
                    const particle = document.createElement('div');
                    particle.className = 'particle';
                    
                    // Random starting position
                    particle.style.left = Math.random() * 100 + 'vw';
                    particle.style.animationDuration = (Math.random() * 15 + 10) + 's';
                    particle.style.animationDelay = Math.random() * 5 + 's';
                    
                    // Random color variation
                    const colors = ['#00FFFF', '#FF00FF', '#39FF14', '#0080FF', '#FF1493'];
                    const color = colors[Math.floor(Math.random() * colors.length)];
                    particle.style.backgroundColor = color;
                    particle.style.boxShadow = `0 0 10px ${{color}}`;
                    
                    particleContainer.appendChild(particle);
                    
                    // Remove particle after animation
                    setTimeout(() => {{
                        if (particle.parentNode) {{
                            particle.parentNode.removeChild(particle);
                        }}
                    }}, 25000);
                }}
                
                // Create particles continuously
                setInterval(createParticle, 500);
                
                // Initial burst of particles
                for (let i = 0; i < 20; i++) {{
                    setTimeout(createParticle, i * 100);
                }}
            }}

            // === NEURAL NETWORK SETUP ===
            var edges, nodes, network;
            var options, data;
            var filter = {{
                item: '',
                property: '',
                value: []
            }};

            // Enhanced cyberpunk network drawing function
            function drawGraph() {{
                var container = document.getElementById('mynetwork');

                // Parse nodes with cyberpunk enhancements
                nodes = new vis.DataSet({nodes_js});

                // Enhanced edges with cyberpunk styling
                edges = new vis.DataSet({edges_js});

                // Cyberpunk network options
                var options = {{
                    physics: {{
                        enabled: true,
                        stabilization: {{ iterations: 100 }},
                        barnesHut: {{
                            gravitationalConstant: -8000,
                            centralGravity: 0.3,
                            springLength: 120,
                            springConstant: 0.04,
                            damping: 0.09,
                            avoidOverlap: 0.5
                        }}
                    }},
                    interaction: {{
                        hover: true,
                        tooltipDelay: 200,
                        hideEdgesOnDrag: false,
                        hideNodesOnDrag: false
                    }},
                    nodes: {{
                        borderWidth: 3,
                        borderWidthSelected: 5,
                        font: {{
                            size: 14,
                            color: '#00FFFF',
                            face: 'Orbitron, monospace',
                            strokeWidth: 2,
                            strokeColor: '#000000'
                        }},
                        shadow: {{
                            enabled: true,
                            color: '#00FFFF',
                            size: 10,
                            x: 0,
                            y: 0
                        }}
                    }},
                    edges: {{
                        width: 2,
                        shadow: {{
                            enabled: true,
                            color: '#00FFFF',
                            size: 5,
                            x: 0,
                            y: 0
                        }},
                        smooth: {{
                            type: 'continuous',
                            forceDirection: 'none'
                        }}
                    }}
                }};

                data = {{ nodes: nodes, edges: edges }};
                network = new vis.Network(container, data, options);

                // Cyberpunk loading progress
                network.on("stabilizationProgress", function(params) {{
                    document.getElementById('loadingBar').removeAttribute("style");
                    var maxWidth = 496;
                    var minWidth = 20;
                    var widthFactor = params.iterations/params.total;
                    var width = Math.max(minWidth, maxWidth * widthFactor);
                    document.getElementById('bar').style.width = width + 'px';
                    document.getElementById('text').innerHTML = Math.round(widthFactor*100) + '% NEURAL SYNC...';
                }});

                network.once("stabilizationIterationsDone", function() {{
                    document.getElementById('text').innerHTML = '100% MATRIX ONLINE';
                    document.getElementById('bar').style.width = '496px';
                    document.getElementById('loadingBar').style.opacity = 0;
                    setTimeout(function() {{
                        document.getElementById('loadingBar').style.display = 'none';
                    }}, 2000);
                }});

                // Enhanced cyberpunk interactions
                network.on("hoverNode", function(params) {{
                    // Add glow effect on hover
                    const nodeElement = container.querySelector(`[data-id="${{params.node}}"]`);
                    if (nodeElement) {{
                        nodeElement.style.filter = 'brightness(1.5) saturate(1.5)';
                    }}
                }});

                network.on("blurNode", function(params) {{
                    // Remove glow effect
                    const nodeElement = container.querySelector(`[data-id="${{params.node}}"]`);
                    if (nodeElement) {{
                        nodeElement.style.filter = '';
                    }}
                }});

                return network;
            }}

            // === CYBERPUNK CONTROL SYSTEM ===
            function setupCyberpunkControls() {{
                // Gravity slider control
                const gravitySlider = document.getElementById('gravitySlider');
                const gravityValue = document.getElementById('gravityValue');
                
                gravitySlider.addEventListener('input', function() {{
                    gravityValue.textContent = this.value;
                    if (network) {{
                        network.setOptions({{
                            physics: {{
                                barnesHut: {{
                                    gravitationalConstant: parseInt(this.value)
                                }}
                            }}
                        }});
                    }}
                }});

                // Node search functionality
                const searchInput = document.getElementById('nodeSearch');
                searchInput.addEventListener('input', function() {{
                    const searchTerm = this.value.toLowerCase();
                    if (searchTerm === '') {{
                        // Reset all nodes to visible
                        nodes.forEach(function(node) {{
                            nodes.update({{id: node.id, hidden: false}});
                        }});
                        return;
                    }}

                    // Filter nodes based on search
                    nodes.forEach(function(node) {{
                        const isMatch = node.label.toLowerCase().includes(searchTerm) ||
                                       (node.title && node.title.toLowerCase().includes(searchTerm));
                        nodes.update({{id: node.id, hidden: !isMatch}});
                    }});
                }});

                // Node type filters
                const filters = {{
                    showFiles: document.getElementById('showFiles'),
                    showClasses: document.getElementById('showClasses'),
                    showFunctions: document.getElementById('showFunctions'),
                    showMethods: document.getElementById('showMethods')
                }};

                Object.keys(filters).forEach(filterId => {{
                    filters[filterId].addEventListener('change', function() {{
                        updateNodeVisibility();
                    }});
                }});

                function updateNodeVisibility() {{
                    const showTypes = {{
                        files: filters.showFiles.checked,
                        classes: filters.showClasses.checked,
                        functions: filters.showFunctions.checked,
                        methods: filters.showMethods.checked
                    }};

                    nodes.forEach(function(node) {{
                        const shouldShow = showTypes[node.group] || false;
                        nodes.update({{id: node.id, hidden: !shouldShow}});
                    }});
                }}

                // Animation controls
                document.getElementById('pulseBtn').addEventListener('click', function() {{
                    triggerNetworkPulse();
                }});

                document.getElementById('resetBtn').addEventListener('click', function() {{
                    if (network) {{
                        network.fit();
                        network.stabilize();
                    }}
                }});
            }}

            function triggerNetworkPulse() {{
                if (!network) return;
                
                const nodeIds = nodes.getIds();
                let pulseIndex = 0;
                
                function pulseNext() {{
                    if (pulseIndex >= nodeIds.length) return;
                    
                    const nodeId = nodeIds[pulseIndex];
                    const originalNode = nodes.get(nodeId);
                    
                    // Temporarily increase size and add glow
                    nodes.update({{
                        id: nodeId,
                        size: originalNode.size * 1.5,
                        borderWidth: 6
                    }});
                    
                    // Reset after animation
                    setTimeout(() => {{
                        nodes.update({{
                            id: nodeId,
                            size: originalNode.size,
                            borderWidth: originalNode.borderWidth || 3
                        }});
                    }}, 300);
                    
                    pulseIndex++;
                    setTimeout(pulseNext, 100);
                }}
                
                pulseNext();
            }}

            // Enhanced particle system with neural pulses
            function createEnhancedParticleSystem() {{
                createParticleSystem();
                
                // Add periodic neural pulse effect
                setInterval(() => {{
                    if (network && Math.random() > 0.7) {{
                        const nodeIds = nodes.getIds();
                        const randomNode = nodeIds[Math.floor(Math.random() * nodeIds.length)];
                        
                        // Create pulse effect around random node
                        const nodePosition = network.getPositions([randomNode])[randomNode];
                        if (nodePosition) {{
                            createPulseEffect(nodePosition.x, nodePosition.y);
                        }}
                    }}
                }}, 3000);
            }}

            function createPulseEffect(x, y) {{
                const networkDiv = document.getElementById('mynetwork');
                const pulse = document.createElement('div');
                pulse.style.position = 'absolute';
                pulse.style.left = x + 'px';
                pulse.style.top = y + 'px';
                pulse.style.width = '10px';
                pulse.style.height = '10px';
                pulse.style.borderRadius = '50%';
                pulse.style.border = '2px solid var(--cyber-cyan)';
                pulse.style.pointerEvents = 'none';
                pulse.style.animation = 'pulseExpand 1.5s ease-out forwards';
                
                networkDiv.appendChild(pulse);
                
                setTimeout(() => {{
                    if (pulse.parentNode) {{
                        pulse.parentNode.removeChild(pulse);
                    }}
                }}, 1500);
            }}

            // Initialize the cyberpunk neural network
            document.addEventListener('DOMContentLoaded', function() {{
                createEnhancedParticleSystem();
                drawGraph();
                setupCyberpunkControls();
            }});
        </script>
    </body>
</html>'''
    
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


def main():
    """Generate cyberpunk neural network knowledge graph from analysis data"""
    
    # Load the enhanced analysis - try sample data first for testing
    input_file = "sample_analysis_data.json" if os.path.exists("sample_analysis_data.json") else "enhanced_ecological_analysis.json"
    if not os.path.exists(input_file):
        print(f"Analysis file '{input_file}' not found!")
        print("Please run the MCP analysis first to generate the data, or provide sample_analysis_data.json for testing.")
        return
    
    with open(input_file, "r") as f:
        analysis_data = json.load(f)
    
    # Generate the cyberpunk neural network graph
    generator = CyberpunkKnowledgeGraphGenerator()
    output_file = generator.generate_cyberpunk_graph(analysis_data)
    
    print(f"Cyberpunk Neural Network Knowledge Graph generated: {output_file}")
    print(f"Neural Matrix contains:")
    print(f"   * {len(analysis_data.get('files', []))} data crystals (files)")
    print(f"   * {sum(len(f.get('classes', [])) for f in analysis_data.get('files', []))} neural cores (classes)")
    print(f"   * {sum(len(f.get('functions', [])) for f in analysis_data.get('files', []))} synapses (functions)")
    print(f"   * {len(analysis_data.get('relationships', {}).get('dependency', []))} neural pathways (dependencies)")
    print(f"   * {len(analysis_data.get('semantic_clusters', []))} neural clusters")
    print(f"   * {len(analysis_data.get('cross_cutting_concerns', []))} cross-cutting neural bridges")
    print(f"Ready to explore the digital consciousness of your codebase!")


if __name__ == "__main__":
    main()