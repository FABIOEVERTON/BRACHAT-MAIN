# SPEC — Runtime Governance Gate (RGG)

Control plane que limita o estrago de um agente de IA comprometido.
Determinístico nas travas. LLM apenas como classificador de risco, nunca autoridade.

## 1. Problema

- Agentes executam ações com credenciais (bancos, deploy, DB, e-mail).
- Um agente comprometido executa ações MÁXIMAS com a credencial que tem.
- Soluções atuais:
  - Guardrails = contra alucinação, não contra ataque.
  - Aprovação humana = fraca se o humano é inundado (approval fatigue) ou enganado.
  - Sidecar = resolve o roubo da credencial (o agente não segura a chave), mas NÃO resolve:
    a) o quanto a credencial pode destruir (blink radius);
    b) parar a ação no caminho com base no risco do efeito.
- Gap: nenhuma ferramenta entrega limitar + medir + travar juntas.

## 2. Modelo de ameaça

Ator: atacante com controle total do agente (prompt injection persistente, jailbreak, compromise).
Capacidades do atacante:
- Cria instruções que o agente cumpre fielmente.
- Envia qualquer tool call (nome + argumentos).
- Esconde a intenção em passos pequenos (drip campaign): apaga 1 registro por vez, 1000x.

Ameaças fora de escopo deste produto:
- Roubo do próprio control plane (defendemos o agente, não o control plane).
- Comprometimento do host/OS.
- Exfiltração de dados pura por rede (o control plane vê chamadas, não tráfego cru).

## 3. Princípios de design

1. Não-bypassable: toda ação do agente passa pelo gate; não existe caminho alternativo.
2. Determinismo nas travas: autorização é decidida por regras (código), não por LLM.
3. Menor privilégio dinâmico: a credencial efetiva é derivada por tarefa, não fixa no processo.
4. Blink radius conhecido: toda credencial tem uma "ficha de dano" pré-computada.
5. Evidência replayable: todo efeito é registrado de forma imutável e reproduzível.
6. Fracasso fechado: se o gate não consegue decidir, nega.
7. Aprovação humana só quando o risco passa do limiar; nunca para o risco alto máximo.

## 4. Decisões de projeto

- FERRAMENTA (control plane), não agente.
- Linguagem: Python (ecossistema MCP, produtividade, manutenibilidade pelo autor).
- Protocolo: MCP (intercepta tools/call); também expõe HTTP para agentes não-MCP.
- Persistência: SQLite (registro de evidência) + arquivos de policy versionados (YAML).
- LLM: apenas no classificador de risco (avaliação heurística auxiliar), sem poder de autorizar.

## 5. Arquitetura

```
        AGENTE (MCP client)
             |
      tools/call ------+
                       v
        +---- RGG GATE (sidecar/control plane) ----+
        | 1. Intercept  (recebe tool call)         |
        | 2. Resolve    (mapa nome->efeito)        |
        | 3. Score      (risco do efeito)          |
        | 4. Enforce    (policy -> allow/deny/approve) |
        | 5. Act        (executa com credencial derivada) |
        | 6. Record     (evidência imutável)       |
        +----------------+------------------------+
                         |
        executor externo (tool real: banco, API, FS, cmd)
```

Componentes:

### A. Registry (inventário de efeitos)
- Mapa declarativo: `tool_name -> effect`.
- Efeito = { id, kind, resources[], irreversible?, cost_model }.
- Exemplos de kinds: `read`, `write`, `delete`, `transfer`, `exec`, `network`, `identity`.
- O registry é a fonte para o blink radius (sem ele, não há medição).

### B. Blink Engine (medir)
- Para cada credencial/capacidade: ficha de dano pré-computada.
  - `max_damage_estimate` (o que o pior uso legítimo destrói).
  - `irreversible?` (delete destrutivo vs. inserção).
  - `spread` (quantos recursos atingíveis: rows, buckets, contas).
- Em runtime: um tool call é traduzido em efeito; o efeito é pontuado.

### C. Policy Engine (travar)
- Regras determinísticas (YAML): allow/deny/approve, por efeito/kind/resource/limiar.
- Modos: `enforce` (trava de verdade), `observe` (registra mas não trava), `dry-run`.
- Após N negações do mesmo padrão: escalate (bloqueia toda a categoria).

### D. Credential Broker (limitar)
- O gate SEGURA as credenciais; o agente nunca as vê.
- Cada execução usa um "token derivado" com escopo da tarefa.
- Fallback: se a tool real só aceita credencial global, o gate roda executor sandbox
  (containers) com a credencial injetada apenas no sandbox.
- Anti-drip: limite de taxa por recurso/kind por janela (ex.: máx. 50 deletes/hora).

### E. Human Loop
- `approve` entra numa fila (Telegram/Web). Timeout de aprovação curto (ex.: 60s).
- Rejeição grava motivo. Aprovação é scoped (uma execução, não "sempre").

