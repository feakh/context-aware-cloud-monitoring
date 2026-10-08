"""SQLite storage for observations and their classifications."""
import json
import sqlite3
from contextlib import closing
from pathlib import Path

class Store:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with closing(sqlite3.connect(self.path)) as db, db:
            db.execute('CREATE TABLE IF NOT EXISTS observations (id INTEGER PRIMARY KEY, timestamp TEXT NOT NULL, priority TEXT NOT NULL, payload TEXT NOT NULL)')

    def save(self, result):
        with closing(sqlite3.connect(self.path)) as db, db:
            cursor = db.execute('INSERT INTO observations(timestamp, priority, payload) VALUES (?, ?, ?)',
                (result['timestamp'], result['priority'], json.dumps(result)))
            return cursor.lastrowid

    def list(self):
        with closing(sqlite3.connect(self.path)) as db, db:
            rows = db.execute('SELECT id, payload FROM observations ORDER BY id DESC LIMIT 200').fetchall()
        return [dict(json.loads(payload), id=identifier) for identifier, payload in rows]
