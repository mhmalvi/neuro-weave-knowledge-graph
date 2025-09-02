#!/bin/bash
# NeuroWeave Knowledge Graph MCP Server Installation Script

echo "🧠 NeuroWeave Knowledge Graph - MCP Server Installation"
echo "================================================="

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check Python version
python_version=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python version: $python_version"

# Install dependencies
echo "📦 Installing MCP server dependencies..."
pip install -r requirements-mcp.txt

# Check if .env exists
if [ ! -f .env ]; then
    echo "📋 Creating environment file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your API keys"
fi

# Add to Claude Code
echo "🔧 Adding MCP server to Claude Code CLI..."
claude mcp add codebase-knowledge-graph python "$(pwd)/mcp_server.py"

echo ""
echo "🎉 Installation complete!"
echo ""
echo "📝 Next steps:"
echo "1. Edit .env file and add your OpenAI API key"
echo "2. Optionally add your GitHub token for better rate limits"
echo "3. Start using: ask Claude to 'analyze this codebase'"
echo ""
