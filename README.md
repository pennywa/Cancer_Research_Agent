---
title: Cancer Research Agent
emoji: 🧬
colorFrom: blue
colorTo: red
sdk: gradio
sdk_version: 4.44.1
python_version: 3.11
app_file: app.py
pinned: false
---
# 🏥 Oncology Research & Interaction Network
This application allows users to query oncology research while interacting with a dynamic knowledge graph of cancer stages and treatment pathways.

## Hugging Face Link: https://huggingface.co/spaces/pennywa/Cancer_Research_Agent

# Cancer_Research_Agent
Correlation of Cancer Stage at Diagnosis and its Impact on Survival Rates and Cost of Treatment.
Uses LangChain and the ArXiv API to synthesize recent academic papers based on cancer type, stage, and patient demographics.

# Cost Correlation Plot: 
Matplotlib-driven analysis visualizing the inverse relationship between Survival Probability and Treatment Cost across diagnostic stages.

# Interactive Roadmap: 
Pyvis-powered force-directed graph (hosted in an IFrame) that maps the connections between AICR-recognized cancer types, progression stages, and clinical interventions.

## ⚠️ Medical Disclaimer
This tool is for educational and research purposes only. The data visualizations and literature summaries are generated via automated algorithms and do not constitute medical advice, professional diagnosis, or treatment recommendations.

# Sources
ArXiv integration: https://docs.langchain.com/oss/python/integrations/tools/arxiv

Cancer Types Visualization Nodes Source: https://www.aicr.org/cancer-survival/cancer-type/?gad_source=1&gad_campaignid=22658424638&gbraid=0AAAAAD7w6z5hHTX4za7nDWOtKRdbNMRuV&gclid=CjwKCAjwyYPOBhBxEiwAgpT8P2G1tNaVGtsO1_pPa7LEQPodGeLjikzeUSjNNIEc88kTudSWEn3OtBoCabkQAvD_BwE
