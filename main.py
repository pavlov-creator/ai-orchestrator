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


@app.post("/task")
async def task(payload: TaskPayload):
    # payload — это JSON, который пришёл в теле запроса
    return {
        "status": "received",
        "payload": payload,
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port)















