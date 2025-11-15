from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import os

app = FastAPI()


class TaskPayload(BaseModel):
    message: str
    step: int


# --- Simple LLM router (прототип) ---
def route_to_llm(message: str, step: int):
    """
    Простейший роутер.
    Здесь позже будут реальные вызовы OpenAI / DeepSeek / Gemini / Anthropic.
    Сейчас это заглушка, чтобы проверить архитектуру.
    """

    text = message.lower()

    if "анализ" in text:
        llm = "gpt-4.1"              # пример: аналитика
    elif "код" in text:
        llm = "deepseek-coder"       # пример: генерация кода
    else:
        llm = "claude-3.5-sonnet"    # пример: универсальные задачи

    return {
        "selected_llm": llm,
        "input_message": message,
        "step": step,
        "output": f"LLM({llm}) получил сообщение: {message}",
    }


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/task")
async def task(payload: TaskPayload):
    # лог в stdout → попадает в Cloud Run Logs
    print(
        f"NEW_TASK message={payload.message!r} step={payload.step}",
        flush=True,
    )

    result = route_to_llm(payload.message, payload.step)

    return {
        "status": "processed",
        "result": result,
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=port)
















