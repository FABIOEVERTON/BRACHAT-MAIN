import type { Permission } from "@opencode-ai/sdk"
import type { Plugin } from "@opencode-ai/plugin"
import { appendLedger, nowISO } from "./memory-core.ts"

/**
 * Tipos de permissão que exigem skill carregada no turno.
 * Ferramentas de mutação apenas — leitura (read/glob) e o tool `skill`
 * (enabler) ficam livres para evitar deadlock.
 */
const GATED_PERMISSIONS = new Set(["bash", "edit", "write", "task"])

const GATED_MCP_PREFIXES = ["mcp__brachat-mcp__"]

function isGated(type: string): boolean {
  if (GATED_PERMISSIONS.has(type)) return true
  return GATED_MCP_PREFIXES.some((p) => type.startsWith(p))
}

/**
 * skill-gate — trava dura de roteamento por skill.
 *
 * Nenhum tool de mutação roda sem que o tool `skill` tenha sido chamado
 * no turno atual da sessão. A trava é por turno: `session.idle` retrava,
 * obrigando a recarregar a skill a cada tarefa nova.
 *
 * Toda negação é registrada no ledger (auditoria + insumo de aprendizado).
 */
export const skillGate: Plugin = async ({ directory }) => {
  const root = directory
  const unlockedSessions = new Set<string>()

  function auditDeny(permission: Permission): void {
    appendLedger(root, {
      timestamp: nowISO(),
      actor: "skill-gate",
      action: "permission_denied_no_skill",
      risk_tier: "High",
      state_hash_before: "unavailable",
      state_hash_after: "unavailable",
      token_cost: 0, // TODO: capturar custo real quando exposto pelo runtime
      rationale: `skill-gate DENY: perm=${permission.type} session=${permission.sessionID} — nenhuma skill carregada neste turno. Carregar skill do manifest antes de mutar.`,
    })
  }

  return {
    // -----------------------------------------------------------------------
    // Eventos — retrava a sessão ao fim do turno
    // -----------------------------------------------------------------------
    event: async ({ event }) => {
      if (event.type !== "session.idle") return
      try {
        const sessionID = (event.properties as { sessionID?: string }).sessionID
        if (sessionID) unlockedSessions.delete(sessionID)
      } catch {
        // Nunca bloquear eventos; perda de reset apenas relaxa a trava.
      }
    },

    // -----------------------------------------------------------------------
    // Registra que a skill foi carregada neste turno
    // -----------------------------------------------------------------------
    "tool.execute.after": async (input) => {
      if (input.tool === "skill") {
        unlockedSessions.add(input.sessionID)
      }
    },

    // -----------------------------------------------------------------------
    // Decisão de permissão — o gate propriamente dito
    // -----------------------------------------------------------------------
    "permission.ask": async (input, output) => {
      if (!isGated(input.type)) return
      if (unlockedSessions.has(input.sessionID)) {
        output.status = "allow"
        return
      }
      output.status = "deny"
      auditDeny(input)
    },
  }
}

export default skillGate
