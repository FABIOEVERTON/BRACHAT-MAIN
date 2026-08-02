---
name: memory-management
id: S20
cluster: memoria
description: Gere gerenciamento autonómo de memória entre sesse de curto e longo prazo usando mem0, com captura automática, compressão e injeção no boot.
---

### When
- No **final de toda interação** (captura + compressão)
- No **boot de toda sessão** (recuperação + injeção)
- Quando uma **decisão ou observação relevante** ocorre

### How

#### Boot (SessionStart)

1. Buscar clusters relevantes no mem0 via API direta:
   - `GET https://api.mem0.ai/v1/memories/?user_id=mem0-mcp` com filtro de tags `cluster:*`
   - Se resultado vazio → cold start
2. Agrupar resultados por cluster tag. Para cada cluster com relevância > 0.3, carregar o resumo do cluster
3. Injetar: "Clusters de sessões anteriores: [cluster: resumo]"

#### Durante a Sessão

Para cada **decisão**, **descoberta**, ou **observação relevante**:
- `mem0_add_memory(text="[cluster:<nome>] [tipo] resumo comprimido")`
- Anexar `cluster` nas tags do metadata: `tags: ["cluster:<nome>", "tipo"]`

Clusters agrupam memórias relacionadas para recuperação por lote.

Critério de relevância:
- Decisão arquitetural
- Mudança de rota/governança
- Preferência do usuário
- Bloqueador encontrado
- Bug ou workaround

#### Final da Interação (SessionEnd - hooks comportamentais)

1. **Compressão**: resumir a interação em 2-3 frases
2. **Salvar no mem0**:
   ```
   mem0_add_memory(text="[data] [tipo] [summary comprimido]")
   ```
3. **Tokens economizados**: NÃO salvar o raw transcript — só o resumo

#### Progressive Disclosure (4 camadas)

| Camada | O que contém | Quando carrega |
|---|---|---|
| **Cluster** | Nome do cluster + data range | Boot (busca por tag `cluster:*`) |
| **Índice** | Título + data + tipo | Ao acessar um cluster |
| **Resumo** | 2-3 frases do fato | Ao referenciar um índice |
| **Detalhe** | Raw completo | Só se o usuário pedir |

#### Estrutura de cada memória

```
[cluster:<nome>] [tipo] [data] [brevíssimo contexto]
```
Tipos:
- `[decisao]` - escolha arquitetural ou de rota
- `[progresso]` - avanço em tarefa
- `[bloqueador]` - impedimento encontrado
- `[preferencia]` - preferência do usuário
- `[contexto]` - observação geral

Metadata tags obrigatórias: `tags: ["cluster:<nome>", "<tipo>"]`

#### Token Budget

| Operação | Tokens estimados |
|---|---|
| Boot: search (5 results) | ~200-400 |
| Save: add_memory (resumo) | ~50-100 |
| Durante: add_memory decisão | ~30-80 |

Total: **menos de 500 tokens por sessão** — contra ~5000 do antigo state.json.

### Política de Retenção

Faço `mem0_search_memories` periodicamente e se mais de **30 dias** sem uso, apago com `mem0_delete_memory`:

| Critério | Ação |
|---|---|
| `[progresso]` concluído há > 30 dias | Apagar |
| `[decisao]` implementada há > 60 dias | Apagar |
| `[bloqueador]` resolvido há > 14 dias | Apagar |
| `[contexto]` com > 30 dias sem referência | Apagar |
| `[preferencia]` | **Nunca apagar** (são regras do usuário) |

Também **consolidar**: a cada 30 dias, se houver mais de 20 memórias do mesmo assunto, comprimo tudo num único resumo mensal e apago as individuais via `mem0_delete_memory`.

### Safety
- Não salvar PII ou secrets no mem0
- Não salvar transcrições brutas — só resumos comprimidos
- mem0 é cloud → assumir que dados saem da máquina
- Se mem0 falhar (erro na chamada), falhar silenciosamente sem bloquear a sessão
