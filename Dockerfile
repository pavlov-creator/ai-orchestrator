FROM python:3.11-slim

# где будет жить приложение
WORKDIR /app

# ставим зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# копируем весь код
COPY . .

# порт для Cloud Run
ENV PORT=8080

# запускаем fastapi через uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]



