# Remote MCP Server Installation

## Quick Installation

To add this MCP server to your Claude Code CLI remotely (no local setup required):

```bash
claude mcp add --transport http neuro-weave-kg https://neuro-weave-knowledge-graph.vercel.app/api/mcp
```

## Verify Installation

Check that the server is connected:

```bash
claude mcp list
```

You should see:
```
neuro-weave-kg: https://neuro-weave-knowledge-graph.vercel.app/api/mcp (HTTP) - ✓ Connected
```

## Available Tools

Once installed, all 4 MCP tools will be available in Claude Code CLI:

### 1. `analyze_github_repo`
Analyze a GitHub repository structure and metadata via GitHub API

**Usage**: Automatically available when you ask Claude to analyze GitHub repositories

**Example**: "Analyze this GitHub repository: https://github.com/user/repo"

### 2. `get_repo_info` 
Get basic information about a GitHub repository

**Usage**: Automatically available when you ask Claude for GitHub repository information

### 3. `analyze_codebase_enhanced` 
Perform comprehensive enhanced analysis with pattern detection and semantic clustering (serverless version)

**Usage**: Automatically available for deep repository analysis

**Example**: "Perform enhanced analysis on this repository: https://github.com/facebook/react"

### 4. `generate_codebase_graph`
Generate interactive knowledge graph from GitHub repository data (serverless version)

**Usage**: Automatically available for visualization generation  

**Example**: "Create a knowledge graph visualization for this repository"

## Features

- 🌐 **Serverless**: Runs on Vercel, no local Python installation required
- 🔄 **Latest Protocol**: Uses MCP protocol version 2025-06-18
- 🚀 **GitHub Integration**: Direct GitHub API access for repository analysis  
- 📊 **Rich Analysis**: Repository metadata, stats, and structural insights
- 🔧 **Zero Setup**: Just one command to install and start using

## Requirements

- Claude Code CLI installed
- Internet connection (for Vercel-hosted server)

## Removal

To remove the MCP server:

```bash
claude mcp remove neuro-weave-kg
```

## Local Alternative

If you prefer running the MCP server locally with enhanced analysis capabilities, see the main README for local installation instructions.

---

🤖 This MCP server provides seamless GitHub repository analysis through Claude Code CLI without requiring any local setup.