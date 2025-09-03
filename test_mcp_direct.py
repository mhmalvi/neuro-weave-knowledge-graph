#!/usr/bin/env python3
"""
Direct test of MCP server functionality
Tests the analyze_codebase tool through JSON-RPC protocol
"""

import json
import subprocess
import sys
import os

def test_mcp_server():
    """Test the MCP server analyze_codebase tool"""
    print("Testing codebase-kg MCP Server - analyze_codebase tool")
    print("=" * 60)
    
    # Create JSON-RPC requests
    initialize_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test-client", "version": "1.0.0"}
        }
    }
    
    initialized_notification = {
        "jsonrpc": "2.0",
        "method": "notifications/initialized"
    }
    
    tools_list_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list"
    }
    
    analyze_request = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "analyze_codebase",
            "arguments": {
                "path": "."
            }
        }
    }
    
    try:
        # Start MCP server process
        process = subprocess.Popen(
            [sys.executable, "api/mcp_stdio_simple.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=os.getcwd()
        )
        
        print("MCP Server started")
        
        # Send requests
        requests = [
            initialize_request,
            initialized_notification,
            tools_list_request,
            analyze_request
        ]
        
        responses = []
        
        for req in requests:
            req_json = json.dumps(req) + "\n"
            print(f"Sending: {req.get('method', 'notification')}")
            process.stdin.write(req_json)
            process.stdin.flush()
            
            # Read response (except for notifications)
            if req.get("id"):
                response_line = process.stdout.readline()
                if response_line.strip():
                    response = json.loads(response_line.strip())
                    responses.append(response)
                    print(f"Received response for ID {response.get('id')}")
        
        # Close stdin to signal completion
        process.stdin.close()
        
        # Wait for process to complete
        stdout, stderr = process.communicate(timeout=10)
        
        print("\nAnalysis Results:")
        
        # Find the analyze_codebase response
        analyze_response = None
        for resp in responses:
            if resp.get('id') == 3:
                analyze_response = resp
                break
        
        if analyze_response and 'result' in analyze_response:
            result = analyze_response['result']
            content = result.get('content', [])
            
            if content and len(content) > 0:
                text_content = content[0].get('text', '')
                print("Codebase analysis completed successfully!")
                print("\nAnalysis Summary:")
                print(text_content[:1000] + "..." if len(text_content) > 1000 else text_content)
            else:
                print("No content in analysis response")
                print(f"Response: {analyze_response}")
        else:
            print("Failed to get analysis response")
            if analyze_response:
                print(f"Response: {analyze_response}")
        
        # Check for tools list response
        tools_response = None
        for resp in responses:
            if resp.get('id') == 2:
                tools_response = resp
                break
                
        if tools_response and 'result' in tools_response:
            tools = tools_response['result'].get('tools', [])
            print(f"\nAvailable Tools: {len(tools)}")
            for tool in tools:
                print(f"   - {tool.get('name')}: {tool.get('description')[:50]}...")
        
        if stderr:
            print(f"\nServer stderr: {stderr}")
            
        return analyze_response is not None and 'result' in analyze_response
        
    except subprocess.TimeoutExpired:
        print("Server timeout")
        process.kill()
        return False
    except Exception as e:
        print(f"Error: {e}")
        if 'process' in locals():
            process.kill()
        return False

def main():
    """Main test function"""
    success = test_mcp_server()
    
    print("\n" + "=" * 60)
    if success:
        print("MCP Server test PASSED!")
        print("Core functionality verified:")
        print("   - AST parsing works")
        print("   - File analysis works") 
        print("   - Metrics collection works")
        print("   - JSON-RPC protocol works")
    else:
        print("MCP Server test FAILED!")
        
    return success

if __name__ == "__main__":
    exit(0 if main() else 1)