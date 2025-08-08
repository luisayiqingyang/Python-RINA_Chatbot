import sqlite3
from datetime import datetime
from backend.config import DB_PATH
import bcrypt


def is_valid_password(password: str) -> bool:
    return (
        len(password) >= 8
        and any(c.isupper() for c in password)
        and any(c in "*_#" for c in password)
    )


class ConversationDB:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT,
                created_at TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                session_id INTEGER,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (session_id) REFERENCES sessions(id)
            )
        ''')
        self.conn.commit()

    def create_user(self, username: str, password: str) -> tuple[bool, str]:
        if not is_valid_password(password):
            return False, "Password must be at least 8 characters, include one uppercase letter, and one of: * _ #"
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        try:
            self.cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            self.conn.commit()
            return True, None
        except sqlite3.IntegrityError:
            return False, "Username already exists."

    def validate_user(self, username: str, password: str):
        self.cursor.execute(
            "SELECT id, password_hash FROM users WHERE username = ?", (username,)
        )
        row = self.cursor.fetchone()
        if row and bcrypt.checkpw(password.encode(), row[1]):
            return row[0]
        return None

    def save(self, user_id: int, question: str, answer: str, session_id: int = None):
        if user_id is None:
            print("EROARE: save() apelat cu user_id=None")
            return
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''
            INSERT INTO conversations (user_id, session_id, question, answer, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, session_id, question, answer, timestamp))
        self.conn.commit()

    def get_conversation_by_session(self, session_id: int):
        self.cursor.execute('''
            SELECT question, answer, timestamp FROM conversations
            WHERE session_id = ? ORDER BY id ASC
        ''', (session_id,))
        return self.cursor.fetchall()

    def get_sessions(self, user_id: int):
        self.cursor.execute('''
            SELECT id, title, created_at FROM sessions
            WHERE user_id = ? ORDER BY id DESC
        ''', (user_id,))
        return self.cursor.fetchall()

    def create_session(self, user_id: int, title: str = "New Chat") -> int:
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''
            INSERT INTO sessions (user_id, title, created_at) VALUES (?, ?, ?)
        ''', (user_id, title, created_at))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_latest_session(self, user_id: int):
        self.cursor.execute('''
            SELECT id FROM sessions WHERE user_id = ? ORDER BY id DESC LIMIT 1
        ''', (user_id,))
        row = self.cursor.fetchone()
        return row[0] if row else None

    def rename_session(self, session_id: int, new_title: str):
        self.cursor.execute("UPDATE sessions SET title = ? WHERE id = ?", (new_title, session_id))
        self.conn.commit()

    def delete_session(self, session_id: int):
        self.cursor.execute("DELETE FROM conversations WHERE session_id = ?", (session_id,))
        self.cursor.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
        self.conn.commit()

    def delete_user(self, user_id: int):
        self.cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.cursor.execute("DELETE FROM sessions WHERE user_id = ?", (user_id,))
        self.cursor.execute("DELETE FROM conversations WHERE user_id = ?", (user_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()
