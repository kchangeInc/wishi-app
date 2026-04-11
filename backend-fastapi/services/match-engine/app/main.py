from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

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
    query_candidates = [
        f"{req.product} {req.year} {req.city} under {req.price}",
        f"{req.product} site:olx.in {req.city}",
        f"{req.product} {req.price} {req.city} used"
    ]
    # In a real engine, call source scrapers; here we return candidate templates for validation pipeline
    return {"queries": query_candidates}
