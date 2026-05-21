import sqlite3

DB_NAME = "facts.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS facts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        claim TEXT UNIQUE,
        status TEXT,
        evidence TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """ )

    conn.commit()
    conn.close()