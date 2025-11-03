from fastapi import FastAPI
from pydantic import BaseModel
import os

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
    # Пишем в stdout, Cloud Run это точно залогирует
    print(f"NEW_TASK step={payload.step} message={payload.message}", flush=True)
    return {
        "status": "received",
        "payload": payload,
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)



















