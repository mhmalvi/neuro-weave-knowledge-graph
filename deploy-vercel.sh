#!/bin/bash
# Deploy to Vercel script

echo "🚀 Deploying NeuroWeave MCP Server to Vercel..."

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

# Set environment variables
echo "🔧 Setting up environment variables..."
echo "Please add these environment variables in Vercel dashboard:"
echo "1. OPENAI_API_KEY (optional - for enhanced features)"
echo "2. GITHUB_TOKEN (optional - for better API rate limits)"

# Deploy to Vercel
echo "📦 Deploying to Vercel..."
vercel --prod

echo ""
echo "🎉 Deployment complete!"
echo ""
echo "📝 Your MCP server is now available at: https://your-project.vercel.app"
echo ""
echo "🔧 To use with Claude Code CLI:"
echo "claude mcp add --transport http codebase-kg https://your-project.vercel.app"
echo ""
