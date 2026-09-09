import sqlite3
from pathlib import Path


DB_PATH = Path("data/memory.db")


def initialize_memory_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            memory_key TEXT NOT NULL,
            memory_value TEXT NOT NULL,
            UNIQUE(user_id, memory_key)
        )
        """
    )

    conn.commit()
    conn.close()


def save_memory(
    user_id: str,
    memory_key: str,
    memory_value: str
) -> None:

    initialize_memory_db()

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO user_memory (
            user_id,
            memory_key,
            memory_value
        )
        VALUES (?, ?, ?)
        ON CONFLICT(user_id, memory_key)
        DO UPDATE SET
            memory_value = excluded.memory_value
        """,
        (
            user_id,
            memory_key,
            memory_value
        )
    )

    conn.commit()
    conn.close()


def get_memory(
    user_id: str,
    memory_key: str
):

    initialize_memory_db()

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT memory_value
        FROM user_memory
        WHERE user_id = ?
        AND memory_key = ?
        """,
        (
            user_id,
            memory_key
        )
    )

    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]

    return None


def get_all_memories(
    user_id: str
) -> dict:

    initialize_memory_db()

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT memory_key, memory_value
        FROM user_memory
        WHERE user_id = ?
        """,
        (user_id,)
    )

    rows = cursor.fetchall()

    conn.close()

    return {
        key: value
        for key, value in rows
    }