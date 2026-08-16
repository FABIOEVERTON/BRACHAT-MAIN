import json
import os
import subprocess


class MCPClient:
    def __init__(self, server_path):
        self.proc = subprocess.Popen(
            ["node", server_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )

    def _call(self, method, params=None, rid=1):
        req = {"jsonrpc": "2.0", "id": rid, "method": method, "params": params or {}}
        self.proc.stdin.write(json.dumps(req).encode("utf-8") + b"\n")
        self.proc.stdin.flush()
        line = self.proc.stdout.readline()
        if not line:
            raise RuntimeError("mcp server fechou stdout")
        return json.loads(line.decode("utf-8"))

    def initialize(self):
        return self._call("initialize", {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "parashat", "version": "1.0.0"}})

    def get_secret(self, name):
        resp = self._call("tools/call", {"name": "mcp_secrets_get", "arguments": {"name": name}})
        try:
            content = resp["result"]["content"]
            data = json.loads(content[0]["text"])
            return data.get("value")
        except (KeyError, IndexError, ValueError, AttributeError):
            raise RuntimeError(f"mcp_secrets_get({name}) falhou: {resp}")

    def close(self):
        try:
            self.proc.terminate()
        except Exception:
            pass


def _read_secret(name):
    client = MCPClient(os.environ.get("BRACHAT_MCP_SERVER", "/home/ubuntu/ezra_bot1/.opencode/mcp/server.mjs"))
    try:
        client.initialize()
        return client.get_secret(name)
    except Exception:
        return None
    finally:
        client.close()


def groq_key_from_mcp():
    server = os.environ.get("BRACHAT_MCP_SERVER", "/home/ubuntu/ezra_bot1/.opencode/mcp/server.mjs")
    if not os.path.exists(server):
        return None
    return _read_secret("GROQ_API_KEY")
