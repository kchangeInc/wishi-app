FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY services/worker /app
COPY shared /app/shared

CMD ["celery", "-A", "app.tasks", "worker", "--loglevel=info"]



