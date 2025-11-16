from fastapi import FastAPI
from pydantic import BaseModel
import os
import uvicorn
from openai import OpenAI

app = FastAPI()

# Клиент OpenAI. Ключ берём из переменной окружения OPENAI_API_KEY
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class TaskPayload(BaseModel):
    prompt: str


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/task")
async def task(payload: TaskPayload):
    # Лог в Cloud Run
    print(f"[NEW_TASK] prompt={payload.prompt}", flush=True)

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": payload.prompt},
            ],
            max_tokens=200,
        )
        ai_answer = completion.choices[0].message.content
    except Exception as e:
        ai_answer = f"ERROR: {e}"

    return {
        "status": "processed",
        "input": payload.dict(),
        "ai_answer": ai_answer,
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port)






