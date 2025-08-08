import aiosqlite
from datetime import datetime
from backend.config import DB_PATH


async def save_conversation(user_id: int, question: str, answer: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        await db.execute(
            "INSERT INTO conversations (user_id, question, answer, timestamp) VALUES (?, ?, ?, ?)",
            (user_id, question, answer, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        await db.commit()
