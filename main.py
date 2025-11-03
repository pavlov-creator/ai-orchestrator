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
    # Простой лог в stdout — Cloud Run его подхватит
    print(f"NEW_TASK message={payload.message!r} step={payload.step}")

    return {
        "status": "received",
        "payload": {
            "message": payload.message,
            "step": payload.step,
        },
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=port)



















