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

ASSISTANT_ID = "asst_obkTcxOabucx8H50lbfQd99t"

import asyncio

async def ask_openai_assistant(user_message, thread_id=None):
    if not thread_id:
        thread = await openai.beta.threads.acreate()
        thread_id = thread.id

    await openai.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_message
    )

    run = await openai.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=ASSISTANT_ID
    )

    # Ждём завершения run (polling)
    while True:
        run_status = await openai.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        if run_status.status == "completed":
            break
        await asyncio.sleep(1)

    messages = await openai.beta.threads.messages.list(thread_id=thread_id)
    answer = messages.data[0].content[0].text.value
    return answer, thread_id

class ManyChatMessage(BaseModel):
    # Примерная структура, уточним позже по документации ManyChat
    user_id: str
    message: str
    raw: Dict[str, Any] = {}

@app.post("/manychat-webhook")
async def manychat_webhook(payload: ManyChatMessage):
    db: Session = SessionLocal()
    # Ищем последний thread_id для пользователя
    last_msg = db.query(Message).filter(Message.user_id == payload.user_id).order_by(Message.id.desc()).first()
    thread_id = last_msg.thread_id if last_msg else None
    ai_response, thread_id = await ask_openai_assistant(payload.message, thread_id)
    msg = Message(user_id=payload.user_id, message=payload.message, response=ai_response, thread_id=thread_id)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    db.close()
    return {"status": "ok", "message_id": msg.id, "response": ai_response} 