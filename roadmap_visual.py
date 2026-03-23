import gradio as gr
from pyvis.network import Network

def generate_roadmap_graph():
    # Initialize Gephi-style network
    net = Network(height="600px", width="100%", bgcolor="#222222", font_color="white", directed=True, cdn_resources="remote")
    
    # CANCER TYPES (Source AICR: https://www.aicr.org/cancer-survival/cancer-type/?gad_source=1&gad_campaignid=22658424638&gbraid=0AAAAAD7w6z5hHTX4za7nDWOtKRdbNMRuV&gclid=CjwKCAjwyYPOBhBxEiwAgpT8P2G1tNaVGtsO1_pPa7LEQPodGeLjikzeUSjNNIEc88kTudSWEn3OtBoCabkQAvD_BwE) 
    # Blue Nodes
    aicr_list = [
        "Bladder", "Breast", "Cervical", "Colorectal", "Endometrial", 
        "Esophageal", "Gallbladder", "Kidney", "Liver", "Lung", 
        "Mouth, Pharynx, Larynx", "Nasopharyngeal", "Ovarian", 
        "Pancreatic", "Prostate", "Skin", "Stomach"
    ]
    
    for i, name in enumerate(aicr_list):
        net.add_node(i, label=name, color="#3399ff", size=25, shape="dot",
                     title=f"AICR Type: {name}")

    # DETECTION STAGES 
    # Diamond nodes represent diagnostic journey
    stages = {
        100: "Stage 0-1 (Localized)", 
        101: "Stage 2-3 (Regional)", 
        102: "Stage 4 (Advanced/Metastatic)"
    }
    for node_id, label in stages.items():
        # Green for early detection, Red for late
        color = "#99ff66" if node_id == 100 else "#ff6666"
        net.add_node(node_id, label=label, color=color, size=35, shape="diamond")

    # TREATMENTS & COST CATEGORIES 
    # Triangle nodes representing the economic and clinical response
    treatments = {
        200: "Curative Surgery",
        201: "Standard Chemotherapy",
        202: "Precision Immunotherapy",
        203: "Palliative/Supportive Care"
    }
    
    costs = {
        200: "High Initial Cost (Lower Long-term)",
        201: "Recurring Moderate-High Cost",
        202: "Very High Cost (Advanced Care)",
        203: "Supportive Maintenance Cost"
    }

    for node_id, label in treatments.items():
        net.add_node(node_id, label=label, color="#ffcc00", size=30, shape="triangle",
                     title=f"Cost Category: {costs[node_id]}")

    # CONNECTIONS Here
    # Connect every Cancer Type to the "Localized" Stage to show the starting point
    for i in range(len(aicr_list)):
        net.add_edge(i, 100, color="grey", alpha=0.3)
        net.add_edge(i, 101, color="grey", alpha=0.3)
        net.add_edge(i, 102, color="grey", alpha=0.3)

    # Logic-based clinical pathways
    # Stage 0-1 -> Surgery (High survival)
    net.add_edge(100, 200, weight=5, color="#00ffcc", title="Primary Curative Route")
    
    # Stage 2-3 -> Chemo/Surgery
    net.add_edge(101, 201, weight=5, color="#ffcc00")
    
    # Stage 4 -> Immunotherapy/Palliative (Highest cost burden)
    net.add_edge(102, 202, weight=5, color="#ffcc00")
    net.add_edge(102, 203, weight=5, color="#ffcc00")

    # Gephi-style Bouncy Physics
    net.set_options("""
    var options = {
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -80,
          "springLength": 100,
          "springConstant": 0.05
        },
        "solver": "forceAtlas2Based"
      }
    }
    """)
    
    net.save_graph("roadmap.html")
    with open("roadmap.html", 'r', encoding='utf-8') as f:
        html_content = f.read()

    # WRAP IN IFRAME: Prevent JS from being blocked or clashing with Gradio
    iframe_html = f"""
    <iframe srcdoc='{html_content.replace("'", "&apos;")}' 
            width="100%" 
            height="600px" 
            style="border:none; border-radius: 10px; background-color: #222222;">
    </iframe>
    """
    return iframe_html

# Gradio Tab Component
with gr.Blocks() as roadmap_page:
    gr.Markdown("## 🌐 Oncology Interaction Network")
    gr.Markdown("An interactive visualization of the AICR cancer types, their progression stages, and the resulting treatment/cost pathways.")
    gr.Markdown("""
    > ### ⚠️ Disclaimer: Non-Exhaustive Model
    > This visualization is a research-oriented roadmap and is **not inclusive of all cancer types, rare subtypes, or every available treatment protocol.** > Relationships shown are simplified for architectural visualization of clinical-economic trends and should not be used for medical decision-making.
    """)
    
    gr.HTML(value=generate_roadmap_graph())
    
    gr.Markdown("""
    ### 📈 Improvements & Future Iterations
    * **Demographic Gaps:** Future nodes could visualize specific survival disparities in men vs women and different age demographics.
    * **Cost-Stage Correlation:** Visualizing how economic burden shifts from "one-time" surgical costs in early stages to "continuous" high-cost in metastatic stages.
    * **Inclusive Data:** Ensuring rare types like Nasopharyngeal have the same depth of data as common types like Lung or Skin.
    """)
