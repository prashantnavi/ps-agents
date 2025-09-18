import gradio as gr
from dotenv import load_dotenv
from enhanced_research_manager import EnhancedResearchManager
import asyncio

load_dotenv(override=True)

async def run_enhanced_research(query: str, enable_handoffs: bool = True):
    """Run the enhanced research process with handoffs"""
    async for chunk in EnhancedResearchManager(enable_handoffs=enable_handoffs).run(query):
        yield chunk

def run_sync(query: str, enable_handoffs: bool = True):
    """Synchronous wrapper for the async function"""
    import asyncio
    
    async def _run():
        async for chunk in run_enhanced_research(query, enable_handoffs):
            yield chunk
    
    # Use asyncio.run for better context management
    try:
        # Create a new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def collect_chunks():
            chunks = []
            async for chunk in _run():
                chunks.append(chunk)
            return chunks
        
        chunks = loop.run_until_complete(collect_chunks())
        
        # Yield all chunks
        for chunk in chunks:
            yield chunk
            
    except Exception as e:
        yield f"Error: {str(e)}"
    finally:
        if 'loop' in locals():
            loop.close()

with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
    gr.Markdown("# Enhanced Deep Research with Handoffs")
    gr.Markdown("""
    This enhanced version includes handoff capabilities:
    - **Expert Consultation**: For specialized domains
    - **Human Review**: For complex decisions
    - **Quality Checks**: For report validation
    - **Approval Workflows**: For important actions
    """)
    
    with gr.Row():
        with gr.Column(scale=3):
            query_textbox = gr.Textbox(
                label="What topic would you like to research?",
                placeholder="e.g., 'What are the latest trends in AI?' or 'Medical implications of new diabetes treatments'",
                lines=3
            )
            
            enable_handoffs_checkbox = gr.Checkbox(
                label="Enable Handoffs",
                value=True,
                info="Enable expert consultation, human review, and approval workflows"
            )
            
            run_button = gr.Button("Run Enhanced Research", variant="primary", size="lg")
            
        with gr.Column(scale=1):
            gr.Markdown("### Handoff Types")
            gr.Markdown("""
            **🤖 Expert Consultation**
            - Medical, legal, technical domains
            - Specialized knowledge requests
            
            **👤 Human Review**
            - Complex analysis decisions
            - Quality validation
            
            **✅ Quality Checks**
            - Report completeness
            - Accuracy validation
            
            **📋 Approval Workflows**
            - Search plan approval
            - Email sending approval
            """)
    
    report = gr.Markdown(label="Research Report", show_copy_button=True)
    
    # Event handlers
    run_button.click(
        fn=run_sync, 
        inputs=[query_textbox, enable_handoffs_checkbox], 
        outputs=report
    )
    
    query_textbox.submit(
        fn=run_sync, 
        inputs=[query_textbox, enable_handoffs_checkbox], 
        outputs=report
    )

if __name__ == "__main__":
    ui.launch(inbrowser=True)
