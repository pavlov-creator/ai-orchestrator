from fastapi import FastAPI
from pydantic import BaseModel
import os
import uvicorn
from openai import OpenAI

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
    print(f"[NEW_TASK] message={payload.message} step={payload.step}", flush=True)

    # Вызов OpenAI
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": payload.message}
            ]
        )

        ai_answer = completion.choices[0].message["content"]

    except Exception as e:
        ai_answer = f"ERROR: {str(e)}"

    return {
        "status": "processed",
        "input": payload.dict(),
        "ai_answer": ai_answer
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port)
# trigger build






