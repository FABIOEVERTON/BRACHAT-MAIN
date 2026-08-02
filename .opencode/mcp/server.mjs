#!/usr/bin/env node
import { createInterface } from "node:readline"
import { readFile, writeFile, mkdir, readdir, stat, realpath, appendFile } from "node:fs/promises"
import { resolve, join, sep } from "node:path"
import { fileURLToPath } from "node:url"

const __dirname = fileURLToPath(new URL(".", import.meta.url))
const BOUNDARY = await realpath(__dirname)
const SECRETS_FILE = join(BOUNDARY, "credentials", "secrets.env")
const AUDIT_FILE = join(BOUNDARY, "audit.log")
const PROTECTED_FILES = new Set([resolve(BOUNDARY, "server.mjs"), resolve(BOUNDARY, "README.md"), resolve(BOUNDARY, ".gitignore"), resolve(BOUNDARY, "audit.log")])
const READONLY_DIRS = ["credentials"]
const PROTOCOL_VERSIONS = new Set(["2024-11-05", "2025-03-26", "2025-06-18"])

const TOOLS = [
  {
    name: "mcp_list",
    description: "Lista arquivos e pastas dentro da boundary protegida (mcp/). path é relativo à raiz da boundary.",
    inputSchema: {
      type: "object",
      properties: {
        path: { type: "string", description: "Subpasta relativa, ex.: 'credentials' ou ''" },
      },
    },
  },
  {
    name: "mcp_read",
    description: "Lê conteúdo textual de um arquivo dentro da boundary (mcp/). Não expõe credenciais.",
    inputSchema: {
      type: "object",
      properties: {
        path: { type: "string", description: "Caminho relativo dentro da boundary, ex.: 'personal/resumes/x.md'" },
      },
      required: ["path"],
    },
  },
  {
    name: "mcp_write",
    description: "Grava/cria um arquivo dentro da boundary (mcp/). Bloqueado para server.mjs, README.md, .gitignore, audit.log e pasta credentials/.",
    inputSchema: {
      type: "object",
      properties: {
        path: { type: "string", description: "Caminho relativo dentro da boundary" },
        content: { type: "string", description: "Conteúdo textual" },
      },
      required: ["path", "content"],
    },
  },
  {
    name: "mcp_secrets_list",
    description: "Lista apenas os NOMES das chaves de credenciais disponíveis (nunca os valores).",
    inputSchema: { type: "object", properties: {} },
  },
  {
    name: "mcp_secrets_get",
    description: "Retorna o VALOR de UMA chave de credencial pelo nome. Acesso auditado em mcp/audit.log.",
    inputSchema: {
      type: "object",
      properties: {
        name: { type: "string", description: "Nome exato da chave, ex.: 'COMPOSIO_API_KEY'" },
      },
      required: ["name"],
    },
  },
]

function audit(entry) {
  appendFile(AUDIT_FILE, `${new Date().toISOString()} ${entry}\n`).catch(() => {})
}

function resolveInBoundary(rel) {
  if (typeof rel !== "string" || rel === "") {
    throw new Error("path obrigatório")
  }
  const resolved = resolve(BOUNDARY, rel)
  const within = resolved === BOUNDARY || resolved.startsWith(BOUNDARY + sep)
  if (!within) {
    throw new Error("Acesso fora da boundary bloqueado")
  }
  return resolved
}

async function realWithinBoundary(abs) {
  try {
    const real = await realpath(abs)
    return real === BOUNDARY || real.startsWith(BOUNDARY + sep)
  } catch {
    return true
  }
}

async function listTree(rel) {
  const base = rel ? resolveInBoundary(rel) : BOUNDARY
  if (!(await realWithinBoundary(base))) throw new Error("Acesso fora da boundary bloqueado")
  const out = []
  async function walk(dir, prefix) {
    const entries = await readdir(dir, { withFileTypes: true })
    for (const e of entries.sort((a, b) => a.name.localeCompare(b.name))) {
      const abs = join(dir, e.name)
      const label = prefix ? `${prefix}/${e.name}` : e.name
      if (e.isDirectory()) {
        out.push(`${label}/`)
        await walk(abs, label)
      } else {
        out.push(label)
      }
    }
  }
  const st = await stat(base)
  if (st.isDirectory()) {
    await walk(base, rel || "")
  } else {
    out.push(rel)
  }
  return { root: BOUNDARY, entries: out }
}

