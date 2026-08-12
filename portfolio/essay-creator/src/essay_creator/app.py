import gradio as gr
import uuid
from .workflow import build_workflow, get_snapshot, human_override
from .state import EssayState


def create_demo():
    graph, memory = build_workflow(db_path="./essay_data.db")

    def start_essay(topic: str):
        thread_id = str(uuid.uuid4())
        config = {"configurable": {"thread_id": thread_id}}

        initial_state = {
            "topic": topic,
            "messages": [],
            "draft": "",
            "research_notes": "",
            "critique": "",
            "reflection": "",
            "planner_output": "",
            "current_phase": "planning",
            "iteration": 0,
            "max_iterations": 2,
            "thread_id": thread_id,
        }

        final_state = graph.invoke(initial_state, config)
        snapshot = get_snapshot(graph, config)

        draft = final_state.get("draft", "Nenhum rascunho gerado.")
        plan = final_state.get("planner_output", "")
        research = final_state.get("research_notes", "")
        critique = final_state.get("critique", "")
        reflection = final_state.get("reflection", "")
        paused = len(snapshot.get("next", [])) > 0

        status = "⏸️ Pausado para revisão humana" if paused else "✅ Concluído"

        return (
            f"**Plano:**\n{plan}\n\n"
            f"**Pesquisa:**\n{research}\n\n"
            f"**Rascunho:**\n{draft}\n\n"
            f"**Reflexão:**\n{reflection}\n\n"
            f"**Crítica:**\n{critique}\n\n"
            f"**Status:** {status}",
            thread_id
        )

    def resume_with_override(thread_id: str, override_text: str):
        if not thread_id:
            return "❌ Forneça um thread_id válido", ""

        config = {"configurable": {"thread_id": thread_id}}

        try:
            snapshot = get_snapshot(graph, config)
            if not snapshot.get("next"):
                return "✅ Fluxo já finalizado", ""

            updates = {"critique": override_text}
            final_state = human_override(graph, config, updates)

            draft = final_state.get("draft", "")
            return (
                f"**Rascunho atualizado:**\n{draft}",
                thread_id
            )
        except Exception as e:
            return f"❌ Erro: {str(e)}", ""

    def view_snapshot(thread_id: str):
        if not thread_id:
            return "❌ Forneça um thread_id"

        config = {"configurable": {"thread_id": thread_id}}
        try:
            snap = get_snapshot(graph, config)
            return (
                f"**Thread ID:** {thread_id}\n"
                f"**Próximo nó:** {snap.get('next', 'N/A')}\n"
                f"**Fase atual:** {snap.get('values', {}).get('current_phase', 'N/A')}\n"
                f"**Iteração:** {snap.get('values', {}).get('iteration', 0)}\n"
                f"**Tarefas pendentes:** {len(snap.get('tasks', []))}"
            )
        except Exception as e:
            return f"❌ Erro: {str(e)}"

    with gr.Blocks(title="Criador de Redações - Multiagente LangGraph") as demo:
        gr.Markdown("# ✍️ Criador de Redações Multiagente")
        gr.Markdown("Sistema com 5 agentes: Planejador, Pesquisador, Escritor, Refletor e Crítico")

        with gr.Tab("📝 Criar Redação"):
            topic_input = gr.Textbox(label="Tópico da Redação", placeholder="Ex: IA e o Futuro do Trabalho")
            btn_start = gr.Button("🚀 Gerar Redação", variant="primary")
            output_text = gr.Markdown()
            thread_output = gr.Textbox(label="Thread ID (salve para retomar)")

            btn_start.click(
                fn=start_essay,
                inputs=[topic_input],
                outputs=[output_text, thread_output]
            )

        with gr.Tab("🔄 HITL - Override Humano"):
            gr.Markdown("Interrompa antes do Crítico e injete sua avaliação")
            thread_input = gr.Textbox(label="Thread ID")
            override_input = gr.Textbox(label="Sua Crítica/Override", lines=5)
            btn_resume = gr.Button("▶️ Retomar com Override")
            resume_output = gr.Markdown()

            btn_resume.click(
                fn=resume_with_override,
                inputs=[thread_input, override_input],
                outputs=[resume_output, thread_input]
            )

        with gr.Tab("📸 Snapshot"):
            snap_thread = gr.Textbox(label="Thread ID")
            btn_snap = gr.Button("📸 Ver Snapshot")
            snap_output = gr.Markdown()

            btn_snap.click(
                fn=view_snapshot,
                inputs=[snap_thread],
                outputs=[snap_output]
            )

    return demo


if __name__ == "__main__":
    demo = create_demo()
    demo.launch()
