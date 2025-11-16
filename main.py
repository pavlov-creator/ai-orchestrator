import os
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import google.auth
from google.cloud import storage
import requests

app = FastAPI()

# ====== ENV EXACTLY AS ON YOUR SCREEN ======
BUCKET_NAME = os.getenv("BUCKET_NAME")
OPENAI_API_KEY = os.getenv("OPENAIAPIKEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
XAI_API_KEY = os.getenv("XAI_API_KEY")

# ====== CLIENTS ======
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# ====== DATA MODEL ======
class Task(BaseModel):
    prompt: str
    model: str   # "openai" | "gemini" | "deepseek" | "xai"

# ====== ROUTE ======
@app.post("/run")
async def run_task(task: Task):

    if task.model == "openai":
        ans = openai_client.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "user", "content": task.prompt}]
        )
        return {"answer": ans.choices[0].message.content}

    if task.model == "gemini":
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateText"
        r = requests.post(url, params={"key": GEMINI_API_KEY},
            json={"prompt": {"text": task.prompt}})
        return {"answer": r.json()["candidates"][0]["output"]}

    if task.model == "deepseek":
        url = "https://api.deepseek.com/v1/chat/completions"
        r = requests.post(url,
            headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}"},
            json={"model": "deepseek-chat", "messages": [{"role": "user", "content": task.prompt}]})
        return {"answer": r.json()["choices"][0]["message"]["content"]}

    if task.model == "xai":
        url = "https://api.x.ai/v1/chat/completions"
        r = requests.post(url,
            headers={"Authorization": f"Bearer {XAI_API_KEY}"},
            json={"model": "grok-beta", "messages": [{"role": "user", "content": task.prompt}]})
        return {"answer": r.json()["choices"][0]["message"]["content"]}

    return {"error": "unknown model"}




