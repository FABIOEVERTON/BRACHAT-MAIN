import { createHash } from "node:crypto"
import { readFileSync, writeFileSync, existsSync, mkdirSync } from "node:fs"
import { dirname, resolve } from "node:path"

export const STATE_PATH = ".opencode/state.json"
export const LEDGER_PATH = ".opencode/governance-ledger.jsonl"
export const PROPOSAL_PATH = ".opencode/proposals/proposal-pendente.md"
export const CLUSTERS = [
  "governanca",
  "seguranca",
  "arquitetura",
  "orquestracao",
  "memoria",
  "avaliacao",
  "integracao",
]

// ---------------------------------------------------------------------------
// Tipos base do estado — substituem Record<string, any> nas assinaturas públicas
// ---------------------------------------------------------------------------
export interface Mem0Entry {
  ts: string
  text: string
  tags: string[]
  meta: Record<string, unknown>
  status: "pending" | "in-flight" | "flushed" | "error"
}

export interface StateMemory {
  short_term: Record<string, unknown>[]
  episodic: Record<string, unknown>[]
  checkpoints: Record<string, unknown>[]
  long_term: Record<string, unknown>[]
  pending_mem0: Mem0Entry[]
}

export interface AppState {
  memory: StateMemory
  audit: { events: unknown[] }
  session?: { last_zeroed?: string }
  learning?: { last_learned?: string }
  [key: string]: unknown
}

export type LedgerEntry = {
  timestamp: string
  actor: string
  action: string
  risk_tier: "Low" | "Medium" | "High" | "Critical"
  state_hash_before: string
  state_hash_after: string
  // NOTA FORMAL (F-19): token_cost é sempre 0 porque o runtime do opencode
  // não expõe o custo de tokens em hooks de plugin. Decisão aprovada por
  // Fabio: documentar a limitação, NÃO instrumentar contadores manuais (que
  // seriam imprecisos e não auditáveis). Reavaliar quando o runtime expuser
  // custo por chamada de hook.
  token_cost: number
  rationale: string
}

const MEMORY_KEYS = [
  "short_term",
  "episodic",
  "checkpoints",
  "long_term",
  "pending_mem0",
] as const

// ---------------------------------------------------------------------------
// Paths
// ---------------------------------------------------------------------------
export function rootDir(): string {
  return process.env.EZRA_ROOT ?? process.cwd()
}

export function statePath(root: string): string {
  return resolve(root, STATE_PATH)
}

export function ledgerPath(root: string): string {
  return resolve(root, LEDGER_PATH)
}

// ---------------------------------------------------------------------------
// Hash — auditoria MUT-01
// ---------------------------------------------------------------------------

/**
 * Hash SHA-256 truncado de um valor serializado. Usado nos campos
 * state_hash_before/after do ledger para vincular mutações ao estado.
 */
export function hashState(value: unknown): string {
  return createHash("sha256")
    .update(JSON.stringify(value))
    .digest("hex")
    .slice(0, 16)
}

// ---------------------------------------------------------------------------
// Estado — leitura e escrita
// ---------------------------------------------------------------------------

/**
 * Retorna um AppState vazio para uso em primeiro arranque.
 * Exportado para permitir que outros módulos inicializem o ficheiro
 * sem depender de leitura prévia.
 */
export function emptyState(): AppState {
  return {
    memory: {
      short_term: [],
      episodic: [],
      checkpoints: [],
      long_term: [],
      pending_mem0: [],
    },
    audit: { events: [] },
    session: {},
    learning: {},
  }
}

/**
 * Lê o estado do disco. Se o ficheiro não existir, inicializa e persiste
 * um estado vazio em vez de lançar — necessário para primeiro arranque.
 */
export function readState(root: string): AppState {
  const p = statePath(root)
  if (!existsSync(p)) {
    const initial = emptyState()
    mkdirSync(dirname(p), { recursive: true })
    writeFileSync(p, JSON.stringify(initial, null, 1) + "\n", "utf-8")
    return initial
  }
  return JSON.parse(readFileSync(p, "utf-8")) as AppState
}

export function writeState(root: string, state: AppState): void {
  writeFileSync(statePath(root), JSON.stringify(state, null, 1) + "\n", "utf-8")
}

