import type { Plugin } from "@opencode-ai/plugin"
import { appendLedger, hashState, nowISO, readState, rootDir } from "./memory-core.ts"

// Boot enxuto (Section 1): remove o bloco <available_skills> e sua intro do
// prompt de sistema. Skills passam a ser carregadas sob demanda via manifest
// (skill-router), nunca pré-carregadas no boot.
const SKILLS_INTRO =
  /Skills provide specialized instructions and workflows for specific tasks\.\s*\nUse the skill tool to load a skill when a task matches its description\.\s*/g
const SKILLS_BLOCK = /<available_skills>[\s\S]*?<\/available_skills>\s*/g

export const leanBoot: Plugin = async () => ({
  "experimental.chat.system.transform": async (_input, output) => {
    const root = rootDir()
    const before = hashState(readState(root))

    output.system = output.system.map((part) =>
      part.replace(SKILLS_INTRO, "").replace(SKILLS_BLOCK, ""),
    )
    // TODO: hook experimental. Validar empiricamente que o opencode aplica a
    // transformação depois de montar o bloco <available_skills> — caso o bloco
    // seja anexado após o plugin, a remoção aqui não tem efeito.

    try {
      appendLedger(root, {
        timestamp: nowISO(),
        actor: "lean-boot",
        action: "system_prompt_skills_stripped",
        risk_tier: "Low",
        state_hash_before: before,
        state_hash_after: hashState(readState(root)),
        token_cost: 0, // NOTA FORMAL (F-19): runtime não expõe custo real de tokens em hooks.
        rationale:
          "Boot: bloco <available_skills> removido do prompt de sistema. Transformação read-only; hashes devem coincidir.",
      })
    } catch (err) {
      console.error("[lean-boot] ledger write failed:", err)
    }
  },
})

export default leanBoot
