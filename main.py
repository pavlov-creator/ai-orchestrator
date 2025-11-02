from fastapi import FastAPI, Request
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
async def task(request: Request):
    body = await request.json()
    # тут пока просто эхо, дальше вставим логику оркестратора
    return {
        "status": "received",
        "payload": body,
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port)