### F. Ledger (evidência)
- SQLite imutável (append-only, hash chain por bloco).
- Registra: tool call, hash, efeito, decisão, quem (agent/id), credencial derivada, resultado.
- Export replayable: o log reproduz exatamente a sequência de efeitos.

## 6. Modelo de dados

```
tool_call     { id, agent_id, tool, args, ts, nonce }
effect        { id, kind, resources[], irreversible, max_damage, cost }
decision      { id, tool_call_id, outcome: allow|deny|approve, reason, rule_id }
execution     { decision_id, credential_scope, result_hash, executor }
ledger_entry  { block_id, prev_hash, tool_call, effect, decision, execution }
policy        { id, version, rules[] }   # YAML versionado
credential    { id, name, scope, damage_card, holder: gate_only }
```

## 7. Blink radius na prática

1. Onboarding: ao registrar uma credencial, o operador declara a ficha de dano:
   `damage_card: { kind: delete, resources: ["DB.prod.orders"], irreversible: true, max_damage: "all_orders" }`.
2. Registry: mapeia `delete_order` -> efeito `{ kind: delete, resources:["DB.prod.orders"], irreversible: true }`.
3. Blink: cada `delete_order` em produção = risco ALTO -> requer approve; janela 50/hora.
4. Se o agente for tomado: mesmo com a tool certa, o atacante esbarra em
   (a) credencial derivada só para `orders` (não acessa `users`), e
   (b) limiar de risco + taxa que param o drip.

## 8. Fluxo de uma ação

1. Agente chama `tools/call delete_order({id: 42})`.
2. Gate intercepta; Registry resolve -> efeito {kind: delete, irreversible: true}.
3. Blink Engine pontua: risco alto.
4. Policy Engine: regra diz `delete + irreversible + prod => approve`.
5. Fila humana: notifica Telegram, aguarda 60s.
6. Humano aprova (scoped a esta execução).
7. Broker emite credencial derivada `orders:delete:1` por 30s.
8. Executor roda a tool real com a credencial.
9. Ledger grava bloco. Resultado hashado.
10. Se 10 aprovações de delete em 1h -> escalate: nega a categoria até reset manual.

## 9. API

```
POST /call            { agent_id, tool, args }  -> decision+result
GET  /policies         lista policies
PUT  /policies         atualiza (versiona)
GET  /ledger?since=     evidência
POST /approve/{id}     aprova decisão pendente
POST /deny/{id}        rejeita com motivo
POST /credentials      registra credencial + damage_card
GET  /blink/{credential}  retorna ficha de dano
GET  /risk/{tool_call}     retorna score sem executar (what-if)
```

## 10. Integração

- Modo primário: MCP — o gate é um MCP server "middleware"; o agente aponta para o gate
  e o gate encadeia para o MCP server real. (Ex.: agent -> RGG -> tool_server).
- Modo HTTP: para agentes próprios (ezra_bot, parashat), wrapper de 10 linhas que envia
  a chamada ao gate.
- Compatível com qualquer LLM: o gate não conhece modelo; vê só tool calls.

## 11. Auditoria

- Ledger com hash chain; integridade verificável (`check-ledger`).
- Relatório de "últimas N decisões" para revisão humana.
- Métricas: taxa de negação, latência de aprovação, picos de efeitos destrutivos.

## 12. Limites explícitos (o que NÃO é)

- Não é firewall de rede nem DLP de tráfego.
- Não protege o control plane em si (assume-se host confiável).
- Não remove a necessidade de credentials corretas na tool real.
- Aprovação humana é fraco se o humano não revisa — o produto diminui a frequência,
  não elimina a necessidade.

## 13. Roadmap

- Fase 0 (esta semana): registry + policy engine + ledger, modo dry-run, tests.
  Entrega: exemplo com uma tool de exemplo (ex.: delete_order fake).
- Fase 1: MCP server real (intercept + forward), credential broker com escopo,
  blink engine com fichas declaradas.
- Fase 2: human loop via Telegram, anti-drip, escalação.
- Fase 3: conectar a um bot real (parashat ou ezra) em modo observe; demo público.
- Fase 4 (se der certo): executor sandbox, ledger replay tool, relatórios.

## 14. Métricas de sucesso

- Demo: 2 cenários — (1) ação legítima passa; (2) agente "comprometido" tenta
  drip-delete 1000 registros e é barrado (taxa + escopo + limiar).
- Portfólio: o spec + demo se transformam no estudo de caso do posicionamento
  "AI Governance Lead".
- Zero LLM nas decisões de autorização (determinismo verificável).

## 15. Apresentação (portfólio)

- README curto: problema, ameaça, arquitetura (ASCII), demo.
- Vídeo/transcrição: ataque simulado barrado em tempo real.
- Reaproveitar material: debate com James W. Niu + axiomas de John Willis como
  referências externas citadas no README (linkbacks de autoridade).
