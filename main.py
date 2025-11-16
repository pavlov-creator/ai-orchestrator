from fastapi import FastAPI
from pydantic import BaseModel
import os
from openai import OpenAI

app = FastAPI()

# 1) Берём ключ из ENV
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


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
    """
    Простой запрос к OpenAI, возвращаем ответ модели.
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "user", "content": payload.prompt}
            ],
        )
        ai_answer = completion.choices[0].message.content
    except Exception as e:
        ai_answer = f"ERROR: {str(e)}"

    return {
        "status": "processed",
        "input": payload.model_dump(),
        "ai_answer": ai_answer,
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)





