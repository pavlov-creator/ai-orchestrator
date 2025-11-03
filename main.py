from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import logging
import os

# Простейшая настройка логов: всё, что мы пишем logging.info/print, уходит в stdout
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
    # Лог в stdout – его точно увидим в Cloud Run Logs
    logging.info(f"New task: {payload.json()}")
    print(f"New task (print): {payload.json()}")

    return {
        "status": "received",
        "payload": payload,
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port)


















