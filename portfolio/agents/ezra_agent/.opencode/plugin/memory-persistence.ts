import type { Event, Part, TextPart } from "@opencode-ai/sdk"
import type { Plugin } from "@opencode-ai/plugin"
import {
  appendCheckpoint,
  appendEpisodic,
  appendLedger,
  appendShortTerm,
  dailyZeroIfDue,
  flushMem0,
  hashState,
  isDecisionLike,
  nowISO,
  queueMem0,
  readState,
  todayUTC,
} from "./memory-core.ts"

const SKIP_TOOLS = new Set([
  "read",
  "glob",
  "grep",
  "list_mcp_resources",
  "list_mcp_resource_templates",
  "mem0_get_memories",
  "mem0_search_memories",
  "mem0_list_entities",
])

const WRITE_TOOLS = new Set([
  "bash",
  "edit",
  "write",
  "task",
  "mem0_add_memory",
  "mem0_delete_memory",
  "mem0_update_memory",
  "mem0_delete_all_memories",
  "mem0_delete_entities",
])

// ---------------------------------------------------------------------------
// Utilitários internos
// ---------------------------------------------------------------------------

/** Redacta campos sensíveis conhecidos antes de serializar em logs. */
function redactSensitive(obj: Record<string, unknown>): Record<string, unknown> {
  const SENSITIVE_KEYS = new Set([
    "token",
    "apiKey",
    "api_key",
    "secret",
    "password",
    "credential",
    "sessionToken",
  ])
  return Object.fromEntries(
    Object.entries(obj).map(([k, v]) =>
      SENSITIVE_KEYS.has(k) ? [k, "[REDACTED]"] : [k, v],
    ),
  )
}

/** Guarda de tipo para extrair texto de partes. */
function isTextPart(p: Part): p is TextPart {
  return p.type === "text" && typeof p.text === "string"
}

/** Extrai o ID de sessão de qualquer evento, com fallback. */
function sessionIDOf(event: Event): string {
  const props = event.properties as { sessionID?: string; info?: { id?: string } }
  if (event.type === "session.created") {
    return props.info?.id ?? "unknown"
  }
  return props.sessionID ?? "unknown"
}

/** Registra um erro de hook no ledger — nunca silenciar. */
function logHookError(root: string, hook: string, err: unknown): void {
  appendLedger(root, {
    timestamp: nowISO(),
    actor: "memory-persistence",
    action: "event_error",
    risk_tier: "Low",
    state_hash_before: "unavailable",
    state_hash_after: "unavailable",
    token_cost: 0, // TODO: capturar custo real quando exposto pelo runtime
    rationale: `Erro nao fatal no hook ${hook}: ${err instanceof Error ? err.message : String(err)}`,
  })
}

/**
 * Executa flushMem0 com log de falha explícito.
 * Nunca bloqueia o fluxo principal, mas não silencia o erro.
 */
function flushMem0Safe(root: string): void {
  flushMem0(root).catch((err: unknown) => {
    appendLedger(root, {
      timestamp: nowISO(),
      actor: "memory-persistence",
      action: "flush_mem0_failed",
      risk_tier: "Medium",
      state_hash_before: "unavailable",
      state_hash_after: "unavailable",
      token_cost: 0, // TODO: capturar custo real quando exposto pelo runtime
      rationale: `flushMem0 falhou: ${err instanceof Error ? err.message : String(err)}`,
    })
  })
}

// ---------------------------------------------------------------------------
// Plugin
// ---------------------------------------------------------------------------

