# LangGraph Multi-Agent System

Stateful multi-agent research system using LangGraph with conditional workflows and persistent state.

## Overview

Uses **StateGraph** (explicit state), **Conditional Routing** (dynamic paths), **Persistent State** (survives iterations), and **Cycle Detection** (handles loops).

## LangGraph vs LangChain

| Feature | LangChain | LangGraph |
|---------|-----------|-----------|
| State Management | Implicit | Explicit (TypedDict) |
| Workflow Control | Sequential | Graph-based with cycles |
| Conditional Logic | Limited | Full support |
| Persistence | Manual | Built-in |

## Architecture

```
CLI (Typer) -> StateGraph -> Researcher / Analyst / Reviewer -> Writer -> Output (MD + sources + score)
```

## Features

- Stateful workflows with persistence, conditional routing, cycle detection
- Human-in-the-loop support and checkpointing

## Installation

```bash
git clone <repo> && cd langraph-estudo
python -m venv venv && source venv/bin/activate
pip install -e .
cp .env.example .env  # add GOOGLE_STUDIO_API_KEY
playwright install chromium
```

## Usage

```bash
python -m src.cli research "Comparar OCI vs AWS para workloads de IA"
python -m src.cli research "Tendencias de AI em 2026" --verbose
python -m src.cli list-reports
python -m src.cli review ./output/report.md
```

## Configuration

| Variable | Default |
|----------|---------|
| `GOOGLE_STUDIO_API_KEY` | Required |
| `GEMINI_MODEL` | `gemini-2.0-flash` |
| `MAX_SOURCES` | `10` |
| `SOURCE_TIMEOUT` | `30` |
| `OUTPUT_DIR` | `output` |

## Project Structure

```
langraph-estudo/
├── src/
│   ├── cli.py              # CLI
│   ├── config.py           # Config
│   ├── orchestrator.py     # Orchestrator
│   ├── workflow.py         # StateGraph
│   ├── agents/             # researcher, analyst, writer, reviewer
│   ├── tools/              # web_search, scraper, pdf_export
│   ├── states/             # schemas
│   └── utils/              # logger
├── tests/                  # test_agents, test_workflow, test_states
└── output/
```

## Testing

```bash
pytest                           # all tests
pytest --cov=src --cov-report=term-missing
```

## Docker

```bash
docker build -t langgraph-agent .
docker run -it --env-file .env langgraph-agent research "Your query"
```

## Technologies

LangGraph, LangChain, Google Gemini, Playwright, BeautifulSoup, Typer, Rich, Pydantic

## Author

**Fabio Everton** — [jae.engenharia@gmail.com](mailto:jae.engenharia@gmail.com) | [LinkedIn](https://www.linkedin.com/in/jae/) | [Portfolio](https://portfolio-jae.netlify.app)
