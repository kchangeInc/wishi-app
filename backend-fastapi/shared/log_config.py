# shared/log_config.py
"""Centralized logging configuration for all WISHI backend services."""

import logging
import os
import time
import uuid
import traceback

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse


def setup_logging(service_name: str):
    """Configure logging for a service. Call once at process startup."""
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    fmt = f"%(asctime)s | %(levelname)-8s | {service_name} | %(name)s | %(message)s"
    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format=fmt,
        datefmt="%Y-%m-%d %H:%M:%S",
        force=True,
    )

    # Quiet noisy third-party loggers
    for name in ("uvicorn.access", "httpx", "kafka", "httpcore"):
        logging.getLogger(name).setLevel(logging.WARNING)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Logs every request/response with duration. Adds X-Request-ID header."""

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        # Skip health/metrics to avoid log noise
        if path in ("/health", "/metrics"):
            return await call_next(request)

        request_id = request.headers.get("X-Request-ID", uuid.uuid4().hex[:8])
        logger = logging.getLogger("http")
        logger.info(f"[{request_id}] --> {request.method} {path}")

        start = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            duration_ms = (time.perf_counter() - start) * 1000
            logger.error(f"[{request_id}] {request.method} {path} unhandled error ({duration_ms:.0f}ms)", exc_info=True)
            raise

        duration_ms = (time.perf_counter() - start) * 1000
        logger.info(f"[{request_id}] <-- {request.method} {path} {response.status_code} ({duration_ms:.0f}ms)")
        response.headers["X-Request-ID"] = request_id
        return response


async def global_exception_handler(request: Request, exc: Exception):
    """Catch unhandled exceptions, log traceback, return JSON 500."""
    logger = logging.getLogger("http")
    logger.error(f"Unhandled exception on {request.method} {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


def add_logging_middleware(app):
    """Wire up request logging middleware and global exception handler."""
    app.add_middleware(RequestLoggingMiddleware)
    app.add_exception_handler(Exception, global_exception_handler)
