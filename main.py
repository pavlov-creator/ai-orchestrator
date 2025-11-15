from fastapi import FastAPI
from pydantic import BaseModel
import json
import sys

app = FastAPI()

class Task(BaseModel):
    message: str
    step: int

def log(msg: dict):
    # Печать в stdout, чтобы Cloud Run точно видел
    print(json.dumps(msg), file=sys.stdout, flush=True)

@app.post("/task")
async def process_task(task: Task):
    log({
        "event": "task_received",
        "message": task.message,
        "step": task.step
    })

    return {
        "status": "received",
        "payload": task.dict()
    }









