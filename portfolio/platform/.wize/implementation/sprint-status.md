# STATUS ATUAL DO PROJETO & SPRINT DIÁRIA — BRACHATEC

* **Responsável:** Maria Hill (`wize-agent-pm`)
* **Última Atualização:** 2026-09-23
* **Status Geral:** 🟢 NO PRAZO / ENTERPRISE-GRADE ESCALA REAL
* **Fase Atual:** FASE 1 — Mercado, Jornada de Compra e Calibração de Preços

---

## 📌 SNAPSHOT DIÁRIO

* **Dia Atual:** **Dia 10 de 32 (Concluído) → Preparação para o Dia 11**
* **Concluído Hoje (Dias 9 e 10):**
  * Calibração final da Matriz de Preços nos 3 Ramos (Gov IA Enterprise "Sob Consulta / Personalizado", Setor Público R$ 3.900/mês + Setup R$ 9.500 [Lei 14.133], RIG Tech R$ 3.500/mês + Setup R$ 5.900, White-Label R$ 1.350/mês com Setup Isento R$ 0).
  * Construção e ativação do **Simulador de Risco em 60 Segundos** na Home com diagnósticos em tempo real nos 3 idiomas (PT, ES, EN).
  * Conexão direta dos CTAs de planos para o Onboarding do App (`/app/cadastro.html`).
* **Próximo Passo (Dia 11):** Início da **FASE 2** — Criação do `docker-compose.yml` (PostgreSQL 16 Multi-Database + Redis 7) com isolamento total dos 6 bancos.

---

## 🚦 QUADRO KANBAN DA SPRINT

### ✅ Concluído (Dias 1 a 10)
- [X] **Dia 1:** Identidade visual e front-end completo em `site_oficial/`.
- [X] **Dia 2:** Deploy e publicação do site na Cloudflare.
- [X] **Dia 3:** Instalação e configuração do Wize Dev Kit (`.wize/`).
- [X] **Dia 4:** PRD Mestre consolidado com Critérios de Aceite AC-01 a AC-14.
- [X] **Dia 5:** Política Global de Clean Code instalada no projeto e no kit global.
- [X] **Dia 6:** Arquitetura de 6 Microserviços + Database-per-Service e Auditoria Controlador-Operador (LGPD).
- [X] **Dia 7:** Bifurcação no Hero da Home (*Blindar Organização* vs *White-Label*).
- [X] **Dia 8:** Benchmarking de 15 concorrentes consolidado em `.wize/planning/market-benchmark.md`.
- [X] **Dia 9:** Calibração e validação das tabelas de preços e pacotes nos 3 ramos.
- [X] **Dia 10:** Implementação do Simulador de Risco em 60s e linkagem dos CTAs para `/app/cadastro.html`.

### 🔄 Em Andamento (Dia 11)
- [ ] **Dia 11:** Criação do `docker-compose.yml` (PostgreSQL 16 Multi-Database + Redis 7).

### ⏳ Próximos na Fila (Dias 12 a 14)
- [ ] **Dia 12:** Script `init_databases.sql` criando os 6 bancos independentes (`db_identity`, `db_gov_ai`, `db_gov_municipal`, `db_rigtech`, `db_forensic_ledger`, `db_admin_billing`).
- [ ] **Dia 13:** Estrutura base de pastas dos 6 microserviços Python/FastAPI (`services/`).
- [ ] **Dia 14:** Configuração das variáveis de ambiente (`.env.example`) e scripts de health check.
