from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Root endpoint - MCP server info"""
        response_data = {
            "name": "NeuroWeave Knowledge Graph MCP Server",
            "version": "1.0.0", 
            "description": "Remote codebase analysis and interactive knowledge graph generation",
            "transport": "http",
            "author": "mhmalvi",
            "repository": "https://github.com/mhmalvi/neuro-weave-knowledge-graph",
            "capabilities": ["tools", "resources"],
            "tools": [
                {
                    "name": "analyze_github_repo", 
                    "description": "Analyze a GitHub repository structure and metadata"
                },
                {
                    "name": "get_repo_info",
                    "description": "Get GitHub repository information"
                }
            ],
            "installation": {
                "cli": "claude mcp add --transport http codebase-kg https://neuroweave-1083h2gf3-info-quadquetechs-projects.vercel.app",
                "requirements": ["GitHub Token (optional for better rate limits)"]
            }
        }
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response_data, indent=2).encode())

