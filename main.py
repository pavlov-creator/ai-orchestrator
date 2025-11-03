from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import os
from typing import Optional

app = FastAPI()


class TaskPayload(BaseModel):
    # Любая структура данных, чтобы Swagger понял, что это body
    message: Optional[str] = None
    data: Optional[dict] = None


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/task")
async def task(payload: Optional[TaskPayload] = None):
    return {
        "status": "received",
        "payload": payload,
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port)












