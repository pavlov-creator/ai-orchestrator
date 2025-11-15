from fastapi import FastAPI
from pydantic import BaseModel
import logging
import os

# Настраиваем логгер (уходит в stdout, Cloud Run это подхватывает)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai-orchestrator")

app = FastAPI()


class TaskPayload(BaseModel):
    message: str
    step: int


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/task")
async def task(payload: TaskPayload):
    # КЛЮЧЕВАЯ СТРОКА: именно по этому слову будем фильтровать логи
    logger.info("task_received | message=%s | step=%s", payload.message, payload.step)

    return {
        "status": "received",
        "payload": payload.dict(),
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8080"))
    uvicorn.run("main:app", host="0.0.0.0", port=port)






