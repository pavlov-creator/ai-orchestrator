from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("orchestrator")

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
    # Логируем задачу в stdout → попадёт в Cloud Run Logs
    logger.info(f"NEW_TASK {payload.model_dump()}")
    return {
        "status": "received",
        "payload": payload,
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port)




















