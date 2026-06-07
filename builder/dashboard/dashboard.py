#!/usr/bin/env python3
"""BRACHAT Dashboard — servidor HTTP que serve index.html."""
import http.server, json, subprocess, time
from pathlib import Path

HOST = "0.0.0.0"; PORT = 8080
HTML = (Path(__file__).parent / "index.html").read_text(encoding="utf-8")

def run(cmd):
    try: return subprocess.run(cmd, capture_output=True, text=True, timeout=5).stdout.strip()
    except: return ""

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/status":
            data = {
                "git":{
                    "branch":run(["bash","-c","git -C /opt/brachat/repo rev-parse --abbrev-ref HEAD 2>/dev/null||echo -"]),
                    "last_commit":run(["bash","-c","git -C /opt/brachat/repo log --oneline -1 2>/dev/null||echo -"]),
                },
                "timestamp":time.strftime("%d/%m/%Y %H:%M:%S"),
            }
            self.send_response(200)
            self.send_header("Content-Type","application/json")
            self.send_header("Access-Control-Allow-Origin","*")
            self.end_headers()
            self.wfile.write(json.dumps(data,indent=2).encode())
        else:
            self.send_response(200)
            self.send_header("Content-Type","text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML.encode())

if __name__=="__main__":
    print(f"BRACHAT Organograma em http://{HOST}:{PORT}")
    http.server.HTTPServer((HOST,PORT),Handler).serve_forever()