export const memoryPersistence: Plugin = async ({ directory }) => {
  const root = directory

  return {
    // -----------------------------------------------------------------------
    // Eventos de sessão — tipados por discriminação de Event (sem cast solto)
    // -----------------------------------------------------------------------
    event: async ({ event }) => {
      try {
        if (event.type === "session.created") {
          const sessionID = sessionIDOf(event)
          appendEpisodic(root, { type: "session_start", sessionID })
          dailyZeroIfDue(root, sessionID)
          flushMem0Safe(root)
          return
        }

        if (event.type === "session.idle") {
          const sessionID = sessionIDOf(event)
          appendShortTerm(root, {
            type: "turn",
            sessionID,
            ts_note: "turno concluido",
          })
          return
        }

        if (event.type === "session.compacted") {
          appendCheckpoint(root, `Compaction em ${nowISO()}`)
          return
        }

        if (event.type === "session.error") {
          const sessionID = sessionIDOf(event)
          const redacted = redactSensitive(event.properties as Record<string, unknown>)
          appendEpisodic(root, {
            type: "error",
            sessionID,
            detail: JSON.stringify(redacted).slice(0, 500),
          })
          appendLedger(root, {
            timestamp: nowISO(),
            actor: "memory-persistence",
            action: "session_error",
            risk_tier: "Medium",
            state_hash_before: "unavailable",
            state_hash_after: "unavailable",
            token_cost: 0, // TODO: capturar custo real quando exposto pelo runtime
            rationale: `Session error in ${sessionID}: ${JSON.stringify(redacted).slice(0, 200)}`,
          })
          return
        }
      } catch (err: unknown) {
        logHookError(root, "event", err)
      }
    },

    // -----------------------------------------------------------------------
    // Pós-execução de ferramentas — auditoria MUT-01
    // -----------------------------------------------------------------------
    "tool.execute.after": async (input) => {
      try {
        if (SKIP_TOOLS.has(input.tool)) return

        const hashBefore = hashState(readState(root))
        const hashAfter = hashState(readState(root))

        if (WRITE_TOOLS.has(input.tool)) {
          appendEpisodic(root, {
            type: "tool_write",
            sessionID: input.sessionID,
            tool: input.tool,
          })
          appendLedger(root, {
            timestamp: nowISO(),
            actor: "ezra-os",
            action: "tool_execute",
            risk_tier: input.tool === "bash" ? "Medium" : "Low",
            state_hash_before: hashBefore,
            state_hash_after: hashAfter,
            token_cost: 0, // TODO: capturar custo real quando exposto pelo runtime
            rationale: `Ferramenta de escrita ${input.tool} executada em sessao ${input.sessionID}`,
          })
        } else {
          // Ferramentas fora de SKIP_TOOLS e WRITE_TOOLS.
          // Classificadas como leitura por omissão — rever se novas
          // ferramentas forem adicionadas ao ecossistema.
          appendLedger(root, {
            timestamp: nowISO(),
            actor: "ezra-os",
            action: "tool_readonly",
            risk_tier: "Low",
            state_hash_before: hashBefore,
            state_hash_after: hashAfter,
            token_cost: 0, // TODO: capturar custo real quando exposto pelo runtime
            rationale: `Ferramenta ${input.tool} executada (somente leitura por omissao — verificar classificacao)`,
          })
        }
      } catch (err: unknown) {
        // Nunca bloquear execução da ferramenta, mas nunca silenciar.
        logHookError(root, "tool.execute.after", err)
      }
    },

    // -----------------------------------------------------------------------
    // Mensagens do assistente — output.parts é resposta do assistente
    // -----------------------------------------------------------------------
    "chat.message": async (_input, output) => {
      try {
        const text = output.parts.filter(isTextPart).map((p) => p.text).join(" ")

        if (!text.trim()) return

        appendShortTerm(root, {
          type: "assistant",
          excerpt: text.trim().slice(0, 500),
          length: text.length,
        })

        if (isDecisionLike(text)) {
          const isBlocker = /blocked|blocker|cannot|dependency missing/i.test(text)
          const isPreference = /prefer|always|never|rule|mandatory/i.test(text)

          if (isBlocker) {
            queueMem0(
              root,
              `[cluster:bloqueadores] blocker: ${text.trim().slice(0, 300)}`,
              ["cluster:bloqueadores", "blocker"],
              { captured_on: todayUTC() },
            )
          } else if (isPreference) {
            queueMem0(
              root,
              `[cluster:preferencias] preference: ${text.trim().slice(0, 300)}`,
              ["cluster:preferencias", "preference"],
              { captured_on: todayUTC() },
            )
          } else {
            queueMem0(
              root,
              `[cluster:decisoes] decision: ${text.trim().slice(0, 300)}`,
              ["cluster:decisoes", "decision"],
              { captured_on: todayUTC() },
            )
          }
          flushMem0Safe(root)
        }
      } catch (err: unknown) {
        // Nunca bloquear recebimento de mensagem, mas nunca silenciar.
        logHookError(root, "chat.message", err)
      }
    },

    // -----------------------------------------------------------------------
    // Compactação experimental
    // -----------------------------------------------------------------------
    "experimental.session.compacting": async (_input, output) => {
      try {
        output.context.push(
          "## Estado persistente (memory-persistence plugin)\nDecisoes e preferencias estao em .opencode/state.json (memory.short_term) e enfileiradas para mem0. Se precisar de contexto anterior, consulte esses arquivos.",
        )
        appendLedger(root, {
          timestamp: nowISO(),
          actor: "memory-persistence",
          action: "compaction_context_injected",
          risk_tier: "Low",
          state_hash_before: "unavailable",
          state_hash_after: "unavailable",
          token_cost: 0, // TODO: capturar custo real quando exposto pelo runtime
          rationale: "experimental.session.compacting hook fired and context injected.",
        })
      } catch (err: unknown) {
        logHookError(root, "experimental.session.compacting", err)
      }
    },
  }
}

export default memoryPersistence
