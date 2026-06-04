import os
import psycopg2
import psycopg2.extras


def _connect():
    url = os.getenv("DATABASE_URL", "")
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return psycopg2.connect(url)


def init_db() -> None:
    conn = _connect()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id        BIGINT PRIMARY KEY,
                    height         REAL,
                    weight         REAL,
                    age            INTEGER,
                    gender         TEXT,
                    goal           TEXT,
                    daily_calories REAL
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS food_diary (
                    id        SERIAL PRIMARY KEY,
                    user_id   BIGINT,
                    food_name TEXT,
                    grams     REAL,
                    calories  REAL,
                    date      TEXT
                )
            """)
        conn.commit()
    finally:
        conn.close()


def get_user(user_id: int) -> dict | None:
    conn = _connect()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            row = cur.fetchone()
            return dict(row) if row else None
    finally:
        conn.close()


def save_user(user_id: int, height: float, weight: float,
              age: int, gender: str, goal: str) -> None:
    conn = _connect()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (user_id, height, weight, age, gender, goal)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (user_id) DO UPDATE SET
                    height = EXCLUDED.height,
                    weight = EXCLUDED.weight,
                    age    = EXCLUDED.age,
                    gender = EXCLUDED.gender,
                    goal   = EXCLUDED.goal
            """, (user_id, height, weight, age, gender, goal))
        conn.commit()
    finally:
        conn.close()


def update_calories(user_id: int, calories: int) -> None:
    conn = _connect()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE users SET daily_calories = %s WHERE user_id = %s",
                (calories, user_id),
            )
        conn.commit()
    finally:
        conn.close()


def delete_user(user_id: int) -> None:
    conn = _connect()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        conn.commit()
    finally:
        conn.close()


def get_today_entries(user_id: int, date: str) -> list:
    conn = _connect()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                "SELECT * FROM food_diary WHERE user_id = %s AND date = %s",
                (user_id, date),
            )
            return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()


def add_food_entry(user_id: int, food_name: str, grams: float,
                   calories: int, date: str) -> None:
    conn = _connect()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO food_diary (user_id, food_name, grams, calories, date)"
                " VALUES (%s, %s, %s, %s, %s)",
                (user_id, food_name, grams, calories, date),
            )
        conn.commit()
    finally:
        conn.close()
