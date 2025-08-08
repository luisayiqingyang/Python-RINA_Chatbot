# core/ai.py

from google import generativeai as genai
from backend.config import GEMINI_API_KEY, MODEL_NAME


class GeminiClient:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(MODEL_NAME)

    def get_response(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"[ERROR] Gemini API failed: {e}"
