"""
Enhanced Codebase Knowledge Graph Visualizer

This module provides specialized visualization for codebase analysis,
creating interactive knowledge graphs that show code structure,
dependencies, and relationships.
"""

import os
import json
from typing import Dict, List, Any, Set, Tuple
from pyvis.network import Network
import colorsys
import hashlib

class CodebaseVisualizer:
    """Creates interactive knowledge graphs specifically for codebase visualization"""
    
    def __init__(self):
        self.node_colors = {
            'file': '#00ffff',      # Cyan for files
            'class': '#ff00ff',     # Magenta for classes  
            'function': '#00ff00',  # Green for functions
            'method': '#ffff00',    # Yellow for methods
            'import': '#ff6600',    # Orange for imports
            'package': '#8000ff',   # Purple for packages
            'module': '#00ccff',    # Light blue for modules
            'variable': '#ff0080',  # Pink for variables
        }
        
        self.node_shapes = {
            'file': 'square',
            'class': 'triangle',
            'function': 'dot',
            'method': 'diamond',
            'import': 'star',
            'package': 'hexagon',
            'module': 'ellipse',
            'variable': 'box',
        }
        
        self.edge_colors = {
            'contains': '#00ffff',     # File contains class/function
            'inherits': '#ff00ff',     # Class inheritance
            'calls': '#00ff00',        # Function calls
            'imports': '#ff6600',      # Import relationships
            'uses': '#ffff00',         # Uses relationship
            'defines': '#8000ff',      # Defines relationship
            'depends_on': '#ff0080',   # Dependency relationship
        }
    
    def create_codebase_graph(self, analysis_data: Dict[str, Any], output_file: str = "codebase_graph.html") -> Network:
        """Create an interactive knowledge graph from codebase analysis data"""
        
        # Initialize neural visualization with enhanced settings
        net = Network(
            height="1200px", 
            width="100%", 
            directed=True,
            notebook=False, 
            bgcolor="#0a0a0a", 
            font_color="#00ffff",
            filter_menu=True, 
            select_menu=True,
            cdn_resources='remote'
        )
        
        # Track all nodes to avoid duplicates
        added_nodes: Set[str] = set()
        node_data: Dict[str, Dict] = {}
        
        # Process files and their contents
        files = analysis_data.get('files', [])
        
        for file_info in files:
            file_path = file_info.get('file', '')
            if not file_path:
                continue
                
            # Create file node
            file_node_id = f"file:{file_path}"
            if file_node_id not in added_nodes:
                self._add_node(net, file_node_id, {
                    'label': os.path.basename(file_path),
                    'type': 'file',
                    'full_path': file_path,
                    'file_type': file_info.get('type', 'unknown')
                })
                added_nodes.add(file_node_id)
                node_data[file_node_id] = file_info
            
            # Process classes in the file
            classes = file_info.get('classes', [])
            for class_info in classes:
                class_name = class_info.get('name', '')
                if not class_name:
                    continue
                    
                class_node_id = f"class:{file_path}:{class_name}"
                if class_node_id not in added_nodes:
                    self._add_node(net, class_node_id, {
                        'label': class_name,
                        'type': 'class',
                        'file': file_path,
                        'line': class_info.get('line', 0),
                        'methods': class_info.get('methods', []),
                        'bases': class_info.get('bases', [])
                    })
                    added_nodes.add(class_node_id)
                    node_data[class_node_id] = class_info
                    
                    # Add edge from file to class
                    net.add_edge(file_node_id, class_node_id, 
                               label="contains", 
                               color=self.edge_colors['contains'],
                               width=2)
                
                # Process methods in the class
                methods = class_info.get('methods', [])
                for method_name in methods:
                    method_node_id = f"method:{file_path}:{class_name}:{method_name}"
                    if method_node_id not in added_nodes:
                        self._add_node(net, method_node_id, {
                            'label': method_name,
                            'type': 'method',
                            'class': class_name,
                            'file': file_path
                        })
                        added_nodes.add(method_node_id)
                        
                        # Add edge from class to method
                        net.add_edge(class_node_id, method_node_id,
                                   label="contains",
                                   color=self.edge_colors['contains'],
                                   width=1)
                
                # Add inheritance relationships
                bases = class_info.get('bases', [])
                for base_class in bases:
                    base_node_id = f"class:external:{base_class}"
                    if base_node_id not in added_nodes:
                        self._add_node(net, base_node_id, {
                            'label': base_class,
                            'type': 'class',
                            'external': True
                        })
                        added_nodes.add(base_node_id)
                    
                    # Add inheritance edge
                    net.add_edge(class_node_id, base_node_id,
                               label="inherits",
                               color=self.edge_colors['inherits'],
                               width=3,
                               dashes=True)
            
            # Process functions in the file
            functions = file_info.get('functions', [])
            for func_info in functions:
                func_name = func_info.get('name', '')
                if not func_name:
                    continue
                    
                func_node_id = f"function:{file_path}:{func_name}"
                if func_node_id not in added_nodes:
                    self._add_node(net, func_node_id, {
                        'label': func_name,
                        'type': 'function',
                        'file': file_path,
                        'line': func_info.get('line', 0),
                        'args': func_info.get('args', [])
                    })
                    added_nodes.add(func_node_id)
                    node_data[func_node_id] = func_info
                    
                    # Add edge from file to function
                    net.add_edge(file_node_id, func_node_id,
                               label="contains",
                               color=self.edge_colors['contains'],
                               width=2)
            
            # Process imports
            imports = file_info.get('imports', [])
            for import_info in imports:
                module_name = import_info.get('module', '')
                if not module_name:
                    continue
                    
                # Create module/package nodes
                parts = module_name.split('.')
                parent_id = None
                
                for i, part in enumerate(parts):
                    if i == 0:
                        node_id = f"package:{part}"
                        node_type = 'package'
                    else:
                        node_id = f"module:{'.'.join(parts[:i+1])}"
                        node_type = 'module'
                    
                    if node_id not in added_nodes:
                        self._add_node(net, node_id, {
                            'label': part,
                            'type': node_type,
                            'full_name': '.'.join(parts[:i+1])
                        })
                        added_nodes.add(node_id)
                    
                    # Add hierarchy edges
                    if parent_id:
                        net.add_edge(parent_id, node_id,
                                   label="contains",
                                   color=self.edge_colors['contains'],
                                   width=1)
                    
                    parent_id = node_id
                
                # Add import edge from file to imported module
                if parent_id:
                    net.add_edge(file_node_id, parent_id,
                               label="imports",
                               color=self.edge_colors['imports'],
                               width=2,
                               dashes=True)
        
        # Add repository info if available
        if 'repo_url' in analysis_data:
            repo_node_id = "repo:main"
            self._add_node(net, repo_node_id, {
                'label': analysis_data.get('repo_url', 'Repository').split('/')[-1],
                'type': 'repository',
                'url': analysis_data['repo_url']
            })
            added_nodes.add(repo_node_id)
            
            # Connect repository to all files
            for file_info in files:
                file_path = file_info.get('file', '')
                file_node_id = f"file:{file_path}"
                if file_node_id in added_nodes:
                    net.add_edge(repo_node_id, file_node_id,
                               label="contains",
                               color=self.edge_colors['contains'],
                               width=1)
        
        # Configure physics and layout
        self._configure_network(net)
        
        # Save with enhanced styling
        self._save_enhanced_graph(net, output_file, analysis_data)
        
        return net
    
    def _add_node(self, net: Network, node_id: str, node_info: Dict[str, Any]):
        """Add a node to the network with appropriate styling"""
        node_type = node_info.get('type', 'default')
        label = node_info.get('label', node_id)
        
        # Generate color based on node type
        color = self.node_colors.get(node_type, '#00ccff')
        shape = self.node_shapes.get(node_type, 'dot')
        
        # Size based on importance/type
        size_map = {
            'file': 25,
            'class': 30,
            'function': 20,
            'method': 15,
            'import': 18,
            'package': 35,
            'module': 25,
            'repository': 40,
        }
        size = size_map.get(node_type, 20)
        
        # Create detailed title for hover
        title_parts = [f"🧠 {node_type.title()}: {label}"]
        
        if 'file' in node_info:
            title_parts.append(f"📁 File: {node_info['file']}")
        if 'line' in node_info and node_info['line']:
            title_parts.append(f"📍 Line: {node_info['line']}")
        if 'full_path' in node_info:
            title_parts.append(f"🗂️ Path: {node_info['full_path']}")
        if 'args' in node_info and node_info['args']:
            title_parts.append(f"⚙️ Args: {', '.join(node_info['args'])}")
        if 'methods' in node_info and node_info['methods']:
            title_parts.append(f"🔧 Methods: {', '.join(node_info['methods'][:5])}{'...' if len(node_info['methods']) > 5 else ''}")
        
        title = "\n".join(title_parts)
        
        try:
            net.add_node(
                node_id,
                label=label,
                title=title,
                group=node_type,
                color={
                    'background': color,
                    'border': '#ffffff',
                    'highlight': {'background': '#ffffff', 'border': color},
                    'hover': {'background': color, 'border': '#ffffff'}
                },
                shape=shape,
                size=size,
                borderWidth=2,
                borderWidthSelected=4,
                font={
                    'color': '#ffffff',
                    'size': 12,
                    'face': 'Orbitron, monospace',
                    'strokeWidth': 1,
                    'strokeColor': '#000000'
                },
                shadow={'enabled': True, 'color': color, 'size': 8, 'x': 0, 'y': 0}
            )
        except Exception as e:
            print(f"Error adding node {node_id}: {e}")
    
    def _configure_network(self, net: Network):
        """Configure network physics and interaction settings"""
        net.set_options("""
        {
            "physics": {
                "forceAtlas2Based": {
                    "gravitationalConstant": -200,
                    "centralGravity": 0.015,
                    "springLength": 300,
                    "springConstant": 0.08,
                    "damping": 0.4,
                    "avoidOverlap": 1
                },
                "maxVelocity": 50,
                "minVelocity": 0.1,
                "solver": "forceAtlas2Based",
                "timestep": 0.35,
                "adaptiveTimestep": true
            },
            "interaction": {
                "hover": true,
                "hoverConnectedEdges": true,
                "selectConnectedEdges": true,
                "tooltipDelay": 200,
                "zoomView": true,
                "dragView": true,
                "multiselect": true
            },
            "manipulation": {
                "enabled": false
            },
            "layout": {
                "improvedLayout": true,
                "hierarchical": {
                    "enabled": false
                },
                "randomSeed": 42
            },
            "groups": {
                "file": {"color": {"background": "#00ffff"}, "shape": "square"},
                "class": {"color": {"background": "#ff00ff"}, "shape": "triangle"},
                "function": {"color": {"background": "#00ff00"}, "shape": "dot"},
                "method": {"color": {"background": "#ffff00"}, "shape": "diamond"},
                "package": {"color": {"background": "#8000ff"}, "shape": "hexagon"},
                "module": {"color": {"background": "#00ccff"}, "shape": "ellipse"},
                "repository": {"color": {"background": "#ff0080"}, "shape": "star"}
            }
        }
        """)
    
    def _save_enhanced_graph(self, net: Network, output_file: str, analysis_data: Dict[str, Any]):
        """Save the graph with enhanced styling and metadata"""
        
        # Save the basic network
        net.save_graph(output_file)
        
        # Read and enhance the HTML
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Get metadata
            metrics = analysis_data.get('metrics', {})
            repo_name = analysis_data.get('repo_url', 'Unknown').split('/')[-1] if 'repo_url' in analysis_data else 'Local Codebase'
            
            # Enhanced CSS and JavaScript
            enhancements = f"""
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');
                
                body {{
                    background: #0a0a0a;
                    overflow: hidden;
                    font-family: 'Orbitron', monospace;
                    margin: 0;
                    padding: 0;
                }}
                
                /* Enhanced neural grid background */
                body::before {{
                    content: '';
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background-image: 
                        linear-gradient(rgba(0, 255, 255, 0.05) 1px, transparent 1px),
                        linear-gradient(90deg, rgba(0, 255, 255, 0.05) 1px, transparent 1px),
                        radial-gradient(circle at 25% 25%, rgba(0, 255, 255, 0.15) 0%, transparent 50%),
                        radial-gradient(circle at 75% 75%, rgba(255, 0, 255, 0.15) 0%, transparent 50%);
                    background-size: 30px 30px, 30px 30px, 100% 100%, 100% 100%;
                    animation: neural-grid-pulse 6s ease-in-out infinite alternate;
                    pointer-events: none;
                    z-index: -1;
                }}
                
                @keyframes neural-grid-pulse {{
                    0% {{ opacity: 0.3; transform: scale(1); }}
                    100% {{ opacity: 0.6; transform: scale(1.02); }}
                }}
                
                /* Enhanced network container */
                #mynetworkid {{
                    border: 2px solid #00ffff;
                    border-radius: 15px;
                    box-shadow: 
                        0 0 40px rgba(0, 255, 255, 0.6),
                        inset 0 0 40px rgba(0, 255, 255, 0.1);
                    background: radial-gradient(circle at center, rgba(0, 0, 0, 0.95) 0%, rgba(10, 10, 10, 0.98) 100%);
                    backdrop-filter: blur(5px);
                }}
                
                /* Info panel */
                .info-panel {{
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    background: rgba(0, 0, 0, 0.9);
                    border: 1px solid #00ffff;
                    border-radius: 10px;
                    padding: 15px;
                    z-index: 1000;
                    color: #00ffff;
                    font-family: 'Rajdhani', sans-serif;
                    backdrop-filter: blur(10px);
                    box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
                }}
                
                .info-panel h3 {{
                    margin: 0 0 10px 0;
                    color: #ffffff;
                    font-family: 'Orbitron', monospace;
                    font-size: 16px;
                }}
                
                .metric {{
                    margin: 5px 0;
                    font-size: 14px;
                }}
                
                .metric-value {{
                    color: #ffffff;
                    font-weight: bold;
                }}
                
                /* Enhanced tooltips */
                .vis-tooltip {{
                    background: rgba(0, 0, 0, 0.95) !important;
                    border: 1px solid #00ffff !important;
                    border-radius: 8px !important;
                    color: #00ffff !important;
                    font-family: 'Rajdhani', sans-serif !important;
                    font-size: 14px !important;
                    box-shadow: 0 0 25px rgba(0, 255, 255, 0.7) !important;
                    backdrop-filter: blur(10px) !important;
                }}
                
                /* Loading enhancement */
                .vis-loading-text {{
                    color: #00ffff !important;
                    font-family: 'Orbitron', monospace !important;
                    font-size: 18px !important;
                    text-shadow: 0 0 15px #00ffff !important;
                }}
                
                /* Control panels */
                .vis-configuration-wrapper {{
                    background: rgba(0, 0, 0, 0.95) !important;
                    border: 1px solid #00ffff !important;
                    border-radius: 10px !important;
                    backdrop-filter: blur(10px);
                }}
                
                .vis-configuration-wrapper .vis-configuration {{
                    color: #00ffff !important;
                    font-family: 'Rajdhani', sans-serif !important;
                }}
            </style>
            
            <div class="info-panel">
                <h3>📊 Codebase Metrics</h3>
                <div class="metric">Repository: <span class="metric-value">{repo_name}</span></div>
                <div class="metric">Files: <span class="metric-value">{metrics.get('total_files', 0)}</span></div>
                <div class="metric">Classes: <span class="metric-value">{metrics.get('total_classes', 0)}</span></div>
                <div class="metric">Functions: <span class="metric-value">{metrics.get('total_functions', 0)}</span></div>
                <div class="metric">Imports: <span class="metric-value">{metrics.get('total_imports', 0)}</span></div>
            </div>
            
            <script>
                document.addEventListener('DOMContentLoaded', function() {{
                    // Add title overlay
                    const titleDiv = document.createElement('div');
                    titleDiv.innerHTML = `
                        <div style="position: fixed; top: 20px; left: 50%; transform: translateX(-50%); z-index: 1000; text-align: center;">
                            <h1 style="color: #00ffff; font-family: 'Orbitron', monospace; font-size: 2.5rem; margin: 0; text-shadow: 0 0 25px #00ffff; animation: title-glow 3s ease-in-out infinite alternate;">
                                🧠 Codebase Architecture Map
                            </h1>
                            <p style="color: #00ffff; font-family: 'Rajdhani', sans-serif; opacity: 0.9; margin: 8px 0 0 0; font-size: 1.2rem;">
                                Interactive Code Structure Visualization
                            </p>
                        </div>
                    `;
                    document.body.appendChild(titleDiv);
                    
                    // Add enhanced animations
                    const style = document.createElement('style');
                    style.textContent = `
                        @keyframes title-glow {{
                            0% {{ text-shadow: 0 0 25px #00ffff, 0 0 35px #00ffff, 0 0 45px #00ffff; }}
                            100% {{ text-shadow: 0 0 35px #00ffff, 0 0 45px #00ffff, 0 0 55px #00ffff; }}
                        }}
                    `;
                    document.head.appendChild(style);
                    
                    // Enhanced canvas effects
                    const canvas = document.querySelector('canvas');
                    if (canvas) {{
                        canvas.style.filter = 'drop-shadow(0 0 15px rgba(0, 255, 255, 0.4))';
                    }}
                    
                    console.log('🧠 NeuroWeave Codebase Visualization loaded successfully');
                }});
            </script>
            """
            
            # Inject enhancements
            enhanced_html = html_content.replace('<head>', '<head>' + enhancements)
            
            # Write enhanced HTML
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(enhanced_html)
                
            print(f"Enhanced codebase visualization saved to {os.path.abspath(output_file)}")
            
        except Exception as e:
            print(f"Error enhancing visualization: {e}")