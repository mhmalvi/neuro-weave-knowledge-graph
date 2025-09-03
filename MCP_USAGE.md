# 🧠 NeuroWeave Knowledge Graph MCP Server - Complete Usage Guide

## ✅ **Connection Status**
```
codebase-kg: python api/mcp_stdio_simple.py - ✓ Connected
```

## 🛠️ **Complete Tool Suite**

### 1. **🔍 analyze_codebase** - *Local Directory Analysis*
**Description**: Deep analysis of local codebase with AST parsing and multi-language support

**Usage**:
```bash
# Claude Code CLI:
"Analyze this codebase"
"Analyze the ./src directory"  
"Show me the structure of my project"
```

**Parameters**:
- `path` (required): Local directory path to analyze

**Features**:
- **Multi-language support**: Python, JavaScript, TypeScript, Java, C++, Go, Rust, Ruby, PHP
- **AST parsing** for Python files (classes, functions, imports with line numbers)
- **File metrics**: Total files, lines of code, file type breakdown
- **Smart filtering**: Ignores .git, node_modules, __pycache__, etc.

**Example Output**:
```
📁 **Codebase Analysis Complete!**

🗂️ **Path:** ./api
📊 **Files:** 5 files
📝 **Lines:** 1,245 lines of code

🏗️ **Structure:**
• **Classes:** 5
• **Functions:** 18
• **Imports:** 35

📂 **File Types:**
• **.py**: 5 files

✅ **Local codebase analysis complete!**
```

### 2. **🌐 analyze_github_repo** - *GitHub Repository Analysis*
**Description**: Advanced GitHub repository analysis with optional cloning for deep inspection

**Usage**:
```bash
# Basic GitHub API analysis:
"Analyze https://github.com/microsoft/vscode"

# Extended analysis with cloning:
"Clone and analyze the React repository with detailed inspection"
```

**Parameters**:
- `repo_url` (required): GitHub repository URL
- `clone_for_analysis` (optional): Set to `true` for extended analysis with git clone

**Features**:
- **GitHub API integration** with authentication support
- **Optional repository cloning** for file-level analysis
- **Repository metrics**: Stars, forks, language, size
- **Extended analysis**: File counts, language breakdown when cloned
- **Intelligent error handling**: Fallback to API-only if clone fails

**Example Output**:
```
🔍 **GitHub Repository Analysis (with Cloning)**

🌐 **Repository:** vscode
⭐ **Stars:** 176341
🍴 **Forks:** 34749
📝 **Language:** TypeScript
📈 **Size:** 1062973 KB

📁 **Cloned Analysis:**
• **Total Files:** 12,547
• **Python Files:** 23
• **Clone Status:** ✅ Successfully cloned and analyzed

✅ **Extended analysis complete via GitHub API + Git Clone!**
```

### 3. **🕸️ generate_codebase_graph** - *Knowledge Graph Visualization*
**Description**: Generate beautiful ASCII knowledge graph visualizations of code structure

**Usage**:
```bash
# Generate visualization:
"Create a knowledge graph for this project"
"Generate a visualization of the ./src directory"
"Show me the code relationships in my API folder"
```

**Parameters**:
- `path` (required): Directory path to visualize

**Features**:
- **Hierarchical visualization** showing file → class → function relationships
- **Import mapping** showing dependencies between modules
- **Smart truncation** for large codebases (shows top items + count)
- **ASCII art styling** with emojis and tree structure
- **Summary statistics** at the bottom

**Example Output**:
```
🕸️  **CODEBASE KNOWLEDGE GRAPH**
==================================================

📁 **mcp.py**
  └─ 🏛️  Classes (2)
      ├─ MCPJsonRpcError
      ├─ handler
  └─ ⚙️  Functions (9)
      ├─ create_json_rpc_response
      ├─ create_json_rpc_error  
      ├─ analyze_github_repo
      └─ ... and 6 more
  └─ 📦 Imports (7)
      ├─ requests
      ├─ typing
      └─ ... and 5 more

📊 **GRAPH STATISTICS**
==============================
📁 Files: 5
🏛️  Classes: 5
⚙️  Functions: 18
📦 Import Statements: 25

✅ **Knowledge graph generated successfully!**
```

### 4. **📊 get_repo_info** - *Raw Repository Data*
**Description**: Get complete JSON data from GitHub API for programmatic use

**Usage**:
```bash
# Get raw technical data:
"Get detailed repository info for https://github.com/anthropics/claude-code"
"I need the GitHub API response for the Vue.js repository"
```

**Parameters**:
- `repo_url` (required): GitHub repository URL

**Features**:
- **Complete GitHub API response** with all metadata
- **Formatted JSON output** for easy reading
- **Comprehensive data**: Repository ID, creation date, license, custom properties, etc.

### 5. **🧪 echo_test** - *Connection Testing*
**Description**: Simple test tool to verify MCP server functionality

**Usage**:
```bash
# Test connection:
"Echo test with message 'Hello World'"
"Test the MCP server connectivity"
```

**Parameters**:
- `message` (required): Text message to echo back

## 🚀 **How to Use**

### **In Claude Code CLI**:
Simply use natural language to invoke the tools:

```bash
# Repository analysis
"Can you analyze the React repository on GitHub?"

# Get detailed info
"I need the raw JSON data for the Vue.js repository"

# Test connection  
"Test the MCP server with a hello message"
```

### **Direct JSON-RPC Testing** (for debugging):
```bash
# Test analyze_github_repo
echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"analyze_github_repo","arguments":{"repo_url":"https://github.com/facebook/react"}}}' | python api/mcp_stdio_simple.py

# Test get_repo_info  
echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_repo_info","arguments":{"repo_url":"https://github.com/vuejs/vue"}}}' | python api/mcp_stdio_simple.py

# List all tools
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | python api/mcp_stdio_simple.py
```

## ⚙️ **Configuration**

### **GitHub Token** (Optional but recommended):
Set `GITHUB_TOKEN` environment variable for higher API rate limits:
```bash
# Windows
set GITHUB_TOKEN=your_token_here

# Linux/Mac  
export GITHUB_TOKEN=your_token_here
```

### **MCP Server Configuration**:
```json
// Located in: C:\Users\AAA Technology\.claude.json
{
  "codebase-kg": {
    "transport": "stdio",
    "command": "python",
    "args": ["api/mcp_stdio_simple.py"]
  }
}
```

## 🔧 **Technical Details**

- **Transport**: STDIO (fastest, most reliable for CLI)
- **Protocol**: JSON-RPC 2.0 MCP compliance
- **GitHub API**: Uses GitHub REST API v4
- **Rate Limits**: 60 requests/hour (unauthenticated), 5000/hour (with token)
- **Timeout**: 10 seconds per API request
- **Dependencies**: `requests`, `urllib.parse`, `os` (lazy loaded)

## 🎯 **Use Cases**

1. **Repository Research**: Quick analysis of open source projects
2. **Competitive Analysis**: Compare repository metrics
3. **Due Diligence**: Get detailed repository information
4. **Development Planning**: Understand project scope and activity
5. **API Integration**: Access raw GitHub data for custom workflows

## ✅ **Success Indicators**

- MCP server shows "✓ Connected" in `claude mcp list`
- Tools respond within 10 seconds
- GitHub API returns valid JSON data
- Natural language commands work in Claude Code CLI

---

**🤖 Generated with Claude Code MCP Server - Working as of Sept 2025**