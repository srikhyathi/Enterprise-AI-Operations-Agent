import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "database" / "operations.db"

def get_connection():
    c = sqlite3.connect(DATABASE_PATH)
    c.row_factory = sqlite3.Row
    return c

def initialize_database():
    c = get_connection()
    c.execute("""
    CREATE TABLE IF NOT EXISTS incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        incident_number TEXT UNIQUE NOT NULL,
        metric TEXT NOT NULL,
        value REAL NOT NULL,
        severity TEXT NOT NULL,
        message TEXT NOT NULL,
        root_cause TEXT DEFAULT '[]',
        recommendations TEXT DEFAULT '[]',
        status TEXT NOT NULL DEFAULT 'OPEN',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        remediation_action TEXT,
        remediation_result TEXT,
        verified INTEGER DEFAULT 0
    )""")
    existing = {r["name"] for r in c.execute("PRAGMA table_info(incidents)").fetchall()}
    migrations = {
        "root_cause": "TEXT DEFAULT '[]'",
        "recommendations": "TEXT DEFAULT '[]'",
        "updated_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "remediation_action": "TEXT",
        "remediation_result": "TEXT",
        "verified": "INTEGER DEFAULT 0",
    }
    for col, typ in migrations.items():
        if col not in existing:
            c.execute(f"ALTER TABLE incidents ADD COLUMN {col} {typ}")
    c.commit()
    c.close()
