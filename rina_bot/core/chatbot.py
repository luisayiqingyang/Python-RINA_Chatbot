# core/chatbot.py

from core.ai import GeminiClient
from core.database import ConversationDB


class ChatBot:
    def __init__(self):
        self.ai = GeminiClient()
        self.db = ConversationDB()

    def ask(self, user_id: int, question: str, session_id: int = None) -> str:
        answer = self.ai.get_response(question)
        self.db.save(user_id, question, answer, session_id)
        return answer

    def close(self):
        self.db.close()
