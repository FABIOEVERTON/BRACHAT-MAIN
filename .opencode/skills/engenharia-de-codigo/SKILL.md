---
name: engenharia-de-codigo
id: S32
cluster: arquitetura
description: Protocolo determinístico de engenharia de código para escrever, corrigir, revisar ou refatorar qualquer código, com SPEC, contratos de tipos, mapeamento de caminhos e auto-revisão adversarial.
---

# Code Engineering — Protocolo Determinístico

Protocolo determinístico de engenharia de código para agentes que operam com múltiplos LLMs. Use esta skill **SEMPRE** que for escrever, corrigir, revisar ou refatorar qualquer código — independentemente da linguagem, framework ou tamanho do arquivo.

**Aciona obrigatoriamente em**: "escreva um plugin", "corrija este código", "implemente X", "refatore Y", "crie um módulo", "adicione uma função", "revise este arquivo".

**Nunca escreva código sem seguir esta skill.**

Esta skill define os caminhos obrigatórios que qualquer agente deve percorrer para produzir código correto, auditável e sem regressões. É derivada da análise forense dos erros reais cometidos em `memory-core.ts` e `memory-persistence.ts`.

## Por que agentes erram código

Os erros abaixo foram observados diretamente. Cada um mapeia para uma fase obrigatória desta skill.

| Erro observado | Causa raiz | Fase que previne |
| :--- | :--- | :--- |
| `Array.isArray(state.audit)` guardando um objecto | Condição escrita sem verificar o invariante do tipo | FASE 3 — Contratos |
| `readState` chamado duas vezes em `dailyZeroIfDue` | Posse do estado não mapeada antes de delegar | FASE 4 — Caminhos |
| `Record<string, any>` em todas as assinaturas | Tipagem adiada e nunca refinada | FASE 3 — Contratos |
| `readState` lançava em primeiro arranque | Caminho "estado ausente" não executado mentalmente | FASE 4 — Caminhos |
| `.catch(() => {})` silenciando falhas | Caminho de falha não modelado | FASE 4 — Caminhos |
| `type: "user"` lendo `output.parts` do assistente | Assinatura do hook não lida antes de assumir fonte | FASE 2 — Dependências |
| Campos `"pending"` e `token_cost: 0` nunca substituídos | Spec não definiu o que cada campo deve conter | FASE 1 — SPEC |
| Estado inicializado externamente sem documentação | Responsabilidade de inicialização não especificada | FASE 1 — SPEC |

## Estrutura do protocolo

```
FASE 0 — Parar e ler
FASE 1 — Especificação (SPEC)          ← obrigatória antes de qualquer código
FASE 2 — Mapear dependências externas
FASE 3 — Definir contratos de tipos
FASE 4 — Mapear todos os caminhos de execução
FASE 5 — Escrever o código
FASE 6 — Auto-revisão adversarial
FASE 7 — Entrega
```

Nenhuma fase pode ser pulada. Se uma fase bloqueante não puder ser concluída (ex.: arquivo ausente), declarar o bloqueio explicitamente antes de prosseguir com assunções marcadas como `TODO:UNVERIFIED`.

A **FASE 1 (SPEC)** é a porta de entrada para todo o trabalho de implementação. Nenhuma linha de código é escrita antes da spec estar completa e validada.

---

## FASE 0 — Parar e ler

Antes de escrever qualquer linha de código:

### 0.1 — Inventariar o que existe

- Listar todos os arquivos mencionados ou referenciados pelo código a ser escrito.
- Para cada arquivo: está disponível? Foi lido integralmente?
- Se não está disponível: declarar explicitamente o que é desconhecido.

### 0.2 — Identificar o tipo de tarefa

| Tipo | Definição | Ação obrigatória |
| :--- | :--- | :--- |
| NOVO | Arquivo não existe | Executar FASES 1 → 7 completas |
| CORRECÇÃO | Bug identificado em código existente | Ler o arquivo completo antes de qualquer edição |
| ADIÇÃO | Nova função/módulo em base existente | Ler todos os arquivos que a adição vai tocar |
| REFACTOR | Mudança estrutural sem mudança de comportamento | Mapear todos os chamadores antes de alterar assinaturas |

### 0.3 — Declarar o que não foi lido

Se qualquer dependência está ausente, escrever explicitamente:

```
BLOQUEIO: [nome do arquivo] não disponível.
Assunções feitas: [lista].
Risco: [o que pode estar errado se as assunções falharem].
```

---

## FASE 1 — Especificação (SPEC)

Nenhum código é escrito antes desta fase estar completa. A spec é o contrato entre o que foi pedido e o que será implementado. Erros de spec geram código correto para o problema errado.

