# Import necessary modules
import streamlit as st
import streamlit.components.v1 as components  # For embedding custom HTML
from generate_knowledge_graph import generate_knowledge_graph
from mcp_server import GitHubAnalyzer, CodebaseAnalyzer
from codebase_visualizer import CodebaseVisualizer
import os
import re
from urllib.parse import urlparse

# GitHub Analysis Functions
@st.cache_data(ttl=3600)  # Cache for 1 hour
def validate_github_url(url: str) -> dict:
    """Validate GitHub URL and return repository info"""
    try:
        # Clean URL
        url = url.strip().rstrip('/')
        if url.endswith('.git'):
            url = url[:-4]
            
        # Parse URL
        parsed = urlparse(url)
        if 'github.com' not in parsed.netloc.lower():
            return {"valid": False, "error": "Only GitHub repositories are supported"}
        
        # Extract owner and repo
        path_parts = parsed.path.strip('/').split('/')
        if len(path_parts) < 2:
            return {"valid": False, "error": "Invalid GitHub repository URL"}
        
        owner, repo = path_parts[0], path_parts[1]
        
        return {
            "valid": True,
            "owner": owner,
            "repo": repo,
            "full_name": f"{owner}/{repo}",
            "url": url
        }
    except Exception as e:
        return {"valid": False, "error": f"Invalid URL format: {str(e)}"}

def analyze_github_repository(repo_url: str, progress_placeholder):
    """Complete GitHub repository analysis pipeline"""
    try:
        # Initialize analyzers
        github_analyzer = GitHubAnalyzer()
        codebase_analyzer = CodebaseAnalyzer()
        visualizer = CodebaseVisualizer()
        
        # Stage 1: Validate URL
        progress_placeholder.markdown("🔍 **Validating Repository URL...**")
        url_info = validate_github_url(repo_url)
        if not url_info["valid"]:
            return None, None, url_info["error"]
        
        # Stage 2: Get repository info (optional, for display)
        progress_placeholder.markdown("📊 **Fetching Repository Information...**")
        try:
            repo_info = github_analyzer.get_repo_info(repo_url)
        except:
            repo_info = {"name": url_info["repo"], "full_name": url_info["full_name"]}
        
        # Stage 3: Clone repository
        progress_placeholder.markdown("📥 **Cloning Repository...**")
        target_dir = f"./temp_repos/{url_info['repo']}"
        local_path = github_analyzer.clone_or_update_repo(repo_url, target_dir)
        
        # Stage 4: Analyze codebase
        progress_placeholder.markdown("🧠 **Analyzing Codebase Structure...**")
        analysis = codebase_analyzer.analyze_codebase(local_path)
        analysis['repo_info'] = repo_info
        analysis['repo_url'] = repo_url
        
        # Stage 5: Generate visualization
        progress_placeholder.markdown("🎨 **Generating Knowledge Graph...**")
        output_file = f"{url_info['repo']}_analysis.html"
        network = visualizer.create_codebase_graph(analysis, output_file)
        
        progress_placeholder.markdown("✨ **Analysis Complete!**")
        return analysis, network, output_file
        
    except Exception as e:
        error_msg = f"Analysis failed: {str(e)}"
        progress_placeholder.markdown(f"❌ **{error_msg}**")
        return None, None, error_msg

# Set up Streamlit page configuration
st.set_page_config(
    page_title="🧠 NeuroWeave AI - Neural Knowledge Architecture",
    page_icon="🧠", 
    layout="wide",  # Use wide layout for better graph display
    initial_sidebar_state="expanded", 
    menu_items={
        'Get Help': 'https://github.com/neuroweave-ai',
        'Report a bug': "https://github.com/neuroweave-ai/issues",
        'About': "# NeuroWeave AI\n### Neural Knowledge Architecture System\nAdvanced AI-powered cognitive mapping platform"
    }
)

