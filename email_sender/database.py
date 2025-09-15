"""
Lightweight SQLite storage for conversations and messages.
"""

import os
import sqlite3
from contextlib import contextmanager
from typing import Optional, Tuple, Dict, Any


DB_PATH = os.environ.get("EMAIL_DB_PATH", os.path.join(os.path.dirname(__file__), "email_conversations.db"))


def init_db() -> None:
    with get_conn() as con:
        cur = con.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT,
                prospect_email TEXT,
                last_message_id TEXT,
                status TEXT DEFAULT 'open',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER,
                direction TEXT,
                message_id TEXT,
                in_reply_to TEXT,
                headers TEXT,
                body_text TEXT,
                body_html TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(message_id)
            );
            """
        )
        con.commit()


@contextmanager
def get_conn():
    con = sqlite3.connect(DB_PATH)
    try:
        yield con
    finally:
        con.close()


def find_conversation_by_message_ref(in_reply_to: Optional[str], prospect_email: Optional[str]) -> Optional[int]:
    with get_conn() as con:
        cur = con.cursor()
        if in_reply_to:
            cur.execute(
                """
                SELECT conversation_id FROM messages WHERE message_id = ?
                """,
                (in_reply_to,),
            )
            row = cur.fetchone()
            if row:
                return row[0]
        if prospect_email:
            cur.execute(
                """
                SELECT id FROM conversations WHERE prospect_email = ? ORDER BY id DESC LIMIT 1
                """,
                (prospect_email,),
            )
            row = cur.fetchone()
            if row:
                return row[0]
    return None


def upsert_conversation(subject: str, prospect_email: str) -> int:
    with get_conn() as con:
        cur = con.cursor()
        cur.execute(
            """
            INSERT INTO conversations(subject, prospect_email)
            VALUES(?, ?)
            """,
            (subject, prospect_email),
        )
        con.commit()
        return cur.lastrowid


def insert_message(conversation_id: int, direction: str, message_id: Optional[str], in_reply_to: Optional[str], headers: Optional[str], body_text: Optional[str], body_html: Optional[str]) -> int:
    with get_conn() as con:
        cur = con.cursor()
        cur.execute(
            """
            INSERT OR IGNORE INTO messages(conversation_id, direction, message_id, in_reply_to, headers, body_text, body_html)
            VALUES(?, ?, ?, ?, ?, ?, ?)
            """,
            (conversation_id, direction, message_id, in_reply_to, headers, body_text, body_html),
        )
        con.commit()
        return cur.lastrowid


def set_conversation_last_message(conversation_id: int, message_id: Optional[str]) -> None:
    with get_conn() as con:
        cur = con.cursor()
        cur.execute(
            """
            UPDATE conversations
            SET last_message_id = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (message_id, conversation_id),
        )
        con.commit()