### 1.1 — O que este código deve fazer (comportamento observável)

Descrever em linguagem natural, sem código:

- Qual é a entrada? (tipos, formato, restrições)
- Qual é a saída? (tipos, formato, restrições)
- O que acontece em cada caso de erro?
- Quem é o chamador? (outro módulo, hook de framework, CLI, teste)

Formato obrigatório:

```
SPEC: [nome da função/módulo]
ENTRADA:  [descrição]
SAÍDA:    [descrição]
ERROS:    [o que cada tipo de falha deve produzir]
CHAMADOR: [quem usa isto e como]
```

### 1.2 — Responsabilidades e fronteiras

Para cada função ou módulo a ser criado, declarar explicitamente:

- O que é responsabilidade DESTA função?
- O que NÃO é responsabilidade desta função (delegado para onde)?
- Quem é dono do estado compartilhado?

Exemplo do erro real — responsabilidade não declarada:

```
PROBLEMA: dailyZeroIfDue era dona do estado mas delegava para appendEpisodic
          que também lia e escrevia o mesmo estado.
          Nenhum dos dois tinha a responsabilidade documentada.

SPEC CORRETA:
  dailyZeroIfDue: DONA do estado durante sua execução.
  Responsabilidade: ler uma vez, modificar em memória, escrever uma vez.
  appendEpisodic: NÃO deve ser chamada internamente — inline a modificação.
```

### 1.3 — Campos de dados: o que cada um significa

Para cada campo de struct, interface ou objeto de configuração:

- Qual é o tipo concreto?
- Qual é o valor em estado vazio/inicial?
- Como é calculado? (quem o preenche, quando, com qual fonte)
- O que significa se estiver vazio/zero/null?

Exemplo do erro real — campos sem spec:

```
PROBLEMA: state_hash_before e state_hash_after foram escritos como "pending"
          porque a spec nunca definiu o que esses campos devem conter.

SPEC CORRETA:
  state_hash_before: string — SHA-256 truncado (16 chars) do estado antes da operação.
                     Calculado em: tool.execute.after, antes de chamar a ferramenta.
                     Fonte: hashState({ tool, sessionID, phase: "before" })
  state_hash_after:  idem, com phase: "after", calculado após execução.
  token_cost:        number — custo em tokens da operação.
                     Fonte: exposta por memory-core via API (não disponível ainda).
                     Valor enquanto não disponível: 0 com TODO:UNVERIFIED explícito.
```

### 1.4 — Inicialização e primeiro arranque

Para qualquer módulo que persiste estado:

- Quem cria o estado inicial? (este módulo? um módulo externo? o usuário?)
- O que acontece se o estado não existir quando este código rodar?
- A função deve auto-inicializar ou lançar?

Regra: se a função pode ser a primeira a rodar, deve auto-inicializar. Se depende de estado externo, deve declarar explicitamente esse pré-requisito.

Exemplo do erro real — inicialização não especificada:

```
PROBLEMA: readState lançava se state.json não existia.
          Não havia spec definindo quem criava o arquivo inicial.

SPEC CORRETA:
  readState: se state.json ausente → criar com emptyState() e retornar.
             Responsabilidade: auto-inicialização no primeiro arranque.
             Pré-requisito: nenhum — deve funcionar em ambiente zerado.
```

### 1.5 — Checklist da SPEC antes de avançar

- [ ] Entrada e saída de cada função estão descritas?
- [ ] Responsabilidade de cada função está delimitada?
- [ ] Dono do estado compartilhado está declarado?
- [ ] Cada campo de dados tem: tipo, valor inicial, fonte, semântica de vazio?
- [ ] Comportamento em primeiro arranque está definido?
- [ ] Comportamento em cada tipo de erro está definido?
- [ ] Quem chama cada função está identificado?

---

## FASE 2 — Mapear dependências externas

Para cada import, SDK, hook ou API externa usada:

### 2.1 — Verificar assinaturas reais

Nunca assumir parâmetros de memória. Para cada função chamada de módulo externo:

- Qual é o tipo de retorno?
- Quais parâmetros são obrigatórios?
- A função é síncrona ou assíncrona?
- O que ela faz quando falha?

Exemplo do erro real:

```typescript
// ERRADO — assinatura assumida
flushMem0(root).catch(() => {})  // o que flushMem0 retorna? Promise<number>? void?

// CORRETO — assinatura verificada primeiro
// flushMem0(root: string): Promise<number>  ← lida em memory-core.ts
// Retorna número de entradas enviadas. Rejeita se fetch falhar.
flushMem0Safe(root)  // wrapper com log de falha explícito
```

