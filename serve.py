#!/usr/bin/env python3
"""Local HTTP server so the dashboard can load data/policies.json."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
WEB = ROOT / "web"


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB), **kwargs)

    def do_POST(self):
        if urlparse(self.path).path != "/api/crawl":
            self.send_error(404)
            return
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scraper" / "crawl.py")],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        body = json.dumps({
            "ok": proc.returncode == 0,
            "code": proc.returncode,
            "stdout": (proc.stdout or "")[-4000],
            "stderr": (proc.stderr or "")[-2000],
        }).encode("utf-8")
        self.send_response(200 if proc.returncode == 0 else 500)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    httpd = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"Open http://127.0.0.1:{args.port}/")
    print("POST /api/crawl runs one crawl from the Refresh button.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
