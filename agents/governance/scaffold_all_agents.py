#!/usr/bin/env python3
"""
[BR-EZRA-001] Scaffold All Agents
Creates the complete foundational structure for every agent:
  - context_memory.json (role-specific)
  - skills_memory.json
  - hermes_agent/ (4 evolution mechanisms)
  - receipts/ directory
  - worklog.jsonl
  - state.json updated to canonical schema

Run: python3 scaffold_all_agents.py
"""
import json, sys, os, shutil
from datetime import datetime
from pathlib import Path

BASE = Path(os.environ.get("HOME")) / "brachat-main"
GOVERNANCE = BASE / "agents" / "governance"
HERMES_TEMPLATE = BASE / "agents" / "orchestrator_agents" / "ezra" / "hermes_agent"

AGENTS = [
    ("orchestrator", "ezra", BASE / "agents" / "orchestrator_agents" / "ezra",
     "Orchestrator. Ponto unico de contato com Fabio. Coordena todos os agentes.",
     "orchestrator", "BR-EZRA-001"),
    ("director", "aisio", BASE / "agents" / "director_agents" / "aisio",
     "Governance. Gate keeper. Valida U1-U11 em runtime. Aprova ou bloqueia toda acao produtiva.",
     "governance", "BR-AISIO-010"),
    ("director", "gilmario", BASE / "agents" / "director_agents" / "gilmario",
     "Branding. Identidade visual, copia publicitaria, autoridade de marca.",
     "branding", "BR-GILMAR-011"),
    ("director", "jessica", BASE / "agents" / "director_agents" / "jessica",
     "Legal. LGPD, compliance, contratos, riscos regulatorios. Pode vetar acoes.",
     "legal", "BR-JESSIC-012"),
    ("director", "josue", BASE / "agents" / "director_agents" / "josue",
     "Commercial. Vendas OLX, divulgacao de anuncios. Fabio posta, Josue promove.",
     "commercial", "BR-JOSUE-013"),
    ("director", "nice", BASE / "agents" / "director_agents" / "nice",
     "Domestic. Financas domesticas, kashrut, compras, lista de supermercado.",
     "domestic", "BR-NICE-014"),
    ("production", "artur", BASE / "agents" / "production_planning_agents" / "artur",
     "Builder Director. Recebe spec do Architect, escreve spec em portfolio/tasks/, dispatcha Baruch.",
     "builder_director", "BR-ARTUR-002"),
    ("production", "architect", BASE / "agents" / "production_planning_agents" / "architect",
     "Builder Planner. Planeja arquitetura de projetos, gera spec de alto nivel, envia para Artur.",
     "builder_planner", "BR-ARCHIT-004"),
    ("studies", "john", BASE / "agents" / "studies_agents" / "john",
     "English tutor. Prompt ou NotebookLM. Registro de vocabulario.",
     "english", "BR-JOHN-020"),
    ("studies", "temer", BASE / "agents" / "studies_agents" / "temer",
     "Public exam tutor. NotebookLM + revisao espaçada para concurso.",
     "public_exam", "BR-TEMER-022"),
    ("studies", "badge", BASE / "agents" / "studies_agents" / "badge",
     "Certifications tutor. OCI Foundations, AI, GenAI, Architect, Multicloud, AIGP.",
     "certifications", "BR-BADGE-030"),
    ("studies", "aristotle", BASE / "agents" / "studies_agents" / "aristotle",
     "Philosophy tutor. Aristoteles, corpus 12.7M chars.",
     "philosophy", "BR-ARISTO-023"),
    ("studies", "dev", BASE / "agents" / "studies_agents" / "dev",
     "Python tutor. Algoritmos, pensamento computacional.",
     "python", "BR-DEV-021"),
    ("studies", "calculus", BASE / "agents" / "studies_agents" / "calculus",
     "ML Engineer tutor. Calculo, estatistica, machine learning.",
     "ml_engineer", "BR-CALCUL-029"),
    ("studies", "showcase", BASE / "agents" / "studies_agents" / "showcase",
     "Portfolio builder. Projetos, evidencias de aprendizado, demonstracoes.",
     "portfolio_builder", "BR-SHOWCA-028"),
    ("studies", "certifications", BASE / "agents" / "studies_agents" / "certifications",
     "OCI Skills tutor. Compute, storage, networking, IAM, database. Certificacoes OCI.",
     "oci_skills", "BR-GOOGLE-025"),
    ("job", "justus", BASE / "agents" / "job" / "justus",
     "Job hunter. 15 apps/dia via jae.engenharia. Checa respostas, reenvia bounces.",
     "job_hunter", "BR-JUSTUS-027"),
    ("job", "freela", BASE / "agents" / "job" / "freela",
     "Freelancer. Projetos em plataformas, Fiverr.",
     "freelancer", "BR-FREELA-026"),
    ("portfolio", "baruch", BASE / "portfolio" / "engineer",
     "Lead Software Engineer. Claude Code CLI. Executa builds, cria pastas, cria agentes-projeto.",
     "lead_software_engineer", "BR-BARUCH-003"),
    ("portfolio", "imersion_agent", BASE / "portfolio" / "one_oracle" / "imersion_agent",
     "ONE Oracle Imersion project agent. Projeto de imersao Oracle.",
     "one_oracle_imersion", "BR-OP-IMERSION-001"),
]

HERMES_FILES = [
    "skill_factory.py", "gepa_evolver.py", "darwinian_evolver.py",
    "background_review.py", "hermes_agent_self_evolution.py"
]