### 2.2 — Verificar semântica de hooks

Para qualquer hook de framework/SDK:

- Quem chama este hook? (framework, usuário, sistema)
- O que input contém? O que output contém?
- Os dados em output são do assistente, do usuário, ou do sistema?

Exemplo do erro real:

```typescript
// ERRADO — semântica assumida
"chat.message": async (_input, output) => {
  appendShortTerm(root, { type: "user", ... })  // ERRADO: output = resposta do assistente
}

// CORRETO — após verificar contrato do hook
appendShortTerm(root, { type: "assistant", ... })
```

### 2.3 — Verificar comportamento em estado ausente

Para qualquer função que lê estado persistido (arquivo, banco, cache):

- O que acontece se o arquivo/recurso não existe?
- Lança exceção? Retorna null? Retorna valor padrão?
- O chamador trata esse caso?

Exemplo do erro real:

```typescript
// ERRADO — lança em primeiro arranque
export function readState(root: string) {
  if (!existsSync(p)) throw new Error(`state.json nao existe: ${p}`)
}

// CORRETO — inicializa em primeiro arranque (conforme SPEC 1.4)
export function readState(root: string): AppState {
  if (!existsSync(p)) {
    const initial = emptyState()
    writeFileSync(p, JSON.stringify(initial, null, 1) + "\n", "utf-8")
    return initial
  }
  return JSON.parse(readFileSync(p, "utf-8")) as AppState
}
```

---

## FASE 3 — Definir contratos de tipos

### 3.1 — Nunca usar `any` como tipo de trabalho

`Record<string, any>` e `any` são proibidos em assinaturas públicas. São permitidos apenas em cast temporário com comentário explicando por que e com `TODO:` para remoção.

```typescript
// PROIBIDO em assinatura pública
export function readState(root: string): Record<string, any>

// OBRIGATÓRIO — derivado da SPEC 1.3
export interface AppState {
  memory: StateMemory
  audit: { events: unknown[] }
  session?: { last_zeroed?: string }
}
export function readState(root: string): AppState
```

### 3.2 — Definir interfaces antes de implementar

Ordem obrigatória:

1. Escrever as interfaces/tipos (derivados da SPEC 1.3).
2. Escrever `emptyState()` ou equivalente que respeita as interfaces.
3. Só então escrever as funções que operam sobre esses tipos.

### 3.3 — Verificar invariantes de tipo antes de escrever guardas

Para cada guarda de tipo (ex.: `if (!Array.isArray(x))`), executar mentalmente com 3 valores concretos:

| Valor | Cenário | Guarda deve |
| :--- | :--- | :--- |
| Valor 1 | tipo esperado no caminho feliz | deixar passar |
| Valor 2 | tipo corrompido (ex.: array) | inicializar |
| Valor 3 | ausente (undefined/null) | inicializar |

Exemplo do erro real:

```typescript
// ERRADO — lógica invertida, não testada com valores concretos
if (!Array.isArray(state.audit)) state.audit = { events: [] }
// Array.isArray({events:[]}) === false → inicializa → OK por acidente
// Array.isArray([])          === false → FALSO → não inicializa → estado corrupto

// CORRETO — verificação de tipo explícita, testada com os 3 valores
if (typeof state.audit !== "object" || state.audit === null || Array.isArray(state.audit)) {
  state.audit = { events: [] }
}
```

### 3.4 — Checklist de tipos antes de avançar

- [ ] Todas as assinaturas públicas têm tipos concretos (sem `any`)?
- [ ] Todas as interfaces têm um construtor/factory (`emptyState`, `createX`)?
- [ ] Todas as guardas de tipo foram verificadas com 3 valores concretos?
- [ ] Tipos de retorno de funções assíncronas estão declarados (`Promise<T>`)?

---

## FASE 4 — Mapear todos os caminhos de execução

### 4.1 — Posse do estado (state ownership)

Para qualquer função que lê e escreve estado compartilhado, mapear o ciclo completo antes de escrever:

```
LEITURA → MODIFICAÇÃO → ESCRITA
```

Regra: entre LEITURA e ESCRITA, nenhuma outra função deve ler ou escrever o mesmo estado. Se uma sub-operação precisa do estado, ela recebe o estado como parâmetro — não lê o disco de novo.

Exemplo do erro real:

