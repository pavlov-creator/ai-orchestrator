from fastapi import FastAPI
from pydantic import BaseModel
import os
import sys

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
    # Лог в stdout — его увидит Cloud Run
    print(
        f"NEW_TASK | message={payload.message} | step={payload.step}",
        file=sys.stdout,
        flush=True,
    )
    return {
        "status": "received",
        "payload": payload.dict(),
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)










