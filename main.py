from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import logging
import time
from openai import OpenAI

app = FastAPI(
    title="AI Orchestrator",
    version="1.0.0",
    description="LLM orchestrator for 4-model testing phase"
)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("orchestrator")

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Init OpenAI client (GPT)
client = OpenAI()

# Request model
class TaskRequest(BaseModel):
    message: str
    step: int = 1
    model: str = "gpt"   # пока только gpt


@app.post("/task")
async def run_task(req: TaskRequest):

    start = time.time()

    # Base system prompt — позже заменим на разные роли
    system_prompt = f"""
You are an analytical assistant. 
You perform step {req.step}. 
Return structured, clear output.
"""

    # GPT call
    completion = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": req.message}
        ],
        temperature=0.2
    )

    answer = completion.choices[0].message.content

    latency = round((time.time() - start) * 1000, 1)

    logger.info(
        f"task_received | model=gpt | step={req.step} | latency={latency}ms | msg={req.message[:40]}"
    )

    return {
        "status": "ok",
        "model": "gpt",
        "step": req.step,
        "latency_ms": latency,
        "response": answer
    }