```typescript
// ERRADO — lê o estado duas vezes criando race condition
export function dailyZeroIfDue(root: string, sessionID: string): boolean {
  const state = readState(root)           // LEITURA 1
  appendEpisodic(root, { ... })           // readState + writeState internos ← ESCRITA INTERMEDIÁRIA
  const state2 = readState(root)          // LEITURA 2 — estado já divergiu
  state2.session.last_zeroed = today
  writeState(root, state2)
}

// CORRETO — operação única conforme SPEC 1.2
export function dailyZeroIfDue(root: string, sessionID: string): boolean {
  const state = readState(root)           // LEITURA ÚNICA
  state.memory.episodic.push({ ... })    // modificação inline
  state.memory.pending_mem0.push({ ... }) // modificação inline
  state.session.last_zeroed = today
  state.memory.short_term = []
  writeState(root, state)                // ESCRITA ÚNICA
  return true
}
```

### 4.2 — Mapeamento de todos os caminhos

Para cada função, executar mentalmente todos os branches:

```
Caminhos obrigatórios a verificar:
├── Caminho feliz (happy path)
├── Estado/arquivo ausente (first run)     ← definido na SPEC 1.4
├── Estado corrompido ou tipo errado
├── Falha de I/O (disco, rede, permissão)
├── Concorrência (dois processos simultâneos)
└── Dados fora do limite esperado (array vazio, string muito longa)
```

### 4.3 — Erros nunca devem ser silenciados

`.catch(() => {})` é proibido sem logging. Todo caminho de erro deve:

- Logar com contexto suficiente para diagnóstico.
- Não bloquear o fluxo principal (se for operação de background).
- Indicar o nível de risco (Low, Medium, High).

```typescript
// PROIBIDO
flushMem0(root).catch(() => {})

// OBRIGATÓRIO
flushMem0(root).catch((err: unknown) => {
  appendLedger(root, {
    action: "flush_mem0_failed",
    risk_tier: "Medium",
    rationale: `flushMem0 falhou: ${err instanceof Error ? err.message : String(err)}`,
  })
})
```

### 4.4 — Dados sensíveis em logs

Antes de serializar qualquer objeto em log ou arquivo de auditoria:

- O objeto pode conter tokens, chaves, senhas, credenciais?
- Se sim, aplicar redação antes de serializar.

```typescript
// PROIBIDO
detail: JSON.stringify(event.properties).slice(0, 500)

// OBRIGATÓRIO
const redacted = redactSensitive(event.properties)
detail: JSON.stringify(redacted).slice(0, 500)
```

### 4.5 — Checklist de caminhos antes de avançar

- [ ] Caminho de primeiro arranque (conforme SPEC 1.4) está implementado?
- [ ] Todas as funções que leem E escrevem estado fazem isso em operação única?
- [ ] Nenhum `.catch(() => {})` sem logging?
- [ ] Dados sensíveis são redatados antes de logs?
- [ ] Recursos desconhecidos têm classificação por omissão explicitamente comentada?

---

## FASE 5 — Escrever o código

### 5.1 — Ordem de escrita

1. Tipos e interfaces          (derivados da SPEC 1.3)
2. Factories / `emptyState()`  (derivados da SPEC 1.3 + 1.4)
3. Funções utilitárias puras   (sem I/O)
4. Funções de I/O              (leitura/escrita)
5. Funções de negócio          (usam I/O + lógica)
6. Handlers / hooks            (usam funções de negócio)

Nunca escrever um handler antes das funções que ele chama.

### 5.2 — Regras de escrita

- Cada função tem responsabilidade única declarada em JSDoc se não for óbvia.
- Limitações conhecidas são documentadas com `// LIMITAÇÃO CONHECIDA:`.
- TODOs têm formato `// TODO: [o que falta] — [bloqueio ou razão]`.
- Cast de tipo tem comentário explicando por que é necessário.

### 5.3 — Placeholders proibidos sem TODO explícito

| Valor | Problema |
| :--- | :--- |
| `"pending"` em campo de hash | Hash nunca foi calculado — viola SPEC 1.3 |
| `0` em campo de custo real | Custo nunca foi medido — viola SPEC 1.3 |
| `any` em assinatura pública | Tipo nunca foi definido — viola FASE 3 |
| `// TODO` sem bloqueio identificado | Dívida técnica invisível |

---

## FASE 6 — Auto-revisão adversarial

Após escrever o código, executar esta revisão antes de entregar.

### 6.1 — Verificar aderência à SPEC

Para cada função implementada:

- Pergunta: o comportamento implementado corresponde exatamente à SPEC 1.1?
- Pergunta: os campos de dados correspondem às definições da SPEC 1.3?
- Pergunta: o comportamento em primeiro arranque corresponde à SPEC 1.4?

### 6.2 — Verificação de contratos de estado

Para cada função que lida com estado compartilhado:

