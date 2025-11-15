import logging
from fastapi import FastAPI
from pydantic import BaseModel

# Настройка логов для Cloud Run
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
def task(payload: TaskPayload):
    logger.info({
        "event": "task_received",
        "message": payload.message,
        "step": payload.step
    })
    return {
        "status": "received",
        "payload": payload.dict()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, proxy_headers=True)







