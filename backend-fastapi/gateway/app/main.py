# gateway/app/main.py

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import httpx
import logging
from fastapi.middleware.cors import CORSMiddleware
import os
from shared.auth import verify_token
from shared.log_config import setup_logging, add_logging_middleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from prometheus_client import Counter, Histogram, generate_latest

# Prometheus metrics
REQUEST_COUNT = Counter('gateway_requests_total', 'Total requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('gateway_request_duration_seconds', 'Request duration', ['method', 'endpoint'])

setup_logging("gateway")
logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title='WISHI Gateway')

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
add_logging_middleware(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ROUTES = {
    "auth": os.getenv("AUTH_SERVICE_URL", "http://localhost:8001"),
    "wishlist": os.getenv("WISHLIST_SERVICE_URL", "http://localhost:8002"),
    "seller": os.getenv("SELLER_SERVICE_URL", "http://localhost:8003"),
    "matching": os.getenv("MATCHING_SERVICE_URL", "http://localhost:8004"),
    "cluster": os.getenv("CLUSTER_SERVICE_URL", "http://localhost:8005"),
    "match": os.getenv("MATCH_ENGINE_SERVICE_URL", "http://localhost:8006"),
    "validation": os.getenv("VALIDATION_SERVICE_URL", "http://localhost:8007"),
    "notification": os.getenv("NOTIFICATION_SERVICE_URL", "http://localhost:8008"),
    "admin": os.getenv("ADMIN_SERVICE_URL", "http://localhost:8009"),
}

# Public endpoints that don't require authentication
PUBLIC_ENDPOINTS = {
    "auth": ["/google-token", "/token", "/login", "/health"],
    "wishlist": ["/categories", "/cities", "/marketplace-sources", "/health"],
    "match": ["/templates", "/health"],
    "validation": ["/health"],
    "notification": ["/health"],
}


def is_public_endpoint(service: str, path: str) -> bool:
    public_paths = PUBLIC_ENDPOINTS.get(service, [])
    for public_path in public_paths:
        if path.startswith(public_path.lstrip("/")):
            return True
    return False


def extract_user_from_token(token: str) -> dict:
    try:
        payload = verify_token(token)
        return {
            "user_id": payload.get("sub"),
            "email": payload.get("email"),
            "role": payload.get("role", "buyer"),
            "iss": payload.get("iss"),
        }
    except ValueError as e:
        logger.warning(f"Token verification failed: {e}")
        raise HTTPException(status_code=401, detail=str(e))


@app.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
@limiter.limit("100/minute")
async def proxy(service: str, path: str, request: Request):
    if service not in ROUTES:
        raise HTTPException(status_code=404, detail=f"Service '{service}' not found")

    logger.info(f"Proxying request to {service}/{path}")

    user_info = None
    if not is_public_endpoint(service, path):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
        token = auth_header.replace("Bearer ", "")
        user_info = extract_user_from_token(token)

    url = f"{ROUTES[service]}/{path}"

    headers = dict(request.headers)
    if user_info:
        headers["X-User-ID"] = str(user_info["user_id"])
        headers["X-User-Email"] = user_info["email"]
        headers["X-User-Role"] = user_info["role"]

    try:
        async with httpx.AsyncClient() as client:
            response = await client.request(
                request.method,
                url,
                headers=headers,
                content=await request.body(),
                params=dict(request.query_params),
            )
    except httpx.RequestError as e:
        logger.error(f"Downstream service error: {service}/{path} - {e}")
        raise HTTPException(status_code=502, detail=f"Service '{service}' unavailable")

    REQUEST_COUNT.labels(method=request.method, endpoint=f"{service}/{path}", status=str(response.status_code)).inc()
    return JSONResponse(status_code=response.status_code, content=response.json())


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "gateway"}


@app.get("/metrics")
def metrics():
    return generate_latest()
