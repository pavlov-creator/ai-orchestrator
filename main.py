from fastapi import FastAPI
import uvicorn
import os
from typing import Any

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/task")
async def task(payload: Any = None):
    return {
        "status": "received",
        "payload": payload,
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port)











