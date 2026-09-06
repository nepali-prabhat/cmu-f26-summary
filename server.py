#!/usr/bin/env python3
"""Serves index.html and persists its checkbox/note state to a local SQLite file.

Usage: python3 server.py
Then open http://localhost:8000/index.html
"""
import http.server
import json
import os
import re
import socketserver
import sqlite3
import subprocess

PORT = 8000
DB_PATH = "state.db"
EMPTY_STATE = json.dumps({"completed": {}, "notes": {}})
VIZ_DATA_RE = re.compile(
    r'<script type="application/json" id="viz-data">(.*?)</script>', re.S
)


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS state (id INTEGER PRIMARY KEY CHECK (id = 1), data TEXT NOT NULL)")
    return conn


def get_course_folders():
    """Course code -> folder path, read straight from index.html's embedded
    viz-data JSON so this stays the single source of truth (no duplicated list)."""
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    match = VIZ_DATA_RE.search(html)
    if not match:
        return {}
    data = json.loads(match.group(1))
    return {c["code"]: c["folder"] for c in data["courses"] if c.get("folder")}


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/state":
            conn = get_db()
            row = conn.execute("SELECT data FROM state WHERE id = 1").fetchone()
            conn.close()
            self._send_json((row[0] if row else EMPTY_STATE).encode("utf-8"))
            return
        super().do_GET()

    def do_POST(self):
        if self.path == "/api/open-folder":
            self._handle_open_folder()
            return
        if self.path != "/api/state":
            self.send_response(404)
            self.end_headers()
            return
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length)
        try:
            json.loads(raw)
        except ValueError:
            self.send_response(400)
            self.end_headers()
            return
        conn = get_db()
        conn.execute(
            "INSERT INTO state (id, data) VALUES (1, ?) "
            "ON CONFLICT(id) DO UPDATE SET data = excluded.data",
            (raw.decode("utf-8"),),
        )
        conn.commit()
        conn.close()
        self.send_response(204)
        self.end_headers()

    def _handle_open_folder(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length)
        try:
            body = json.loads(raw)
            course = body["course"]
        except (ValueError, KeyError, TypeError):
            self.send_response(400)
            self.end_headers()
            return

        folders = get_course_folders()
        folder = folders.get(course)
        if not folder:
            self.send_response(404)
            self.end_headers()
            return

        path = os.path.expanduser(folder)
        if not os.path.isdir(path):
            self.send_response(404)
            self.end_headers()
            return

        try:
            subprocess.run(["open", path], check=True)
        except (OSError, subprocess.CalledProcessError):
            self.send_response(500)
            self.end_headers()
            return

        self.send_response(204)
        self.end_headers()

    def _send_json(self, body):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving http://localhost:{PORT}/index.html  (state -> {DB_PATH})")
        httpd.serve_forever()
