import sqlite3
from datetime import datetime

DB_PATH = "bot_history.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                role TEXT,
                content TEXT,
                timestamp DATETIME
            )
        """)
        conn.commit()

def add_message(chat_id, role, content):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO messages (chat_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
            (chat_id, role, content, datetime.now())
        )
        conn.commit()

def get_history(chat_id, limit=10):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            "SELECT role, content FROM messages WHERE chat_id = ? ORDER BY timestamp DESC LIMIT ?",
            (chat_id, limit)
        )
        # Форматируем историю в строку для Gemma
        history = cursor.fetchall()
        formatted_history = ""
        for role, content in history[::-1]:  # Возвращаем в хронологическом порядке
            formatted_history += f"{role.capitalize()}: {content}\n"
        formatted_history += "Assistant:"  # Подсказка модели
        return formatted_history
