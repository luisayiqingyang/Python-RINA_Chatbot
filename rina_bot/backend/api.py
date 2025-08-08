from fastapi import FastAPI
# from fastapi import Request
from pydantic import BaseModel
import google.generativeai as genai
from backend.db import save_conversation
from backend.config import GEMINI_API_KEY, MODEL_NAME
# import threading
# import asyncio
# import time

app = FastAPI()

cache = {}  # Format: {(user_id, question): response}

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)


class ChatInput(BaseModel):
    message: str
    user_id: int


@app.post("/chat")
async def chat_endpoint(chat: ChatInput):
    question = chat.message.strip().lower()
    user_id = chat.user_id

    print(f"[BACKEND] user_id={user_id}, question='{question}'")

    if not user_id:
        return {"response": "[ERROR] user not authenticated."}

    cache_key = (user_id, question)
    if cache_key in cache:
        print("[CACHE HIT]")
        return {"response": cache[cache_key]}

    try:
        response = await model.generate_content_async(question)
        reply = response.text.strip()
        cache[cache_key] = reply
        await save_conversation(user_id, question, reply)
        return {"response": reply}
    except Exception as e:
        return {"response": f"[ERROR] {e}"}


@app.get("/ping")
async def ping():
    try:
        await model.generate_content_async("ping")
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
