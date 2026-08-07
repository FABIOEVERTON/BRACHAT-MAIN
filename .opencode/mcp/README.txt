EZRA OS BOUNDARY MCP — this folder is the Mac security boundary. Data here is accessible ONLY by the MCP server (server.mjs) with whitelisted tools — opencode permissions block direct read/write of mcp/**.
STRUCTURE:
credentials/secrets.env | API keys (Composio, Groq, NVIDIA, Google Studio, etc.) | Restricted
audit.log | credential access log (append-only) | Internal
NOTE: personal/ was removed from the boundary at Fabio's request. Personal data (resumes, schedules) lives as subagent content in .opencode/agents/.
MCP SERVER TOOLS:
mcp_list | list files/folders | within boundary
mcp_read | read file text | no credentials/secrets.env
mcp_write | write file | blocked for server.mjs, README, .gitignore, audit.log, credentials/
mcp_secrets_list | list key names | never values
mcp_secrets_get | return 1 key by name | audited in audit.log
RULES:
- No path may escape the boundary (path traversal blocked, including via symlink).
- Credentials never read via mcp_read — only via mcp_secrets_*.
- audit.log is append-only by the server; tool write is blocked.
- What protects server.mjs is the opencode permission config (read/edit deny on mcp/**).
DATA ORIGIN:
- credentials/secrets.env <- former integrations/APIS/.env.log (normalized, original deleted with Fabio approval on 2026-07-31).
