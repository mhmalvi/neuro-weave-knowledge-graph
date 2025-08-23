from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from pyvis.network import Network

from dotenv import load_dotenv
import os
import asyncio


# Load the .env file
load_dotenv()
# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(temperature=0, model_name="gpt-4o")

graph_transformer = LLMGraphTransformer(llm=llm)


# Extract neural pathways from cognitive input
async def extract_graph_data(text):
    """
    Asynchronously extracts neural pathways from cognitive input using AI graph transformer.

    Args:
        text (str): Cognitive input text to be processed into neural format.

    Returns:
        list: A list of Neural GraphDocument objects containing synaptic nodes and pathways.
    """
    documents = [Document(page_content=text)]
    graph_documents = await graph_transformer.aconvert_to_graph_documents(documents)
    return graph_documents


def visualize_graph(graph_documents):
    """
    Renders neural architecture using PyVis quantum visualization based on extracted neural documents.

    Args:
        graph_documents (list): A list of Neural GraphDocument objects with synaptic nodes and pathways.

    Returns:
        pyvis.network.Network: The rendered neural network visualization object.
    """
    # Initialize neural visualization engine with cyberpunk theme
    net = Network(height="1200px", width="100%", directed=True,
                      notebook=False, bgcolor="#0a0a0a", font_color="#00ffff", 
                      filter_menu=True, cdn_resources='remote') 

    nodes = graph_documents[0].nodes
    relationships = graph_documents[0].relationships

    # Build lookup for valid nodes
    node_dict = {node.id: node for node in nodes}
    
    # Filter out invalid edges and collect valid node IDs
    valid_edges = []
    valid_node_ids = set()
    for rel in relationships:
        if rel.source.id in node_dict and rel.target.id in node_dict:
            valid_edges.append(rel)
            valid_node_ids.update([rel.source.id, rel.target.id])

    # Neural node type styling with cyberpunk colors
    node_styles = {
        'Person': {'color': '#00ffff', 'shape': 'dot', 'size': 25, 'borderWidth': 3, 'borderWidthSelected': 5},
        'Organization': {'color': '#ff00ff', 'shape': 'triangle', 'size': 20, 'borderWidth': 2},
        'Location': {'color': '#ffff00', 'shape': 'square', 'size': 18, 'borderWidth': 2},
        'Event': {'color': '#ff6600', 'shape': 'diamond', 'size': 22, 'borderWidth': 2},
        'Concept': {'color': '#00ff00', 'shape': 'ellipse', 'size': 20, 'borderWidth': 2},
        'Award': {'color': '#ff0080', 'shape': 'star', 'size': 24, 'borderWidth': 3},
        'ResearchField': {'color': '#8000ff', 'shape': 'hexagon', 'size': 20, 'borderWidth': 2},
        'default': {'color': '#00ccff', 'shape': 'dot', 'size': 18, 'borderWidth': 2}
    }

    # Add neural nodes with futuristic styling
    for node_id in valid_node_ids:
        node = node_dict[node_id]
        node_type = node.type if hasattr(node, 'type') else 'default'
        style = node_styles.get(node_type, node_styles['default'])
        
        try:
            net.add_node(
                node.id, 
                label=node.id,
                title=f"🧠 Neural Node: {node.id}\n🔬 Type: {node_type}\n⚡ Synaptic Entity",
                group=node_type,
                color={
                    'background': style['color'],
                    'border': '#ffffff',
                    'highlight': {'background': '#ffffff', 'border': style['color']},
                    'hover': {'background': style['color'], 'border': '#ffffff'}
                },
                shape=style['shape'],
                size=style['size'],
                borderWidth=style['borderWidth'],
                borderWidthSelected=style.get('borderWidthSelected', 4),
                font={'color': '#ffffff', 'size': 14, 'face': 'Orbitron, monospace', 'strokeWidth': 2, 'strokeColor': '#000000'},
                shadow={'enabled': True, 'color': style['color'], 'size': 10, 'x': 0, 'y': 0}
            )
        except:
            continue  # Skip node if error occurs

    # Add neural pathways (edges) with cyberpunk styling
    for rel in valid_edges:
        try:
            # Dynamic edge color based on relationship type
            edge_colors = {
                'works_at': '#00ffff',
                'located_in': '#ffff00', 
                'developed': '#00ff00',
                'contributed_to': '#ff00ff',
                'member_of': '#ff6600',
                'born_in': '#00ccff',
                'awarded': '#ff0080'
            }
            
            rel_type = rel.type.lower().replace(' ', '_')
            edge_color = edge_colors.get(rel_type, '#00ffff')
            
            net.add_edge(
                rel.source.id, 
                rel.target.id,
                label=f"⚡ {rel.type}",
                title=f"🧠 Neural Pathway: {rel.type}\n🔗 Synaptic Connection",
                color={'color': edge_color, 'highlight': '#ffffff', 'hover': '#ffffff', 'opacity': 0.8},
                width=3,
                length=200,
                font={'color': '#ffffff', 'size': 12, 'face': 'Rajdhani, sans-serif', 'strokeWidth': 1, 'strokeColor': '#000000'},
                shadow={'enabled': True, 'color': edge_color, 'size': 5, 'x': 0, 'y': 0},
                smooth={'enabled': True, 'type': 'curvedCW', 'roundness': 0.2},
                arrows={'to': {'enabled': True, 'scaleFactor': 1.5, 'type': 'arrow'}}
            )
        except:
            continue  # Skip edge if error occurs

    # Advanced neural physics and visualization configuration
    net.set_options("""
        {
            "physics": {
                "forceAtlas2Based": {
                    "gravitationalConstant": -150,
                    "centralGravity": 0.02,
                    "springLength": 250,
                    "springConstant": 0.06,
                    "damping": 0.4,
                    "avoidOverlap": 1
                },
                "maxVelocity": 30,
                "minVelocity": 0.5,
                "solver": "forceAtlas2Based",
                "timestep": 0.35,
                "adaptiveTimestep": true
            },
            "interaction": {
                "hover": true,
                "hoverConnectedEdges": true,
                "selectConnectedEdges": false,
                "tooltipDelay": 200,
                "zoomView": true,
                "dragView": true
            },
            "manipulation": {
                "enabled": false
            },
            "layout": {
                "improvedLayout": true,
                "randomSeed": 42
            }
        }
    """)

    output_file = "neural_map.html"
    try:
        # Save the basic network
        net.save_graph(output_file)
        
        # Read the generated HTML and enhance it with neural effects
        with open(output_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Inject custom neural CSS and effects
        neural_css = """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');
            
            body {
                background: #0a0a0a;
                overflow: hidden;
                font-family: 'Orbitron', monospace;
            }
            
            /* Neural grid background animation */
            body::before {
                content: '';
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-image: 
                    linear-gradient(rgba(0, 255, 255, 0.1) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(0, 255, 255, 0.1) 1px, transparent 1px),
                    radial-gradient(circle at 20% 20%, rgba(0, 255, 255, 0.2) 0%, transparent 50%),
                    radial-gradient(circle at 80% 80%, rgba(128, 0, 255, 0.2) 0%, transparent 50%);
                background-size: 50px 50px, 50px 50px, 100% 100%, 100% 100%;
                animation: neural-pulse 4s ease-in-out infinite alternate;
                pointer-events: none;
                z-index: -1;
            }
            
            @keyframes neural-pulse {
                0% { opacity: 0.3; }
                100% { opacity: 0.6; }
            }
            
            /* Enhanced vis-network styling */
            #mynetworkid {
                border: 2px solid #00ffff;
                border-radius: 15px;
                box-shadow: 
                    0 0 30px rgba(0, 255, 255, 0.5),
                    inset 0 0 30px rgba(0, 255, 255, 0.1);
                background: radial-gradient(circle at center, rgba(0, 0, 0, 0.9) 0%, rgba(10, 10, 10, 0.95) 100%);
            }
            
            /* Neural loading effect */
            .vis-loading-text {
                color: #00ffff !important;
                font-family: 'Orbitron', monospace !important;
                font-size: 18px !important;
                text-shadow: 0 0 10px #00ffff;
            }
            
            /* Filter menu styling */
            .vis-configuration-wrapper {
                background: rgba(0, 0, 0, 0.9) !important;
                border: 1px solid #00ffff !important;
                border-radius: 10px !important;
                backdrop-filter: blur(10px);
            }
            
            .vis-configuration-wrapper .vis-configuration {
                color: #00ffff !important;
                font-family: 'Rajdhani', sans-serif !important;
            }
            
            /* Tooltip enhancement */
            .vis-tooltip {
                background: rgba(0, 0, 0, 0.95) !important;
                border: 1px solid #00ffff !important;
                border-radius: 8px !important;
                color: #00ffff !important;
                font-family: 'Rajdhani', sans-serif !important;
                font-size: 14px !important;
                box-shadow: 0 0 20px rgba(0, 255, 255, 0.6) !important;
            }
            
            /* Custom scrollbar */
            ::-webkit-scrollbar {
                width: 8px;
            }
            
            ::-webkit-scrollbar-track {
                background: rgba(0, 0, 0, 0.5);
                border-radius: 4px;
            }
            
            ::-webkit-scrollbar-thumb {
                background: linear-gradient(45deg, #00ffff, #0080ff);
                border-radius: 4px;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: linear-gradient(45deg, #0080ff, #8000ff);
            }
        </style>
        
        <script>
            // Enhanced neural network effects
            document.addEventListener('DOMContentLoaded', function() {
                // Add neural glow effect to canvas
                const canvas = document.querySelector('canvas');
                if (canvas) {
                    canvas.style.filter = 'drop-shadow(0 0 10px rgba(0, 255, 255, 0.3))';
                }
                
                // Neural title overlay
                const titleDiv = document.createElement('div');
                titleDiv.innerHTML = `
                    <div style="position: absolute; top: 20px; left: 50%; transform: translateX(-50%); z-index: 1000; text-align: center;">
                        <h1 style="color: #00ffff; font-family: 'Orbitron', monospace; font-size: 2rem; margin: 0; text-shadow: 0 0 20px #00ffff; animation: neural-glow 2s ease-in-out infinite alternate;">
                            🧠 Neural Architecture Map
                        </h1>
                        <p style="color: #00ffff; font-family: 'Rajdhani', sans-serif; opacity: 0.8; margin: 5px 0 0 0;">
                            Interactive Synaptic Network Visualization
                        </p>
                    </div>
                `;
                document.body.appendChild(titleDiv);
                
                // Add neural glow animation
                const style = document.createElement('style');
                style.textContent = `
                    @keyframes neural-glow {
                        0% { text-shadow: 0 0 20px #00ffff, 0 0 30px #00ffff, 0 0 40px #00ffff; }
                        100% { text-shadow: 0 0 30px #00ffff, 0 0 40px #00ffff, 0 0 50px #00ffff; }
                    }
                `;
                document.head.appendChild(style);
            });
        </script>
        """
        
        # Inject the neural CSS right after the <head> tag
        enhanced_html = html_content.replace('<head>', '<head>' + neural_css)
        
        # Write the enhanced HTML back
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(enhanced_html)
        
        print(f"Neural map exported to {os.path.abspath(output_file)}")
        return net
    except Exception as e:
        print(f"Error exporting neural map: {e}")
        return None


def generate_knowledge_graph(text):
    """
    Generates and renders neural architecture from cognitive input.

    This function executes neural pathway extraction asynchronously and then renders
    the resulting neural network using quantum visualization protocols.

    Args:
        text (str): Cognitive input to convert into neural architecture.

    Returns:
        pyvis.network.Network: The rendered neural network visualization object.
    """
    neural_documents = asyncio.run(extract_graph_data(text))
    neural_net = visualize_graph(neural_documents)
    return neural_net