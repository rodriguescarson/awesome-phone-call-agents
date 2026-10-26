"""Capture a running Call Review Console into snapshot/ as a static site.

    python scripts/build_snapshot.py http://127.0.0.1:8765 <console-token>

Reads come from JSON files; search and deep links keep working because the page's
`authed()` wrapper is rewritten to map each API path to its file. The note buttons
(the only writes) show a notice instead.
"""
import json, sys, urllib.request
from pathlib import Path

base, token = sys.argv[1].rstrip("/"), sys.argv[2]
root = Path(__file__).resolve().parents[1]
out = root / "snapshot"
(out / "api" / "calls").mkdir(parents=True, exist_ok=True)


def get(path):
    req = urllib.request.Request(f"{base}{path}", headers={"X-CRC-Console": token})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


for p in ("calls", "benchmark", "health"):
    (out / "api" / f"{p}.json").write_bytes(get(f"/api/{p}"))
for c in json.loads((out / "api" / "calls.json").read_text()):
    (out / "api" / "calls" / f"{c['id']}.json").write_bytes(get(f"/api/calls/{c['id']}"))
    (out / "api" / "calls" / f"{c['id']}.llm.json").write_bytes(get(f"/api/calls/{c['id']}?llm=true"))

NOTICE = ("This is a static snapshot of the Call Review Console taken on 26 Oct 2026, after the CALL-E "
          "hackathon closed. The Cloud Run service is retired; the five fixture calls, their reviews and the "
          "benchmark are the real output of the deterministic checks, and the note buttons no longer save.")
h = (root / "static" / "index.html").read_text()
for a, b in [
    ("const TOKEN=()=>sessionStorage.getItem('crcToken')||'';", "const TOKEN=()=>'snapshot';"),
    ("const authed=(u,o={})=>fetch(u,{...o,headers:{...(o.headers||{}),'X-CRC-Console':TOKEN()}});",
     "const authed=(u,o={})=>{if((o.method||'GET').toUpperCase()!=='GET'){alert(%s);return Promise.resolve(new Response('{}',{status:200}));}"
     "const [p,qs]=u.split('?');const q=new URLSearchParams(qs||'');"
     "let f=p==='/api/health'?'/api/health.json':p==='/api/calls'?'/api/calls.json':p==='/api/benchmark'?'/api/benchmark.json':"
     "p.startsWith('/api/calls/')?('/api/calls/'+decodeURIComponent(p.slice(11))+(q.get('llm')==='true'?'.llm':'')+'.json'):p;"
     "return fetch(f);};" % json.dumps(NOTICE)),
    ('<div class="shell">', '<div class="shell"><div style="padding:10px 16px;background:#c7891c;color:#111;font:500 13px/1.45 system-ui,sans-serif">'
     + NOTICE + ' <a href="https://github.com/CALLE-AI/awesome-phone-call-agents/tree/main/apps/web/call-review-console" style="color:inherit">Run it yourself from the repo.</a></div>'),
]:
    assert a in h, a
    h = h.replace(a, b, 1)
(out / "index.html").write_text(h)
print("wrote", out)
