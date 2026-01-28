import sqlite3
import time

START_BALANCE = 1000

conn = sqlite3.connect("moonlight.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    balance INTEGER,
    last_daily INTEGER DEFAULT 0
)
""")
conn.commit()

def get_balance(user_id: int) -> int:
    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    if row is None:
        cursor.execute(
            "INSERT INTO users (user_id, balance, last_daily) VALUES (?, ?, ?)",
            (user_id, START_BALANCE, 0)
        )
        conn.commit()
        return START_BALANCE
    return row[0]

def ensure_user(user_id: int):
    cursor.execute(
        "SELECT 1 FROM users WHERE user_id = ?",
        (user_id,)
    )
    if cursor.fetchone() is None:
        cursor.execute(
            "INSERT INTO users (user_id, balance, last_daily) VALUES (?, ?, ?)",
            (user_id, START_BALANCE, 0)
        )
        conn.commit()

def set_balance(user_id: int, amount: int):
    cursor.execute(
        "UPDATE users SET balance = ? WHERE user_id = ?",
        (amount, user_id)
    )
    conn.commit()

def get_top_balances(limit=10):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT user_id, balance FROM users ORDER BY balance DESC LIMIT ?",
        (limit,)
    )
    return cursor.fetchall()

def get_last_daily(user_id: int) -> int:
    cursor.execute("SELECT last_daily FROM users WHERE user_id = ?", (user_id,))
    return cursor.fetchone()[0]

def set_daily(user_id: int, timestamp: int) -> None:
    cursor.execute(
        "UPDATE users SET last_daily = ? WHERE user_id = ?",
        (timestamp, user_id)
    )

def db_get_daily(user_id: int) -> int:
    ensure_user(user_id)
    cursor.execute(
        "SELECT last_daily FROM users WHERE user_id = ?",
        (user_id,)
    )
    row = cursor.fetchone()
    return row[0] if row and row[0] is not None else 0
    conn.commit()
