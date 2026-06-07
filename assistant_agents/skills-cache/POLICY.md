# Skills Cache — Política de Economia de Tokens

## Princípio
1.465 skills disponíveis (312MB). Zero carregadas em contexto por padrão.

## Regras

1. **SEMPRE carregar**: `skills-cache/active-index.json` (~4KB) — nomes, descrições e categorias das skills + agentes ativos.

2. **NUNCA carregar**: `skills-cache/master-index.json` (549KB) ou qualquer `SKILL.md` individual, a menos que seja explicitamente necessária para a tarefa atual.

3. **Sob demanda**: Quando uma skill for necessária:
   - `grep` no `master-index.json` para encontrar a skill certa por nome/tag
   - Ler APENAS o `SKILL.md` da skill específica
   - Descartar do contexto após uso

4. **Governança**: `shared/governance/` — 5 arquivos (15KB total). Carregados no início da sessão (passo 8 do protocolo).

5. **Agentes BRACHÁT**: 18 agentes listados no active-index. Cada um tem seu `AGENT.md` individual (<200 linhas). Carregados apenas quando o orquestrador faz dispatch para eles.

## Pipeline de decisão
```
Tarefa chega → active-index.json → skill necessária? 
  → SIM: grep master-index.json → read SKILL.md → executa → descarta
  → NÃO: executa com contexto atual
```
