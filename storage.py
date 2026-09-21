import os
import sqlite3
import config

def db():
    os.makedirs(os.path.dirname(config.DB_PATH) or ".", exist_ok=True)
    c = sqlite3.connect(config.DB_PATH)
    c.execute("CREATE TABLE IF NOT EXISTS seen (id TEXT PRIMARY KEY, ts INTEGER)")
    return c

def is_new(c, pid):
    r = c.execute("SELECT 1 FROM seen WHERE id=?", (pid,)).fetchone()
    return r is None

def mark(c, pid, ts):
    c.execute("INSERT OR IGNORE INTO seen (id, ts) VALUES (?,?)", (pid, ts))
    c.commit()
