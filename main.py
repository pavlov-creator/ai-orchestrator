from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import os
from typing import Optional

app = FastAPI()


class TaskPayload(BaseModel):
    message: Optional[str] = None
    step: Optional[int] = None


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/health")
def health():
    return {"status": "healthy"}


from typing import Optional
from pydantic import BaseModel
# эти импорты у тебя уже должны быть вверху файла, но если чего-то нет – добавь

class TaskPayload(BaseModel):
    message: str
    step: Optional[int] = 0


@app.post("/task")
async def task(payload: TaskPayload):
    """
    Простейший «движок шагов».
    Мы смотрим на step и даём ответ, что делать дальше.
    """

    current_step = payload.step or 0

    if current_step == 0:
        next_step = 1
        reply = (
            "Шаг 0. Я принял задачу. "
            "В двух-трёх предложениях опиши, что ты хочешь получить в итоге."
        )
    elif current_step == 1:
        next_step = 2
        reply = (
            "Шаг 1. Давай набросаем варианты / идеи. "
            "Напиши несколько вариантов, как можно подойти к задаче."
        )
    elif current_step == 2:
        next_step = 3
        reply = (
            "Шаг 2. Выбери один вариант, который нравится больше всего. "
            "Напиши, почему именно он."
        )
    else:
        next_step = current_step + 1
        reply = (
            f"Шаг {current_step}. Продолжаем. "
            "Опиши, что изменилось по сравнению с прошлым шагом, "
            "и что хочешь улучшить дальше."
        )

    return {
        "status": "ok",
        "current_step": current_step,
        "next_step": next_step,
        "reply": reply,
        "echo": payload.message,
    }



if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port)
















