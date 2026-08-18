import type { Plugin } from "@opencode-ai/plugin"

type CompactDef = {
  description: string
  properties: Record<string, unknown>
  required: string[]
}

const COMPACT: Record<string, CompactDef> = {
  bash: {
    description: "Executes a bash command in a persistent shell with optional timeout.",
    properties: {
      command: { type: "string" },
      timeout: { type: "integer" },
      workdir: { type: "string" },
    },
    required: ["command"],
  },
  read: {
    description: "Read a file or directory from the filesystem (optional line offset/limit).",
    properties: {
      filePath: { type: "string" },
      offset: { type: "integer" },
      limit: { type: "integer" },
    },
    required: ["filePath"],
  },
  write: {
    description: "Writes a file to the filesystem, overwriting existing content.",
    properties: {
      filePath: { type: "string" },
      content: { type: "string" },
    },
    required: ["filePath", "content"],
  },
  glob: {
    description: "Find files by glob pattern (e.g. src/**/*.ts).",
    properties: {
      pattern: { type: "string" },
      path: { type: "string" },
    },
    required: ["pattern"],
  },
  grep: {
    description: "Search file contents by regex pattern.",
    properties: {
      pattern: { type: "string" },
      path: { type: "string" },
      include: { type: "string" },
    },
    required: ["pattern"],
  },
  task: {
    description: "Launch a subagent to handle a complex task autonomously.",
    properties: {
      description: { type: "string" },
      prompt: { type: "string" },
      subagent_type: { type: "string" },
      task_id: { type: "string" },
      command: { type: "string" },
    },
    required: ["description", "prompt"],
  },
  webfetch: {
    description: "Fetch content from a URL (markdown/text/html).",
    properties: {
      url: { type: "string" },
      format: { type: "string", enum: ["markdown", "text", "html"] },
      timeout: { type: "integer" },
    },
    required: ["url"],
  },
  websearch: {
    description: "Search the web using the session's web search provider.",
    properties: {
      query: { type: "string" },
      numResults: { type: "integer" },
      type: { type: "string", enum: ["auto", "fast", "deep"] },
      livecrawl: { type: "string", enum: ["fallback", "preferred"] },
      contextMaxCharacters: { type: "integer" },
    },
    required: ["query"],
  },
}

export const schemaSlim: Plugin = async () => {
  return {
    "tool.definition": async (input, output) => {
      const def = COMPACT[input.toolID]
      if (!def) return
      output.description = def.description
      output.jsonSchema = {
        type: "object",
        properties: def.properties,
        required: def.required,
        additionalProperties: false,
      }
    },
  }
}

export default schemaSlim
