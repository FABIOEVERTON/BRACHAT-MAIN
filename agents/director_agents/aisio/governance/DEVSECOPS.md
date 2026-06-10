# DevSecOps & Commit Boundary Governance

## AGCP-style Commit Boundary Architecture

Cada commit (git ou ação de agente) passa por validação governada antes de executar:

```
SUBMIT → SCHEMA VALIDATION → SIGNATURE CHECK → POLICY EVALUATION → 
CONSTRAINTS → INVARIANTS → HITL? → AUTHORIZE/REJECT → COMMIT
```

## Git Governance (pre-commit hook)

### What runs before every git commit
1. **Security scan** — secrets, credentials, tokens no código
2. **Policy check** — arquivos <200 linhas (MVI), sem hardcoded secrets
3. **Agent compliance** — AGENT.md <60 linhas, Harness pattern presente
4. **License check** — dependências com licenças compatíveis
5. **Audit trail** — commit message deve referenciar governance ticket se aplicável

### Pre-commit rejection codes (AGCP-style)
| Code | Motivo |
|------|--------|
| SCHEMA_INVALID | Config fora do schema |
| SIGNATURE_MISSING | Committer não autorizado |
| POLICY_VIOLATION | MVI >200 linhas ou prompt >60 |
| CONSTRAINT_VIOLATION | Secret hardcoded |
| INVARIANT_VIOLATION | Harness pattern ausente |

## Governance Flow

```
Desenvolvedor/Agente
    │
    ▼
[SUBMIT] → Aísio avalia ação
    │
    ├── SCHEMA → formato, campos obrigatórios
    ├── SECURITY → assinatura, autenticação
    ├── TENANT → escopo permitido
    ├── POLICY → compliance framework
    ├── CONSTRAINTS → limites operacionais
    ├── INVARIANTS → regras estruturais
    ├── HITL? → approval gate se >R$500
    │
    ▼
[AUTHORIZED] → ação executada
    │
    ▼
[COMMIT] → ledger append + audit trail
    │
    ▼
[QILIS TRACE] → interpretabilidade do lifecycle
```

## Scripts
- `governance/hooks/pre-commit` — git hook
- `governance/boundary.sh` — AGCP-style commit validation CLI
- `governance/audit.sh` — gera relatório de auditoria do ledger

## Ledger Structure
Cada ação gera um entry no `assistant_agents/.opencode/governance-ledger.jsonl`:
```json
{"action_id":"...","sequence":1,"state":"AUTHORIZED","tenant":"daily/ingles","timestamp":"...","evidence":"..."}
```

## Kill Switch
Aísio pode emitir um governance block que impede commits de agentes específicos ou do sistema inteiro. O block é registrado no ledger e propagado via `Branding/governance/blocks.json`.
