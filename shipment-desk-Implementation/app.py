import gradio as gr
from pipeline import process_exception
from session import add_to_log, generate_daily_summary, triage_log


def handle_submission(report_text, shipment_value, customer_tier):
    """Passes UI inputs to the backend pipeline and formats the output."""
    if not report_text or shipment_value is None:
        return "⚠️ Error: Please provide both a report and a shipment value.", "", triage_log
    
    # 1. Run the pipeline
    result = process_exception(report_text, float(shipment_value), customer_tier)
    
    # 2. Add to session log
    add_to_log(result)
    
    # 3. Format the trace logic and outcome for the UI
    trace_steps = "\n".join(result["log"])
    
    outcome_display = f"""### Final Decision: {result['outcome']}
**Category Identified:** {result['category'].capitalize()}
**Calculated Compensation:** ${result['compensation_amount']:.2f}

**Generated Communication Draft:**
{result['message_draft']}
"""
    return outcome_display, trace_steps, triage_log

def handle_summary():
    """Fetches the aggregated daily summary."""
    return generate_daily_summary()

# Build the Gradio UI Layout
with gr.Blocks(title="Shipment Exception Desk", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 📦 Northwind Logistics: Shipment Exception Desk")
    gr.Markdown("Automated AI triage for incoming customer shipment issues.")
    
    with gr.Row():
        # Left Column: Input Form
        with gr.Column():
            gr.Markdown("### 1. Submit Exception Report")
            report_input = gr.Textbox(lines=5, label="Raw Customer Report", placeholder="E.g., The box arrived completely crushed and the item is broken...")
            value_input = gr.Number(label="Shipment Value ($)", value=0.0)
            tier_input = gr.Radio(choices=["standard", "premium"], value="standard", label="Customer Tier")
            submit_btn = gr.Button("Process Exception", variant="primary")
            
        # Right Column: AI Output & Trace
        with gr.Column():
            gr.Markdown("### 2. Processing Outcome")
            outcome_output = gr.Markdown(label="Final Decision")
            trace_output = gr.Textbox(lines=6, label="Step-by-Step Logic Trace", interactive=False)
            
    gr.HTML("<hr>")
    
    with gr.Row():
        # Bottom Left: Running Log
        with gr.Column():
            gr.Markdown("### Daily Triage Log")
            log_output = gr.JSON(label="All Processed Exceptions (Session)")
            
        # Bottom Right: Aggregation
        with gr.Column():
            gr.Markdown("### Daily Summary Aggregation")
            summary_btn = gr.Button("Get Daily Summary")
            summary_output = gr.JSON(label="Real-time Metrics")

    # Wire up the button click events to our Python functions
    submit_btn.click(
        fn=handle_submission,
        inputs=[report_input, value_input, tier_input],
        outputs=[outcome_output, trace_output, log_output]
    )
    
    summary_btn.click(
        fn=handle_summary,
        inputs=[],
        outputs=summary_output
    )

if __name__ == "__main__":
    demo.launch()