def make_context_memory(name, role, description, agent_id):
    return {
        "agent": {
            "name": name,
            "id": agent_id,
            "role": role,
            "temperature": 0,
            "model": "custom-proxy/big-pickle",
            "reasoning": False
        },
        "persona": description,
        "system_rules": {
            "universal": {
                "U1_MVI": "Nenhum arquivo >200 linhas",
                "U3_NO_SECRETS": "Sem tokens/keys hardcoded",
                "U8_TRACEABILITY": "Logs/commits comecam com [BR-ID]",
                "U11_ENGLISH_ONLY": "Tudo em ingles em system files/logs/commits"
            },
            "gate_aisio": "Toda acao produtiva passa pelo GATE AISIO. Se bloquear, nao executo."
        },
        "receipt_type": {
            "orchestrator": "session",
            "governance": "gate_validation",
            "branding": "email_sent",
            "legal": "compliance_check",
            "commercial": "sales_action",
            "domestic": "email_sent",
            "builder_director": "spec_dispatch",
            "builder_planner": "spec_dispatch",
            "english": "study_delivery",
            "public_exam": "study_delivery",
            "certifications": "study_delivery",
            "philosophy": "study_delivery",
            "python": "study_delivery",
            "ml_engineer": "study_delivery",
            "portfolio_builder": "consolidation",
            "oci_skills": "study_delivery",
            "job_hunter": "job_application",
            "freelancer": "email_sent",
            "one_oracle_imersion": "consolidation"
        }.get(role, "task"),
        "requires_aisio_gate": True,
        "produces_receipt": True,
        "updated_at": datetime.now().strftime("%Y-%m-%d")
    }


def make_skills_memory(name, agent_id):
    return {
        "version": 1,
        "agent_id": agent_id,
        "agent_name": name,
        "learned_skills": [],
        "insights": [],
        "hermes_loop": {
            "status": "active",
            "activated_at": datetime.now().isoformat(),
            "cycle_steps": [
                "1. search_memories",
                "2. load_general_skill",
                "3. apply_skill",
                "4. log_insight",
                "5. consolidate",
                "6. mem0_add_memory"
            ],
            "skill_resolution_path": [
                "1. Local Cache: cache_skills/",
                "2. active-index.json",
                "3. master-index.json (grep)",
                "4. Hydrate to cache_skills/"
            ]
        },
        "updated_at": datetime.now().strftime("%Y-%m-%d")
    }


def scaffold_agent(category, name, agent_dir, description, role, agent_id):
    agent_dir.mkdir(parents=True, exist_ok=True)

    ctx_path = agent_dir / "context_memory.json"
    if ctx_path.exists() and ctx_path.stat().st_size > 300:
        print(f"  [SKIP] context_memory.json {name} (preserved existing)")
    else:
        ctx = make_context_memory(name, role, description, agent_id)
        ctx_path.write_text(json.dumps(ctx, indent=2) + "\n")
        print(f"  [OK] context_memory.json  {name}")

    sk = make_skills_memory(name, agent_id)
    sk_path = agent_dir / "skills_memory.json"
    sk_path.write_text(json.dumps(sk, indent=2) + "\n")
    print(f"  [OK] skills_memory.json   {name}")

    hermes_dir = agent_dir / "hermes_agent"
    hermes_dir.mkdir(parents=True, exist_ok=True)
    (hermes_dir / "population").mkdir(exist_ok=True)
    (hermes_dir / "reviews").mkdir(exist_ok=True)

    for hf in HERMES_FILES:
        src = HERMES_TEMPLATE / hf
        dst = hermes_dir / hf
        if src.exists() and not dst.exists():
            shutil.copy2(src, dst)
            dst.chmod(0o755)
    print(f"  [OK] hermes_agent/        {name}")

    receipts_dir = agent_dir / "receipts"
    receipts_dir.mkdir(exist_ok=True)
    (receipts_dir / ".gitkeep").touch()
    print(f"  [OK] receipts/            {name}")

    wl_path = agent_dir / "worklog.jsonl"
    if not wl_path.exists():
        wl_path.write_text("")
    print(f"  [OK] worklog.jsonl        {name}")

    state_path = agent_dir / "state.json"
    if state_path.exists():
        try:
            state = json.loads(state_path.read_text())
            state["agent_id"] = state.get("agent_id", agent_id)
            state["name"] = state.get("name", name)
            state["role"] = state.get("role", role)
            state["status"] = state.get("status", "idle")
            state["sessions"] = state.get("sessions", [])
            state["updated_at"] = datetime.now().isoformat()
            state_path.write_text(json.dumps(state, indent=2) + "\n")
        except (json.JSONDecodeError, Exception):
            pass
    print(f"  [OK] state.json           {name}")

    return str(agent_dir)


def main():
    print(f"[BR-EZRA-001] Scaffolding all {len(AGENTS)} agents...\n")

    results = []
    for category, name, agent_dir, description, role, agent_id in AGENTS:
        path = scaffold_agent(category, name, agent_dir, description, role, agent_id)
        results.append(name)

    print(f"\n{'='*50}")
    print(f"Scaffold complete. {len(results)} agents structured.")
    for r in results:
        print(f"  - {r}")
    print(f"\nEach agent now has:")
    print(f"  context_memory.json + skills_memory.json + hermes_agent/ + receipts/ + worklog.jsonl")
    return 0


if __name__ == "__main__":
    sys.exit(main())
