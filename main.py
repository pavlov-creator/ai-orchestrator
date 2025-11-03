from fastapi import FastAPI
import uvicorn
import os

app = FastAPI()


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/task")
async def task(body: dict):
    # пока просто эхо — вернём то, что получили
    return {
        "status": "received",
        "payload": body,
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port)










