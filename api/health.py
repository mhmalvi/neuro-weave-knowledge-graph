from http.server import BaseHTTPRequestHandler
import json
import time

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Health check endpoint"""
        response_data = {
            "status": "healthy",
            "timestamp": int(time.time()),
            "service": "NeuroWeave MCP Server",
            "version": "1.0.0"
        }
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode())

