import type { Plugin } from "@opencode-ai/plugin"
import {
  appendEpisodic,
  appendLedger,
  buildProposal,
  clusterForToday,
  flushMem0,
  hashState,
  lastLearnedDay,
  nowISO,
  readState,
  setLastLearned,
  todayUTC,
  writeProposal,
} from "./memory-core.ts"

export const learningDriver: Plugin = async ({ directory }) => {
  const root = directory

  /** Registra falhas no ledger — nunca silenciar. */
  function logFailure(action: string, err: unknown): void {
    appendLedger(root, {
      timestamp: nowISO(),
      actor: "learning-driver",
      action,
      risk_tier: "Medium",
      state_hash_before: "unavailable",
      state_hash_after: "unavailable",
      token_cost: 0, // TODO: capturar custo real quando exposto pelo runtime
      rationale: `${action} falhou: ${err instanceof Error ? err.message : String(err)}`,
    })
  }

  return {
    event: async ({ event }) => {
      if (event.type !== "session.created") return

      try {
        const hashBefore = hashState(readState(root))

        // Flush assíncrono com log de falha (não bloqueia boot, não silencia)
        flushMem0(root).catch((err: unknown) => {
          logFailure("flush_mem0_failed", err)
        })

        const last = lastLearnedDay(root)
        const today = todayUTC()
        if (last === today) return

        const cluster = clusterForToday()
        const proposal = buildProposal(root, cluster)
        const path = writeProposal(root, proposal)
        setLastLearned(root)

        const hashAfter = hashState(readState(root))

        appendEpisodic(root, {
          type: "learning",
          detail: `Cluster do dia: ${cluster}. Proposta em ${path}`,
        })
        appendLedger(root, {
          timestamp: nowISO(),
          actor: "learning-driver",
          action: "learning_proposal",
          risk_tier: "Low",
          state_hash_before: hashBefore,
          state_hash_after: hashAfter,
          token_cost: 0, // TODO: capturar custo real quando exposto pelo runtime
          rationale: `Aprendizado diario: cluster ${cluster} revisado, proposta pendente gerada em ${path}. Aguardando aprovacao de Fabio.`,
        })
      } catch (err: unknown) {
        logFailure("learning_proposal_failed", err)
      }
    },
  }
}

export default learningDriver
