#!/usr/bin/env python3
"""Serves index.html and persists its checkbox/note state to a local SQLite file.

Usage: python3 server.py
Then open http://localhost:8000/index.html
"""
import http.server
import json
import socketserver
import sqlite3

PORT = 8000
DB_PATH = "state.db"
EMPTY_STATE = json.dumps({"completed": {}, "notes": {}})


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS state (id INTEGER PRIMARY KEY CHECK (id = 1), data TEXT NOT NULL)")
    return conn


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
