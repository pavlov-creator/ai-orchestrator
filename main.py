from fastapi import FastAPI
import uvicorn
import os
from typing import Optional

app = FastAPI()


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/task")
async def task(body: Optional[dict] = None):
    # body – это JSON, который придёт в запросе
    return {
        "status": "received",
        "payload": body,
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port)