# Custom CSS for futuristic neural theme
st.markdown("""
<style>
    /* Import futuristic fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');
    
    /* Main app styling */
    .main .block-container {
        padding-top: 2rem;
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
        border-radius: 15px;
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.3);
    }
    
    /* Title styling */
    h1 {
        font-family: 'Orbitron', monospace !important;
        background: linear-gradient(45deg, #00ffff, #0080ff, #8000ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        text-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
        animation: pulse 2s ease-in-out infinite alternate;
    }
    
    /* Subtitle styling */
    h3 {
        font-family: 'Rajdhani', sans-serif !important;
        color: #00ffff !important;
        text-align: center;
        font-style: italic;
        margin-bottom: 2rem !important;
        font-size: 1.5rem !important;
        opacity: 0.8;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 2px solid #00ffff;
    }
    
    /* Sidebar title */
    .css-1d391kg h1 {
        color: #00ffff !important;
        font-family: 'Orbitron', monospace !important;
        font-size: 1.5rem !important;
        text-shadow: 0 0 10px rgba(0, 255, 255, 0.8);
    }
    
    /* Radio buttons */
    .stRadio > div {
        background: rgba(0, 255, 255, 0.1);
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid rgba(0, 255, 255, 0.3);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(45deg, #00ffff, #0080ff) !important;
        color: #000 !important;
        border: none !important;
        border-radius: 25px !important;
        font-family: 'Orbitron', monospace !important;
        font-weight: 600 !important;
        padding: 0.75rem 2rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.4) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 25px rgba(0, 255, 255, 0.6) !important;
        background: linear-gradient(45deg, #0080ff, #8000ff) !important;
    }
    
    /* Text areas */
    .stTextArea textarea {
        background: rgba(0, 0, 0, 0.8) !important;
        border: 1px solid #00ffff !important;
        border-radius: 10px !important;
        color: #00ffff !important;
        font-family: 'Rajdhani', monospace !important;
    }
    
    /* File uploader */
    .stFileUploader {
        background: rgba(0, 255, 255, 0.1);
        border: 1px dashed #00ffff;
        border-radius: 10px;
        padding: 1rem;
    }
    
    /* Success messages */
    .stSuccess {
        background: rgba(0, 255, 0, 0.1) !important;
        border: 1px solid #00ff00 !important;
        color: #00ff00 !important;
        border-radius: 10px !important;
        font-family: 'Rajdhani', sans-serif !important;
    }
    
    /* Spinner */
    .stSpinner {
        color: #00ffff !important;
    }
    
    /* Pulse animation */
    @keyframes pulse {
        from { opacity: 0.8; }
        to { opacity: 1; }
    }
    
    /* Neural grid background */
    body {
        background-image: 
            radial-gradient(circle at 20% 20%, rgba(0, 255, 255, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(128, 0, 255, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 40% 60%, rgba(0, 128, 255, 0.1) 0%, transparent 50%);
    }
    
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Neural header with animated title
st.markdown("""
<div style="text-align: center; margin: 2rem 0;">
    <h1>🧠 NeuroWeave AI</h1>
    <h3><i>Neural Knowledge Architecture System</i></h3>
    <div style="background: linear-gradient(90deg, transparent, #00ffff, transparent); height: 1px; margin: 1rem auto; width: 60%;"></div>
    <p style="color: #00ffff; font-family: 'Rajdhani', sans-serif; opacity: 0.8; font-size: 1.1rem;">
        🚀 Advanced AI-powered cognitive mapping platform<br>
        💡 Transform text into interactive neural networks
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar section for neural input method
st.sidebar.markdown("""
<div style="text-align: center; margin-bottom: 1.5rem;">
    <h2 style="color: #00ffff; font-family: 'Orbitron', monospace; font-size: 1.5rem;">
        🔬 Neural Input Stream
    </h2>
    <div style="background: linear-gradient(90deg, transparent, #00ffff, transparent); height: 1px; margin: 0.5rem auto; width: 80%;"></div>
</div>
""", unsafe_allow_html=True)

input_method = st.sidebar.radio(
    "🧬 Select cognitive input method:",
    ["📄 Upload Neural Data", "⌨️ Direct Input", "🌐 GitHub Repository"],  # Options for uploading a file, manually inputting text, or analyzing GitHub repo
)

# Case 1: User chooses to upload a .txt file
if input_method == "📄 Upload Neural Data":
    # File uploader widget in the sidebar
    st.sidebar.markdown("#### 📊 Neural Data Upload")
    uploaded_file = st.sidebar.file_uploader(label="📁 Upload Neural Data File", type=["txt"], help="Upload .txt files containing data for neural analysis")
    
    if uploaded_file is not None:
        # Read the uploaded file content and decode it as UTF-8 text
        text = uploaded_file.read().decode("utf-8")
 
        # Neural processing section
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🚀 Neural Processing")
        if st.sidebar.button("⚡ Generate Neural Map", key="upload_btn"):
            with st.spinner("🧠 Synthesizing neural pathways..."):
                # Call the function to generate the graph from the text
                net = generate_knowledge_graph(text)
                st.success("✨ Neural map synthesized successfully!")
                
                # Export neural map to visualization format
                output_file = "neural_map.html"
                net.save_graph(output_file) 

                # Display neural architecture visualization
                st.markdown("### 🧠 Neural Architecture Visualization")
                st.markdown("*Interactive synaptic network mapping*")
                
                # Render neural visualization interface
                HtmlFile = open(output_file, 'r', encoding='utf-8')
                components.html(HtmlFile.read(), height=1000)

# Case 2: User chooses direct neural input
elif input_method == "⌨️ Direct Input":
    # Text area for direct cognitive input
    st.sidebar.markdown("#### 🧬 Direct Cognitive Input")
    text = st.sidebar.text_area("🧠 Input cognitive data", height=300, placeholder="Enter your text data for neural analysis...")

    if text:  # Check if the text area is not empty
        # Neural processing section
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🚀 Neural Processing")
        if st.sidebar.button("⚡ Generate Neural Map", key="input_btn"):
            with st.spinner("🧠 Synthesizing neural pathways..."):
                # Call the function to generate the graph from the input text
                net = generate_knowledge_graph(text)
                st.success("✨ Neural map synthesized successfully!")
                
                # Export neural map to visualization format
                output_file = "neural_map.html"
                net.save_graph(output_file) 

                # Display neural architecture visualization
                st.markdown("### 🧠 Neural Architecture Visualization")
                st.markdown("*Interactive synaptic network mapping*")
                
                # Render neural visualization interface
                HtmlFile = open(output_file, 'r', encoding='utf-8')
                components.html(HtmlFile.read(), height=1000)

# Case 3: User chooses GitHub repository analysis
else:
    # GitHub repository input
    st.sidebar.markdown("#### 🔗 Repository Analysis")
    repo_url = st.sidebar.text_input(
        "🌐 Repository URL:", 
        placeholder="https://github.com/user/repo",
        help="Enter a GitHub repository URL for codebase analysis"
    )
    
    if repo_url:
        # Validate URL in real-time
        url_info = validate_github_url(repo_url)
        
        if url_info["valid"]:
            st.sidebar.success(f"✅ Valid GitHub URL: **{url_info['full_name']}**")
            
            # Neural processing section
            st.sidebar.markdown("---")
            st.sidebar.markdown("### 🚀 Neural Processing")
            if st.sidebar.button("🔍 Analyze Repository", key="github_btn"):
                
                # Create progress placeholder
                progress_placeholder = st.sidebar.empty()
                
                # Run analysis
                analysis, network, result = analyze_github_repository(repo_url, progress_placeholder)
                
                if analysis and network:
                    # Success - display results
                    st.success("✨ Repository analysis complete!")
                    
                    # Display repository metrics
                    metrics = analysis.get('metrics', {})
                    repo_name = analysis.get('repo_info', {}).get('name', 'Repository')
                    
                    st.markdown(f"### 🧠 {repo_name} - Codebase Architecture")
                    
                    # Metrics display
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("📁 Files", metrics.get('total_files', 0))
                    with col2:
                        st.metric("🏗️ Classes", metrics.get('total_classes', 0))
                    with col3:
                        st.metric("⚡ Functions", metrics.get('total_functions', 0))
                    with col4:
                        st.metric("📦 Dependencies", metrics.get('total_imports', 0))
                    
                    st.markdown("*Interactive codebase architecture mapping*")
                    
                    # Render codebase visualization
                    HtmlFile = open(result, 'r', encoding='utf-8')
                    components.html(HtmlFile.read(), height=1000)
                    
                    # Download link
                    st.markdown(f"📥 **Download:** [Open {result} in new tab](./{result})")
                    
                else:
                    # Error occurred
                    st.error(f"❌ **Analysis Failed**\n\n{result}")
                    progress_placeholder.empty()
        else:
            st.sidebar.error(f"❌ {url_info['error']}")
    else:
        st.sidebar.info("💡 Enter a GitHub repository URL to begin analysis")

# Add neural footer at the end
st.markdown("---")
st.markdown("""
<div style="text-align: center; margin-top: 3rem; padding: 2rem; background: linear-gradient(135deg, rgba(0, 255, 255, 0.1) 0%, rgba(128, 0, 255, 0.1) 100%); border-radius: 15px; border: 1px solid rgba(0, 255, 255, 0.3);">
    <h4 style="color: #00ffff; font-family: 'Orbitron', monospace; margin-bottom: 1rem;">
        🧠 NeuroWeave AI - Neural Knowledge Architecture
    </h4>
    <p style="color: #00ffff; font-family: 'Rajdhani', sans-serif; opacity: 0.8; margin-bottom: 1rem;">
        🚀 Transforming text into interactive neural networks using advanced AI<br>
        💡 Powered by GPT-4o and LangChain experimental graph transformers
    </p>
    <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 1rem;">
        <div style="color: #00ffff; opacity: 0.7; font-family: 'Rajdhani', sans-serif;">
            ⚡ Neural Processing Engine
        </div>
        <div style="color: #00ffff; opacity: 0.7; font-family: 'Rajdhani', sans-serif;">
            🔬 Cognitive Analysis
        </div>
        <div style="color: #00ffff; opacity: 0.7; font-family: 'Rajdhani', sans-serif;">
            🌐 Synaptic Visualization
        </div>
    </div>
</div>
""", unsafe_allow_html=True)