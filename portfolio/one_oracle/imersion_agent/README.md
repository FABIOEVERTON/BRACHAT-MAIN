<div align="center">
  <h1>ONE Imersion Agent — HR Buddy</h1>
  <p><strong>AI Agent built during Oracle Next Education (ONE) Imersion 2026</strong></p>
  <p>n8n · Cohere · Telegram · RAG · MySQL</p>
</div>

---

**HR Buddy** is an intelligent AI agent developed during the Oracle Next Education (ONE) Imersion — a free 5-day program by Oracle in partnership with Alura and FIAP. The agent acts as a virtual HR assistant for **ChocolaTech**, answering employee questions about HR policies, vacation balances, and time banks using RAG (Retrieval-Augmented Generation) and structured database queries.

---

## ONE Oracle Next Education 2026

The [ONE](https://www.oracle.com/br/education/oracle-next-education/) is Oracle's free capacitation program (10th edition, 2026) with 32,000 scholarships across Latin America.

| Phase | Duration | Content |
|-------|----------|---------|
| **Imersion** | 1 week (15-19 Jun) | Build first AI Agent — RAG, n8n, Telegram, MySQL |
| **Cursos Tech** | 9 weeks | n8n, LangChain, LangGraph, OCI, Agents |
| **Certification** | 7 weeks | OCI AI Foundation Associate prep |
| **Hackathon** | 6 weeks | Multi-country project |

This agent is the **final project from Class 3** of the Imersion phase — a complete AI Agent connected to Telegram, with memory, RAG vector store, and MySQL integration.

---

## Agent Architecture

```
Telegram User → Telegram Trigger → AI Agent (HR Buddy)
                                        ↓
                            ┌───────────┼───────────┐
                            ↓           ↓           ↓
                      Cohere Chat    Simple     Simple Vector
                        Model        Memory     Store (RAG)
                                                   ↓
                                              Embeddings
                                               Cohere
                                        ↓
                                  Send a text message
                                        ↓
                                 Telegram User ← Reply
```

### Nodes
| Node | Type | Purpose |
|------|------|---------|
| Telegram Trigger | `n8n-nodes-base.telegramTrigger` | Listens for incoming Telegram messages |
| AI Agent | `@n8n/n8n-nodes-langchain.agent` | Core agent with HR Buddy system prompt |
| Cohere Chat Model | `@n8n/n8n-nodes-langchain.lmChatCohere` | LLM provider (Cohere) for responses |
| Simple Memory | `@n8n/n8n-nodes-langchain.memoryBufferWindow` | Session memory per Telegram chat |
| Simple Vector Store | `@n8n/n8n-nodes-langchain.vectorStoreInMemory` | RAG knowledge base (currently disabled) |
| Embeddings Cohere | `@n8n/n8n-nodes-langchain.embeddingsCohere` | Embedding model for RAG |
| Send a text message | `n8n-nodes-base.telegram` | Sends AI response back to user |

---

## System Prompt (AI Agent)

The agent follows strict HR guidelines:

- **Language**: Portuguese only
- **Scope**: HR-related questions only (filter out off-topic)
- **Identity**: If the user does not identify themselves, asks for full name
- **MySQL Tool**: Searches the `funcionarios` table by full name for vacation/time bank balances
- **Fallback**: If employee not found, answers based on general HR policies from the Vector Store knowledge base

---

## Files in this package

| File | Description |
|------|-------------|
| `README.md` | This file — project overview for recruiters |
| `producao_aula_3.workflow.json` | Complete n8n workflow export (nodes, connections, settings) |
| `credentials_template.json` | Required credentials template (Cohere API, Telegram Bot Token) |
| `cache.json` | Lifecycle tracking — export, import, and deployment status |
| `one_imersion_agent.md` | AI Agent system file for Brachat ecosystem integration |

---

## How to run locally

### Prerequisites
- n8n installed (v2.8.4+) — local instance at `http://localhost:5678`
- Cohere API key
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))

### Steps
1. Import the workflow:
   ```bash
   npx n8n import:workflow --input=producao_aula_3.workflow.json
   ```
2. Create credentials at `http://localhost:5678/home/credentials`:
   - **Cohere account**: paste your Cohere API key
   - **Telegram account**: paste your Bot Token
3. Open the workflow in the n8n editor
4. Connect credentials to each node
5. Activate and test via Telegram

---

## Tech Stack

| Technology | Use |
|------------|-----|
| **n8n** | Workflow automation & agent orchestration |
| **Cohere** | LLM (chat + embeddings) |
| **Telegram API** | User interface / messaging channel |
| **RAG (Vector Store)** | Knowledge base for HR policies |
| **MySQL** | Employee data (vacation, time bank) |
| **ONE Program** | 23-week Oracle + Alura + FIAP capacitation |

---

## Status

✅ Exported from paid n8n cloud  
✅ Imported to local n8n instance  
⏳ Credentials pending (Cohere + Telegram)  
❌ Vector Store disabled (awaiting MySQL + document ingestion)

---

*Built during Oracle Next Education Imersion 2026 — Class 3: "Product real: AI agents with Telegram and automation"*
