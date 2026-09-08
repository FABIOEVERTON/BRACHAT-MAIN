import gradio as gr
import uuid
from .workflow import build_workflow, get_snapshot, human_override
from .memory import SemanticMemory


def create_demo():
    graph, memory = build_workflow(db_path="./email_data.db")
    memory_store = SemanticMemory()

    def process_email(email_content: str, sender: str, subject: str):
        thread_id = str(uuid.uuid4())
        config = {"configurable": {"thread_id": thread_id}}

        initial_state = {
            "email_content": email_content,
            "sender": sender,
            "subject": subject,
            "messages": [],
            "intent": "unknown",
            "reply_draft": "",
            "schedule_info": "",
            "memory_context": "",
            "human_approval": "",
            "current_phase": "classify",
            "thread_id": thread_id,
            "needs_human": False,
        }

        final_state = graph.invoke(initial_state, config)
        snapshot = get_snapshot(graph, config)

        intent = final_state.get("intent", "unknown")
        draft = final_state.get("reply_draft", "")
        schedule = final_state.get("schedule_info", "")
        memory_ctx = final_state.get("memory_context", "")
        paused = len(snapshot.get("next", [])) > 0

        status = "⏸️ Aguardando aprovação humana" if paused else "✅ Processado"

        result = f"**Intenção:** {intent}\n\n"
        if memory_ctx:
            result += f"**Memória:**\n{memory_ctx}\n\n"
        if draft:
            result += f"**Rascunho:**\n{draft}\n\n"
        if schedule:
            result += f"**Agendamento:**\n{schedule}\n\n"
        result += f"**Status:** {status}"

        return result, thread_id

    def approve_schedule(thread_id: str):
        if not thread_id:
            return "❌ Forneça um thread_id"

        config = {"configurable": {"thread_id": thread_id}}
        try:
            snapshot = get_snapshot(graph, config)
            if not snapshot.get("next"):
                return "✅ Fluxo já finalizado"

            final_state = human_override(graph, config, {"human_approval": "approved"})
            schedule = final_state.get("schedule_info", "")
            return f"✅ Agendamento aprovado e salvo na memória:\n{schedule}"
        except Exception as e:
            return f"❌ Erro: {str(e)}"

    def search_memory(query: str):
        facts = memory_store.search_facts(query, k=5)
        if facts:
            return "🔍 Resultados da memória:\n" + "\n".join(f"- {f}" for f in facts)
        return "🔍 Nenhum resultado encontrado."

    def store_fact(fact: str):
        if not fact:
            return "❌ Forneça um fato para armazenar"
        memory_store.store_fact(fact)
        return f"💾 Fato armazenado: {fact}"

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
                f"**Intenção:** {snap.get('values', {}).get('intent', 'N/A')}\n"
                f"**Precisa de humano:** {snap.get('values', {}).get('needs_human', False)}"
            )
        except Exception as e:
            return f"❌ Erro: {str(e)}"

    with gr.Blocks(title="Assistente de E-mail Executivo") as demo:
        gr.Markdown("# 📧 Assistente de E-mail Executivo")
        gr.Markdown("Sistema com memória semântica, roteamento inteligente e HITL")

        with gr.Tab("📨 Processar E-mail"):
            sender_input = gr.Textbox(label="Remetente", placeholder="nome@empresa.com")
            subject_input = gr.Textbox(label="Assunto", placeholder="Reunião sobre projeto X")
            email_input = gr.Textbox(label="Conteúdo do E-mail", lines=6)
            btn_process = gr.Button("🚀 Processar", variant="primary")
            result_output = gr.Markdown()
            thread_output = gr.Textbox(label="Thread ID")

            btn_process.click(
                fn=process_email,
                inputs=[email_input, sender_input, subject_input],
                outputs=[result_output, thread_output]
            )

        with gr.Tab("✅ Aprovar Agendamento"):
            approve_thread = gr.Textbox(label="Thread ID")
            btn_approve = gr.Button("✅ Aprovar")
            approve_output = gr.Markdown()

            btn_approve.click(
                fn=approve_schedule,
                inputs=[approve_thread],
                outputs=[approve_output]
            )

        with gr.Tab("🧠 Memória Semântica"):
            gr.Markdown("### Buscar Memória")
            search_input = gr.Textbox(label="Busca", placeholder="Reunião com João")
            btn_search = gr.Button("🔍 Buscar")
            search_output = gr.Markdown()

            btn_search.click(
                fn=search_memory,
                inputs=[search_input],
                outputs=[search_output]
            )

            gr.Markdown("### Armazenar Fato")
            fact_input = gr.Textbox(label="Fato", placeholder="João prefere reuniões às terças")
            btn_store = gr.Button("💾 Armazenar")
            store_output = gr.Markdown()

            btn_store.click(
                fn=store_fact,
                inputs=[fact_input],
                outputs=[store_output]
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
