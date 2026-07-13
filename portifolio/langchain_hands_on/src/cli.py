"""CLI interface for the research analyst system."""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from src.orchestrator import Orchestrator

app = typer.Typer(
    name="research-analyst",
    help="AI Research Analyst - Multi-agent RAG research system",
    add_completion=False,
)
console = Console()


@app.command()
def research(
    query: str = typer.Argument(..., help="Research query or topic"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output directory"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed progress"),
    no_export: bool = typer.Option(False, "--no-export", help="Don't export report to file"),
) -> None:
    """Conduct research on a topic and generate a report.

    Examples:
        python -m src.cli research "Comparar OCI vs AWS para workloads de IA"
        python -m src.cli research "Tendências de AI em 2026" --verbose
        python -m src.cli research "Blockchain em supply chain" -o ./my-output
    """
    console.print(Panel(f"[bold]Query:[/bold] {query}", title="🔍 Iniciando Pesquisa", border_style="blue"))

    try:
        orchestrator = Orchestrator(verbose=verbose)
        result = orchestrator.run(query, export=not no_export)

        # Print summary
        orchestrator.print_summary(result)

        # Print executive summary
        console.print("\n[bold]Executive Summary:[/bold]")
        console.print(Markdown(result.report.executive_summary))

        # Print full report if verbose
        if verbose:
            console.print("\n[bold]Full Report:[/bold]")
            console.print(Markdown(result.report.analysis))

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)


@app.command()
def list_reports(
    output_dir: str = typer.Option("output", "--dir", "-d", help="Directory to list"),
) -> None:
    """List generated reports."""
    path = Path(output_dir)
    if not path.exists():
        console.print(f"[yellow]Directory not found: {output_dir}[/yellow]")
        return

    reports = list(path.glob("*.md"))
    if not reports:
        console.print("[yellow]No reports found[/yellow]")
        return

    console.print(f"[bold]Found {len(reports)} reports:[/bold]\n")
    for report in sorted(reports, key=lambda x: x.stat().st_mtime, reverse=True):
        console.print(f"  📄 {report.name}")


@app.command()
def review(
    file_path: str = typer.Argument(..., help="Path to report file"),
) -> None:
    """Review an existing report."""
    path = Path(file_path)
    if not path.exists():
        console.print(f"[red]File not found: {file_path}[/red]")
        raise typer.Exit(1)

    content = path.read_text()
    console.print(Markdown(content))


def main() -> None:
    """Main entry point."""
    app()


if __name__ == "__main__":
    main()
