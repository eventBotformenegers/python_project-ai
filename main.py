# Для запуска локально: uvicorn main:app --reload
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Dict, Any
from db import init_db, SessionLocal, Message
from sqlalchemy.orm import Session
import os
import openai

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

openai.api_key = os.getenv("OPENAI_API_KEY")

async def ask_openai(prompt: str) -> str:
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[OpenAI error: {e}]"

class ManyChatMessage(BaseModel):
    # Примерная структура, уточним позже по документации ManyChat
    user_id: str
    message: str
    raw: Dict[str, Any] = {}

@app.post("/manychat-webhook")
async def manychat_webhook(payload: ManyChatMessage):
    db: Session = SessionLocal()
    ai_response = await ask_openai(payload.message)
    msg = Message(user_id=payload.user_id, message=payload.message, response=ai_response)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    db.close()
    return {"status": "ok", "message_id": msg.id, "response": ai_response} 