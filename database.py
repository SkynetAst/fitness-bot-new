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


def get_user(user_id: int) -> dict | None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()
        return dict(row) if row else None


def save_user(user_id: int, height: float, weight: float,
              age: int, gender: str, goal: str) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """INSERT OR REPLACE INTO users
               (user_id, height, weight, age, gender, goal)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (user_id, height, weight, age, gender, goal),
        )
        conn.commit()


def update_calories(user_id: int, calories: int) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "UPDATE users SET daily_calories = ? WHERE user_id = ?",
            (calories, user_id),
        )
        conn.commit()


def delete_user(user_id: int) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()


def add_food_entry(user_id: int, food_name: str, grams: float,
                   calories: int, date: str) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO food_diary (user_id, food_name, grams, calories, date)"
            " VALUES (?, ?, ?, ?, ?)",
            (user_id, food_name, grams, calories, date),
        )
        conn.commit()
