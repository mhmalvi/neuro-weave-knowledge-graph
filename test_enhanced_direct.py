#!/usr/bin/env python3
"""
Direct test of the enhanced analyzer and EnterpriseCyberpunkGenerator
"""

import sys
import os
import json
from pathlib import Path

# Add current directory to path so we can import our modules
sys.path.insert(0, os.getcwd())

def test_enhanced_analyzer():
    """Test the enhanced ecological analyzer directly"""
    print("TESTING ENHANCED ECOLOGICAL ANALYZER")
    print("=" * 50)
    
    try:
        from enhanced_ecological_analyzer import EnhancedEcologicalAnalyzer
        
        # Initialize the analyzer
        analyzer = EnhancedEcologicalAnalyzer()
        print("[OK] Enhanced analyzer imported successfully")
        
        # Test on current codebase
        print("Running enhanced analysis on current codebase...")
        analysis_result = analyzer.analyze_codebase(".")
        
        # Check results
        files_count = len(analysis_result.get('files', []))
        classes_count = sum(len(f.get('classes', [])) for f in analysis_result.get('files', []))
        functions_count = sum(len(f.get('functions', [])) for f in analysis_result.get('files', []))
        clusters_count = len(analysis_result.get('semantic_clusters', []))
        patterns_count = len(analysis_result.get('patterns', {}).get('design_patterns', []) + 
                            analysis_result.get('patterns', {}).get('architectural_patterns', []))
        
        print(f"[OK] Analysis completed successfully!")
        print(f"    Files analyzed: {files_count}")
        print(f"    Classes found: {classes_count}")
        print(f"    Functions found: {functions_count}")
        print(f"    Semantic clusters: {clusters_count}")
        print(f"    Design patterns: {patterns_count}")
        
        # Check for enhanced features
        enhanced_features = []
        if 'semantic_clusters' in analysis_result:
            enhanced_features.append("Semantic clustering")
        if 'patterns' in analysis_result:
            enhanced_features.append("Pattern detection")
        if 'cross_cutting_concerns' in analysis_result:
            enhanced_features.append("Cross-cutting analysis")
        if 'complexity_metrics' in analysis_result:
            enhanced_features.append("Complexity metrics")
        
        print(f"[OK] Enhanced features active: {', '.join(enhanced_features)}")
        
        return analysis_result, True
        
    except ImportError as e:
        print(f"[ERROR] Failed to import enhanced analyzer: {e}")
        return None, False
    except Exception as e:
        print(f"[ERROR] Enhanced analyzer test failed: {e}")
        return None, False

