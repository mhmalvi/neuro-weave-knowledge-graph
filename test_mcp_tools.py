#!/usr/bin/env python3
"""
Simple test of MCP tools by importing directly from the server module
"""

import sys
import os
import asyncio
import json
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.getcwd())

async def test_mcp_tools():
    """Test the MCP tools directly"""
    print("TESTING MCP TOOLS DIRECTLY")
    print("=" * 50)
    
    try:
        # Import the MCP server module
        from mcp_server import (
            codebase_analyzer, 
            enterprise_cyberpunk_generator, 
            enhanced_analyzer
        )
        
        print("[OK] MCP server modules imported successfully")
        
        # Test 1: Basic codebase analysis
        print("\n1. Testing basic codebase analysis...")
        basic_analysis = codebase_analyzer.analyze_codebase(".")
        print(f"   [OK] Basic analysis: {len(basic_analysis.get('files', []))} files found")
        
        # Test 2: Enhanced ecological analysis
        print("\n2. Testing enhanced ecological analysis...")
        enhanced_analysis = enhanced_analyzer.analyze_codebase(".")
        print(f"   [OK] Enhanced analysis: {len(enhanced_analysis.get('files', []))} files")
        print(f"   [OK] Semantic clusters: {len(enhanced_analysis.get('semantic_clusters', []))}")
        print(f"   [OK] Design patterns: {len(enhanced_analysis.get('patterns', {}).get('design_patterns', []))}")
        
        # Test 3: Enterprise cyberpunk visualization generation
        print("\n3. Testing enterprise cyberpunk graph generation...")
        output_file = "mcp_test_cyberpunk.html"
        result_file = enterprise_cyberpunk_generator.generate_enterprise_graph(enhanced_analysis, output_file)
        
        if result_file and os.path.exists(result_file):
            file_size = os.path.getsize(result_file) / 1024  # KB
            print(f"   [OK] Cyberpunk graph generated: {result_file} ({file_size:.1f} KB)")
            
            # Check file content for enterprise features
            with open(result_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            enterprise_features = []
            if 'EnterpriseCyberpunkGenerator' in content:
                enterprise_features.append("Enterprise class detected")
            if 'analytics' in content.lower():
                enterprise_features.append("Analytics dashboard")
            if 'neural network' in content.lower():
                enterprise_features.append("Neural network theme")
            if 'professional' in content.lower():
                enterprise_features.append("Professional styling")
                
            if enterprise_features:
                print(f"   [OK] Enterprise features found: {len(enterprise_features)}")
                for feature in enterprise_features:
                    print(f"        - {feature}")
        else:
            print("   [ERROR] Failed to generate cyberpunk visualization")
            return False
            
        print("\n[SUCCESS] All MCP tools working correctly!")
        print("The EnterpriseCyberpunkGenerator is integrated and functional!")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] MCP tools test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_mcp_tool_calls():
    """Test the actual MCP tool call handlers"""
    print("\nTESTING MCP TOOL CALL HANDLERS")  
    print("=" * 50)
    
    try:
        # Import the MCP server app and handlers
        from mcp_server import app, handle_call_tool
        
        print("[OK] MCP app and handlers imported")
        
        # Test analyze_codebase_enhanced tool call
        print("\nTesting analyze_codebase_enhanced tool call...")
        
        result = await handle_call_tool(
            name="analyze_codebase_enhanced",
            arguments={"path": "."}
        )
        
        if result and len(result) > 0:
            content = result[0].text if hasattr(result[0], 'text') else str(result[0])
            print("[OK] Enhanced analysis tool call successful!")
            
            # Look for enterprise indicators in the response
            enterprise_indicators = [
                "Neural Cores", "Synapses", "Semantic Clusters", 
                "Architectural Patterns", "Cyberpunk", "Enhanced"
            ]
            
            found_indicators = []
            for indicator in enterprise_indicators:
                if indicator in content:
                    found_indicators.append(indicator)
            
            if found_indicators:
                print(f"   [OK] Enterprise indicators found: {', '.join(found_indicators)}")
            
            # Show part of the response (handle unicode)
            try:
                preview = content[:300].encode('ascii', 'ignore').decode('ascii')
                print(f"\n   Response preview: {preview}...")
            except UnicodeError:
                print(f"\n   Response preview: [Unicode content - {len(content)} characters]")
            
        else:
            print("[ERROR] No result from enhanced analysis tool")
            return False
            
        print("\n[SUCCESS] MCP tool call handlers working correctly!")
        return True
        
    except Exception as e:
        print(f"[ERROR] MCP tool call test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("NEURO-WEAVE KNOWLEDGE GRAPH - MCP TOOLS TESTING")
    print("Testing EnterpriseCyberpunkGenerator via MCP Server")
    print("=" * 60)
    
    # Run async tests
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        # Test direct tool access
        direct_success = loop.run_until_complete(test_mcp_tools())
        
        # Test MCP tool call handlers  
        handler_success = loop.run_until_complete(test_mcp_tool_calls())
        
        # Summary
        print("\n" + "=" * 60)
        print("FINAL TEST RESULTS")
        print("=" * 60)
        
        tests = [
            ("Direct MCP Tools", direct_success),
            ("MCP Tool Call Handlers", handler_success)
        ]
        
        passed = sum(1 for _, success in tests if success)
        total = len(tests)
        
        for test_name, success in tests:
            status = "[PASS]" if success else "[FAIL]"
            print(f"{status} {test_name}")
        
        print(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            print("\n[SUCCESS] EnterpriseCyberpunkGenerator is fully integrated!")
            print("The MCP server is ready to provide enterprise-grade visualizations.")
            
            # Show generated files
            generated_files = [f for f in os.listdir(".") if f.startswith("mcp_test_") and f.endswith(".html")]
            if generated_files:
                print(f"\nGenerated visualizations:")
                for file in generated_files:
                    abs_path = os.path.abspath(file)
                    print(f"   {abs_path}")
        else:
            print("\n[WARNING] Some MCP tools need attention.")
        
        return passed == total
        
    finally:
        loop.close()

if __name__ == "__main__":
    exit(0 if main() else 1)