// ---------------------------------------------------------------------------
// Ledger
// ---------------------------------------------------------------------------
export function appendLedger(root: string, entry: LedgerEntry): void {
  const p = ledgerPath(root)
  mkdirSync(dirname(p), { recursive: true })
  writeFileSync(p, JSON.stringify(entry) + "\n", { flag: "a" })
  // LIMITAÇÃO CONHECIDA: writeFileSync com flag "a" não é atómico em
  // sistemas de ficheiros partilhados. Em ambiente multi-agente, entradas
  // concorrentes podem intercalar-se. Mitigação requer lock externo ou
  // migração para base de dados append-only (ex.: SQLite WAL).
}

// ---------------------------------------------------------------------------
// Utilitários de tempo
// ---------------------------------------------------------------------------
export function todayUTC(): string {
  return new Date().toISOString().slice(0, 10)
}

export function nowISO(): string {
  return new Date().toISOString()
}

// ---------------------------------------------------------------------------
// ensureMemory
// ---------------------------------------------------------------------------

/**
 * Garante que state.memory e state.audit existem com a estrutura esperada.
 *
 * CORRECÇÃO: a guarda original usava Array.isArray(state.audit) para decidir
 * se inicializava state.audit como objecto — lógica invertida e enganosa.
 * Substituído por verificação de tipo explícita.
 */
export function ensureMemory(state: AppState): void {
  if (typeof state.memory !== "object" || state.memory === null) {
    state.memory = emptyState().memory
  }
  const memory = state.memory as unknown as { [key: string]: unknown[] }
  for (const k of MEMORY_KEYS) {
    if (!Array.isArray(memory[k])) memory[k] = []
  }
  if (typeof state.audit !== "object" || state.audit === null || Array.isArray(state.audit)) {
    state.audit = { events: [] }
  }
  if (!Array.isArray(state.audit.events)) {
    state.audit.events = []
  }
}

// ---------------------------------------------------------------------------
// Short-term e Episodic
// ---------------------------------------------------------------------------
export function appendShortTerm(root: string, entry: Record<string, unknown>): void {
  const state = readState(root)
  ensureMemory(state)
  state.memory.short_term.push({ ts: nowISO(), ...entry })
  if (state.memory.short_term.length > 200) {
    state.memory.short_term = state.memory.short_term.slice(-200)
  }
  writeState(root, state)
}

export function appendEpisodic(root: string, entry: Record<string, unknown>): void {
  const state = readState(root)
  ensureMemory(state)
  state.memory.episodic.push({ ts: nowISO(), ...entry })
  if (state.memory.episodic.length > 500) {
    state.memory.episodic = state.memory.episodic.slice(-500)
  }
  writeState(root, state)
}

// ---------------------------------------------------------------------------
// Checkpoints
// ---------------------------------------------------------------------------
export function appendCheckpoint(root: string, rationale: string): void {
  const state = readState(root)
  ensureMemory(state)
  const checkpoints = state.memory.checkpoints
  const nextId = checkpoints.length + 1
  checkpoints.push({
    id: `cp-${nextId}`,
    timestamp: nowISO(),
    snapshot: "version, identity, session, context, memory, last_decision, audit",
    rationale,
  })
  while (checkpoints.length > 10) checkpoints.shift()
  writeState(root, state)
}

// ---------------------------------------------------------------------------
// Mem0 — fila e flush
// ---------------------------------------------------------------------------
export function queueMem0(
  root: string,
  text: string,
  tags: string[],
  meta?: Record<string, unknown>,
): void {
  const state = readState(root)
  ensureMemory(state)
  state.memory.pending_mem0.push({
    ts: nowISO(),
    text,
    tags,
    meta: meta ?? {},
    status: "pending",
  })
  writeState(root, state)
}

/**
 * Carrega a chave de API do Mem0 a partir de variável de ambiente ou
 * ficheiro de configuração do OpenCode.
 *
 * LIMITAÇÃO CONHECIDA: a chave fica retida como string no heap até GC.
 * Em ambientes com dumps de memória, representa risco menor sem mitigação
 * possível em JS puro sem buffers de memória controlada.
 */
