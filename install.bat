@echo off
REM NeuroWeave Knowledge Graph MCP Server Installation Script

echo 🧠 NeuroWeave Knowledge Graph - MCP Server Installation
echo =================================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Show Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do echo ✅ Python version: %%i

REM Install dependencies
echo 📦 Installing MCP server dependencies...
pip install -r requirements-mcp.txt

REM Check if .env exists
if not exist .env (
    echo 📋 Creating environment file from template...
    copy .env.example .env
    echo ⚠️  Please edit .env file and add your API keys
)

REM Add to Claude Code
echo 🔧 Adding MCP server to Claude Code CLI...
claude mcp add codebase-knowledge-graph python "%cd%\mcp_server.py"

echo.
echo 🎉 Installation complete!
echo.
echo 📝 Next steps:
echo 1. Edit .env file and add your OpenAI API key
echo 2. Optionally add your GitHub token for better rate limits
echo 3. Start using: ask Claude to 'analyze this codebase'
echo.
pause
