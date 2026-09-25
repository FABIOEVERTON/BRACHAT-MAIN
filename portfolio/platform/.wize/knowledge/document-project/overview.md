# Overview do Sistema (Baseline Brownfield)

**Data de Registro:** 2026-09-24
**Status Atual:** O site de marketing (vitrine) está avançado e funcional. O esqueleto do backend e infraestrutura foi inicializado. Nenhuma modificação nos arquivos operacionais foi realizada por este registro.

## Estrutura Real Atual
- **frontend/site_oficial/**: Contém a vitrine completa.
  - `app/`: Telas de login, cadastro, dashboard.
  - `aigovernance/`, `publicsector/`, `rigtech/`, `academy/`: Páginas dos ramos de produto.
- **backend/**: Possui `requirements.txt` e a estrutura de pastas vazias (`gov_ai/`, `gov_muni/`, `rig_tech/`, `shared/`).
- **infra/**: Contém `docker-compose.yml` para banco de dados.
- **docs/**: Contém os PDFs de referência.
- **.wize/**: Diretório do Wize Dev Kit com planejamento, solução e implementação (ADRs, EPICs, PRD, Arquitetura).