export function loadMem0Key(): string | null {
  if (process.env.MEM0_API_KEY) return process.env.MEM0_API_KEY
  const candidates = [
    resolve(process.env.HOME ?? "", ".config/opencode/opencode.jsonc"),
    resolve(process.env.HOME ?? "", ".config/opencode/opencode.json"),
  ]
  for (const p of candidates) {
    if (!existsSync(p)) continue
    const raw = readFileSync(p, "utf-8")
    const noComments = raw.replace(/^\s*\/\/.*$/gm, "").replace(/\/\*[\s\S]*?\*\//g, "")
    try {
      const cfg = JSON.parse(noComments) as Record<string, unknown>
      const key = (cfg?.mcp as Record<string, unknown>)
        ?.["mem0"] as Record<string, unknown>
        | undefined
      const apiKey = (key?.environment as Record<string, unknown>)?.MEM0_API_KEY
      if (typeof apiKey === "string" && apiKey.length > 0) return apiKey
    } catch {
      continue
    }
  }
  return null
}

/**
 * Envia entradas pendentes para a API do Mem0.
 *
 * GUARDAS APLICADAS:
 * 1. Double-flush (F-15): entradas "pending" são reclamadas como "in-flight"
 *    (escrita imediata) antes do loop de awaits. Se um segundo flush rodar
 *    em paralelo, não envia as mesmas entradas.
 * 2. Race de escrita (F-07): o estado é re-lido imediatamente antes do
 *    writeState final e somente os status de resultado são aplicados sobre
 *    a cópia fresca — não sobrescreve alterações externas durante os awaits.
 *
 * Retorna o número de entradas enviadas com sucesso.
 */
export async function flushMem0(root: string): Promise<number> {
  const state = readState(root)
  ensureMemory(state)
  const pending = state.memory.pending_mem0.filter((m) => m.status === "pending")
  if (pending.length === 0) return 0
  const key = loadMem0Key()
  if (!key) return 0

  // Reclama as entradas como in-flight antes de aguardar (guarda F-15)
  for (const m of pending) m.status = "in-flight"
  writeState(root, state)

  const results = new Map<string, "flushed" | "error">()
  let flushed = 0
  for (const m of pending) {
    try {
      const res = await fetch("https://api.mem0.ai/v1/memories/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Token ${key}`,
        },
        body: JSON.stringify({
          messages: [{ role: "user", content: m.text }],
          user_id: "fabioeverton",
          metadata: { tags: m.tags, ...m.meta },
        }),
      })
      results.set(m.ts, res.ok ? "flushed" : "error")
      if (res.ok) flushed++
    } catch {
      results.set(m.ts, "error")
    }
  }

  // Re-leitura fresca para não sobrescrever escrita externa (F-07)
  const fresh = readState(root)
  ensureMemory(fresh)
  for (const m of fresh.memory.pending_mem0) {
    const result = results.get(m.ts)
    if (result) m.status = result
  }
  writeState(root, fresh)
  return flushed
}

// ---------------------------------------------------------------------------
// dailyZeroIfDue
// ---------------------------------------------------------------------------

/**
 * Executa o zero diário se ainda não realizado hoje.
 *
 * CORRECÇÃO: a versão original lia o estado duas vezes (antes e depois de
 * appendEpisodic), criando race condition de ficheiro. Substituído por
 * operação única: lê o estado, modifica em memória, escreve uma vez.
 */
export function dailyZeroIfDue(root: string, sessionID: string): boolean {
  const state = readState(root)
  ensureMemory(state)
  const last = state.session?.last_zeroed
  const today = todayUTC()
  if (last === today) return false

  const count = state.memory.short_term.length

  // Registo episódico inline — sem segunda leitura do disco
  state.memory.episodic.push({
    ts: nowISO(),
    type: "zero",
    sessionID,
    rationale: `Zero diario estrutural: ${count} turnos de short_term arquivados. Compressao semantica delegada ao learning-driver.`,
  })
  if (state.memory.episodic.length > 500) {
    state.memory.episodic = state.memory.episodic.slice(-500)
  }

  // Enfileira mem0 inline — sem segunda leitura do disco
  state.memory.pending_mem0.push({
    ts: nowISO(),
    text: `[contexto] zero-diario: ${count} turnos arquivados antes de ${today}`,
    tags: ["cluster:zero-diario", "contexto"],
    meta: { count, archived_before: today },
    status: "pending",
  })

  // Actualiza sessão e limpa short_term
  if (!state.session) state.session = {}
  state.session.last_zeroed = today
  state.memory.short_term = []

  // Escrita única — elimina race condition
  writeState(root, state)
  return true
}

