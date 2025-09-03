# Neuro-Weave Knowledge Graph - MCP Server

🧠 **Advanced MCP Server for Codebase Knowledge Graph Analysis & Interactive Visualization**

A powerful Model Context Protocol (MCP) server that provides comprehensive codebase analysis and interactive knowledge graph generation capabilities for Claude Code CLI.

## 🚀 Quick Remote Installation

**No local setup required!** Add this MCP server to your Claude Code CLI remotely:

```bash
claude mcp add --transport http neuro-weave-kg https://neuro-weave-knowledge-graph.vercel.app/api/mcp
```

Verify installation:
```bash
claude mcp list
```

You should see: `neuro-weave-kg: ✓ Connected`

## 🛠️ Available Tools

### Remote Tools (HTTP Transport)
- **`analyze_github_repo`** - Analyze GitHub repository structure and metadata via GitHub API
- **`get_repo_info`** - Get basic information about a GitHub repository

### Enhanced Local Tools (STDIO Transport)
For advanced analysis with interactive visualizations, use local installation:
- **`analyze_codebase_enhanced`** - Deep ecological analysis with pattern detection
- **`generate_codebase_graph`** - Interactive knowledge graph generation

## 📋 Features

### 🌐 Remote Serverless Mode
- Zero local setup required
- Hosted on Vercel for 99.9% uptime
- GitHub API integration for repository analysis
- MCP protocol 2025-06-18 compatible

### 🔬 Enhanced Local Mode  
- Interactive HTML knowledge graphs
- Design pattern detection
- Semantic clustering
- Cross-cutting concern analysis
- Multi-dimensional relationship mapping

## 🏗️ Installation Options

### Option 1: Remote Installation (Recommended)
```bash
# One command - no dependencies
claude mcp add --transport http neuro-weave-kg https://neuro-weave-knowledge-graph.vercel.app/api/mcp
```

### Option 2: Local Installation (Advanced Features)
```bash
# Clone and setup locally for enhanced features
git clone https://github.com/mhmalvi/neuro-weave-knowledge-graph.git
cd neuro-weave-knowledge-graph

# Install dependencies
pip install -r requirements.txt

# Add local MCP server
claude mcp add --transport stdio codebase-kg python api/mcp_stdio_server.py
```

## 📝 Usage Examples

### Analyze Any GitHub Repository
```bash
# In Claude Code CLI, simply ask:
"Analyze this GitHub repository: https://github.com/microsoft/vscode"
"What's the structure of the React repository?"
"Get information about the TensorFlow project"
```

The MCP server will automatically use the appropriate tools to provide detailed analysis.

### Enhanced Local Analysis
With local installation, you can analyze any codebase:
```bash
"Analyze this codebase and create a knowledge graph"
"Generate an interactive visualization of the project structure"
```

## 🔧 Technical Details

- **Protocol**: MCP 2025-06-18
- **Transports**: HTTP (remote) + STDIO (local)  
- **Languages**: Python
- **Deployment**: Vercel (serverless)
- **Dependencies**: Minimal for remote, enhanced for local

## 📊 Supported Analysis Types

### Remote Analysis
- Repository metadata and statistics
- Language detection and file counts
- License and contributor information
- Stars, forks, and activity metrics

### Local Enhanced Analysis
- File structure and dependency mapping
- Class and function relationship graphs
- Design pattern recognition
- Semantic code clustering
- Interactive multi-dimensional visualizations

## 🗑️ Removal

Remove remote MCP server:
```bash
claude mcp remove neuro-weave-kg
```

Remove local MCP server:
```bash
claude mcp remove codebase-kg
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 About

This MCP server transforms how developers analyze and understand codebases by providing both lightweight remote analysis and comprehensive local visualization capabilities through the Model Context Protocol.

Perfect for:
- 🔍 Quick repository analysis
- 📈 Project structure understanding  
- 🧬 Complex codebase exploration
- 🎯 Architecture documentation
- 🚀 Developer productivity enhancement

---

**Ready to explore code like never before?** 

🌐 **Remote**: `claude mcp add --transport http neuro-weave-kg https://neuro-weave-knowledge-graph.vercel.app/api/mcp`

🔬 **Local**: Clone this repo for enhanced features

🤖 Generated with [Claude Code](https://claude.ai/code)