import gradio as gr
from langchain_community.utilities import ArxivAPIWrapper
import matplotlib.pyplot as plt

def generate_plot(stage):
    # Simplified Stages 0 through 4
    stages = ["0", "1", "2", "3", "4"]
    # Survival Rates: Stage 0 is close to 100%, Stage 4 is the lowest
    survival_rates = [98, 85, 60, 30, 15] 
    # Costs: Stage 0 is minimal, Stage 4 is peak (Immunotherapy/Late-stage care)
    costs = [10, 35, 75, 130, 190]        # Estimated in $1k USD
    
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
    # Try to fetch research data with error handling
    try:
        arxiv = ArxivAPIWrapper(top_k_results=2, doc_content_chars_max=500)
        query = f"{cancer_type} cancer survival rate stage {detection_stage} age {age} cost"
        if gender:
            query += " sex-based clinical differences"
        results = arxiv.run(query)
    except Exception:
        # Fallback message if API fails ? or what is happening here 
        results = "⚠️ The ArXiv research database is currently busy or rate-limited. The visualization below still reflects clinical benchmarks."

    # Build report
    report = f"""
    # 📑 Clinical Research Report: {cancer_type}
    **Patient Profile:** Age {age} | Diagnostic Stage: {detection_stage}
    
    ### 📊 Thesis Analysis
    Detection at **Stage {detection_stage}** identifies a specific coordinate between diagnostic timing and the resulting clinical-economic burden.
    Early detection (Stage 0-1) prioritizes curative outcomes at lower systemic costs.
    
    ### 🔍 Evidence Summary:
    {results}
    
    ---
    **Disclaimer:** This agent uses ArXiv API for research purposes only. Not for medical diagnosis.
    """
    
    # Generate visual
    plot = generate_plot(detection_stage)
    
    return report, plot

# UI Layout
with gr.Blocks() as demo:
    gr.Markdown("# 🏥 Cancer Research Agent (Staging & Economics)")
    
    with gr.Row():
        with gr.Column(scale=1):
            c_type = gr.Textbox(label="Cancer Type", value="Lung Cancer")
            stage = gr.Dropdown(label="Detection Stage", choices=["0", "1", "2", "3", "4"], value="1")
            age_input = gr.Slider(0, 100, 65, label="Patient Age")
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
