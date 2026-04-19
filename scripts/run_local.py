"""Run all backend services locally without Docker."""

import subprocess
import sys
import os
import time

BACKEND_DIR = os.path.join(os.path.dirname(__file__), "..", "backend-fastapi")
BACKEND_DIR = os.path.abspath(BACKEND_DIR)

# Environment variables shared by all services
ENV = {
    **os.environ,
    "PYTHONPATH": BACKEND_DIR,
    "DB_HOST": "localhost",
    "DB_PORT": "5432",
    "DB_NAME": "wishi",
    "DB_USER": "postgres",
    "DB_PASSWORD": "admin",
    "SECRET_KEY": "local-dev-secret-key",
    "GOOGLE_CLIENT_ID": "",
    "GOOGLE_CLIENT_SECRET": "",
    "KAFKA_BOOTSTRAP_SERVERS": "localhost:9092",
    "CELERY_BROKER_URL": "redis://localhost:6379/0",
    "LOG_LEVEL": "INFO",
    "LOG_FORMAT": "text",
    "ENABLE_STDOUT_LOGS": "true",
    "ENABLE_FILE_LOGS": "false",
    "DB_BACKEND": "firestore",  # "postgresql" or "firestore"
    "FIRESTORE_PROJECT_ID": "wishi-87328",
    "GOOGLE_APPLICATION_CREDENTIALS": os.path.join(
        os.path.dirname(__file__), "..", "wishi-87328-firebase-adminsdk-fbsvc-810e2462d6.json"
    ),
    # Service URLs for gateway routing
    "AUTH_SERVICE_URL": "http://localhost:8001",
    "WISHLIST_SERVICE_URL": "http://localhost:8002",
    "SELLER_SERVICE_URL": "http://localhost:8003",
    "MATCHING_SERVICE_URL": "http://localhost:8004",
    "CLUSTER_SERVICE_URL": "http://localhost:8005",
    "MATCH_ENGINE_SERVICE_URL": "http://localhost:8006",
    "VALIDATION_SERVICE_URL": "http://localhost:8007",
    "NOTIFICATION_SERVICE_URL": "http://localhost:8008",
    "ADMIN_SERVICE_URL": "http://localhost:8009",
    "SERPER_API_KEY": os.getenv("SERPER_API_KEY", ""),
    "GOOGLE_CSE_API_KEY": os.getenv("GOOGLE_CSE_API_KEY", ""),
    "GOOGLE_CSE_CX": os.getenv("GOOGLE_CSE_CX", ""),
    "FLIPKART_AFFILIATE_ID": os.getenv("FLIPKART_AFFILIATE_ID", ""),
    "FLIPKART_AFFILIATE_TOKEN": os.getenv("FLIPKART_AFFILIATE_TOKEN", ""),
    "AMAZON_PARTNER_TAG": os.getenv("AMAZON_PARTNER_TAG", ""),
    "AMAZON_ACCESS_KEY": os.getenv("AMAZON_ACCESS_KEY", ""),
    "AMAZON_SECRET_KEY": os.getenv("AMAZON_SECRET_KEY", ""),
}

# Each service: name, directory relative to BACKEND_DIR, uvicorn app path, port
SERVICES = [
    {"name": "auth",         "dir": "services/auth",         "app": "app.main:app", "port": 8001},
    {"name": "wishlist",     "dir": "services/wishlist",     "app": "app.main:app", "port": 8002},
    {"name": "seller",       "dir": "services/seller",       "app": "app.main:app", "port": 8003},
    {"name": "matching",     "dir": "services/matching",     "app": "app.main:app", "port": 8004},
    {"name": "cluster",      "dir": "services/cluster",      "app": "app.main:app", "port": 8005},
    {"name": "match-engine", "dir": "services/match-engine", "app": "app.main:app", "port": 8006},
    {"name": "validation",   "dir": "services/validation",   "app": "app.main:app", "port": 8007},
    {"name": "notification", "dir": "services/notification", "app": "app.main:app", "port": 8008},
    {"name": "admin",        "dir": "services/admin",        "app": "app.main:app", "port": 8009},
    {"name": "gateway",      "dir": "gateway",               "app": "app.main:app", "port": 8000},
]

processes = []


def start_services():
    python = sys.executable
    for svc in SERVICES:
        svc_dir = os.path.join(BACKEND_DIR, svc["dir"])
        # PYTHONPATH includes both the service dir and the backend root (for shared imports)
        svc_env = {**ENV, "PYTHONPATH": f"{BACKEND_DIR}{os.pathsep}{svc_dir}"}

        print(f"Starting {svc['name']:20s} on port {svc['port']}...")
        proc = subprocess.Popen(
            [python, "-m", "uvicorn", svc["app"],
             "--host", "0.0.0.0", "--port", str(svc["port"])],
            cwd=svc_dir,
            env=svc_env,
        )
        processes.append((svc["name"], svc["port"], proc))
        time.sleep(0.3)

    print("\n" + "=" * 60)
    print(" All services started:")
    print("=" * 60)
    for name, port, _ in processes:
        print(f"  {name:20s} -> http://localhost:{port}")
    print("=" * 60)
    print(" Press Ctrl+C to stop all services\n")


def stop_services():
    print("\nStopping all services...")
    for name, port, proc in processes:
        if proc.poll() is None:
            print(f"  Stopping {name} (PID {proc.pid})...")
            proc.terminate()
    for name, port, proc in processes:
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
    print("All services stopped.")


if __name__ == "__main__":
    try:
        start_services()
        while True:
            time.sleep(2)
            for name, port, proc in processes:
                ret = proc.poll()
                if ret is not None:
                    print(f"  [WARN] {name} (port {port}) exited with code {ret}")
    except KeyboardInterrupt:
        stop_services()
