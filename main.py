from fastapi import FastAPI
from pydantic import BaseModel
import logging

# Настройка логов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai-orchestrator")

app = FastAPI()

class TaskPayload(BaseModel):
    message: str
    step: int

@app.post("/task")
async def process_task(payload: TaskPayload):
    logger.info(f"Received task: {payload.dict()}")
    return {
        "status": "received",
        "payload": payload.dict()
    }










