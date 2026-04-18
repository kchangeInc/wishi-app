from fastapi import FastAPI
import logging
from shared.log_config import setup_logging, add_logging_middleware

setup_logging("seller")
logger = logging.getLogger(__name__)

app = FastAPI()
add_logging_middleware(app)

@app.get("/insights")
def insights():
    return {"top_category": "mobiles", "demand": 100}


@app.get("/health")
def health():
    return {"status": "seller ok"}
