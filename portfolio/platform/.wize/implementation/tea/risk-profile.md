---
gate: risk
status: PASS
score: 82
created_at: 2026-09-18T12:30:00Z
findings:
  - id: R-1
    area: "WORM — Object Lock COMPLIANCE em LocalStack vs AWS"
    probability: medium
    impact: high
    rationale: "Se o comportamento do Object Lock divergir entre LocalStack (dev) e AWS (prod), a imutabilidade prometida em contrato pode falhar em produção. Validade jurídica depende da deleção bloquear SEMPRE."
    mitigation: "Teste de deleção automatizado no CI contra LocalStack E stage AWS (S07, S10). Script verify_worm faz put/head/delete e exige delete FAIL. Também configura AWS Config rule no ephemeral."
    owner: shuri + tony
    verified_when: story E0-S07 + E0-S10 + pre-launch
  - id: R-2
    area: "Cadeia SHA-256 — corrida na escrita de laudos por tenant"
    probability: medium
    impact: high
    rationale: "Se dois laudos do mesmo tenant forem emitidos concorrentemente, ler o último chain_hash pode produzir hashes fora de ordem — quebrando a cadeia probatória silenciosamente."
    mitigation: "Serialização da emissão por tenant (lock/transaction na leitura+escrita do chain_hash). Teste de concorrência (2 emits paralelos → cadeia consistente verificável). AMD com HITL para reencadeamento."
    owner: shuri
    verified_when: story E0-S05 + E0-S06
  - id: R-3
    area: "Migrations schema-per-tenant sob carga"
    probability: medium
    impact: high
    rationale: "Aplicar migration em N schemas de tenant pode travar ou ficar parcial. Um schema atualizado e outro não gera divergência de esquema invisível."
    mitigation: "Migrations idempotentes e transacionais por schema; canary em staging; script de verificação de versão por schema (audit). PRD §11.2 cross-tenant test cobre o residual."
    owner: tony
    verified_when: story E0-S04 + pre-launch
  - id: R-4
    area: "Auth RBAC — matriz de permissões vazando entre ramos"
    probability: low
    impact: high
    rationale: "Roles/permissions compartilhados entre gov_ai e gov_municipal: um usuário de um ramo pode herdar permissão indevida se a matriz não for validada por tenant+branch."
    mitigation: "Matriz RBAC testada por combinação (role × permission × branch). Teste negativo para cada permissão não concedida. Revisão da matriz no epic NFR gate."
    owner: shuri + hawkeye
    verified_when: story E0-S03 + epic E0 gate NFR
  - id: R-5
    area: "Fila SQS/jobs — idempotência e duplicação de laudo"
    probability: medium
    impact: high
    rationale: "Se um job for reprocessado (retry/at-least-once) e emitir laudo duas vezes, o tenant recebe laudo duplicado e a cadeia de custódia registra estado indevido."
    mitigation: "Dedup key por job_id na emissão; worker idempotente (busca job_id antes de emitir). Teste de entrega duplicada (2x processar mesmo job → 1 laudo)."
    owner: shuri
    verified_when: story E0B-S02
  - id: R-6
    area: "White-label — signatário errado em laudo"
    probability: low
    impact: medium
    rationale: "Se a config white-label não for resolvida corretamente no momento da emissão, o laudo pode sair com signatário EZRA em vez do operador — invalida o laudo para o cliente final."
    mitigation: "Teste de emissão sob white-label (S08 F0-33) com fixture de operador; asserts no signatário; uso do mesmo resolveTenant do request (impossível divergir por construção)."
    owner: shuri
    verified_when: story E0-S08
  - id: R-7
    area: "Soberania sa-east-1 — recurso criado fora da região"
    probability: low
    impact: high
    rationale: "Um recurso (S3, RDS, ECS) criado sem região explícita pode cair em outra região e violar LGPD Art. 33 sem alerta."
    mitigation: "Terraform com região fixa e cláusula de não-região; AWS Config rule (s3 bucket região ≠ sa-east-1 → alerta); infra check no CI (E0-S10)."
    owner: tony
    verified_when: story E0-S10 + pre-launch
---

# TEA Risk Profile — Plataforma EZRA

Matriz probability × impact do núcleo da plataforma. **Alta** probabilidade de impacto regulatório/data-loss inverte a ordem de teste: a imutabilidade WORM e a cadeia SHA-256 não são "features", são o produto jurídico — testam-se PESSIMISTICAMENTE (provar que a falha NÃO acontece).

## Matrix

| | Impact LOW | Impact MEDIUM | Impact HIGH |
|---|---|---|---|
| **Prob HIGH** | — | — | — |
| **Prob MEDIUM** | — | R-6 | R-1, R-2, R-3, R-5 |
| **Prob LOW** | — | — | R-4, R-7 |

## Top-3 (drive test design)

1. **R-1** — WORM COMPLIANCE divergence LocalStack/AWS. Verificação pré-launch mandatória + CI em todas as runs.
2. **R-2** — Corrida na cadeia SHA-256. Teste de concorrência na emissão por tenant.
3. **R-5** — Idempotência de jobs (laudo duplicado). Dedup key obrigatório, teste de entrega duplicada.

## Documentação gap

Repo é greenfield com PRD completo como fonte — sem risco de baseline órfão. `knowledge/document-project/` quick-only gerado; sem marcadores `_(To be generated)_` relevantes.

## O que isto significa para `tea-design.md`

- **E0-S07 (WORM):** 1 unit store, 1 integration delete-blocked (CRÍTICO — LocalStack), 1 perf smoke. CI reforça com script aws cli.
- **E0-S06 (chain):** 1 unit âncora, 1 unit encode, 1 integration sequência, 1 script verificação externa + 1 teste de concorrência (2 emits paralelos).
- **E0B-S02 (jobs):** 1 unit JobResponse, 4 integration (ciclo, falha, idempotência, webhook) com foco em duplicação.
- **E0-S03 (RBAC):** matriz completa role×permission×branch — teste negativo para cada não-concessão.
- **E0-S04 (tenant):** isolamento cross-tenant é o teste de maior valor — prova que A não vê B.
- Demais stories seguem split default 70/20/10.

## Hand-off

> Risk profile em `.wize/implementation/tea/risk-profile.md`. Top-3: R-1, R-2, R-5. Shuri: teste pessimista no WORM e na cadeia. Tony: canary de migrations multi-schema no staging.