async function readText(rel) {
  const abs = resolveInBoundary(rel)
  if (!(await realWithinBoundary(abs))) throw new Error("Acesso fora da boundary bloqueado")
  if (abs === SECRETS_FILE) throw new Error("Uso mcp_secrets_list / mcp_secrets_get para credenciais")
  const buf = await readFile(abs)
  if (buf.includes(0)) throw new Error("Arquivo binário: leitura textual bloqueada")
  return buf.toString("utf8")
}

async function writeText(rel, content) {
  const abs = resolveInBoundary(rel)
  if (PROTECTED_FILES.has(abs) || abs === SECRETS_FILE) {
    throw new Error("Arquivo protegido: escrita bloqueada")
  }
  const relSegments = abs.slice(BOUNDARY.length + 1).split(sep)
  if (READONLY_DIRS.includes(relSegments[0])) {
    throw new Error("Diretório de credenciais: somente leitura")
  }
  await mkdir(resolve(abs, ".."), { recursive: true })
  await writeFile(abs, String(content), "utf8")
  audit(`write ${rel}`)
  return { path: rel, bytes: Buffer.byteLength(String(content)) }
}

async function secretsList() {
  try {
    const raw = await readFile(SECRETS_FILE, "utf8")
    const names = raw.split(/\r?\n/).filter(Boolean).map((l) => l.split("=")[0])
    audit(`secrets_list (${names.length} chaves)`)
    return { count: names.length, keys: names }
  } catch (e) {
    if (e.code === "ENOENT") return { count: 0, keys: [] }
    throw e
  }
}

async function secretsGet(name) {
  if (typeof name !== "string" || !/^[A-Z0-9_]+$/.test(name)) {
    throw new Error("nome inválido (use apenas A-Z, 0-9, _)")
  }
  const raw = await readFile(SECRETS_FILE, "utf8")
  const line = raw.split(/\r?\n/).find((l) => l.startsWith(`${name}=`))
  if (!line) throw new Error(`Chave não encontrada: ${name}`)
  const value = line.slice(name.length + 1)
  audit(`secrets_get ${name}`)
  return { name, value }
}

async function callTool(name, args) {
  switch (name) {
    case "mcp_list":
      return { content: [{ type: "text", text: JSON.stringify(await listTree(args?.path || ""), null, 2) }] }
    case "mcp_read":
      return { content: [{ type: "text", text: await readText(args?.path) }] }
    case "mcp_write":
      return { content: [{ type: "text", text: JSON.stringify(await writeText(args?.path, args?.content ?? ""), null, 2) }] }
    case "mcp_secrets_list":
      return { content: [{ type: "text", text: JSON.stringify(await secretsList(), null, 2) }] }
    case "mcp_secrets_get":
      return { content: [{ type: "text", text: JSON.stringify(await secretsGet(args?.name), null, 2) }] }
    default:
      throw new Error(`Tool desconhecida: ${name}`)
  }
}

const rl = createInterface({ input: process.stdin, crlfDelay: Infinity })
rl.on("line", async (line) => {
  let msg
  try {
    msg = JSON.parse(line)
  } catch {
    process.stderr.write("parse error\n")
    return
  }
  const { id, method, params } = msg

  const respond = (payload) => {
    process.stdout.write(JSON.stringify({ jsonrpc: "2.0", id, ...payload }) + "\n")
  }

  if (method === "initialize") {
    const reqVersion = params?.protocolVersion
    const protocolVersion = PROTOCOL_VERSIONS.has(reqVersion) ? reqVersion : "2024-11-05"
    respond({
      result: {
        protocolVersion,
        capabilities: { tools: {} },
        serverInfo: { name: "brachat-mcp", version: "1.0.0" },
      },
    })
    return
  }
  if (method === "notifications/initialized" || method === "notifications/cancelled") return
  if (method === "ping") {
    respond({ result: {} })
    return
  }
  if (method === "tools/list") {
    respond({ result: { tools: TOOLS } })
    return
  }
  if (method === "tools/call") {
    const { name, arguments: args } = params ?? {}
    try {
      const result = await callTool(name, args ?? {})
      respond({ result: { ...result, isError: false } })
    } catch (e) {
      respond({
        result: {
          content: [{ type: "text", text: `ERRO: ${e.message}` }],
          isError: true,
        },
      })
    }
    return
  }
  if (id !== undefined) {
    respond({ error: { code: -32601, message: `Método não suportado: ${method}` } })
  }
})
