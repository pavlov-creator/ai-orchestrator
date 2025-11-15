from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any
import os
from openai import OpenAI

app = FastAPI()

# ---- МОДЕЛИ ----

class Message(BaseModel):
    role: str
    content: str

class TaskRequest(BaseModel):
    model: str
    messages: List[Message]

class TaskResponse(BaseModel):
    status: str
    payload: Dict[str, Any]


# ---- ИНИЦИАЛИЗАЦИЯ GPT ----

OPENAI_KEY = os.getenv("OPENAI_KEY")
client = OpenAI(api_key=OPENAI_KEY)


# ---- ОБРАБОТКА GPT ----

async def handle_gpt(messages: List[Message]) -> str:
    formatted = [{"role": m.role, "content": m.content} for m in messages]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=formatted,
        max_tokens=200
    )

    return response.choices[0].message.content


# ---- ENDPOINT /task ----

@app.post("/task", response_model=TaskResponse)
async def task(req: TaskRequest):

    if req.model == "gpt":
        answer = await handle_gpt(req.messages)
        return TaskResponse(
            status="ok",
            payload={"message": answer}
        )

    return TaskResponse(
        status="error",
        payload={"message": "unknown model"}
    )







