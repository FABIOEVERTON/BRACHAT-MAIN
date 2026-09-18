import typer
import uuid
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

app = typer.Typer(help="Executive Email Assistant — LangGraph + Semantic Memory + HITL")
console = Console()


@app.command()
def run(
    sender: str = typer.Argument(..., help="Email sender"),
    subject: str = typer.Option("No Subject", "--subject", "-s", help="Email subject"),
    content: str = typer.Option(..., "--content", "-c", help="Email body content"),
    thread_id: str = typer.Option(None, "--thread", "-t", help="Session thread_id"),
    db: str = typer.Option("./email_data.db", "--db", help="SQLite database path"),
):
    from .workflow import build_workflow, get_snapshot

    if thread_id is None:
        thread_id = str(uuid.uuid4())

    graph, memory = build_workflow(db_path=db)
    config = {"configurable": {"thread_id": thread_id}}

    initial_state = {
        "email_content": content,
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

    console.print(Panel(
        f"[bold]From:[/] {sender}\n[bold]Subject:[/] {subject}\n[bold]Thread:[/] {thread_id}",
        title="📧 Email Assistant"
    ))

    final_state = graph.invoke(initial_state, config)
    snapshot = get_snapshot(graph, config)

    paused = len(snapshot.get("next", [])) > 0
    status = "⏸️  Paused for HITL review" if paused else "✅ Completed"
    intent = final_state.get("intent", "unknown")

    console.print(f"[bold]Intent:[/] {intent}")

    if final_state.get("reply_draft"):
        console.print(Markdown(f"### Draft Reply\n{final_state['reply_draft']}"))
    if final_state.get("schedule_info"):
        console.print(Markdown(f"### Schedule Info\n{final_state['schedule_info']}"))
    if final_state.get("memory_context"):
        console.print(Markdown(f"### Memory Context\n{final_state['memory_context']}"))

    console.print(Panel(f"[bold]{status}[/]\nThread: {thread_id}", title="Status"))


@app.command()
def snapshot(
    thread_id: str = typer.Argument(..., help="Session thread_id"),
    db: str = typer.Option("./email_data.db", "--db", help="SQLite database path"),
):
    from .workflow import build_workflow, get_snapshot

    graph, _ = build_workflow(db_path=db)
    config = {"configurable": {"thread_id": thread_id}}

    try:
        snap = get_snapshot(graph, config)
        console.print(Panel(
            f"[bold]Thread:[/] {thread_id}\n"
            f"[bold]Next:[/] {snap.get('next', 'N/A')}\n"
            f"[bold]Phase:[/] {snap.get('values', {}).get('current_phase', 'N/A')}\n"
            f"[bold]Intent:[/] {snap.get('values', {}).get('intent', 'N/A')}\n"
            f"[bold]Pending tasks:[/] {len(snap.get('tasks', []))}",
            title="📸 Snapshot"
        ))
    except Exception as e:
        console.print(f"[red]Error:[/] {e}")


@app.command()
def resume(
    thread_id: str = typer.Argument(..., help="Session thread_id"),
    approval: str = typer.Option("approved", "--approval", "-a", help="Approval text"),
    db: str = typer.Option("./email_data.db", "--db", help="SQLite database path"),
):
    from .workflow import build_workflow, get_snapshot, human_override

    graph, _ = build_workflow(db_path=db)
    config = {"configurable": {"thread_id": thread_id}}

    try:
        snap = get_snapshot(graph, config)
        if not snap.get("next"):
            console.print("[yellow]Flow already finished.[/]")
            return

        final_state = human_override(graph, config, {"human_approval": approval})
        console.print(f"[green]✅ Resumed with approval: {approval}[/]")
    except Exception as e:
        console.print(f"[red]Error:[/] {e}")


if __name__ == "__main__":
    app()
