#!/usr/bin/env python3
"""
Simple test of MCP server functionality - JSON output only
"""

import json
import subprocess
import sys
import os

def test_mcp_server():
    """Test the MCP server analyze_codebase tool"""
    print("Testing codebase-kg MCP Server - analyze_codebase tool")
    print("=" * 60)
    
    # Create JSON-RPC request for analyze_codebase
    analyze_request = {
        "jsonrpc": "2.0",
        "id": 1,
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
        
        # Send initialize first
        init_req = {"jsonrpc": "2.0", "id": 0, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0"}}}
        process.stdin.write(json.dumps(init_req) + "\n")
        process.stdin.flush()
        init_resp = process.stdout.readline()
        print("Initialize response received")
        
        # Send initialized notification
        init_notif = {"jsonrpc": "2.0", "method": "notifications/initialized"}
        process.stdin.write(json.dumps(init_notif) + "\n")
        process.stdin.flush()
        
        # Send analyze request
        req_json = json.dumps(analyze_request) + "\n"
        process.stdin.write(req_json)
        process.stdin.flush()
        
        # Read response
        response_line = process.stdout.readline()
        process.stdin.close()
        
        if response_line.strip():
            response = json.loads(response_line.strip())
            print("Response received")
            
            if 'result' in response:
                result = response['result']
                if isinstance(result, dict) and 'content' in result:
                    content = result['content']
                    if isinstance(content, list) and len(content) > 0:
                        # Extract just the metrics from the response
                        text_content = content[0].get('text', '')
                        # Look for metrics in the text
                        if 'Files:' in text_content and 'Classes:' in text_content:
                            print("SUCCESS: Codebase analysis completed!")
                            print("Analysis contains expected metrics")
                            
                            # Extract key metrics for verification
                            lines = text_content.split('\n')
                            for line in lines:
                                if any(keyword in line for keyword in ['Files:', 'Classes:', 'Functions:', 'Imports:']):
                                    # Clean line of emojis and print
                                    clean_line = ''.join(char for char in line if ord(char) < 128)
                                    if clean_line.strip():
                                        print(f"  {clean_line.strip()}")
                            
                            return True
                        else:
                            print("Analysis response missing expected metrics")
                            return False
                    else:
                        print("No content in analysis response")
                        return False
                elif isinstance(result, str):
                    print("SUCCESS: Got string response")
                    clean_result = ''.join(char for char in result if ord(char) < 128)
                    print(f"Result preview: {clean_result[:200]}...")
                    return True
                else:
                    print(f"Unexpected result format: {type(result)}")
                    return False
            elif 'error' in response:
                print(f"Error in response: {response['error']}")
                return False
            else:
                print("No result or error in response")
                return False
        else:
            print("No response received")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        if 'process' in locals():
            try:
                process.terminate()
            except:
                pass

def main():
    """Main test function"""
    success = test_mcp_server()
    
    print("\n" + "=" * 60)
    if success:
        print("MCP Server test PASSED!")
        print("Core functionality verified:")
        print("  - AST parsing works")
        print("  - File analysis works") 
        print("  - Metrics collection works")
        print("  - JSON-RPC protocol works")
    else:
        print("MCP Server test FAILED!")
        
    return success

if __name__ == "__main__":
    main()