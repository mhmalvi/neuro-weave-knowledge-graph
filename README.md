# 🧠 NeuroWeave Knowledge Graph
### *Advanced MCP Server for Codebase Analysis & Interactive Visualization*

A comprehensive Model Context Protocol (MCP) server that analyzes codebases and generates interactive knowledge graph visualizations, featuring multi-language support, neural-themed styling, and seamless GitHub integration.

## 🚀 Key Features

### 🔍 **Multi-Language Codebase Analysis**
- **Python**: Full AST parsing for classes, functions, imports
- **JavaScript/TypeScript**: Function and class detection, import analysis  
- **Java**: Class and method extraction, import mapping
- **C++, C#, Go, Rust**: Basic structural analysis

### 🎨 **Interactive Knowledge Graphs**
- **Neural-themed visualizations** with cyberpunk aesthetics
- **Force-directed layouts** with physics simulation
- **Real-time interaction** with zoom, pan, and hover details
- **Hierarchical relationships** between files, classes, functions

### 🌐 **GitHub Integration**
- **Repository cloning** and analysis
- **GitHub API integration** for metadata
- **Automatic updates** for existing repositories

### 📊 **MCP Server Tools**
- `analyze_codebase` - Local codebase analysis
- `analyze_github_repo` - GitHub repository analysis
- `generate_codebase_graph` - Interactive visualizations
- `get_repo_info` - Repository metadata extraction

## Installation

### 🔧 System Requirements

- Python 3.8+ (Neural Runtime Environment)
- OpenAI API Key (Cognitive Access Token)

### 🧬 Neural Dependencies

The NeuroWeave system requires the following cognitive modules:

- langchain (>= 0.1.0): Core Neural Language Framework
- langchain-experimental (>= 0.0.45): Advanced Cognitive Modules
- langchain-openai (>= 0.1.0): OpenAI Neural Interface
- python-dotenv (>= 1.0.0): Environment Neural Configuration
- pyvis (>= 0.3.2): Synaptic Visualization Engine
- streamlit (>= 1.32.0): Neural Web Interface

Initialize all neural dependencies using the cognitive requirements manifest:

```bash
pip install -r requirements.txt
```

### 🔧 Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/mhmalvi/neuro-weave-knowledge-graph.git
   cd neuro-weave-knowledge-graph
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables in `.env`:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   GITHUB_TOKEN=your_github_token_here  # Optional
   ```

## 🚀 Usage

### Streamlit Web Interface
```bash
streamlit run app.py
```
Opens the web interface at http://localhost:8501

### MCP Server Integration

#### Claude Desktop Configuration
Add to `claude_desktop_config.json`:
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

#### Claude Code Integration
```bash
claude mcp add codebase-knowledge-graph python mcp_server.py
```

## 🎯 How It Works

### Web Interface Usage
1. **Input Selection**: Choose between file upload or direct text input
2. **Data Processing**: Upload code files or paste text directly
3. **Generate Visualization**: Click "Generate Knowledge Graph"
4. **Explore Results**: Navigate the interactive visualization:
   - **Drag nodes** to rearrange the layout
   - **Hover** for detailed information
   - **Zoom and pan** to explore different areas
   - **Filter** nodes by type or relationship

### MCP Tools Usage
Ask Claude to:
- "Analyze this codebase"
- "Create a knowledge graph for my project"  
- "Show me the structure of [GitHub repo URL]"
- "Generate a visualization of the dependencies"

## 🛠️ Architecture

The system uses:
1. **AST Parsing**: Extract structural information from source code
2. **Relationship Mapping**: Identify imports, inheritance, and dependencies
3. **Graph Generation**: Build interactive network visualizations
4. **MCP Integration**: Provide tools for AI assistant integration

## License

This project is licensed under the MIT License - a permissive open source license that allows for free use, modification, and distribution of the software.

For more details, see the [MIT License](https://opensource.org/licenses/MIT) documentation.
