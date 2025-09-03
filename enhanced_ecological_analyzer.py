#!/usr/bin/env python3
"""
Enhanced Ecological Codebase Analyzer

This module provides comprehensive multi-level analysis of codebase ecosystems,
including semantic relationships, architectural patterns, data flows,
inheritance hierarchies, composition patterns, and cross-cutting concerns.
"""

import ast
import os
import re
import json
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple, Optional
from collections import defaultdict, deque
import importlib.util

class EnhancedEcologicalAnalyzer:
    """Multi-dimensional codebase analysis with ecological relationship mapping"""
    
    def __init__(self):
        self.analysis_data = {
            'files': [],
            'classes': [],
            'functions': [],
            'imports': [],
            'relationships': {
                'inheritance': [],
                'composition': [],
                'aggregation': [],
                'dependency': [],
                'association': [],
                'data_flow': [],
                'call_graph': [],
                'module_coupling': [],
                'architectural_layers': []
            },
            'patterns': {
                'design_patterns': [],
                'architectural_patterns': [],
                'anti_patterns': []
            },
            'metrics': {
                'complexity': {},
                'coupling': {},
                'cohesion': {},
                'maintainability': {}
            },
            'semantic_clusters': [],
            'cross_cutting_concerns': []
        }
        
        self.call_graph = defaultdict(set)
        self.dependency_graph = defaultdict(set)
        self.inheritance_tree = defaultdict(set)
        self.composition_map = defaultdict(set)
        self.import_network = defaultdict(set)
        
    def analyze_codebase(self, root_path: str) -> Dict[str, Any]:
        """Perform comprehensive multi-level ecological analysis"""
        root = Path(root_path)
        
        # Phase 1: Basic structural analysis
        self._analyze_structure(root)
        
        # Phase 2: Semantic relationship analysis
        self._analyze_semantic_relationships()
        
        # Phase 3: Architectural pattern detection
        self._detect_architectural_patterns()
        
        # Phase 4: Data flow analysis
        self._analyze_data_flows()
        
        # Phase 5: Cross-cutting concern identification
        self._identify_cross_cutting_concerns()
        
        # Phase 6: Clustering and ecosystem mapping
        self._create_semantic_clusters()
        
        # Phase 7: Quality metrics calculation
        self._calculate_quality_metrics()
        
        return self.analysis_data
    
    def _analyze_structure(self, root: Path):
        """Deep structural analysis with AST parsing"""
        for py_file in root.rglob("*.py"):
            if self._should_skip_file(py_file):
                continue
                
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                tree = ast.parse(content, filename=str(py_file))
                file_analysis = self._analyze_python_file_deep(py_file, tree, content)
                self.analysis_data['files'].append(file_analysis)
                
            except Exception as e:
                print(f"Error analyzing {py_file}: {e}")
    
    def _analyze_python_file_deep(self, file_path: Path, tree: ast.AST, content: str) -> Dict[str, Any]:
        """Comprehensive Python file analysis"""
        analyzer = DeepASTAnalyzer(str(file_path))
        analyzer.visit(tree)
        
        return {
            'file': str(file_path),
            'type': 'python',
            'size': len(content),
            'lines': len(content.splitlines()),
            'classes': analyzer.classes,
            'functions': analyzer.functions,
            'imports': analyzer.imports,
            'variables': analyzer.variables,
            'decorators': analyzer.decorators,
            'docstrings': analyzer.docstrings,
            'complexity': self._calculate_cyclomatic_complexity(tree),
            'dependencies': list(analyzer.dependencies),
            'call_patterns': analyzer.call_patterns,
            'data_structures': analyzer.data_structures,
            'async_patterns': analyzer.async_patterns
        }
    
    def _analyze_semantic_relationships(self):
        """Analyze semantic relationships between components"""
        # Build inheritance relationships
        for file_data in self.analysis_data['files']:
            for class_data in file_data.get('classes', []):
                class_name = class_data['name']
                for base in class_data.get('bases', []):
                    self.inheritance_tree[base].add(class_name)
                    self.analysis_data['relationships']['inheritance'].append({
                        'parent': base,
                        'child': class_name,
                        'file': file_data['file'],
                        'line': class_data.get('line', 0)
                    })
        
        # Build composition relationships
        self._analyze_composition_patterns()
        
        # Build dependency relationships
        self._analyze_dependency_patterns()
        
        # Build call graph relationships
        self._analyze_call_graph()
    
    def _analyze_composition_patterns(self):
        """Detect composition and aggregation patterns"""
        for file_data in self.analysis_data['files']:
            for class_data in file_data.get('classes', []):
                # Look for instance variables that are objects of other classes
                for method in class_data.get('methods', []):
                    if method.get('name') == '__init__':
                        # Analyze constructor for composition patterns
                        for assignment in method.get('assignments', []):
                            if self._is_composition_pattern(assignment):
                                self.analysis_data['relationships']['composition'].append({
                                    'container': class_data['name'],
                                    'component': assignment['type'],
                                    'relationship_type': 'composition',
                                    'file': file_data['file']
                                })
    
    def _analyze_dependency_patterns(self):
        """Analyze module and class dependencies"""
        for file_data in self.analysis_data['files']:
            file_path = file_data['file']
            
            for import_data in file_data.get('imports', []):
                module = import_data['module']
                self.dependency_graph[file_path].add(module)
                
                self.analysis_data['relationships']['dependency'].append({
                    'source': file_path,
                    'target': module,
                    'import_type': import_data.get('type', 'import'),
                    'alias': import_data.get('alias'),
                    'line': import_data.get('line', 0)
                })
    
    def _analyze_call_graph(self):
        """Build comprehensive call graph"""
        for file_data in self.analysis_data['files']:
            for func_data in file_data.get('functions', []):
                func_name = func_data['name']
                
                for call in func_data.get('calls', []):
                    self.call_graph[func_name].add(call)
                    self.analysis_data['relationships']['call_graph'].append({
                        'caller': func_name,
                        'callee': call,
                        'file': file_data['file'],
                        'line': func_data.get('line', 0)
                    })
    
    def _detect_architectural_patterns(self):
        """Detect architectural and design patterns"""
        # Detect MVC pattern
        if self._detect_mvc_pattern():
            self.analysis_data['patterns']['architectural_patterns'].append('MVC')
        
        # Detect Repository pattern
        if self._detect_repository_pattern():
            self.analysis_data['patterns']['design_patterns'].append('Repository')
        
        # Detect Observer pattern
        if self._detect_observer_pattern():
            self.analysis_data['patterns']['design_patterns'].append('Observer')
        
        # Detect Singleton pattern
        if self._detect_singleton_pattern():
            self.analysis_data['patterns']['design_patterns'].append('Singleton')
    
    def _analyze_data_flows(self):
        """Analyze data flow patterns through the system"""
        # Track data transformations
        for file_data in self.analysis_data['files']:
            for func_data in file_data.get('functions', []):
                data_flow = self._trace_data_flow(func_data)
                if data_flow:
                    self.analysis_data['relationships']['data_flow'].append({
                        'function': func_data['name'],
                        'file': file_data['file'],
                        'flow': data_flow
                    })
    
    def _identify_cross_cutting_concerns(self):
        """Identify cross-cutting concerns like logging, security, caching"""
        concerns = {
            'logging': ['log', 'logger', 'debug', 'info', 'warning', 'error'],
            'security': ['auth', 'token', 'password', 'encrypt', 'decrypt'],
            'caching': ['cache', 'redis', 'memcache'],
            'database': ['db', 'sql', 'query', 'connection'],
            'testing': ['test', 'assert', 'mock', 'fixture'],
            'error_handling': ['try', 'except', 'raise', 'exception']
        }
        
        for file_data in self.analysis_data['files']:
            file_concerns = set()
            content_lower = json.dumps(file_data).lower()
            
            for concern, keywords in concerns.items():
                if any(keyword in content_lower for keyword in keywords):
                    file_concerns.add(concern)
            
            if file_concerns:
                self.analysis_data['cross_cutting_concerns'].append({
                    'file': file_data['file'],
                    'concerns': list(file_concerns)
                })
    
    def _create_semantic_clusters(self):
        """Create semantic clusters based on functionality and relationships"""
        # Cluster by functionality
        functionality_clusters = defaultdict(list)
        
        for file_data in self.analysis_data['files']:
            file_path = file_data['file']
            cluster_key = self._determine_functional_cluster(file_data)
            functionality_clusters[cluster_key].append(file_path)
        
        for cluster_name, files in functionality_clusters.items():
            if len(files) > 1:  # Only include clusters with multiple files
                self.analysis_data['semantic_clusters'].append({
                    'type': 'functional',
                    'name': cluster_name,
                    'files': files,
                    'cohesion_score': self._calculate_cluster_cohesion(files)
                })
    
    def _calculate_quality_metrics(self):
        """Calculate various quality metrics"""
        for file_data in self.analysis_data['files']:
            file_path = file_data['file']
            
            # Complexity metrics
            self.analysis_data['metrics']['complexity'][file_path] = {
                'cyclomatic': file_data.get('complexity', 0),
                'lines_of_code': file_data.get('lines', 0),
                'number_of_classes': len(file_data.get('classes', [])),
                'number_of_functions': len(file_data.get('functions', []))
            }
            
            # Coupling metrics
            incoming_deps = len([d for d in self.analysis_data['relationships']['dependency'] 
                               if d['target'] == file_path])
            outgoing_deps = len([d for d in self.analysis_data['relationships']['dependency'] 
                               if d['source'] == file_path])
            
            self.analysis_data['metrics']['coupling'][file_path] = {
                'afferent_coupling': incoming_deps,
                'efferent_coupling': outgoing_deps,
                'instability': outgoing_deps / (incoming_deps + outgoing_deps) if (incoming_deps + outgoing_deps) > 0 else 0
            }
    
    # Helper methods
    def _should_skip_file(self, file_path: Path) -> bool:
        """Determine if file should be skipped"""
        skip_patterns = ['__pycache__', '.git', '.venv', 'venv', 'node_modules', '.pytest_cache']
        return any(pattern in str(file_path) for pattern in skip_patterns)
    
    def _calculate_cyclomatic_complexity(self, tree: ast.AST) -> int:
        """Calculate cyclomatic complexity"""
        complexity = 1  # Base complexity
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor, 
                               ast.ExceptHandler, ast.With, ast.AsyncWith)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        
        return complexity
    
    def _is_composition_pattern(self, assignment: Dict[str, Any]) -> bool:
        """Check if assignment represents composition"""
        # Simplified heuristic - in real implementation, this would be more sophisticated
        return assignment.get('is_object_creation', False)
    
    def _detect_mvc_pattern(self) -> bool:
        """Detect MVC architectural pattern"""
        has_model = any('model' in file_data['file'].lower() 
                       for file_data in self.analysis_data['files'])
        has_view = any('view' in file_data['file'].lower() 
                      for file_data in self.analysis_data['files'])
        has_controller = any('controller' in file_data['file'].lower() 
                           for file_data in self.analysis_data['files'])
        return has_model and has_view and has_controller
    
    def _detect_repository_pattern(self) -> bool:
        """Detect Repository design pattern"""
        return any('repository' in file_data['file'].lower() or 
                  any('repository' in cls['name'].lower() 
                      for cls in file_data.get('classes', []))
                  for file_data in self.analysis_data['files'])
    
    def _detect_observer_pattern(self) -> bool:
        """Detect Observer design pattern"""
        observer_keywords = ['observer', 'listener', 'subscriber', 'notify']
        return any(keyword in json.dumps(file_data).lower() 
                  for file_data in self.analysis_data['files'] 
                  for keyword in observer_keywords)
    
    def _detect_singleton_pattern(self) -> bool:
        """Detect Singleton design pattern"""
        for file_data in self.analysis_data['files']:
            for cls in file_data.get('classes', []):
                methods = [m['name'] for m in cls.get('methods', [])]
                if '__new__' in methods and any('instance' in str(cls).lower() for m in methods):
                    return True
        return False
    
    def _trace_data_flow(self, func_data: Dict[str, Any]) -> List[str]:
        """Trace data flow through a function"""
        # Simplified implementation - would be more sophisticated in practice
        flow = []
        if 'parameters' in func_data:
            flow.extend(func_data['parameters'])
        if 'return_type' in func_data:
            flow.append(f"returns -> {func_data['return_type']}")
        return flow
    
    def _determine_functional_cluster(self, file_data: Dict[str, Any]) -> str:
        """Determine functional cluster for a file"""
        file_path = file_data['file'].lower()
        
        if any(keyword in file_path for keyword in ['test', 'spec']):
            return 'testing'
        elif any(keyword in file_path for keyword in ['model', 'entity']):
            return 'data_model'
        elif any(keyword in file_path for keyword in ['view', 'template', 'ui']):
            return 'presentation'
        elif any(keyword in file_path for keyword in ['controller', 'handler', 'api']):
            return 'control_logic'
        elif any(keyword in file_path for keyword in ['util', 'helper', 'tool']):
            return 'utilities'
        elif any(keyword in file_path for keyword in ['config', 'setting']):
            return 'configuration'
        else:
            return 'core_business_logic'
    
    def _calculate_cluster_cohesion(self, files: List[str]) -> float:
        """Calculate cohesion score for a cluster"""
        # Simplified cohesion calculation
        return min(1.0, len(files) / 10.0)


