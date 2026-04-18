from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import logging
from shared.log_config import setup_logging, add_logging_middleware

setup_logging("match-engine")
logger = logging.getLogger(__name__)

app = FastAPI()
add_logging_middleware(app)

class QueryTemplateResponse(BaseModel):
    templates: List[str]

class SearchRequest(BaseModel):
    product: str
    year: int
    city: str
    price: int

@app.get("/templates", response_model=QueryTemplateResponse)
def templates():
    return QueryTemplateResponse(templates=[
        "{product} {year} {city} under {price}",
        "{product} site:olx.in {city}",
        "{product} {price} {city} used"
    ])

@app.post("/search")
def search(req: SearchRequest):
    logger.info(f"Search request: product={req.product} city={req.city} price={req.price}")
    query_candidates = [
        f"{req.product} {req.year} {req.city} under {req.price}",
        f"{req.product} site:olx.in {req.city}",
        f"{req.product} {req.price} {req.city} used"
    ]
    # In a real engine, call source scrapers; here we return candidate templates for validation pipeline
    return {"queries": query_candidates}


@app.get("/health")
def health():
    return {"status": "match-engine ok"}
