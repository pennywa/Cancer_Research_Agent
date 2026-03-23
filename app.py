import gradio as gr
from langchain_community.utilities import ArxivAPIWrapper

def oncology_researcher(cancer_type, detection_stage, age, gender):
    # Initialize ArXiv engine
    arxiv = ArxivAPIWrapper(top_k_results=3, doc_content_chars_max=1000)
    
    # Query including Age and Gender
    query = f"{cancer_type} cancer survival rate stage {detection_stage} age {age} treatment cost"
    
    # If checkbox is checked, add gender-specific search terms
    if gender:
        query += " male vs female clinical outcomes and demographics"
    
    results = arxiv.run(query)
    
    # Visual Report format
    report = f"""
    # 🧬 Research Report: {cancer_type}
    **Patient Profile:** {age} years old | Detected at Stage {detection_stage}
    
    ### 📊 Thesis Analysis
    For a patient of age {age}, research indicates that detecting {cancer_type} at {detection_stage} 
    is the primary factor in determining both 5-year survival probability $P_s$ and total healthcare expenditure $C$.
    
    ### 🔍 ArXiv Evidence Summary:
    {results}
    
    ---
    **Thesis Conclusion:** At age {age}, early intervention at {detection_stage} significantly avoids the cost curve associated with stage {cancer_type}.
    """
    return report

# UI
with gr.Blocks() as demo:
    gr.Markdown("# 🏥 Cancer Research Agent (ArXiv API)")
    
    with gr.Row():
        with gr.Column():
            c_type = gr.Textbox(label="Cancer Type", placeholder="e.g., Lung Cancer")
            stage = gr.Dropdown(label="Detection Stage", choices=["0", "1", "2", "3", "4"])
            age_input = gr.Slider(minimum=0, maximum=100, value=50, step=1, label="Patient Age")
            gender_input = gr.Checkbox(label="Include Gender Demographics", value=False)
            btn = gr.Button("Generate Research Report", variant="primary")
        
        with gr.Column():
            output = gr.Markdown(label="Generated Report")

    # Map UI components 
    btn.click(
        fn=oncology_researcher, 
        inputs=[c_type, stage, age_input, gender_input], 
        outputs=output
    )

demo.launch(server_name="0.0.0.0", show_error=True)
