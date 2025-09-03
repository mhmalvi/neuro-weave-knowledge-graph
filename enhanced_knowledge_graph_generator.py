#!/usr/bin/env python3
"""
Enhanced Professional Cyberpunk Neural Network Knowledge Graph Generator

Creates industry-standard cyberpunk-themed interactive visualizations with:
- Hierarchical information architecture
- Semantic color coding and shape language
- Professional UI controls and analytics
- Progressive information disclosure
- Enterprise-level performance and accessibility

This addresses all critical issues identified in the analysis while maintaining
the immersive cyberpunk aesthetic for exploring AI codebase consciousness.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple
import hashlib
import math
import networkx as nx
from collections import defaultdict

class ProfessionalCyberpunkGraphGenerator:
    """Professional-grade cyberpunk neural network knowledge graph generator"""
    
    def __init__(self):
        self.node_id_counter = 0
        self.node_registry = {}
        self.hierarchy_levels = {}
        self.semantic_clusters = defaultdict(list)
        
        # Professional cyberpunk color palette with semantic meaning
        self.semantic_colors = {
            'core_functionality': {
                'primary': '#00D4FF',    # Electric Blue
                'secondary': '#0099CC',
                'highlight': '#33DDFF',
                'glow': '#00D4FF'
            },
            'helper_functions': {
                'primary': '#00FF88',    # Neon Green
                'secondary': '#00CC66',
                'highlight': '#33FFAA',
                'glow': '#00FF88'
            },
            'critical_paths': {
                'primary': '#FF0080',    # Hot Pink
                'secondary': '#CC0066',
                'highlight': '#FF33AA',
                'glow': '#FF0080'
            },
            'dependencies': {
                'primary': '#FFB000',    # Amber
                'secondary': '#CC8800',
                'highlight': '#FFCC33',
                'glow': '#FFB000'
            },
            'neutral_elements': {
                'primary': '#404040',    # Cool Gray
                'secondary': '#606060',
                'highlight': '#808080',
                'glow': '#404040'
            },
            'interfaces': {
                'primary': '#8A2BE2',    # Blue Violet
                'secondary': '#6A1BAA',
                'highlight': '#AA55FF',
                'glow': '#8A2BE2'
            }
        }
        
        # Semantic edge types with professional styling
        self.semantic_edges = {
            'core_connection': {'color': '#00D4FF', 'width': 3, 'style': 'solid'},
            'helper_link': {'color': '#00FF88', 'width': 2, 'style': 'solid'},
            'critical_flow': {'color': '#FF0080', 'width': 4, 'style': 'solid'},
            'dependency': {'color': '#FFB000', 'width': 2, 'style': 'dashed'},
            'interface_impl': {'color': '#8A2BE2', 'width': 2, 'style': 'dotted'},
            'data_flow': {'color': '#00FFFF', 'width': 1, 'style': 'solid'}
        }
    
    def generate_professional_graph(self, analysis_data: Dict[str, Any], output_file: str = "professional_cyberpunk_graph.html") -> str:
        """Generate professional cyberpunk neural network knowledge graph"""
        
        # Phase 1: Hierarchical node organization
        nodes, edges = self._create_hierarchical_structure(analysis_data)
        
        # Phase 2: Semantic clustering and spatial layout
        self._apply_semantic_clustering(nodes, edges, analysis_data)
        
        # Phase 3: Smart analytics integration
        analytics_data = self._generate_smart_analytics(analysis_data, nodes, edges)
        
        # Phase 4: Generate enhanced HTML with professional features
        html_content = self._generate_professional_html(nodes, edges, analytics_data)
        
        # Save the visualization
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_file
    
    def _create_hierarchical_structure(self, analysis_data: Dict[str, Any]) -> Tuple[List[Dict], List[Dict]]:
        """Create hierarchical node structure: Root -> Module -> Component -> Element"""
        
        nodes = []
        edges = []
        
        # Level 1: Repository/Project Root
        repo_id = self._get_node_id("repository:root")
        repo_node = {
            'id': repo_id,
            'label': 'CODEBASE CORE',
            'group': 'repository',
            'level': 0,
            'hierarchyLevel': 'root',
            'shape': 'star',
            'size': 50,
            'color': self._get_semantic_color('core_functionality'),
            'font': self._get_professional_font(18, '#00D4FF'),
            'title': self._create_professional_tooltip('🌟 Neural Nexus', {
                'Type': 'Repository Core',
                'Files': len(analysis_data.get('files', [])),
                'Total Complexity': self._calculate_total_complexity(analysis_data),
                'Architecture': 'Multi-layer Neural Network'
            }),
            'physics': {'x': 0, 'y': 0},
            'fixed': True
        }
        nodes.append(repo_node)
        self.hierarchy_levels[0] = [repo_id]
        
        # Level 2: Module/Package clusters
        module_clusters = self._identify_module_clusters(analysis_data)
        level_2_nodes = []
        
        angle_step = (2 * math.pi) / max(len(module_clusters), 1)
        radius = 200
        
        for i, (module_name, module_files) in enumerate(module_clusters.items()):
            module_id = self._get_node_id(f"module:{module_name}")
            angle = i * angle_step
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            
            module_node = {
                'id': module_id,
                'label': f"📦 {module_name.upper()}",
                'group': 'module',
                'level': 1,
                'hierarchyLevel': 'module',
                'shape': 'hexagon',
                'size': 30 + len(module_files) * 2,
                'color': self._get_semantic_color('helper_functions'),
                'font': self._get_professional_font(14, '#00FF88'),
                'title': self._create_professional_tooltip('📦 Neural Module', {
                    'Module': module_name,
                    'Files': len(module_files),
                    'Complexity': self._calculate_module_complexity(module_files),
                    'Type': self._classify_module_type(module_name)
                }),
                'physics': {'x': x, 'y': y}
            }
            nodes.append(module_node)
            level_2_nodes.append(module_id)
            
            # Connect to repository core
            edges.append(self._create_semantic_edge(repo_id, module_id, 'core_connection', 
                f"Core neural pathway to {module_name}"))
        
        self.hierarchy_levels[1] = level_2_nodes
        
        # Level 3: Component level (Files and Classes)
        level_3_nodes = []
        for file_data in analysis_data.get('files', []):
            file_path = file_data['file']
            module_name = self._determine_module_for_file(file_path, module_clusters)
            module_id = self._get_node_id(f"module:{module_name}")
            
            # File node
            file_id = self._get_node_id(f"file:{file_path}")
            file_complexity = file_data.get('complexity', 1)
            file_importance = self._calculate_file_importance(file_data)
            
            file_node = {
                'id': file_id,
                'label': Path(file_path).stem,
                'group': 'file',
                'level': 2,
                'hierarchyLevel': 'component',
                'shape': 'box',
                'size': 15 + file_importance * 3,
                'color': self._get_color_by_importance(file_importance),
                'font': self._get_professional_font(12, '#00D4FF'),
                'title': self._create_professional_tooltip('📄 Data Crystal', {
                    'File': Path(file_path).name,
                    'Lines': file_data.get('lines', 0),
                    'Complexity': file_complexity,
                    'Importance': f"{file_importance:.2f}",
                    'Classes': len(file_data.get('classes', [])),
                    'Functions': len(file_data.get('functions', []))
                }),
                'borderWidth': 2 + file_importance,
                'borderWidthSelected': 4 + file_importance
            }
            nodes.append(file_node)
            level_3_nodes.append(file_id)
            
            # Connect to module
            edges.append(self._create_semantic_edge(module_id, file_id, 'helper_link', 
                f"Module contains {Path(file_path).name}"))
            
            # Add class nodes
            for class_data in file_data.get('classes', []):
                class_id = self._get_node_id(f"class:{class_data['name']}:{file_path}")
                class_complexity = class_data.get('complexity', 1)
                method_count = len(class_data.get('methods', []))
                
                class_node = {
                    'id': class_id,
                    'label': class_data['name'],
                    'group': 'class',
                    'level': 3,
                    'hierarchyLevel': 'element',
                    'shape': 'diamond',
                    'size': 12 + method_count * 2,
                    'color': self._get_semantic_color('critical_paths'),
                    'font': self._get_professional_font(11, '#FF0080'),
                    'title': self._create_professional_tooltip('💎 Neural Core', {
                        'Class': class_data['name'],
                        'Methods': method_count,
                        'Complexity': class_complexity,
                        'File': Path(file_path).name,
                        'Type': self._classify_class_type(class_data)
                    })
                }
                nodes.append(class_node)
                
                # Connect to file
                edges.append(self._create_semantic_edge(file_id, class_id, 'critical_flow', 
                    f"File defines class {class_data['name']}"))
        
        self.hierarchy_levels[2] = level_3_nodes
        
        return nodes, edges
    
    def _apply_semantic_clustering(self, nodes: List[Dict], edges: List[Dict], analysis_data: Dict[str, Any]):
        """Apply semantic clustering with intelligent spatial positioning"""
        
        # Create semantic clusters based on functionality
        semantic_clusters = analysis_data.get('semantic_clusters', [])
        
        for cluster in semantic_clusters:
            cluster_type = cluster.get('type', 'functional')
            cluster_files = cluster.get('files', [])
            
            if len(cluster_files) > 1:
                # Create cluster halo effect
                cluster_center = self._calculate_cluster_center(cluster_files, nodes)
                cluster_radius = self._calculate_cluster_radius(len(cluster_files))
                
                # Add visual cluster indicator
                cluster_id = self._get_node_id(f"cluster:{cluster['name']}")
                cluster_node = {
                    'id': cluster_id,
                    'label': f"🌐 {cluster['name'].upper()}",
                    'group': 'cluster',
                    'level': 1,
                    'hierarchyLevel': 'cluster',
                    'shape': 'ellipse',
                    'size': cluster_radius,
                    'color': {
                        'background': 'rgba(138, 43, 226, 0.1)',
                        'border': '#8A2BE2',
                        'highlight': {'background': 'rgba(138, 43, 226, 0.2)', 'border': '#AA55FF'}
                    },
                    'font': self._get_professional_font(10, '#8A2BE2'),
                    'title': self._create_professional_tooltip('🌐 Semantic Cluster', {
                        'Cluster': cluster['name'],
                        'Type': cluster_type,
                        'Files': len(cluster_files),
                        'Cohesion': f"{cluster.get('cohesion_score', 0):.2f}"
                    }),
                    'physics': cluster_center,
                    'opacity': 0.7
                }
                nodes.append(cluster_node)
    
    def _generate_smart_analytics(self, analysis_data: Dict[str, Any], nodes: List[Dict], edges: List[Dict]) -> Dict[str, Any]:
        """Generate comprehensive smart analytics"""
        
        # Calculate complexity distribution
        complexity_dist = self._analyze_complexity_distribution(analysis_data)
        
        # Identify architectural patterns
        patterns = self._identify_architectural_patterns(analysis_data)
        
        # Calculate network metrics
        network_metrics = self._calculate_network_metrics(nodes, edges)
        
        # Identify hotspots and critical paths
        hotspots = self._identify_performance_hotspots(analysis_data)
        
        # Security and quality indicators
        quality_indicators = self._analyze_code_quality(analysis_data)
        
        return {
            'complexity_distribution': complexity_dist,
            'architectural_patterns': patterns,
            'network_metrics': network_metrics,
            'performance_hotspots': hotspots,
            'quality_indicators': quality_indicators,
            'total_nodes': len(nodes),
            'total_edges': len(edges),
            'hierarchy_depth': max(node.get('level', 0) for node in nodes),
            'cluster_count': len([n for n in nodes if n.get('group') == 'cluster'])
        }
    
    def _generate_professional_html(self, nodes: List[Dict], edges: List[Dict], analytics: Dict[str, Any]) -> str:
        """Generate professional-grade HTML with enterprise features"""
        
        nodes_js = json.dumps(nodes, indent=2)
        edges_js = json.dumps(edges, indent=2)
        analytics_js = json.dumps(analytics, indent=2)
        
        return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌃 Professional Cyberpunk Neural Code Matrix</title>
    
    <!-- Performance optimized libraries -->
    <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&family=Inter:wght@300;400;500;600&family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
    
    <style>
        /* Professional Cyberpunk Theme Variables */
        :root {{
            --cyber-primary: #00D4FF;
            --cyber-secondary: #00FF88;
            --cyber-critical: #FF0080;
            --cyber-warning: #FFB000;
            --cyber-neutral: #404040;
            --cyber-interface: #8A2BE2;
            --cyber-void: #0A0A0F;
            --cyber-grid: #1A1A2E;
            --cyber-glow: 0 0 15px;
            --glass-bg: rgba(0, 0, 0, 0.8);
            --glass-border: rgba(0, 212, 255, 0.3);
        }}

        /* Global Styles */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Inter', sans-serif;
            background: radial-gradient(ellipse at center, 
                var(--cyber-grid) 0%, 
                #0d0a1a 50%, 
                var(--cyber-void) 100%);
            color: var(--cyber-primary);
            overflow: hidden;
            height: 100vh;
        }}

        /* Neural Grid Background */
        body::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                linear-gradient(rgba(0, 212, 255, 0.1) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 212, 255, 0.1) 1px, transparent 1px);
            background-size: 40px 40px;
            animation: gridPulse 6s ease-in-out infinite;
            pointer-events: none;
            z-index: 0;
        }}

        @keyframes gridPulse {{
            0%, 100% {{ opacity: 0.2; }}
            50% {{ opacity: 0.4; }}
        }}

        /* Main Network Container */
        #network-container {{
            position: relative;
            width: 100%;
            height: 100vh;
            z-index: 1;
        }}

        #mynetwork {{
            width: 100%;
            height: 100%;
            background: transparent;
        }}

        /* Professional Header */
        .cyber-header {{
            position: absolute;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 10;
            text-align: center;
        }}

        .cyber-title {{
            font-family: 'Orbitron', monospace;
            font-size: 2.2em;
            font-weight: 900;
            color: var(--cyber-primary);
            text-shadow: var(--cyber-glow) var(--cyber-primary);
            margin-bottom: 5px;
        }}

        .cyber-subtitle {{
            font-family: 'Inter', sans-serif;
            font-size: 0.9em;
            color: var(--cyber-secondary);
            opacity: 0.8;
        }}

        /* Glass Morphism Panel Base */
        .glass-panel {{
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 12px;
            box-shadow: 
                var(--cyber-glow) var(--cyber-primary),
                inset 0 0 20px rgba(0, 212, 255, 0.05);
            position: absolute;
            z-index: 5;
        }}

        /* Advanced Control Panel */
        .control-panel {{
            top: 80px;
            left: 20px;
            width: 320px;
            padding: 20px;
            max-height: calc(100vh - 120px);
            overflow-y: auto;
        }}

        .control-section {{
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 1px solid rgba(0, 212, 255, 0.2);
        }}

        .control-section:last-child {{
            border-bottom: none;
        }}

        .section-title {{
            font-family: 'Orbitron', monospace;
            font-size: 0.9em;
            color: var(--cyber-secondary);
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .search-input {{
            width: 100%;
            padding: 12px;
            background: rgba(0, 0, 0, 0.6);
            border: 1px solid var(--cyber-primary);
            border-radius: 8px;
            color: var(--cyber-primary);
            font-family: 'Roboto Mono', monospace;
            font-size: 0.9em;
            transition: all 0.3s ease;
        }}

        .search-input:focus {{
            outline: none;
            border-color: var(--cyber-secondary);
            box-shadow: 0 0 10px rgba(0, 255, 136, 0.3);
        }}

        .filter-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }}

        .filter-checkbox {{
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px;
            background: rgba(0, 0, 0, 0.4);
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.3s ease;
        }}

        .filter-checkbox:hover {{
            background: rgba(0, 212, 255, 0.1);
        }}

        .filter-checkbox input {{
            accent-color: var(--cyber-primary);
        }}

        .slider-container {{
            margin: 10px 0;
        }}

        .slider {{
            width: 100%;
            height: 6px;
            border-radius: 3px;
            background: rgba(64, 64, 64, 0.5);
            outline: none;
            accent-color: var(--cyber-primary);
        }}

        .button-group {{
            display: flex;
            gap: 10px;
            margin-top: 15px;
        }}

        .cyber-button {{
            flex: 1;
            padding: 12px;
            background: linear-gradient(45deg, var(--cyber-primary), var(--cyber-secondary));
            border: none;
            border-radius: 8px;
            color: black;
            font-family: 'Orbitron', monospace;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 0.8em;
        }}

        .cyber-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 212, 255, 0.4);
        }}

        .cyber-button.secondary {{
            background: linear-gradient(45deg, var(--cyber-critical), var(--cyber-warning));
        }}

        /* Analytics Dashboard */
        .analytics-panel {{
            top: 80px;
            right: 20px;
            width: 300px;
            padding: 20px;
        }}

        .metric-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 20px;
        }}

        .metric-item {{
            text-align: center;
            padding: 12px;
            background: rgba(0, 0, 0, 0.4);
            border-radius: 8px;
            border: 1px solid rgba(0, 212, 255, 0.2);
        }}

        .metric-value {{
            font-family: 'Orbitron', monospace;
            font-size: 1.4em;
            font-weight: bold;
            color: var(--cyber-primary);
            margin-bottom: 5px;
        }}

        .metric-label {{
            font-size: 0.8em;
            color: var(--cyber-secondary);
        }}

        /* Real-time Activity Monitor */
        .activity-monitor {{
            height: 60px;
            background: rgba(0, 0, 0, 0.6);
            border: 1px solid var(--cyber-primary);
            border-radius: 8px;
            position: relative;
            overflow: hidden;
            margin-top: 15px;
        }}

        .activity-wave {{
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(
                to top,
                transparent 0%,
                rgba(0, 212, 255, 0.2) 30%,
                rgba(0, 255, 136, 0.3) 60%,
                transparent 100%
            );
            animation: activityPulse 3s ease-in-out infinite;
        }}

        @keyframes activityPulse {{
            0%, 100% {{ transform: scaleY(0.3); opacity: 0.5; }}
            50% {{ transform: scaleY(1); opacity: 1; }}
        }}

        .activity-label {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-family: 'Orbitron', monospace;
            font-size: 0.8em;
            color: var(--cyber-primary);
            font-weight: bold;
            z-index: 2;
        }}

        /* Legend Panel */
        .legend-panel {{
            bottom: 20px;
            left: 20px;
            width: 280px;
            padding: 20px;
        }}

        .legend-item {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 8px;
            margin: 6px 0;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 6px;
            transition: all 0.3s ease;
        }}

        .legend-item:hover {{
            background: rgba(0, 212, 255, 0.1);
            transform: translateX(5px);
        }}

        .legend-shape {{
            width: 20px;
            height: 20px;
            border: 2px solid;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 10px;
        }}

        .shape-star {{ 
            background: var(--cyber-primary);
            border-color: var(--cyber-primary);
            clip-path: polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%);
        }}

        .shape-hexagon {{ 
            background: var(--cyber-secondary);
            border-color: var(--cyber-secondary);
            clip-path: polygon(25% 0%, 75% 0%, 100% 50%, 75% 100%, 25% 100%, 0% 50%);
        }}

        .shape-diamond {{ 
            background: var(--cyber-critical);
            border-color: var(--cyber-critical);
            transform: rotate(45deg);
        }}

        .shape-box {{ 
            background: var(--cyber-warning);
            border-color: var(--cyber-warning);
        }}

        /* Loading States */
        .loading-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(10, 10, 15, 0.9);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 100;
            transition: opacity 0.5s ease;
        }}

        .loading-content {{
            text-align: center;
        }}

        .loading-spinner {{
            width: 60px;
            height: 60px;
            border: 3px solid rgba(0, 212, 255, 0.3);
            border-top: 3px solid var(--cyber-primary);
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }}

        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}

        .loading-text {{
            font-family: 'Orbitron', monospace;
            color: var(--cyber-primary);
            font-size: 1.2em;
            margin-bottom: 10px;
        }}

        .loading-progress {{
            font-family: 'Inter', sans-serif;
            color: var(--cyber-secondary);
            font-size: 0.9em;
        }}

        /* Responsive Design */
        @media (max-width: 1200px) {{
            .control-panel, .analytics-panel {{
                width: 260px;
            }}
        }}

        @media (max-width: 768px) {{
            .control-panel {{
                left: 10px;
                width: calc(100vw - 20px);
                max-width: 300px;
            }}
            
            .analytics-panel {{
                display: none;
            }}
            
            .cyber-title {{
                font-size: 1.5em;
            }}
        }}

        /* Accessibility */
        .sr-only {{
            position: absolute;
            width: 1px;
            height: 1px;
            padding: 0;
            margin: -1px;
            overflow: hidden;
            clip: rect(0, 0, 0, 0);
            white-space: nowrap;
            border: 0;
        }}

        /* High Contrast Mode */
        @media (prefers-contrast: high) {{
            :root {{
                --cyber-primary: #FFFFFF;
                --cyber-secondary: #FFFF00;
                --cyber-void: #000000;
            }}
        }}

        /* Reduced Motion */
        @media (prefers-reduced-motion: reduce) {{
            *, *::before, *::after {{
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }}
        }}
    </style>
</head>

<body>
    <!-- Professional Header -->
    <div class="cyber-header">
        <h1 class="cyber-title">NEURAL CODEBASE MATRIX</h1>
        <p class="cyber-subtitle">Professional Code Intelligence Platform</p>
    </div>

    <!-- Loading Overlay -->
    <div id="loading-overlay" class="loading-overlay">
        <div class="loading-content">
            <div class="loading-spinner"></div>
            <div class="loading-text">Initializing Neural Matrix</div>
            <div id="loading-progress" class="loading-progress">Parsing codebase architecture...</div>
        </div>
    </div>

    <!-- Main Network Container -->
    <div id="network-container">
        <div id="mynetwork" role="img" aria-label="Interactive code dependency graph"></div>
    </div>

    <!-- Advanced Control Panel -->
    <div class="glass-panel control-panel">
        <div class="control-section">
            <h3 class="section-title">🔍 Neural Search</h3>
            <input type="text" 
                   id="node-search" 
                   class="search-input" 
                   placeholder="Search nodes, functions, classes..."
                   aria-label="Search graph nodes">
        </div>

        <div class="control-section">
            <h3 class="section-title">🎛️ View Controls</h3>
            <div class="filter-grid">
                <label class="filter-checkbox">
                    <input type="checkbox" id="show-repository" checked>
                    <span>Core</span>
                </label>
                <label class="filter-checkbox">
                    <input type="checkbox" id="show-modules" checked>
                    <span>Modules</span>
                </label>
                <label class="filter-checkbox">
                    <input type="checkbox" id="show-files" checked>
                    <span>Files</span>
                </label>
                <label class="filter-checkbox">
                    <input type="checkbox" id="show-classes" checked>
                    <span>Classes</span>
                </label>
            </div>
        </div>

        <div class="control-section">
            <h3 class="section-title">⚙️ Physics</h3>
            <div class="slider-container">
                <label for="gravity-slider">Gravity Field</label>
                <input type="range" 
                       id="gravity-slider" 
                       class="slider"
                       min="-20000" 
                       max="-1000" 
                       value="-8000">
                <span id="gravity-value">-8000</span>
            </div>
        </div>

        <div class="control-section">
            <h3 class="section-title">🎯 Analysis</h3>
            <div class="button-group">
                <button class="cyber-button" id="analyze-paths">
                    Trace Paths
                </button>
                <button class="cyber-button secondary" id="find-clusters">
                    Find Clusters
                </button>
            </div>
            <div class="button-group">
                <button class="cyber-button" id="reset-view">
                    Reset View
                </button>
                <button class="cyber-button secondary" id="export-data">
                    Export
                </button>
            </div>
        </div>
    </div>

    <!-- Analytics Dashboard -->
    <div class="glass-panel analytics-panel">
        <div class="control-section">
            <h3 class="section-title">📊 System Metrics</h3>
            <div class="metric-grid">
                <div class="metric-item">
                    <div class="metric-value" id="node-count">{analytics.get('total_nodes', 0)}</div>
                    <div class="metric-label">Neural Nodes</div>
                </div>
                <div class="metric-item">
                    <div class="metric-value" id="edge-count">{analytics.get('total_edges', 0)}</div>
                    <div class="metric-label">Connections</div>
                </div>
                <div class="metric-item">
                    <div class="metric-value" id="complexity-score">{analytics.get('complexity_distribution', {}).get('total', 0)}</div>
                    <div class="metric-label">Complexity</div>
                </div>
                <div class="metric-item">
                    <div class="metric-value" id="quality-score">{analytics.get('quality_indicators', {}).get('overall_score', 8.5)}</div>
                    <div class="metric-label">Quality</div>
                </div>
            </div>
        </div>

        <div class="control-section">
            <h3 class="section-title">🧠 Neural Activity</h3>
            <div class="activity-monitor">
                <div class="activity-wave"></div>
                <div class="activity-label">SYSTEM ACTIVE</div>
            </div>
        </div>

        <div class="control-section">
            <h3 class="section-title">🎯 Hotspots</h3>
            <div id="hotspot-list">
                <!-- Dynamically populated -->
            </div>
        </div>
    </div>

    <!-- Professional Legend -->
    <div class="glass-panel legend-panel">
        <div class="control-section">
            <h3 class="section-title">🔮 Node Types</h3>
            <div class="legend-item">
                <div class="legend-shape shape-star"></div>
                <span>Repository Core</span>
            </div>
            <div class="legend-item">
                <div class="legend-shape shape-hexagon"></div>
                <span>Neural Modules</span>
            </div>
            <div class="legend-item">
                <div class="legend-shape shape-box"></div>
                <span>Data Crystals</span>
            </div>
            <div class="legend-item">
                <div class="legend-shape shape-diamond"></div>
                <span>Class Cores</span>
            </div>
        </div>
    </div>

    <script>
        // Global variables
        let network, nodes, edges;
        let allNodes, allEdges;
        let analytics = {analytics_js};

        // Professional network configuration
        const networkOptions = {{
            physics: {{
                enabled: true,
                stabilization: {{
                    iterations: 200,
                    updateInterval: 25
                }},
                barnesHut: {{
                    gravitationalConstant: -8000,
                    centralGravity: 0.1,
                    springLength: 150,
                    springConstant: 0.02,
                    damping: 0.1,
                    avoidOverlap: 0.2
                }}
            }},
            interaction: {{
                hover: true,
                tooltipDelay: 100,
                hideEdgesOnDrag: false,
                zoomView: true,
                dragView: true,
                selectConnectedEdges: true
            }},
            nodes: {{
                borderWidth: 2,
                borderWidthSelected: 4,
                shadow: {{
                    enabled: true,
                    color: 'rgba(0, 212, 255, 0.5)',
                    size: 8,
                    x: 0,
                    y: 0
                }},
                chosen: {{
                    node: function(values, id, selected, hovering) {{
                        values.shadow = true;
                        values.shadowColor = '#00FF88';
                        values.shadowSize = 15;
                    }}
                }}
            }},
            edges: {{
                width: 2,
                shadow: {{
                    enabled: true,
                    color: 'rgba(0, 212, 255, 0.3)',
                    size: 3
                }},
                smooth: {{
                    type: 'continuous',
                    forceDirection: 'none',
                    roundness: 0.1
                }},
                arrows: {{
                    to: {{
                        enabled: true,
                        scaleFactor: 0.5
                    }}
                }}
            }},
            layout: {{
                improvedLayout: true,
                hierarchical: {{
                    enabled: false
                }}
            }}
        }};

        // Initialize the professional neural network
        function initializeNeuralMatrix() {{
            const container = document.getElementById('mynetwork');
            
            // Load data
            allNodes = new vis.DataSet({nodes_js});
            allEdges = new vis.DataSet({edges_js});
            
            nodes = allNodes;
            edges = allEdges;
            
            // Create network
            const data = {{ nodes: nodes, edges: edges }};
            network = new vis.Network(container, data, networkOptions);
            
            // Setup event handlers
            setupNetworkEvents();
            setupControlEvents();
            
            // Initialize loading progress
            updateLoadingProgress("Building neural pathways...", 25);
            
            // Network stabilization progress
            network.on("stabilizationProgress", function(params) {{
                const progress = Math.round((params.iterations / params.total) * 75) + 25;
                updateLoadingProgress(`Optimizing layout: ${{Math.round((params.iterations / params.total) * 100)}}%`, progress);
            }});
            
            network.once("stabilizationIterationsDone", function() {{
                updateLoadingProgress("Neural matrix online", 100);
                setTimeout(() => {{
                    document.getElementById('loading-overlay').style.display = 'none';
                }}, 1000);
                
                // Initialize analytics
                updateAnalyticsDashboard();
                populateHotspots();
            }});
        }}

        // Setup network event handlers
        function setupNetworkEvents() {{
            network.on("selectNode", function(params) {{
                if (params.nodes.length > 0) {{
                    highlightConnectedNodes(params.nodes[0]);
                }}
            }});
            
            network.on("deselectNode", function(params) {{
                resetNodeStyles();
            }});
            
            network.on("hoverNode", function(params) {{
                addNodeGlowEffect(params.node);
            }});
            
            network.on("blurNode", function(params) {{
                removeNodeGlowEffect(params.node);
            }});
        }}

        // Setup control panel events
        function setupControlEvents() {{
            // Search functionality
            document.getElementById('node-search').addEventListener('input', function(e) {{
                filterNodes(e.target.value);
            }});
            
            // Filter checkboxes
            ['show-repository', 'show-modules', 'show-files', 'show-classes'].forEach(id => {{
                document.getElementById(id).addEventListener('change', updateNodeVisibility);
            }});
            
            // Gravity slider
            const gravitySlider = document.getElementById('gravity-slider');
            const gravityValue = document.getElementById('gravity-value');
            
            gravitySlider.addEventListener('input', function() {{
                gravityValue.textContent = this.value;
                network.setOptions({{
                    physics: {{
                        barnesHut: {{
                            gravitationalConstant: parseInt(this.value)
                        }}
                    }}
                }});
            }});
            
            // Action buttons
            document.getElementById('analyze-paths').addEventListener('click', analyzeCriticalPaths);
            document.getElementById('find-clusters').addEventListener('click', highlightClusters);
            document.getElementById('reset-view').addEventListener('click', resetView);
            document.getElementById('export-data').addEventListener('click', exportData);
        }}

        // Advanced filtering and search
        function filterNodes(searchTerm) {{
            if (!searchTerm.trim()) {{
                nodes.clear();
                nodes.add(allNodes.get());
                return;
            }}
            
            const filteredNodes = allNodes.get().filter(node => 
                node.label.toLowerCase().includes(searchTerm.toLowerCase()) ||
                (node.title && node.title.toLowerCase().includes(searchTerm.toLowerCase()))
            );
            
            const filteredNodeIds = new Set(filteredNodes.map(n => n.id));
            const filteredEdges = allEdges.get().filter(edge => 
                filteredNodeIds.has(edge.from) && filteredNodeIds.has(edge.to)
            );
            
            nodes.clear();
            edges.clear();
            nodes.add(filteredNodes);
            edges.add(filteredEdges);
            
            network.fit();
        }}

        // Update node visibility based on filters
        function updateNodeVisibility() {{
            const filters = {{
                repository: document.getElementById('show-repository').checked,
                module: document.getElementById('show-modules').checked,
                file: document.getElementById('show-files').checked,
                class: document.getElementById('show-classes').checked
            }};
            
            const visibleNodes = allNodes.get().filter(node => filters[node.group] || false);
            const visibleNodeIds = new Set(visibleNodes.map(n => n.id));
            const visibleEdges = allEdges.get().filter(edge => 
                visibleNodeIds.has(edge.from) && visibleNodeIds.has(edge.to)
            );
            
            nodes.clear();
            edges.clear();
            nodes.add(visibleNodes);
            edges.add(visibleEdges);
        }}

        // Highlight connected nodes
        function highlightConnectedNodes(nodeId) {{
            const connectedNodes = network.getConnectedNodes(nodeId);
            const connectedEdges = network.getConnectedEdges(nodeId);
            
            // Update node styles
            const updates = allNodes.get().map(node => ({{
                ...node,
                color: connectedNodes.includes(node.id) || node.id === nodeId ? 
                    node.color : {{ ...node.color, opacity: 0.3 }}
            }}));
            
            nodes.update(updates);
        }}

        // Reset node styles
        function resetNodeStyles() {{
            const updates = allNodes.get().map(node => ({{
                ...node,
                color: {{ ...node.color, opacity: 1 }}
            }}));
            nodes.update(updates);
        }}

        // Add glow effect to node
        function addNodeGlowEffect(nodeId) {{
            const node = nodes.get(nodeId);
            if (node) {{
                nodes.update({{
                    id: nodeId,
                    borderWidth: node.borderWidth + 2,
                    shadow: {{ ...node.shadow, size: (node.shadow?.size || 8) + 5 }}
                }});
            }}
        }}

        // Remove glow effect from node
        function removeNodeGlowEffect(nodeId) {{
            const originalNode = allNodes.get(nodeId);
            if (originalNode) {{
                nodes.update({{
                    id: nodeId,
                    borderWidth: originalNode.borderWidth,
                    shadow: originalNode.shadow
                }});
            }}
        }}

        // Analyze critical paths
        function analyzeCriticalPaths() {{
            // Highlight high-complexity nodes and their connections
            const highComplexityNodes = allNodes.get().filter(node => 
                node.title && node.title.includes('Complexity') &&
                parseInt(node.title.match(/Complexity[:\\s]*(\\d+)/)?.[1] || 0) > 5
            );
            
            highComplexityNodes.forEach(node => {{
                nodes.update({{
                    id: node.id,
                    borderWidth: 4,
                    color: {{ ...node.color, border: '#FF0080' }}
                }});
            }});
            
            // Focus on these nodes
            if (highComplexityNodes.length > 0) {{
                network.focus(highComplexityNodes[0].id, {{ animation: true }});
            }}
        }}

        // Highlight semantic clusters
        function highlightClusters() {{
            const clusterNodes = allNodes.get().filter(node => node.group === 'cluster');
            
            clusterNodes.forEach(cluster => {{
                network.focus(cluster.id, {{ animation: true, scale: 0.8 }});
                
                setTimeout(() => {{
                    const connectedNodes = network.getConnectedNodes(cluster.id);
                    connectedNodes.forEach(nodeId => {{
                        nodes.update({{
                            id: nodeId,
                            borderWidth: 3,
                            color: {{ ...allNodes.get(nodeId).color, border: '#8A2BE2' }}
                        }});
                    }});
                }}, 1000);
            }});
        }}

        // Reset view
        function resetView() {{
            nodes.clear();
            edges.clear();
            nodes.add(allNodes.get());
            edges.add(allEdges.get());
            network.fit({{ animation: true }});
            
            // Reset all filters
            document.getElementById('node-search').value = '';
            ['show-repository', 'show-modules', 'show-files', 'show-classes'].forEach(id => {{
                document.getElementById(id).checked = true;
            }});
        }}

        // Export functionality
        function exportData() {{
            const exportData = {{
                nodes: allNodes.get(),
                edges: allEdges.get(),
                analytics: analytics,
                timestamp: new Date().toISOString()
            }};
            
            const dataStr = JSON.stringify(exportData, null, 2);
            const dataBlob = new Blob([dataStr], {{ type: 'application/json' }});
            
            const link = document.createElement('a');
            link.href = URL.createObjectURL(dataBlob);
            link.download = 'neural_codebase_analysis.json';
            link.click();
        }}

        // Update loading progress
        function updateLoadingProgress(message, progress) {{
            document.getElementById('loading-progress').textContent = `${{message}} (${{progress}}%)`;
        }}

        // Update analytics dashboard
        function updateAnalyticsDashboard() {{
            document.getElementById('node-count').textContent = analytics.total_nodes || 0;
            document.getElementById('edge-count').textContent = analytics.total_edges || 0;
            
            // Update other metrics as needed
        }}

        // Populate hotspots
        function populateHotspots() {{
            const hotspotList = document.getElementById('hotspot-list');
            const hotspots = analytics.performance_hotspots || [];
            
            hotspotList.innerHTML = hotspots.slice(0, 5).map(hotspot => `
                <div class="metric-item" style="margin-bottom: 10px; cursor: pointer;" 
                     onclick="focusOnNode('${{hotspot.nodeId}}')">
                    <div style="font-size: 0.9em; color: var(--cyber-warning);">
                        ${{hotspot.name}}
                    </div>
                    <div style="font-size: 0.8em; color: var(--cyber-secondary);">
                        Score: ${{hotspot.score}}
                    </div>
                </div>
            `).join('');
        }}

        // Focus on specific node
        function focusOnNode(nodeId) {{
            if (network && nodes.get(nodeId)) {{
                network.focus(nodeId, {{ animation: true, scale: 1.5 }});
                network.selectNodes([nodeId]);
            }}
        }}

        // Initialize on page load
        document.addEventListener('DOMContentLoaded', function() {{
            updateLoadingProgress("Loading neural components...", 10);
            setTimeout(initializeNeuralMatrix, 500);
        }});

        // Handle keyboard shortcuts
        document.addEventListener('keydown', function(e) {{
            if (e.ctrlKey || e.metaKey) {{
                switch(e.key) {{
                    case 'f':
                        e.preventDefault();
                        document.getElementById('node-search').focus();
                        break;
                    case 'r':
                        e.preventDefault();
                        resetView();
                        break;
                    case 'e':
                        e.preventDefault();
                        exportData();
                        break;
                }}
            }}
        }});
    </script>
</body>
</html>'''
    
    # Helper methods for the enhanced generator
    def _identify_module_clusters(self, analysis_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Identify logical module clusters from files"""
        clusters = defaultdict(list)
        
        for file_data in analysis_data.get('files', []):
            file_path = file_data['file']
            path_parts = Path(file_path).parts
            
            if len(path_parts) > 1:
                module_name = path_parts[-2]  # Parent directory
            else:
                module_name = 'core'
            
            clusters[module_name].append(file_path)
        
        return dict(clusters)
    
    def _determine_module_for_file(self, file_path: str, module_clusters: Dict[str, List[str]]) -> str:
        """Determine which module a file belongs to"""
        for module, files in module_clusters.items():
            if file_path in files:
                return module
        return 'core'
    
    def _calculate_total_complexity(self, analysis_data: Dict[str, Any]) -> int:
        """Calculate total codebase complexity"""
        return sum(file_data.get('complexity', 0) for file_data in analysis_data.get('files', []))
    
    def _calculate_file_importance(self, file_data: Dict[str, Any]) -> float:
        """Calculate file importance score based on multiple factors"""
        complexity = file_data.get('complexity', 0)
        classes = len(file_data.get('classes', []))
        functions = len(file_data.get('functions', []))
        lines = file_data.get('lines', 0)
        
        # Weighted importance score
        importance = (
            complexity * 0.3 +
            classes * 0.25 +
            functions * 0.25 +
            (lines / 100) * 0.2
        )
        
        return min(importance, 10.0)  # Cap at 10
    
    def _get_color_by_importance(self, importance: float) -> Dict[str, str]:
        """Get color based on importance level"""
        if importance > 7:
            return self._get_semantic_color('critical_paths')
        elif importance > 4:
            return self._get_semantic_color('core_functionality')
        elif importance > 2:
            return self._get_semantic_color('helper_functions')
        else:
            return self._get_semantic_color('neutral_elements')
    
    def _get_semantic_color(self, color_type: str) -> Dict[str, str]:
        """Get semantic color configuration"""
        colors = self.semantic_colors.get(color_type, self.semantic_colors['core_functionality'])
        return {
            'background': colors['primary'],
            'border': colors['secondary'],
            'highlight': {
                'background': colors['highlight'],
                'border': colors['primary']
            },
            'hover': {
                'background': colors['highlight'],
                'border': colors['primary']
            }
        }
    
    def _get_professional_font(self, size: int, color: str) -> Dict[str, Any]:
        """Get professional font configuration"""
        return {
            'size': size,
            'color': color,
            'face': 'Inter, sans-serif',
            'strokeWidth': 1,
            'strokeColor': '#000000'
        }
    
    def _create_professional_tooltip(self, type_label: str, data: Dict[str, Any]) -> str:
        """Create professional tooltip with structured information"""
        lines = [f"<strong>{type_label}</strong>"]
        for key, value in data.items():
            lines.append(f"<em>{key}:</em> {value}")
        return "<br/>".join(lines)
    
    def _create_semantic_edge(self, from_id: str, to_id: str, edge_type: str, title: str) -> Dict[str, Any]:
        """Create semantically meaningful edge"""
        edge_config = self.semantic_edges.get(edge_type, self.semantic_edges['core_connection'])
        
        return {
            'from': from_id,
            'to': to_id,
            'title': title,
            'color': {
                'color': edge_config['color'],
                'highlight': edge_config['color'],
                'opacity': 0.8
            },
            'width': edge_config['width'],
            'dashes': edge_config['style'] == 'dashed',
            'smooth': {
                'type': 'continuous',
                'forceDirection': 'none'
            },
            'arrows': {
                'to': {
                    'enabled': True,
                    'scaleFactor': 0.5
                }
            }
        }
    
    def _calculate_cluster_center(self, cluster_files: List[str], nodes: List[Dict]) -> Dict[str, float]:
        """Calculate geometric center of a cluster"""
        cluster_nodes = [n for n in nodes if any(f in n.get('title', '') for f in cluster_files)]
        
        if not cluster_nodes:
            return {'x': 0, 'y': 0}
        
        avg_x = sum(n.get('physics', {}).get('x', 0) for n in cluster_nodes) / len(cluster_nodes)
        avg_y = sum(n.get('physics', {}).get('y', 0) for n in cluster_nodes) / len(cluster_nodes)
        
        return {'x': avg_x, 'y': avg_y}
    
    def _calculate_cluster_radius(self, file_count: int) -> int:
        """Calculate appropriate radius for cluster visualization"""
        return min(50 + file_count * 5, 150)
    
    def _classify_module_type(self, module_name: str) -> str:
        """Classify module type for enhanced tooltips"""
        name_lower = module_name.lower()
        
        if any(keyword in name_lower for keyword in ['test', 'spec']):
            return 'Testing Module'
        elif any(keyword in name_lower for keyword in ['util', 'helper', 'common']):
            return 'Utility Module'
        elif any(keyword in name_lower for keyword in ['api', 'service', 'controller']):
            return 'Service Module'
        elif any(keyword in name_lower for keyword in ['model', 'entity', 'data']):
            return 'Data Module'
        elif any(keyword in name_lower for keyword in ['ui', 'view', 'component']):
            return 'Interface Module'
        else:
            return 'Business Logic Module'
    
    def _classify_class_type(self, class_data: Dict[str, Any]) -> str:
        """Classify class type for enhanced tooltips"""
        class_name = class_data.get('name', '').lower()
        methods = [m.get('name', '') for m in class_data.get('methods', [])]
        
        if 'test' in class_name:
            return 'Test Class'
        elif any(method.startswith('get_') or method.startswith('set_') for method in methods):
            return 'Data Access Object'
        elif '__call__' in methods:
            return 'Callable Class'
        elif len([m for m in methods if not m.startswith('_')]) == 0:
            return 'Interface Class'
        else:
            return 'Business Logic Class'
    
    def _analyze_complexity_distribution(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze complexity distribution across the codebase"""
        complexities = []
        for file_data in analysis_data.get('files', []):
            complexities.append(file_data.get('complexity', 0))
        
        if not complexities:
            return {'total': 0, 'average': 0, 'max': 0}
        
        return {
            'total': sum(complexities),
            'average': sum(complexities) / len(complexities),
            'max': max(complexities),
            'distribution': {
                'low': len([c for c in complexities if c <= 3]),
                'medium': len([c for c in complexities if 3 < c <= 7]),
                'high': len([c for c in complexities if c > 7])
            }
        }
    
    def _identify_architectural_patterns(self, analysis_data: Dict[str, Any]) -> List[str]:
        """Identify architectural patterns in the codebase"""
        patterns = []
        
        # Analyze file names and structures
        file_names = [file_data['file'].lower() for file_data in analysis_data.get('files', [])]
        
        if any('controller' in name for name in file_names):
            patterns.append('MVC Pattern')
        
        if any('repository' in name for name in file_names):
            patterns.append('Repository Pattern')
        
        if any('factory' in name for name in file_names):
            patterns.append('Factory Pattern')
        
        if any('observer' in name or 'listener' in name for name in file_names):
            patterns.append('Observer Pattern')
        
        return patterns
    
    def _calculate_network_metrics(self, nodes: List[Dict], edges: List[Dict]) -> Dict[str, Any]:
        """Calculate network topology metrics"""
        node_count = len(nodes)
        edge_count = len(edges)
        
        if node_count == 0:
            return {'density': 0, 'connectivity': 0}
        
        # Calculate network density
        max_edges = node_count * (node_count - 1) / 2
        density = edge_count / max_edges if max_edges > 0 else 0
        
        # Calculate average connectivity
        node_degrees = defaultdict(int)
        for edge in edges:
            node_degrees[edge['from']] += 1
            node_degrees[edge['to']] += 1
        
        avg_degree = sum(node_degrees.values()) / len(node_degrees) if node_degrees else 0
        
        return {
            'density': density,
            'average_degree': avg_degree,
            'max_degree': max(node_degrees.values()) if node_degrees else 0,
            'connectivity_ratio': len(node_degrees) / node_count if node_count > 0 else 0
        }
    
    def _identify_performance_hotspots(self, analysis_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify performance hotspots in the codebase"""
        hotspots = []
        
        for file_data in analysis_data.get('files', []):
            complexity = file_data.get('complexity', 0)
            lines = file_data.get('lines', 0)
            
            # Calculate hotspot score
            score = complexity * 0.6 + (lines / 100) * 0.4
            
            if score > 5:  # Threshold for hotspots
                hotspots.append({
                    'name': Path(file_data['file']).name,
                    'file': file_data['file'],
                    'score': round(score, 2),
                    'complexity': complexity,
                    'lines': lines,
                    'nodeId': self._get_node_id(f"file:{file_data['file']}")
                })
        
        return sorted(hotspots, key=lambda x: x['score'], reverse=True)
    
    def _analyze_code_quality(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze overall code quality indicators"""
        total_files = len(analysis_data.get('files', []))
        total_classes = sum(len(f.get('classes', [])) for f in analysis_data.get('files', []))
        total_functions = sum(len(f.get('functions', [])) for f in analysis_data.get('files', []))
        
        if total_files == 0:
            return {'overall_score': 0}
        
        # Calculate quality indicators
        avg_complexity = sum(f.get('complexity', 0) for f in analysis_data.get('files', [])) / total_files
        class_to_file_ratio = total_classes / total_files
        function_to_file_ratio = total_functions / total_files
        
        # Simple quality scoring (0-10 scale)
        complexity_score = max(0, 10 - (avg_complexity - 1) * 2)  # Lower complexity is better
        structure_score = min(10, (class_to_file_ratio + function_to_file_ratio) * 2)  # More structure is better
        
        overall_score = (complexity_score + structure_score) / 2
        
        return {
            'overall_score': round(overall_score, 1),
            'complexity_score': round(complexity_score, 1),
            'structure_score': round(structure_score, 1),
            'average_complexity': round(avg_complexity, 2)
        }
    
    def _calculate_module_complexity(self, module_files: List[str]) -> int:
        """Calculate total complexity for a module"""
        # This would need access to the analysis data
        # Simplified implementation
        return len(module_files) * 5  # Placeholder
    
    # Helper methods
    def _get_node_id(self, identifier: str) -> str:
        """Get or create a unique node ID"""
        if identifier not in self.node_registry:
            self.node_registry[identifier] = f"node_{self.node_id_counter}"
            self.node_id_counter += 1
        return self.node_registry[identifier]


def main():
    """Generate professional cyberpunk neural network knowledge graph"""
    
    input_file = "enhanced_ecological_analysis.json"
    if not os.path.exists(input_file):
        print(f"❌ Analysis file '{input_file}' not found!")
        print("Please run the enhanced ecological analyzer first.")
        return
    
    with open(input_file, "r") as f:
        analysis_data = json.load(f)
    
    # Generate the professional cyberpunk graph
    generator = ProfessionalCyberpunkGraphGenerator()
    output_file = generator.generate_professional_graph(analysis_data)
    
    print(f"✅ Professional Cyberpunk Neural Network Graph generated: {output_file}")
    print(f"🌟 Enhanced with:")
    print(f"   • Hierarchical information architecture")
    print(f"   • Semantic color coding and shape language")
    print(f"   • Professional UI controls and analytics")
    print(f"   • Smart filtering and search capabilities")
    print(f"   • Performance optimizations and accessibility")
    print(f"   • Enterprise-grade visualization features")
    print(f"🚀 Ready to explore your codebase with professional cyberpunk style!")


if __name__ == "__main__":
    main()