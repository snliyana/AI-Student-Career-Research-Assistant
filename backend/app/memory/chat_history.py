import sqlite3
from pathlib import Path
from datetime import datetime


# =========================================================
# DATABASE PATH
# =========================================================

DB_PATH = Path("data/chat_history.db")


# =========================================================
# INITIALIZE DATABASE
# =========================================================

def initialize_chat_db():
    """
    Create the chat history database and tables
    if they do not already exist.
    """

    DB_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # -----------------------------------------------------
    # Conversations Table
    # -----------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS conversations (
            thread_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            title TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )

    # -----------------------------------------------------
    # Messages Table
    # -----------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            thread_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(thread_id)
                REFERENCES conversations(thread_id)
        )
        """
    )

    conn.commit()
    conn.close()


# =========================================================
# CREATE CONVERSATION
# =========================================================

def create_conversation(
    thread_id: str,
    user_id: str,
    title: str
) -> None:
    """
    Create a new conversation.

    INSERT OR IGNORE prevents duplicate conversations
    when the same thread_id is used again.
    """

    initialize_chat_db()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    now = datetime.now().isoformat()

    cursor.execute(
        """
        INSERT OR IGNORE INTO conversations (
            thread_id,
            user_id,
            title,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            thread_id,
            user_id,
            title,
            now,
            now
        )
    )

    conn.commit()
    conn.close()


# =========================================================
# UPDATE CONVERSATION TITLE
# =========================================================

def update_conversation_title(
    thread_id: str,
    title: str
) -> None:
    """
    Update the title of an existing conversation.
    """

    initialize_chat_db()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE conversations
        SET title = ?
        WHERE thread_id = ?
        """,
        (
            title,
            thread_id
        )
    )

    conn.commit()
    conn.close()


# =========================================================
# SAVE MESSAGE
# =========================================================

def save_message(
    thread_id: str,
    role: str,
    content: str
) -> None:
    """
    Save a user or assistant message
    into the conversation.
    """

    initialize_chat_db()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    now = datetime.now().isoformat()

    cursor.execute(
        """
        INSERT INTO messages (
            thread_id,
            role,
            content,
            created_at
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            thread_id,
            role,
            content,
            now
        )
    )

    # Update conversation timestamp
    cursor.execute(
        """
        UPDATE conversations
        SET updated_at = ?
        WHERE thread_id = ?
        """,
        (
            now,
            thread_id
        )
    )

    conn.commit()
    conn.close()


# =========================================================
# GET RECENT CONVERSATIONS
# =========================================================

def get_recent_conversations(
    user_id: str,
    limit: int = 10
) -> list:
    """
    Return the user's most recent conversations.
    """

    initialize_chat_db()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            thread_id,
            title,
            created_at,
            updated_at
        FROM conversations
        WHERE user_id = ?
        ORDER BY updated_at DESC
        LIMIT ?
        """,
        (
            user_id,
            limit
        )
    )

    rows = cursor.fetchall()

    conn.close()

    return [
        {
            "thread_id": row[0],
            "title": row[1],
            "created_at": row[2],
            "updated_at": row[3]
        }
        for row in rows
    ]


# =========================================================
# GET CONVERSATION MESSAGES
# =========================================================

def get_conversation_messages(
    thread_id: str
) -> list:
    """
    Load all messages from one conversation.
    """

    initialize_chat_db()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            role,
            content,
            created_at
        FROM messages
        WHERE thread_id = ?
        ORDER BY id ASC
        """,
        (thread_id,)
    )

    rows = cursor.fetchall()

    conn.close()

    return [
        {
            "role": row[0],
            "content": row[1],
            "created_at": row[2]
        }
        for row in rows
    ]


# =========================================================
# DELETE CONVERSATION
# =========================================================

def delete_conversation(
    thread_id: str
) -> None:
    """
    Delete a conversation and all messages
    associated with that conversation.
    """

    initialize_chat_db()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Delete messages first
    cursor.execute(
        """
        DELETE FROM messages
        WHERE thread_id = ?
        """,
        (thread_id,)
    )

    # Delete conversation
    cursor.execute(
        """
        DELETE FROM conversations
        WHERE thread_id = ?
        """,
        (thread_id,)
    )

    conn.commit()
    conn.close()