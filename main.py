from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uvicorn
import os
import logging

# Включаем логирование
logging.basicConfig(level=logging.INFO)

app = FastAPI()


class TaskPayload(BaseModel):
    message: str
    step: int = 0


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/task")
async def task(payload: TaskPayload):
    # Логируем входящий запрос в логи Cloud Run
    logging.info(f"New task: {payload.json(ensure_ascii=False)}")
    return {
        "status": "received",
        "payload": payload,
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port)

















