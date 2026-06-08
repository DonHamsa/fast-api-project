import sqlite3
import os

DB_PATH = os.getenv("DB_PATH", "game.db")


def _conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    with _conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                username      TEXT    UNIQUE NOT NULL,
                secret_number INTEGER NOT NULL,
                guess_count   INTEGER NOT NULL DEFAULT 0,
                solved        INTEGER NOT NULL DEFAULT 0
            )
        """)
        conn.commit()


def get_player(username: str) -> dict | None:
    with _conn() as conn:
        row = conn.execute(
            "SELECT * FROM players WHERE username = ?", (username,)
        ).fetchone()
    return dict(row) if row else None


def create_player(username: str, secret: int):
    with _conn() as conn:
        conn.execute(
            "INSERT INTO players (username, secret_number) VALUES (?, ?)",
            (username, secret),
        )
        conn.commit()


def update_guess(username: str, new_count: int, solved: bool):
    with _conn() as conn:
        conn.execute(
            "UPDATE players SET guess_count = ?, solved = ? WHERE username = ?",
            (new_count, 1 if solved else 0, username),
        )
        conn.commit()


def get_leaderboard() -> list[dict]:
    with _conn() as conn:
        rows = conn.execute(
            "SELECT username, guess_count FROM players WHERE solved = 1 ORDER BY guess_count ASC, username ASC"
        ).fetchall()
    return [dict(r) for r in rows]
