import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import uvicorn

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- БЕРЁМ КЛЮЧ РОВНО ТАК, КАК В CLOUD RUN ----
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


class Payload(BaseModel):
    prompt: str


@app.post("/process")
async def process(payload: Payload):
    # Лог в Cloud Run, чтобы видеть вход
    print(f"[NEW_TASK] prompt={payload.prompt}", flush=True)

    # Вызов OpenAI
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": payload.prompt}
        ]
    )

    ai_answer = completion.choices[0].message.content

    return {
        "status": "processed",
        "input": payload.dict(),
        "ai_answer": ai_answer,
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port)






