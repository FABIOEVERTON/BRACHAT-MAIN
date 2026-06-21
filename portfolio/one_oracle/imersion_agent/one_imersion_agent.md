---
name: hr_buddy
id: BR-ONE-AGENT-001
temperature: 0.0
reasoning: false
role: producer
risk_category: Minimal-Risk
model: n8n (Cohere + Telegram)
steps: 1
---

# HR Buddy — ONE Imersion AI Agent

## Purpose
Intelligent HR assistant agent built during the **Oracle Next Education (ONE) Imersion 2026** (Class 3). Responds to employee HR questions via Telegram, using Cohere LLM, RAG for policy knowledge, and MySQL for personal data (vacation/time bank).

## Tech Stack
- **Orchestration**: n8n (low-code workflow automation)
- **LLM**: Cohere Chat Model + Embeddings
- **Interface**: Telegram Bot (trigger + response)
- **Memory**: Session-based per chat
- **Knowledge**: Vector Store (RAG) for HR policies
- **Data**: MySQL for employee records

## Architecture
```
Telegram → n8n → AI Agent (HR Buddy) → Cohere LLM
                ↓
          ┌─────┴─────┐
       Memory      Vector Store (RAG)
       (session)   ↓
                Embeddings Cohere
                ↓
          Send Telegram ← Response
```

## Files
| File | Description |
|------|-------------|
| `producao_aula_3.workflow.json` | Complete n8n workflow |
| `credentials_template.json` | Required API keys template |
| `cache.json` | Deployment tracking |
| `README.md` | Full project documentation |

## Status
✅ Exported from paid n8n cloud
✅ Imported to local n8n
⏳ Credentials pending (Cohere API Key, Telegram Bot Token)
