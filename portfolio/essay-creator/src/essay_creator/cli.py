import typer
import uuid
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

app = typer.Typer(help="Multi-Agent Essay Creator — LangGraph + HITL")
console = Console()


@app.command()
def run(
    topic: str = typer.Argument(..., help="Essay topic"),
    thread_id: str = typer.Option(None, "--thread", "-t", help="Session thread_id"),
    max_iter: int = typer.Option(2, "--max-iter", "-n", help="Max write-reflect-critique cycles"),
    db: str = typer.Option("./essay_data.db", "--db", help="SQLite database path"),
):
    from .workflow import build_workflow, get_snapshot

    if thread_id is None:
        thread_id = str(uuid.uuid4())

    graph, memory = build_workflow(db_path=db)
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
        "max_iterations": max_iter,
        "thread_id": thread_id,
    }

    console.print(Panel(f"[bold]Topic:[/] {topic}\n[bold]Thread:[/] {thread_id}", title="✍️ Essay Creator"))
    final_state = graph.invoke(initial_state, config)
    snapshot = get_snapshot(graph, config)

    paused = len(snapshot.get("next", [])) > 0
    status = "⏸️  Paused for HITL review" if paused else "✅ Completed"

    console.print(Markdown(f"### Plan\n{final_state.get('planner_output', 'N/A')}"))
    console.print(Markdown(f"### Research\n{final_state.get('research_notes', 'N/A')}"))
    console.print(Markdown(f"### Draft\n{final_state.get('draft', 'N/A')}"))
    console.print(Markdown(f"### Reflection\n{final_state.get('reflection', 'N/A')}"))
    console.print(Markdown(f"### Critique\n{final_state.get('critique', 'N/A')}"))
    console.print(Panel(f"[bold]{status}[/]\nThread: {thread_id}", title="Status"))


@app.command()
def snapshot(
    thread_id: str = typer.Argument(..., help="Session thread_id"),
    db: str = typer.Option("./essay_data.db", "--db", help="SQLite database path"),
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
            f"[bold]Iteration:[/] {snap.get('values', {}).get('iteration', 0)}\n"
            f"[bold]Pending tasks:[/] {len(snap.get('tasks', []))}",
            title="📸 Snapshot"
        ))
    except Exception as e:
        console.print(f"[red]Error:[/] {e}")


@app.command()
def resume(
    thread_id: str = typer.Argument(..., help="Session thread_id"),
    override: str = typer.Option(..., "--override", "-o", help="Override text for critique"),
    db: str = typer.Option("./essay_data.db", "--db", help="SQLite database path"),
):
    from .workflow import build_workflow, get_snapshot, human_override

    graph, _ = build_workflow(db_path=db)
    config = {"configurable": {"thread_id": thread_id}}

    try:
        snap = get_snapshot(graph, config)
        if not snap.get("next"):
            console.print("[yellow]Flow already finished.[/]")
            return

        final_state = human_override(graph, config, {"critique": override})
        console.print(Markdown(f"### Updated Draft\n{final_state.get('draft', 'N/A')}"))
    except Exception as e:
        console.print(f"[red]Error:[/] {e}")


if __name__ == "__main__":
    app()
