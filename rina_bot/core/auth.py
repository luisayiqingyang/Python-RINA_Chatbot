# core/auth.py

from core.database import ConversationDB


class Authenticator:
    def __init__(self):
        self.db = ConversationDB()

    def login(self, username: str, password: str) -> int | None:
        return self.db.validate_user(username, password)

    def register(self, username: str, password: str) -> tuple[bool, str | None]:
        return self.db.create_user(username, password)
