# 🧠 Codebase Knowledge Graph MCP Server

A powerful Model Context Protocol (MCP) server that analyzes codebases and generates interactive knowledge graph visualizations showing code structure, dependencies, and relationships.

![Codebase Visualization](https://img.shields.io/badge/Visualization-Interactive%20Knowledge%20Graphs-00ffff)
![MCP](https://img.shields.io/badge/MCP-Server-ff00ff)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)

## ✨ Features

### 🔍 **Multi-Language Codebase Analysis**
- **Python**: Full AST parsing for classes, functions, imports
- **JavaScript/TypeScript**: Function and class detection, import analysis
- **Java**: Class and method extraction, import mapping
- **And more**: Support for C++, C#, Go, Rust

### 🎨 **Interactive Knowledge Graphs**
- **Neural-themed visualizations** with cyberpunk aesthetics
- **Force-directed layouts** with physics simulation
- **Hierarchical relationships** between files, classes, functions
- **Dependency mapping** showing import relationships
- **Real-time interaction** with zoom, pan, and hover details

### 🌐 **GitHub Integration**
- **Repository cloning** and analysis
- **GitHub API integration** for repository metadata
- **Automatic updates** for existing local repositories

### 📊 **Comprehensive Metrics**
- File count and structure analysis
- Class and function distribution
- Import dependency mapping
- Code complexity visualization

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- OpenAI API key (for enhanced analysis)
- Git (for GitHub integration)
- Optional: GitHub Personal Access Token

### Setup Steps

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up environment variables:**
Create a `.env` file:
```env
OPENAI_API_KEY=your_openai_api_key_here
GITHUB_TOKEN=your_github_token_here  # Optional, for private repos
```

3. **Install the MCP server:**
```bash
pip install -e .
```

## 🔧 MCP Configuration

Add this to your Claude Desktop configuration:

### macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
### Windows: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "codebase-knowledge-graph": {
      "command": "python",
      "args": ["path/to/mcp_server.py"],
      "env": {
        "OPENAI_API_KEY": "your_api_key",
        "GITHUB_TOKEN": "your_github_token"
      }
    }
  }
}
```

## 🛠️ Available Tools

### 1. `analyze_codebase`
Analyzes a local codebase directory.

**Parameters:**
- `path`: Directory path to analyze

**Example:**
```json
{
  "path": "/path/to/your/project"
}
```

### 2. `analyze_github_repo`
Clones and analyzes a GitHub repository.

**Parameters:**
- `repo_url`: GitHub repository URL
- `target_dir`: Optional local directory path

**Example:**
```json
{
  "repo_url": "https://github.com/user/repo",
  "target_dir": "./repos/my-project"
}
```

### 3. `generate_codebase_graph`
Creates an interactive knowledge graph visualization.

**Parameters:**
- `analysis_data`: Output from analyze_codebase or analyze_github_repo
- `output_file`: Optional HTML output file path

**Example:**
```json
{
  "analysis_data": { ... },
  "output_file": "my_codebase_graph.html"
}
```

### 4. `get_repo_info`
Fetches GitHub repository metadata.

**Parameters:**
- `repo_url`: GitHub repository URL

## 🎯 Usage Examples

### Analyzing a Local Project
```
User: "Analyze the codebase in /my/project and create a knowledge graph"

Claude will:
1. Use analyze_codebase tool on the directory
2. Generate an interactive visualization with generate_codebase_graph
3. Show metrics and structure insights
```

### Analyzing a GitHub Repository
```
User: "Show me the architecture of https://github.com/user/awesome-project"

Claude will:
1. Use analyze_github_repo to clone and analyze
2. Generate a knowledge graph visualization
3. Provide insights about the codebase structure
```

### Understanding Code Relationships
```
User: "What are the main components and how do they connect in my React app?"

