FROM python:3.11-slim

WORKDIR /app

COPY ai-orchestrator/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ai-orchestrator/ .

CMD ["uvicorn", "main.main:app", "--host", "0.0.0.0", "--port", "8080", "--proxy-headers"]