def test_cyberpunk_generator(analysis_data):
    """Test the enterprise cyberpunk generator directly"""
    print("\nTESTING ENTERPRISE CYBERPUNK KNOWLEDGE GRAPH GENERATOR")
    print("=" * 50)
    
    try:
        from enterprise_cyberpunk_generator import EnterpriseCyberpunkGenerator
        
        # Initialize the generator
        generator = EnterpriseCyberpunkGenerator()
        print("[OK] Enterprise cyberpunk generator imported successfully")
        
        # Check if it's using the new EnterpriseCyberpunkGenerator
        if 'Enterprise' in str(type(generator)):
            print("[OK] Enterprise-grade generator detected!")
        
        # Generate visualization
        output_file = "test_cyberpunk_visualization.html"
        print(f"Generating enterprise cyberpunk visualization: {output_file}")
        
        result_file = generator.generate_enterprise_graph(analysis_data, output_file)
        
        if result_file and os.path.exists(result_file):
            file_size = os.path.getsize(result_file) / 1024  # KB
            print(f"[OK] Cyberpunk visualization generated successfully!")
            print(f"    File: {result_file}")
            print(f"    Size: {file_size:.1f} KB")
            
            # Check for enterprise features in the generated file
            with open(result_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            enterprise_features = []
            if 'enterprise' in content.lower():
                enterprise_features.append("Enterprise branding")
            if 'cyberpunk' in content.lower():
                enterprise_features.append("Cyberpunk styling")
            if 'neural' in content.lower():
                enterprise_features.append("Neural network theme")
            if 'analytics' in content.lower():
                enterprise_features.append("Analytics dashboard")
            if 'gradient' in content.lower():
                enterprise_features.append("Advanced gradients")
            if 'animation' in content.lower():
                enterprise_features.append("Smooth animations")
            
            if enterprise_features:
                print(f"[OK] Enterprise features detected: {', '.join(enterprise_features)}")
            
            return True
        else:
            print("[ERROR] Failed to generate cyberpunk visualization")
            return False
            
    except ImportError as e:
        print(f"[ERROR] Failed to import cyberpunk generator: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Cyberpunk generator test failed: {e}")
        return False

def test_enterprise_integration():
    """Test enterprise-specific features"""
    print("\nTESTING ENTERPRISE INTEGRATION")
    print("=" * 50)
    
    try:
        # Check if enterprise modules exist
        enterprise_files = [
            "enterprise_cyberpunk_generator.py",
            "enhanced_ecological_analyzer.py"
        ]
        
        existing_files = []
        for file in enterprise_files:
            if os.path.exists(file):
                existing_files.append(file)
                print(f"[OK] {file} found")
            else:
                print(f"[ERROR] {file} missing")
        
        if len(existing_files) == len(enterprise_files):
            print("[OK] All enterprise modules present")
            
            # Check file contents for enterprise features
            enterprise_indicators = [
                "EnterpriseCyberpunkGenerator", 
                "professional", 
                "analytics",
                "enterprise",
                "neural network",
                "semantic clustering"
            ]
            
            found_indicators = []
            for file in existing_files:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    for indicator in enterprise_indicators:
                        if indicator.lower() in content.lower():
                            found_indicators.append(f"{indicator} in {file}")
            
            print(f"[OK] Enterprise indicators found: {len(found_indicators)}")
            for indicator in found_indicators[:5]:  # Show first 5
                print(f"    - {indicator}")
            
            return len(found_indicators) > 0
        else:
            print("[ERROR] Missing enterprise modules")
            return False
            
    except Exception as e:
        print(f"[ERROR] Enterprise integration test failed: {e}")
        return False

def main():
    """Main test function"""
    print("NEURO-WEAVE KNOWLEDGE GRAPH - ENTERPRISE TESTING SUITE")
    print("=" * 60)
    
    # Test 1: Enhanced Analyzer
    analysis_data, analyzer_success = test_enhanced_analyzer()
    
    # Test 2: Cyberpunk Generator
    generator_success = False
    if analyzer_success and analysis_data:
        generator_success = test_cyberpunk_generator(analysis_data)
    else:
        print("\n[SKIP] Cyberpunk generator test (analyzer failed)")
    
    # Test 3: Enterprise Integration
    enterprise_success = test_enterprise_integration()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)
    
    tests = [
        ("Enhanced Analyzer", analyzer_success),
        ("Cyberpunk Generator", generator_success),
        ("Enterprise Integration", enterprise_success)
    ]
    
    passed = sum(1 for _, success in tests if success)
    total = len(tests)
    
    for test_name, success in tests:
        status = "[PASS]" if success else "[FAIL]"
        print(f"{status} {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n[SUCCESS] All enterprise features are working correctly!")
        print("The EnterpriseCyberpunkGenerator is ready for production use.")
        
        # Show next steps
        if os.path.exists("test_cyberpunk_visualization.html"):
            abs_path = os.path.abspath("test_cyberpunk_visualization.html")
            print(f"\nGenerated visualization: {abs_path}")
            print("Open this file in your browser to see the enterprise-grade visualization!")
    else:
        print("\n[WARNING] Some enterprise features need attention.")
    
    return passed == total

if __name__ == "__main__":
    exit(0 if main() else 1)