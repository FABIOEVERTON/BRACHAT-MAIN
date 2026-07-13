"""Gradio interface for the LangGraph multi-agent system."""

try:
    import gradio as gr
    HAS_GRADIO = True
except ImportError:
    HAS_GRADIO = False

from src.states import create_initial_state


def research_chat(message: str, history: list) -> str:
    """Chat function for Gradio interface.

    Args:
        message: User message.
        history: Chat history.

    Returns:
        Agent response.
    """
    try:
        from src.workflow import graph

        state = create_initial_state(message)
        response_parts = []

        for step in graph.stream(state, {"recursion_limit": 10}):
            for node_name, output in step.items():
                if "messages" in output:
                    for msg in output["messages"]:
                        if hasattr(msg, "content"):
                            response_parts.append(f"**{node_name}:** {msg.content}")

        return "\n\n".join(response_parts) if response_parts else "No response generated."

    except Exception as e:
        return f"Error: {str(e)}"


def create_gradio_interface():
    """Create Gradio interface.

    Returns:
        Gradio Blocks interface.
    """
    if not HAS_GRADIO:
        raise ImportError("Gradio not installed. Run: pip install gradio")

    with gr.Blocks(
        title="AI Research Analyst",
        theme=gr.themes.Soft(),
    ) as demo:
        gr.Markdown("# 🔍 AI Research Analyst")
        gr.Markdown("Multi-agent research system using LangGraph")

        with gr.Row():
            with gr.Column(scale=3):
                chatbot = gr.Chatbot(
                    label="Research Chat",
                    height=500,
                )
                msg = gr.Textbox(
                    label="Enter your research query",
                    placeholder="Ex: Comparar OCI vs AWS para workloads de IA",
                )
                with gr.Row():
                    submit = gr.Button("🔍 Research", variant="primary")
                    clear = gr.Button("🗑️ Clear")

            with gr.Column(scale=1):
                gr.Markdown("### Examples")
                examples = gr.Examples(
                    examples=[
                        "Comparar n8n vs Make.com para automação de IA",
                        "Tendências de AI em 2026",
                        "Melhores práticas para RAG em produção",
                    ],
                    inputs=msg,
                )

        def respond(message, chat_history):
            response = research_chat(message, chat_history)
            chat_history.append((message, response))
            return "", chat_history

        msg.submit(respond, [msg, chatbot], [msg, chatbot])
        submit.click(respond, [msg, chatbot], [msg, chatbot])
        clear.click(lambda: [], None, chatbot)

    return demo


def launch_app(share: bool = False, port: int = 7860):
    """Launch the Gradio app.

    Args:
        share: Create public link.
        port: Port number.
    """
    demo = create_gradio_interface()
    demo.launch(share=share, server_port=port)
