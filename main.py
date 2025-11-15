from fastapi import FastAPI
from pydantic import BaseModel
import os
import json

app = FastAPI()


class Task(BaseModel):
    message: str
    step: int


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/task")
async def task(task: Task):
    # Лог в stdout → попадает в Cloud Run Logs
    log = {
        "event": "task_received",
        "message": task.message,
        "step": task.step,
    }
    print(json.dumps(log, ensure_ascii=False), flush=True)

    return {
        "status": "received",
        "payload": task.dict(),
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port)







