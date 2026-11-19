"""Local, dependency-free HTML dashboard for test and healing reports."""
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import json, html
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'reports'/'healing_events.jsonl'

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        events=[]
        if REPORT.exists():
            for line in REPORT.read_text(encoding='utf-8').splitlines():
                try: events.append(json.loads(line))
                except json.JSONDecodeError: pass
        counts={s:sum(e.get('status')==s for e in events) for s in ('HEALED','FAILED','REJECTED')}
        rows = ''
        for event in reversed(events[-200:]):
            cells = ''.join('<td>' + html.escape(str(event.get(key, ''))) + '</td>' for key in ('timestamp','original_id','replacement_locator','confidence','status','reason'))
            rows += '<tr>' + cells + '</tr>'
        body=f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>SmartTest AI Dashboard</title><style>body{{font:15px system-ui;background:#101827;color:#e5edf7;margin:32px}}.cards{{display:flex;gap:16px;flex-wrap:wrap}}.card{{background:#1d2a3d;padding:20px;border-radius:12px;min-width:130px}}strong{{font-size:28px}}table{{border-collapse:collapse;width:100%;margin-top:24px}}td,th{{padding:10px;border-bottom:1px solid #34445c;text-align:left}}small{{color:#a8b7ca}}</style></head><body><h1>SmartTest AI</h1><small>Self-healing activity · latest 200 events</small><div class="cards">{''.join(f'<div class="card"><small>{k}</small><br><strong>{v}</strong></div>' for k,v in counts.items())}<div class="card"><small>Total events</small><br><strong>{len(events)}</strong></div></div><table><tr><th>Timestamp</th><th>Original</th><th>Replacement</th><th>Confidence</th><th>Status</th><th>Reason</th></tr>{rows}</table></body></html>'''
        self.send_response(200); self.send_header('Content-Type','text/html; charset=utf-8'); self.end_headers(); self.wfile.write(body.encode())
    def log_message(self,*args): pass

def main():
    print('Dashboard: http://127.0.0.1:8765'); HTTPServer(('127.0.0.1',8765),Handler).serve_forever()
if __name__=='__main__': main()