Claude will:
1. Analyze the codebase structure
2. Create a visual map showing components, imports, and relationships  
3. Highlight the architecture patterns used
```

## 🎨 Visualization Features

### Node Types & Colors
- 🔷 **Files** (Cyan squares): Source code files
- 🔺 **Classes** (Magenta triangles): Class definitions  
- 🟢 **Functions** (Green circles): Function definitions
- 💎 **Methods** (Yellow diamonds): Class methods
- ⭐ **Imports** (Orange stars): Import relationships
- 🔷 **Packages** (Purple hexagons): Package/module containers

### Interactive Features
- **Hover**: Detailed information about nodes and relationships
- **Drag**: Rearrange nodes to customize layout
- **Zoom**: Scale the view for better navigation
- **Filter**: Use built-in controls to focus on specific aspects
- **Physics**: Real-time force simulation for optimal layouts

### Enhanced Styling
- Neural grid background with pulse animations
- Cyberpunk color scheme with glowing effects
- Responsive design that works on all screen sizes
- Information panel with live metrics

## 🧪 Testing

Run the test suite to verify functionality:

```bash
python test_mcp.py
```

This will:
1. Analyze the current codebase
2. Generate test visualizations
3. Validate all MCP tools

## 📁 Project Structure

```
knowledge-graph-llms/
├── mcp_server.py           # Main MCP server implementation
├── codebase_visualizer.py  # Specialized codebase visualization
├── generate_knowledge_graph.py  # Original knowledge graph generator
├── app.py                  # Streamlit web interface
├── test_mcp.py            # Test suite
├── mcp_config.json        # MCP configuration template
├── pyproject.toml         # Package configuration
├── requirements.txt       # Dependencies
└── README.md             # Project documentation
```

## 🔍 Supported Languages

| Language | Classes | Functions | Imports | Inheritance |
|----------|---------|-----------|---------|-------------|
| Python | ✅ | ✅ | ✅ | ✅ |
| JavaScript | ✅ | ✅ | ✅ | ❌ |
| TypeScript | ✅ | ✅ | ✅ | ❌ |
| Java | ✅ | ✅ | ✅ | ❌ |
| C++ | 🔄 | 🔄 | 🔄 | ❌ |
| C# | 🔄 | 🔄 | 🔄 | ❌ |
| Go | 🔄 | 🔄 | 🔄 | ❌ |
| Rust | 🔄 | 🔄 | 🔄 | ❌ |

*Legend: ✅ Full support, 🔄 Basic support, ❌ Not yet supported*

## 🚀 Advanced Usage

### Custom Analysis Filters
The analyzer automatically skips common non-code directories:
- `node_modules`, `__pycache__`, `.git`
- `build`, `dist`, `target`
- Hidden directories starting with `.`

### GitHub API Rate Limits
- Public repositories: 60 requests/hour (no token)
- With GitHub token: 5,000 requests/hour
- Use personal access tokens for better limits

### Large Codebase Optimization
For large codebases (1000+ files):
1. The analyzer processes files in batches
2. Visualizations show only the most important relationships
3. Use filters to focus on specific subsystems

## 🛟 Troubleshooting

### Common Issues

**MCP Server Not Starting:**
- Check Python path in configuration
- Verify all dependencies are installed
- Ensure OpenAI API key is set

**Visualization Not Loading:**
- Check browser console for JavaScript errors
- Ensure HTML file was generated successfully
- Try opening in a different browser

**GitHub Integration Failing:**
- Verify repository URL format
- Check network connectivity
- Ensure GitHub token has proper permissions

**Large Repository Timeout:**
- Break analysis into smaller chunks
- Increase timeout settings
- Use local clones instead of fresh downloads

### Debug Mode
Enable debug logging by setting:
```python
logging.getLogger("codebase-kg-mcp").setLevel(logging.DEBUG)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

### Development Setup
```bash
git clone <repository>
cd knowledge-graph-llms
pip install -e .[dev]
python test_mcp.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♀️ Support

- 📧 **Email**: support@neuroweave-ai.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)

---

**Built with ❤️ by the NeuroWeave AI Team**

*Transform your codebase understanding with the power of interactive knowledge graphs!*