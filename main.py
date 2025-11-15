from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os

app = FastAPI(title="AI Orchestrator")

# ====== МОДЕЛЬ ВХОДЯЩЕГО ЗАПРОСА ======

class TaskRequest(BaseModel):
    message: str
    step: int = 1

# ====== OPENAI КЛИЕНТ ======

openai.api_key = os.getenv("OPENAI_API_KEY")

# ====== ОБРАБОТЧИК AI ======

def run_ai(message: str, step: int):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ты — внутренний процессор задач."},
            {"role": "user", "content": f"message={message}, step={step}"}
        ]
    )
    return response.choices[0].message["content"]

# ====== ENDPOINT ======

@app.post("/task")
def process_task(request: TaskRequest):
    ai_answer = run_ai(request.message, request.step)

    return {
        "status": "ok",
        "input": request.dict(),
        "ai_response": ai_answer
    }







