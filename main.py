from fastapi import FastAPI
from pydantic import BaseModel
import os
import uvicorn
from openai import OpenAI

app = FastAPI()

# Клиент OpenAI берёт ключ из переменной окружения OPENAI_API_KEY
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---- Модель запроса ----
class TaskRequest(BaseModel):
    prompt: str

# ---- Эндпоинты ----

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/task")
async def task(payload: TaskRequest):
    """
    Принимаем:
    {
      "prompt": "Привет, кто ты?"
    }
    """

    print(f"[NEW_TASK] prompt={payload.prompt}", flush=True)

    ai_answer = None

    try:
        completion = client.chat.completions.create(
            model="gpt-4.1-mini",  # при желании позже поменяем
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": payload.prompt},
            ],
        )
        ai_answer = completion.choices[0].message.content

    except Exception as e:
        ai_answer = f"ERROR: {str(e)}"

    return {
        "status": "processed",
        "input": payload.dict(),
        "ai_answer": ai_answer,
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port)




