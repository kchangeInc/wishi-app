# shared/log_config.py
"""Centralized logging configuration for all WISHI backend services."""

import json
import logging
import os
import time
import uuid
from contextvars import ContextVar
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler
from pathlib import Path

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse


TRACE_HEADER = "X-Trace-ID"
REQUEST_ID_HEADER = "X-Request-ID"
_trace_id_ctx: ContextVar[str] = ContextVar("trace_id", default="-")


def _env_flag(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


class JsonFormatter(logging.Formatter):
    """Render log records as structured JSON for aggregation systems."""

    def __init__(self, service_name: str):
        super().__init__()
        self.service_name = service_name

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(timespec="milliseconds"),
            "level": record.levelname,
            "service": self.service_name,
            "trace_id": getattr(record, "trace_id", "-"),
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "process": record.process,
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        if record.stack_info:
            payload["stack"] = self.formatStack(record.stack_info)
        return json.dumps(payload, ensure_ascii=True)


class TextFormatter(logging.Formatter):
    """Human-readable formatter retained for optional local file logs."""

    def __init__(self, service_name: str):
        super().__init__(
            fmt=f"%(asctime)s | %(levelname)-8s | {service_name} | trace=%(trace_id)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )


class TraceContextFilter(logging.Filter):
    """Inject the current trace ID into every log record."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.trace_id = _trace_id_ctx.get()
        return True


def set_trace_id(trace_id: str):
    """Bind a trace ID to the current execution context."""
    return _trace_id_ctx.set(trace_id)


def reset_trace_id(token):
    """Restore the previous trace ID context."""
    _trace_id_ctx.reset(token)


def get_trace_id() -> str:
    """Return the active trace ID or '-' when none is bound."""
    return _trace_id_ctx.get()


def ensure_trace_id() -> str:
    """Reuse the active trace ID or create one for background work."""
    trace_id = get_trace_id()
    if trace_id != "-":
        return trace_id
    trace_id = uuid.uuid4().hex[:12]
    set_trace_id(trace_id)
    return trace_id


def build_trace_headers(headers=None) -> dict:
    """Return headers carrying the current trace ID across service boundaries."""
    trace_id = ensure_trace_id()
    traced_headers = dict(headers or {})
    traced_headers[TRACE_HEADER] = trace_id
    traced_headers.setdefault(REQUEST_ID_HEADER, trace_id)
    return traced_headers


def extract_trace_id(request: Request) -> str:
    """Read trace ID from request headers or generate one."""
    return request.headers.get(TRACE_HEADER) or request.headers.get(REQUEST_ID_HEADER) or uuid.uuid4().hex[:12]


def setup_logging(service_name: str):
    """Configure logging for a service. Call once at process startup."""
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    log_format = os.getenv("LOG_FORMAT", "json").lower()
    enable_stdout_logs = _env_flag("ENABLE_STDOUT_LOGS", True)
    enable_file_logs = _env_flag("ENABLE_FILE_LOGS", False)
    enable_common_tracelog = _env_flag("ENABLE_COMMON_TRACELOG", False)
    log_dir = os.getenv("LOG_DIR", str(Path(__file__).resolve().parents[1] / "logs"))
    max_bytes = int(os.getenv("LOG_MAX_BYTES", str(10 * 1024 * 1024)))
    backup_count = int(os.getenv("LOG_BACKUP_COUNT", "5"))
    common_trace_log = Path(log_dir) / os.getenv("COMMON_TRACELOG_NAME", "common.tracelog")

    if enable_file_logs or enable_common_tracelog:
        Path(log_dir).mkdir(parents=True, exist_ok=True)

    formatter = JsonFormatter(service_name) if log_format == "json" else TextFormatter(service_name)
    file_formatter = TextFormatter(service_name)
    trace_filter = TraceContextFilter()

    service_log_file = Path(log_dir) / f"{service_name}.log"
    trace_log_file = Path(log_dir) / f"{service_name}.tracelog"

    handlers = []

    if enable_stdout_logs:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.addFilter(trace_filter)
        handlers.append(console_handler)

    if enable_file_logs:
        service_file_handler = RotatingFileHandler(
            filename=service_log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        service_file_handler.setFormatter(file_formatter)
        service_file_handler.addFilter(trace_filter)
        handlers.append(service_file_handler)

        trace_file_handler = RotatingFileHandler(
            filename=trace_log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        trace_file_handler.setFormatter(file_formatter)
        trace_file_handler.setLevel(logging.ERROR)
        trace_file_handler.addFilter(trace_filter)
        handlers.append(trace_file_handler)

    if enable_common_tracelog:
        common_trace_handler = logging.FileHandler(
            filename=common_trace_log,
            encoding="utf-8",
        )
        common_trace_handler.setFormatter(file_formatter)
        common_trace_handler.setLevel(logging.ERROR)
        common_trace_handler.addFilter(trace_filter)
        handlers.append(common_trace_handler)

    if not handlers:
        fallback_handler = logging.StreamHandler()
        fallback_handler.setFormatter(formatter)
        fallback_handler.addFilter(trace_filter)
        handlers.append(fallback_handler)

    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        handlers=handlers,
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

        trace_id = extract_trace_id(request)
        token = set_trace_id(trace_id)
        request.state.trace_id = trace_id
        logger = logging.getLogger("http")
        logger.info(f"[{trace_id}] --> {request.method} {path}")

        start = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            duration_ms = (time.perf_counter() - start) * 1000
            logger.error(f"[{trace_id}] {request.method} {path} unhandled error ({duration_ms:.0f}ms)", exc_info=True)
            raise
        finally:
            if 'response' not in locals():
                reset_trace_id(token)

        duration_ms = (time.perf_counter() - start) * 1000
        logger.info(f"[{trace_id}] <-- {request.method} {path} {response.status_code} ({duration_ms:.0f}ms)")
        response.headers[TRACE_HEADER] = trace_id
        response.headers[REQUEST_ID_HEADER] = trace_id
        reset_trace_id(token)
        return response


async def global_exception_handler(request: Request, exc: Exception):
    """Catch unhandled exceptions, log traceback, return JSON 500."""
    logger = logging.getLogger("http")
    trace_id = getattr(request.state, "trace_id", extract_trace_id(request))
    token = set_trace_id(trace_id)
    try:
        logger.error(f"Unhandled exception on {request.method} {request.url.path}: {exc}", exc_info=True)
    finally:
        reset_trace_id(token)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "trace_id": trace_id},
        headers={TRACE_HEADER: trace_id, REQUEST_ID_HEADER: trace_id},
    )


def add_logging_middleware(app):
    """Wire up request logging middleware and global exception handler."""
    app.add_middleware(RequestLoggingMiddleware)
    app.add_exception_handler(Exception, global_exception_handler)