// ---------------------------------------------------------------------------
// Helpers de decisão e cluster
// ---------------------------------------------------------------------------
export function isDecisionLike(text: string): boolean {
  const markers = [
    // Portuguese (retained for backward compatibility)
    "decid", "quero", "aprovo", "nao quero", "prefiro", "regra",
    "proibido", "obrigator", "sempre", "nunca", "vamos mudar",
    "arquitetura", "governanca", "preferenc", "bloqueado", "nao consegue",
    "me ensina", "aprender", "memoria", "skill", "cluster",
    // English (required — output language is American English)
    "decided", "decision", "prefer", "approve", "reject", "never",
    "always", "rule", "prohibited", "mandatory", "architecture",
    "governance", "blocked", "blocker", "cannot", "will not",
    "learning", "memory", "skill", "cluster", "change to",
  ]
  const lower = text.toLowerCase()
  return markers.some((m) => lower.includes(m))
}

export function clusterForToday(): string {
  const day = new Date()
  const start = new Date(Date.UTC(day.getUTCFullYear(), 0, 0))
  const diff = day.getTime() - start.getTime()
  const dayOfYear = Math.floor(diff / 86400000)
  return CLUSTERS[dayOfYear % CLUSTERS.length]
}

export function lastLearnedDay(root: string): string | null {
  const state = readState(root)
  return (state.learning?.last_learned as string | undefined) ?? null
}

export function setLastLearned(root: string): void {
  const state = readState(root)
  if (!state.learning) state.learning = {}
  state.learning.last_learned = todayUTC()
  writeState(root, state)
}

// ---------------------------------------------------------------------------
// Ledger — leitura de tail
// ---------------------------------------------------------------------------
export function readLedgerTail(root: string, lines = 20): string[] {
  const p = ledgerPath(root)
  if (!existsSync(p)) return []
  const raw = readFileSync(p, "utf-8").trim().split("\n")
  return raw.slice(-lines)
}

// ---------------------------------------------------------------------------
// Proposals
// ---------------------------------------------------------------------------
export function buildProposal(root: string, cluster: string): string {
  const state = readState(root)
  ensureMemory(state)
  const weekActions = state.memory.episodic.filter((e) => {
    const t = new Date((e as { ts: string }).ts).getTime()
    return Date.now() - t < 7 * 86400000
  })
  const ledgerTail = readLedgerTail(root, 15)
  return [
    `# Proposta de Melhoria — Cluster ${cluster}`,
    "",
    `- **Gerada em:** ${nowISO()}`,
    `- **Cluster do dia:** ${cluster}`,
    `- **Status:** PENDENTE DE APROVACAO (Fabio)`,
    "",
    "## Evidencias observadas (brutas)",
    "",
    `- Eventos episodicos na semana: ${weekActions.length}`,
    "- Últimas ações do ledger:",
    ...ledgerTail.map((l) => `  - \`${l.slice(0, 160)}\``),
    "",
    "## Regra",
    "",
    "1. REFINAR skills existentes > criar novas (RULE-01).",
    "2. Nada aplica sozinho: aprovacao de Fabio e obrigatoria.",
    "3. Proposta aprovada -> skill atualizada + auditoria no ledger.",
    "",
    "## Decisao de Fabio",
    "",
    "- [ ] APROVAR",
    "- [ ] REJEITAR",
    "- [ ] REVISAR (comentarios abaixo)",
    "",
  ].join("\n")
}

export function writeProposal(root: string, content: string): string {
  const p = resolve(root, PROPOSAL_PATH)
  mkdirSync(dirname(p), { recursive: true })
  writeFileSync(p, content, "utf-8")
  return p
}
