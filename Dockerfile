FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Cloud Run передаёт порт в $PORT
CMD ["sh","-c","uvicorn main:app --app-dir ./ai-orchestrator --host 0.0.0.0 --port ${PORT:-8080}"]

