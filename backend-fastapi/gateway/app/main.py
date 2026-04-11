# gateway/app/main.py

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import httpx
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from shared.auth import verify_token
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from prometheus_client import Counter, Histogram, generate_latest

# Prometheus metrics
REQUEST_COUNT = Counter('gateway_requests_total', 'Total requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('gateway_request_duration_seconds', 'Request duration', ['method', 'endpoint'])

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title='Deal Platform Gateway')

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ROUTES = {
    "auth": "http://auth-service:8001",
    "wishlist": "http://wishlist-service:8002",
    "matching": "http://matching-service:8004",
    "seller": "http://seller-service:8003",
    "cluster": "http://cluster-service:8005",
    "match": "http://match-engine-service:8006",
    "validation": "http://validation-service:8007",
    "notification": "http://notification-service:8008",
    "admin": "http://admin-service:8009"
}

# Public endpoints that don't require authentication
PUBLIC_ENDPOINTS = {
    "auth": ["/login/google", "/callback", "/token", "/health"],
    "match": ["/templates", "/health"],
    "validation": ["/health"],
    "notification": ["/health"]
}

def is_public_endpoint(service: str, path: str) -> bool:
    """Check if endpoint is public (doesn't require authentication)"""
    public_paths = PUBLIC_ENDPOINTS.get(service, [])
    # Check if path starts with any public endpoint
    for public_path in public_paths:
        if path.startswith(public_path.lstrip("/")):
            return True
    return False

def extract_user_from_token(token: str) -> dict:
    """Extract user info from JWT token"""
    try:
        payload = verify_token(token)
        return {
            "user_id": payload.get("sub"),
            "email": payload.get("email"),
            "iss": payload.get("iss")
        }
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@app.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
@limiter.limit("100/minute")
async def proxy(service: str, path: str, request: Request):
    logger.info(f"Proxying request to {service}/{path}")
    # Check if endpoint requires authentication
    if not is_public_endpoint(service, path):
        # Extract and validate token
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
        
        token = auth_header.replace("Bearer ", "")
        user_info = extract_user_from_token(token)
    else:
        user_info = None

    # Build target URL
    url = f"{ROUTES[service]}/{path}"

    # Prepare headers - include user info if authenticated
    headers = dict(request.headers)
    if user_info:
        headers["X-User-ID"] = str(user_info["user_id"])
        headers["X-User-Email"] = user_info["email"]

    async with httpx.AsyncClient() as client:
        response = await client.request(
            request.method,
            url,
            headers=headers,
            content=await request.body()
        )

    REQUEST_COUNT.labels(method=request.method, endpoint=f"{service}/{path}", status=str(response.status_code)).inc()
    return JSONResponse(status_code=response.status_code, content=response.json())


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "gateway"}


@app.get("/metrics")
def metrics():
    return generate_latest()
