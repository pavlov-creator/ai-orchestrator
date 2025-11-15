import logging
import os
from typing import List, Literal, Optional

from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

# Логер (Cloud Run забирает stdout)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai-orchestrator")

# Клиент OpenAI (ключ возьмём из переменной окружения OPENAI_API_KEY)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

app = FastAPI()


# ---------- МОДЕЛИ ЗАПРОСА ----------

class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class TaskPayload(BaseModel):
    model: str                    # например: "gpt"
    messages: List[Message]       # массив сообщений
    step: Optional[int] = None    # шаг сценария (опционально)


# ---------- ЭНДПОИНТЫ ЗДОРОВЬЯ ----------

@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/health")
def health():
    return {"status": "healthy"}


# ---------- ОСНОВНОЙ ЭНДПОИНТ /task ----------

@app.post("/task")
async def run_task(payload: TaskPayload):
    """
    Оркестратор задачи.

    Сейчас логика простая:
    - если model == "gpt" — вызываем OpenAI GPT (gpt-4.1-mini)
    - остальное пока заглушка
    """

    logger.info(
        "task_received | model=%s | step=%s | messages_count=%s",
        payload.model,
        payload.step,
        len(payload.messages),
    )

    # Ветка для GPT
    if payload.model == "gpt":
        # Готовим сообщения в формате OpenAI SDK
        oa_messages = [m.model_dump() for m in payload.messages]

        # Вызов OpenAI Chat Completions
        response = client.chat.completions.create(
            model="gpt-4.1-mini",   # можно сменить позже на другой id
            messages=oa_messages,
            max_tokens=256,
        )

        answer = response.choices[0].message.content

        logger.info(
            "task_completed | model=%s | step=%s | answer=%s",
            payload.model,
            payload.step,
            answer,
        )

        return {
            "status": "ok",
            "model": "gpt",
            "step": payload.step,
            "answer": answer,
        }

    # Заглушка для остальных моделей (мы их подключим дальше)
    logger.info(
        "task_model_not_implemented | model=%s | step=%s",
        payload.model,
        payload.step,
    )

    return {
        "status": "not_implemented",
        "model": payload.model,
        "step": payload.step,
        "answer": None,
    }


# Локальный запуск (для dev). В Cloud Run используется uvicorn из Dockerfile.
if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8080"))
    uvicorn.run("main:app", host="0.0.0.0", port=port)








