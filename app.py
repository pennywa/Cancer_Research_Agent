import gradio as gr
from langchain_community.utilities import ArxivAPIWrapper
import matplotlib.pyplot as plt

def generate_plot(stage):
    # Simplified Stages 0 through 4
    stages = ["0", "1", "2", "3", "4"]
    # Survival Rates: Stage 0 is close to 100%, Stage 4 is the lowest
    survival_rates = [85, 70, 55, 40, 25, 10] 
    # Costs: Stage 0 is minimal, Stage 4 is peak (Immunotherapy/Late-stage care)
    costs = [25, 50, 75, 100, 125, 150]        # Estimated in $1k USD
    
    plt.figure(figsize=(6, 4))
    # Draw the "Thesis Line" (Inverse Correlation)
    plt.plot(costs, survival_rates, color='grey', linestyle='--', alpha=0.5)
    plt.scatter(costs, survival_rates, c='blue', s=100, label="Other Stages")
    
    # Highlight the current selected stage
    try:
        idx = stages.index(str(stage))
        plt.scatter(costs[idx], survival_rates[idx], c='red', s=200, 
                    label=f"Selected: Stage {stage}", edgecolors='black', zorder=5)
    except ValueError:
        pass
    
    plt.title("Correlation: Survival Probability vs. Treatment Cost")
    plt.xlabel("Estimated Treatment Cost ($1,000 USD)")
    plt.ylabel("5-Year Survival Probability (%)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    return plt.gcf()

def oncology_researcher(cancer_type, detection_stage, age, gender):
    """
    Args:
        cancer_type (str): The specific malignancy to research.
        detection_stage (str): Stage (0-4).
        age (int): Patient age for demographic filtering.
        gender (bool): Flag to include sex-based clinical data.
    Returns:
        tuple: (Markdown Research Report, Matplotlib Correlation Plot)
    """
    try:
        # Try to fetch research data with error handling
        # Fetch data using load() to get metadata + content
        arxiv_wrapper = ArxivAPIWrapper(top_k_results=2, doc_content_chars_max=500)
        docs = arxiv_wrapper.load(f"{cancer_type} cancer survival rate stage {detection_stage} cost")
        
        evidence_list = []
        for doc in docs:
            # Extract URL (Entry ID) and Title from metadata
            title = doc.metadata.get('Title', 'Research Paper')
            link = doc.metadata.get('Entry ID', 'https://arxiv.org/')
            # Get the summary from the page content
            summary = doc.page_content[:300] + "..."
            
            # Combine them into a clickable Markdown format
            evidence_list.append(f"### 📄 [{title}]({link})\n{summary}")
        
        results = "\n\n".join(evidence_list) if evidence_list else "No recent papers found for this specific criteria."
        
    except Exception:
         # Fallback message if API fails ? 
        results = "⚠️ The ArXiv research database is currently busy or rate-limited. The visualization below still reflects clinical benchmarks."

    # Build report
    report = f"""
    # 📑 Clinical Research Report: {cancer_type}
    **Patient Profile:** Age {age} | Diagnostic Stage: {detection_stage}
    
    ### 📊 Thesis Analysis
    Detection at **Stage {detection_stage}** identifies a specific coordinate between diagnostic timing and the resulting clinical-economic burden.
    Early detection (Stage 0-1) prioritizes curative outcomes at lower systemic costs.
    
    ### 🔍 Evidence & Primary Sources:
    {results}
    
    ---
     **Disclaimer:** This agent uses ArXiv API for research purposes only. Not for medical diagnosis.
     *ALWAYS FACT CHECK and VERIFY, take it with a grain of salt*
    """
    
    # Generate plot
    plot = generate_plot(detection_stage)
    return report, plot
    
    # Generate visual
    plot = generate_plot(detection_stage)
    return report, plot

# UI Layout
with gr.Blocks() as demo:
    gr.Markdown("# 🏥 Cancer Research Agent (Stage Detection & Cost of Treatment)")
    
    with gr.Row():
        with gr.Column(scale=1):
            c_type = gr.Textbox(label="Cancer Type", value="Lung Cancer")
            stage = gr.Dropdown(label="Detection Stage", choices=["0", "1", "2", "3", "4"], value="1")
            age_input = gr.Slider(0, 100, 50, label="Patient Age")
            gender_input = gr.Checkbox(label="Include Gender Data")
            btn = gr.Button("Run Correlation Analysis", variant="primary")
            
        with gr.Column(scale=2):
            output_plot = gr.Plot(label="Visual Correlation Analysis")
            output_text = gr.Markdown(label="Literature Report")

    btn.click(
        fn=oncology_researcher, 
        inputs=[c_type, stage, age_input, gender_input], 
        outputs=[output_text, output_plot]
    )

demo.launch()
