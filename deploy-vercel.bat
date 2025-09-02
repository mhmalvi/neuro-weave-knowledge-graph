@echo off
REM Deploy to Vercel script

echo 🚀 Deploying NeuroWeave MCP Server to Vercel...

REM Check if Vercel CLI is installed
where vercel >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Vercel CLI not found. Installing...
    npm install -g vercel
)

REM Set environment variables
echo 🔧 Setting up environment variables...
echo Please add these environment variables in Vercel dashboard:
echo 1. OPENAI_API_KEY (optional - for enhanced features)
echo 2. GITHUB_TOKEN (optional - for better API rate limits)

REM Deploy to Vercel
echo 📦 Deploying to Vercel...
vercel --prod

echo.
echo 🎉 Deployment complete!
echo.
echo 📝 Your MCP server is now available at: https://your-project.vercel.app
echo.
echo 🔧 To use with Claude Code CLI:
echo claude mcp add --transport http codebase-kg https://your-project.vercel.app
echo.
pause
