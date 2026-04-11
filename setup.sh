#!/bin/bash

echo "🚀 Creating WISHI Platform Repo..."

PROJECT="wishi-platform"

mkdir -p $PROJECT
cd $PROJECT

# -------------------------------
# COMMON FILES
# -------------------------------
cat > requirements.txt <<EOF
fastapi
uvicorn
psycopg2-binary
celery
redis
httpx
pyjwt
authlib
slowapi
sentence-transformers
EOF

cat > docker-compose.yml <<EOF
version: "3.8"

services:
  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: wishi
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"

  redis:
    image: redis:7
    ports:
      - "6379:6379"

  gateway:
    build: ./gateway
    ports:
      - "8000:8000"

  auth-service:
    build: ./services/auth-service

  wishlist-service:
    build: ./services/wishlist-service

  matching-service:
    build: ./services/matching-service

  seller-service:
    build: ./services/seller-service

  worker:
    build: ./workers/worker-service
EOF

# -------------------------------
# SHARED MODULE
# -------------------------------
mkdir -p shared

cat > shared/auth.py <<EOF
import jwt
from datetime import datetime, timedelta

SECRET = "wishi-secret"

def create_token(user):
    payload = {"user": user, "exp": datetime.utcnow() + timedelta(hours=2)}
    return jwt.encode(payload, SECRET, algorithm="HS256")

def verify_token(token):
    return jwt.decode(token, SECRET, algorithms=["HS256"])
EOF

# -------------------------------
# GATEWAY
# -------------------------------
mkdir -p gateway/app

cat > gateway/app/main.py <<EOF
from fastapi import FastAPI, Request
import httpx

app = FastAPI()

ROUTES = {
    "auth": "http://auth-service:8000",
    "wishlist": "http://wishlist-service:8000",
    "seller": "http://seller-service:8000"
}

@app.api_route("/{service}/{path:path}", methods=["GET", "POST"])
async def proxy(service: str, path: str, request: Request):
    url = f"{ROUTES[service]}/{path}"
    async with httpx.AsyncClient() as client:
        response = await client.request(
            request.method,
            url,
            content=await request.body()
        )
    return response.json()
EOF

cat > gateway/Dockerfile <<EOF
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r ../requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

# -------------------------------
# AUTH SERVICE (Google OAuth ready)
# -------------------------------
mkdir -p services/auth-service/app

cat > services/auth-service/app/main.py <<EOF
from fastapi import FastAPI
from shared.auth import create_token

app = FastAPI()

@app.get("/login")
def login():
    return {"access_token": create_token("user@test.com")}
EOF

cat > services/auth-service/Dockerfile <<EOF
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r ../../requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

# -------------------------------
# WISHLIST SERVICE
# -------------------------------
mkdir -p services/wishlist-service/app

cat > services/wishlist-service/app/main.py <<EOF
from fastapi import FastAPI
import psycopg2

app = FastAPI()

conn = psycopg2.connect(
    dbname="wishi", user="user", password="password", host="postgres"
)

@app.post("/create")
def create():
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS wishlist(id SERIAL PRIMARY KEY, tenant_id TEXT)")
    cur.execute("INSERT INTO wishlist(tenant_id) VALUES ('tenant1') RETURNING id")
    wid = cur.fetchone()[0]
    conn.commit()
    return {"wishlist_id": wid}
EOF

cat > services/wishlist-service/Dockerfile <<EOF
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r ../../requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

# -------------------------------
# MATCHING SERVICE (AI READY)
# -------------------------------
mkdir -p services/matching-service/app

cat > services/matching-service/app/main.py <<EOF
from fastapi import FastAPI
app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}
EOF

cat > services/matching-service/Dockerfile <<EOF
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r ../../requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

# -------------------------------
# SELLER SERVICE
# -------------------------------
mkdir -p services/seller-service/app

cat > services/seller-service/app/main.py <<EOF
from fastapi import FastAPI
app = FastAPI()

@app.get("/insights")
def insights():
    return {"demand": 100}
EOF

cat > services/seller-service/Dockerfile <<EOF
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r ../../requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

# -------------------------------
# WORKER SERVICE
# -------------------------------
mkdir -p workers/worker-service/app

cat > workers/worker-service/app/tasks.py <<EOF
from celery import Celery

celery = Celery("worker", broker="redis://redis:6379/0")

@celery.task
def match_wishlist(wid):
    print("Processing", wid)
EOF

cat > workers/worker-service/Dockerfile <<EOF
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r ../../requirements.txt
CMD ["celery", "-A", "app.tasks", "worker", "--loglevel=info"]
EOF

# -------------------------------
# KUBERNETES
# -------------------------------
mkdir -p infra/k8s

cat > infra/k8s/wishlist-deployment.yaml <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: wishlist
spec:
  replicas: 2
  selector:
    matchLabels:
      app: wishlist
  template:
    metadata:
      labels:
        app: wishlist
    spec:
      containers:
      - name: wishlist
        image: wishlist:latest
EOF

# -------------------------------
# CI/CD
# -------------------------------
mkdir -p .github/workflows

cat > .github/workflows/deploy.yml <<EOF
name: CI

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: docker build .
EOF

echo "✅ WISHI repo created successfully!"
echo "👉 Run: docker-compose up --build"