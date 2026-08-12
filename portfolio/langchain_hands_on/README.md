# AI Research Analyst

Multi-agent RAG research system using LangChain and Google Gemini.

## Overview

Multi-agent architecture for automated research and report generation. Specialized agents research topics, analyze data, and generate comprehensive reports.

## Architecture

```
CLI (Typer) -> Orchestrator -> Researcher / Analyst / Reviewer -> Writer -> Output (MD + sources + score)
```

## Features

- Multi-agent Architecture, RAG Integration, Web Scraping (Playwright + BeautifulSoup)
- Quality Review, CLI Interface, Confidence Scoring

## Installation

```bash
git clone <repo> && cd langchain_hands_on
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
| `GEMINI_MODEL` | `gemini-1.5-flash` |
| `MAX_SOURCES` | `10` |
| `SOURCE_TIMEOUT` | `30` |
| `OUTPUT_DIR` | `output` |

## Project Structure

```
langchain_hands_on/
├── src/
│   ├── cli.py              # CLI
│   ├── config.py           # Config
│   ├── orchestrator.py     # Orchestrator
│   ├── agents/             # researcher, analyst, writer, reviewer
│   ├── tools/              # web_search, scraper, pdf_export
│   ├── models/             # schemas
│   └── utils/              # logger
├── tests/                  # test_agents, test_tools, test_orchestrator
└── output/
```

## Testing

```bash
pytest                           # all tests
pytest --cov=src --cov-report=term-missing
```

## Docker

```bash
docker build -t research-analyst .
docker run -it --env-file .env research-analyst research "Your query"
```

## Technologies

LangChain, Google Gemini, Playwright, BeautifulSoup, Typer, Rich, Pydantic

## Author

**Fabio Everton** — [jae.engenharia@gmail.com](mailto:jae.engenharia@gmail.com) | [LinkedIn](https://www.linkedin.com/in/jae/) | [Portfolio](https://portfolio-jae.netlify.app)