class DeepASTAnalyzer(ast.NodeVisitor):
    """Deep AST analysis for comprehensive code understanding"""
    
    def __init__(self, filename: str):
        self.filename = filename
        self.classes = []
        self.functions = []
        self.imports = []
        self.variables = []
        self.decorators = []
        self.docstrings = []
        self.dependencies = set()
        self.call_patterns = []
        self.data_structures = []
        self.async_patterns = []
        self.current_class = None
        
    def visit_ClassDef(self, node):
        """Visit class definitions"""
        class_info = {
            'name': node.name,
            'line': node.lineno,
            'file': self.filename,
            'bases': [self._get_node_name(base) for base in node.bases],
            'methods': [],
            'decorators': [self._get_node_name(d) for d in node.decorator_list],
            'docstring': ast.get_docstring(node),
            'is_abstract': self._is_abstract_class(node),
            'complexity': 1
        }
        
        old_class = self.current_class
        self.current_class = class_info
        
        # Visit class body
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method_info = self._analyze_method(item)
                class_info['methods'].append(method_info)
            elif isinstance(item, ast.AsyncFunctionDef):
                method_info = self._analyze_async_method(item)
                class_info['methods'].append(method_info)
                
        self.classes.append(class_info)
        self.current_class = old_class
        self.generic_visit(node)
    
    def visit_FunctionDef(self, node):
        """Visit function definitions"""
        if self.current_class is None:  # Only top-level functions
            func_info = self._analyze_function(node)
            self.functions.append(func_info)
        self.generic_visit(node)
    
    def visit_AsyncFunctionDef(self, node):
        """Visit async function definitions"""
        if self.current_class is None:  # Only top-level functions
            func_info = self._analyze_async_function(node)
            self.functions.append(func_info)
            self.async_patterns.append({
                'type': 'async_function',
                'name': node.name,
                'line': node.lineno
            })
        self.generic_visit(node)
    
    def visit_Import(self, node):
        """Visit import statements"""
        for alias in node.names:
            self.imports.append({
                'module': alias.name,
                'alias': alias.asname,
                'type': 'import',
                'line': node.lineno,
                'file': self.filename
            })
            self.dependencies.add(alias.name)
    
    def visit_ImportFrom(self, node):
        """Visit from...import statements"""
        module = node.module or ''
        for alias in node.names:
            self.imports.append({
                'module': f"{module}.{alias.name}" if module else alias.name,
                'alias': alias.asname,
                'from': module,
                'type': 'from_import',
                'line': node.lineno,
                'file': self.filename
            })
            self.dependencies.add(module)
    
    def visit_Call(self, node):
        """Visit function calls"""
        call_name = self._get_node_name(node.func)
        if call_name:
            self.call_patterns.append({
                'function': call_name,
                'line': node.lineno,
                'args_count': len(node.args),
                'kwargs_count': len(node.keywords)
            })
        self.generic_visit(node)
    
    def _analyze_function(self, node) -> Dict[str, Any]:
        """Analyze a function node"""
        return {
            'name': node.name,
            'line': node.lineno,
            'file': self.filename,
            'args': [arg.arg for arg in node.args.args],
            'decorators': [self._get_node_name(d) for d in node.decorator_list],
            'docstring': ast.get_docstring(node),
            'is_async': False,
            'calls': self._extract_calls(node),
            'complexity': self._calculate_function_complexity(node),
            'return_statements': self._count_return_statements(node)
        }
    
    def _analyze_async_function(self, node) -> Dict[str, Any]:
        """Analyze an async function node"""
        func_info = self._analyze_function(node)
        func_info['is_async'] = True
        return func_info
    
    def _analyze_method(self, node) -> Dict[str, Any]:
        """Analyze a method node"""
        method_info = self._analyze_function(node)
        method_info['is_method'] = True
        method_info['is_property'] = any(d == 'property' for d in method_info['decorators'])
        method_info['is_classmethod'] = any(d == 'classmethod' for d in method_info['decorators'])
        method_info['is_staticmethod'] = any(d == 'staticmethod' for d in method_info['decorators'])
        return method_info
    
    def _analyze_async_method(self, node) -> Dict[str, Any]:
        """Analyze an async method node"""
        method_info = self._analyze_method(node)
        method_info['is_async'] = True
        return method_info
    
    def _extract_calls(self, node) -> List[str]:
        """Extract function calls from a node"""
        calls = []
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                call_name = self._get_node_name(child.func)
                if call_name:
                    calls.append(call_name)
        return calls
    
    def _get_node_name(self, node) -> str:
        """Get the name of an AST node"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_node_name(node.value)}.{node.attr}"
        elif isinstance(node, ast.Call):
            return self._get_node_name(node.func)
        else:
            return str(node)
    
    def _is_abstract_class(self, node) -> bool:
        """Check if a class is abstract"""
        # Check for ABC inheritance or abstract methods
        bases = [self._get_node_name(base) for base in node.bases]
        return 'ABC' in bases or any(hasattr(item, 'decorator_list') and 
                                   any(self._get_node_name(d) == 'abstractmethod' 
                                       for d in item.decorator_list)
                                   for item in node.body if hasattr(item, 'decorator_list'))
    
    def _calculate_function_complexity(self, node) -> int:
        """Calculate cyclomatic complexity of a function"""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor,
                                ast.ExceptHandler, ast.With, ast.AsyncWith)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        return complexity
    
    def _count_return_statements(self, node) -> int:
        """Count return statements in a function"""
        return len([child for child in ast.walk(node) if isinstance(child, ast.Return)])


if __name__ == "__main__":
    analyzer = EnhancedEcologicalAnalyzer()
    result = analyzer.analyze_codebase(".")
    
    with open("enhanced_ecological_analysis.json", "w") as f:
        json.dump(result, f, indent=2)
    
    print("Enhanced ecological analysis complete!")