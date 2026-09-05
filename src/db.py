"""
Lightweight SQLite persistence for CerviXAI accounts, profiles and
assessment history.

Why this exists: the original app kept everything (login, profile,
history) in an in-memory singleton inside the Flutter client, so it was
reset every time the app process restarted or the user logged out.
Moving accounts/profile/history to the backend means they survive
closing the app, reinstalling it, or switching devices.
"""
from __future__ import annotations

import json
import os
import secrets
import sqlite3
import threading
from datetime import datetime, timezone

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "cervixai.db")

_lock = threading.Lock()


def _connect():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


_conn = _connect()


def init_db():
    with _lock, _conn:
        _conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                password_salt TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        _conn.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                token TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """
        )
        _conn.execute(
            """
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                kind TEXT NOT NULL,
                title TEXT NOT NULL,
                result TEXT NOT NULL,
                risk_percent REAL,
                details_json TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """
        )


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------
# Users
# ---------------------------------------------------------------------

def create_user(name: str, username: str, email: str, password_hash: str, password_salt: str) -> sqlite3.Row:
    with _lock, _conn:
        cur = _conn.execute(
            "INSERT INTO users (name, username, email, password_hash, password_salt, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (name, username, email, password_hash, password_salt, now_iso()),
        )
        user_id = cur.lastrowid
    return get_user_by_id(user_id)


def get_user_by_username(username: str):
    cur = _conn.execute("SELECT * FROM users WHERE username = ?", (username,))
    return cur.fetchone()


def get_user_by_email(email: str):
    cur = _conn.execute("SELECT * FROM users WHERE email = ?", (email,))
    return cur.fetchone()


def get_user_by_id(user_id: int):
    cur = _conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cur.fetchone()


def update_user_profile(user_id: int, name: str, email: str):
    with _lock, _conn:
        _conn.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id))
    return get_user_by_id(user_id)


def update_user_password(user_id: int, password_hash: str, password_salt: str):
    with _lock, _conn:
        _conn.execute(
            "UPDATE users SET password_hash = ?, password_salt = ? WHERE id = ?",
            (password_hash, password_salt, user_id),
        )


# ---------------------------------------------------------------------
# Sessions (simple bearer tokens; no expiry logic needed for this app's
# scope, but logout removes the row so the token stops working)
# ---------------------------------------------------------------------

def create_session(user_id: int) -> str:
    token = secrets.token_hex(32)
    with _lock, _conn:
        _conn.execute(
            "INSERT INTO sessions (token, user_id, created_at) VALUES (?, ?, ?)",
            (token, user_id, now_iso()),
        )
    return token


def get_user_id_for_token(token: str):
    cur = _conn.execute("SELECT user_id FROM sessions WHERE token = ?", (token,))
    row = cur.fetchone()
    return row["user_id"] if row else None


def delete_session(token: str):
    with _lock, _conn:
        _conn.execute("DELETE FROM sessions WHERE token = ?", (token,))


# ---------------------------------------------------------------------
# History
# ---------------------------------------------------------------------

def add_history_entry(user_id: int, kind: str, title: str, result: str, risk_percent, details: dict):
    with _lock, _conn:
        _conn.execute(
            "INSERT INTO history (user_id, kind, title, result, risk_percent, details_json, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (user_id, kind, title, result, risk_percent, json.dumps(details), now_iso()),
        )


def list_history(user_id: int):
    cur = _conn.execute(
        "SELECT id, kind, title, result, risk_percent, details_json, created_at "
        "FROM history WHERE user_id = ? ORDER BY id DESC",
        (user_id,),
    )
    rows = []
    for r in cur.fetchall():
        rows.append({
            "id": r["id"],
            "kind": r["kind"],
            "title": r["title"],
            "result": r["result"],
            "risk_percent": r["risk_percent"],
            "details": json.loads(r["details_json"]) if r["details_json"] else {},
            "created_at": r["created_at"],
        })
    return rows


def clear_history(user_id: int):
    with _lock, _conn:
        _conn.execute("DELETE FROM history WHERE user_id = ?", (user_id,))


def delete_history_entry(user_id: int, entry_id: int):
    with _lock, _conn:
        _conn.execute("DELETE FROM history WHERE user_id = ? AND id = ?", (user_id, entry_id))
