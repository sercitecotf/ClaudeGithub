#!/usr/bin/env python3
"""Sirve las tres webs en local para verlas en el navegador.

Uso:  python3 tools/preview.py      (Windows: python tools\\preview.py)
Pulsa Ctrl+C para parar. No necesita dependencias.
"""
import functools
import http.server
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITES = [("guiadeisora", 8001), ("imosinformatica", 8002), ("sanisidrodeabona", 8003)]


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


servers = []
for name, port in SITES:
    handler = functools.partial(Quiet, directory=str(ROOT / name))
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    servers.append(srv)
    print(f"{name:18s} http://localhost:{port}")

print("\nIdiomas: añade /en/ o /de/ (ej. http://localhost:8001/en/). Ctrl+C para parar.")
try:
    threading.Event().wait()
except KeyboardInterrupt:
    for s in servers:
        s.shutdown()
