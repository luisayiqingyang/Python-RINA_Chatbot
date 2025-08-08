# config.py
import os
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(os.path.dirname(__file__), "conversations.db")
GEMINI_API_KEY = ""
MODEL_NAME = "gemini-2.0-flash-exp"
