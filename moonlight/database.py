import sqlite3
import threading
import time

START_BALANCE = 1000

# ---------- THREAD SAFETY ----------
lock = threading.Lock()

conn = sqlite3.connect(
    "moonlight.db",
    check_same_thread=False
)
cursor = conn.cursor()

# ---------- TABLES ----------
with lock:
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        balance INTEGER NOT NULL,
        last_daily INTEGER DEFAULT 0
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        leader_id INTEGER,
        balance INTEGER DEFAULT 0,
        level INTEGER DEFAULT 1
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clan_members (
        user_id INTEGER UNIQUE,
        clan_id INTEGER,
        role TEXT
    )
    """)

    conn.commit()

# ---------- USERS ----------
def ensure_user(user_id: int):
    with lock:
        cursor.execute(
            "INSERT OR IGNORE INTO users (user_id, balance, last_daily) VALUES (?, ?, ?)",
            (user_id, START_BALANCE, 0)
        )
        conn.commit()

def get_balance(user_id: int) -> int:
    ensure_user(user_id)
    with lock:
        cursor.execute(
            "SELECT balance FROM users WHERE user_id = ?",
            (user_id,)
        )
        return cursor.fetchone()[0]

def update_balance(user_id: int, change: int):
    ensure_user(user_id)
    with lock:
        cursor.execute(
            "UPDATE users SET balance = balance + ? WHERE user_id = ?",
            (change, user_id)
        )
        conn.commit()

def set_balance(user_id: int, amount: int):
    ensure_user(user_id)
    with lock:
        cursor.execute(
            "UPDATE users SET balance = ? WHERE user_id = ?",
            (amount, user_id)
        )
        conn.commit()

def get_top_balances(limit=10):
    with lock:
        cursor.execute(
            "SELECT user_id, balance FROM users ORDER BY balance DESC LIMIT ?",
            (limit,)
        )
        return cursor.fetchall()

# ---------- DAILY ----------
def get_last_daily(user_id: int) -> int:
    ensure_user(user_id)
    with lock:
        cursor.execute(
            "SELECT last_daily FROM users WHERE user_id = ?",
            (user_id,)
        )
        return cursor.fetchone()[0]

def set_daily(user_id: int, timestamp: int):
    ensure_user(user_id)
    with lock:
        cursor.execute(
            "UPDATE users SET last_daily = ? WHERE user_id = ?",
            (timestamp, user_id)
        )
        conn.commit()