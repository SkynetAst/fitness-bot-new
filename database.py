import sqlite3

DB_PATH = "fitness.db"


def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id        INTEGER PRIMARY KEY,
                height         REAL,
                weight         REAL,
                age            INTEGER,
                gender         TEXT,
                goal           TEXT,
                daily_calories REAL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS food_diary (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id   INTEGER,
                food_name TEXT,
                grams     REAL,
                calories  REAL,
                date      TEXT
            )
        """)
        conn.commit()
