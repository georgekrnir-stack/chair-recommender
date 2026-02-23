FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN alembic upgrade head 2>/dev/null || true

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