- Pergunta 1: quantas vezes o estado é lido do disco? Deveria ser 1.
- Pergunta 2: quantas vezes o estado é escrito no disco? Deveria ser 1.
- Pergunta 3: existe janela entre leitura e escrita onde outro processo pode escrever?

### 6.3 — Verificação de guardas de tipo

Para cada `if (typeof x ...)` ou `if (Array.isArray(x) ...)`:

- Executar com 3 valores concretos:
  - Valor esperado no caminho feliz
  - Valor corrompido (tipo errado)
  - Valor ausente (undefined/null)
- Verificar se a guarda produz o comportamento correto nos três casos.

### 6.4 — Verificação de semântica de hooks

Para cada hook de framework:

- Pergunta: quem gerou os dados em `output`? assistente, usuário, ou sistema?
- Verificar: o campo `type` no registro reflete a fonte correta?

### 6.5 — Verificação de erros silenciados

Buscar no código gerado:

- `.catch(() => {})` → substituir por log com contexto
- `try { } catch { }` vazio → adicionar log mínimo
- `console.error(err)` sem contexto → adicionar identificação da função

### 6.6 — Checklist final

- [ ] Cada função implementada corresponde à sua SPEC?
- [ ] Nenhum `any` em assinatura pública sem `TODO:UNVERIFIED`?
- [ ] Nenhum estado lido mais de uma vez por operação lógica?
- [ ] Nenhum erro silenciado?
- [ ] Todos os caminhos de primeiro arranque implementados?
- [ ] Todas as guardas de tipo verificadas com 3 valores concretos?
- [ ] Semântica de todos os hooks verificada?
- [ ] Dados sensíveis redatados antes de logs?
- [ ] Limitações conhecidas documentadas no código?

---

## FASE 7 — Entrega

### 7.1 — Formato de entrega

Ao entregar código corrigido ou novo:

- SPEC produzida — sumário das especificações definidas na FASE 1.
- Lista de correções — tabela: problema original → correção → confidence.
- Limitações remanescentes — o que não foi possível corrigir e por quê.
- TODOs pendentes — listados com bloqueio identificado.
- Arquivos ausentes — que impediriam verificação completa, se houver.

### 7.2 — O que não entregar

- Código sem SPEC prévia documentada.
- Código com `any` não justificado.
- Código com `.catch(() => {})` sem logging.
- Código com estado lido múltiplas vezes por operação.
- Código que assume semântica de hook sem verificar a assinatura.
- Código com campos de dados sem definição de fonte e valor inicial.

---

## Referência rápida — Erros mais comuns por categoria

### Campos sem especificação
- **SINTOMA**: campo preenchido com `"pending"`, `0`, ou `""` em produção
- **CAUSA**: SPEC não definiu o que o campo deve conter nem quem o calcula
- **SOLUÇÃO**: FASE 1 obrigatória — definir tipo, fonte, valor inicial para cada campo

### Estado compartilhado
- **SINTOMA**: função chama outra função que lê/escreve o mesmo arquivo
- **CAUSA**: dono do estado não foi declarado na SPEC (1.2)
- **SOLUÇÃO**: declarar dono → passar estado como parâmetro → ler uma vez, escrever uma vez

### Guardas de tipo
- **SINTOMA**: guarda usa verificação de array para proteger objecto (ou vice-versa)
- **CAUSA**: condição não foi testada com valores concretos
- **SOLUÇÃO**: executar com 3 valores; usar `typeof` + null check + `Array.isArray` juntos

### Hooks de framework
- **SINTOMA**: dados do assistente classificados como dados do usuário (ou vice-versa)
- **CAUSA**: semântica do hook não verificada antes de implementar (FASE 2)
- **SOLUÇÃO**: ler definição do hook → identificar origem dos dados → só então implementar

### Erros silenciados
- **SINTOMA**: `.catch(() => {})` ou `catch {}` vazio
- **CAUSA**: caminho de falha não modelado na SPEC (1.1) nem na FASE 4
- **SOLUÇÃO**: logar com contexto mínimo (função, parâmetros relevantes, mensagem de erro)

### Tipos ausentes
- **SINTOMA**: `Record<string, any>` em assinatura pública
- **CAUSA**: tipagem adiada — SPEC 1.3 não foi executada
- **SOLUÇÃO**: definir interface antes de implementar; `any` só com `TODO:UNVERIFIED` explícito

### Estado ausente em primeiro arranque
- **SINTOMA**: função lança quando arquivo de estado não existe
- **CAUSA**: SPEC 1.4 não foi executada (responsabilidade de inicialização não declarada)
- **SOLUÇÃO**: toda função de leitura de estado deve auto-inicializar ou ter pré-requisito documentado
