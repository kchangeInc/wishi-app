from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import httpx
from datetime import datetime
from shared.log_config import setup_logging, add_logging_middleware

setup_logging("validation")
logger = logging.getLogger(__name__)

app = FastAPI()
add_logging_middleware(app)

class ValidationRequest(BaseModel):
    url: str
    product: str
    brand: str
    model: str
    location: str
    price: float

class ValidationResult(BaseModel):
    url: str
    score: int
    status: str
    details: dict


def check_url(url: str):
    try:
        with httpx.Client(timeout=10.0, follow_redirects=True) as client:
            resp = client.get(url)
            if resp.status_code != 200:
                return False, "non-200"
            if len(resp.history) > 10:
                return False, "redirect_loop"
            return True, "ok"
    except Exception as e:
        return False, str(e)


def compute_score(req: ValidationRequest, metadata: dict):
    score = 0
    details = {}

    text = (metadata.get("title", "") + " " + metadata.get("description", "")).lower()
    if req.product.lower() in text:
        score += 30
        details['keyword'] = 30
    else:
        details['keyword'] = 0

    if req.brand.lower() in text or req.model.lower() in text:
        score += 15
        details['brand_model'] = 15
    else:
        details['brand_model'] = 0

    if req.location.lower() in text:
        score += 20
        details['location'] = 20
    else:
        details['location'] = 0

    if str(req.price) in text or f"{int(req.price)}" in text:
        score += 25
        details['price'] = 25
    else:
        details['price'] = 0

    details['freshness'] = 10
    score += 10

    if score > 100:
        score = 100

    if score >= 75:
        status = "auto_publish"
    elif score >= 50:
        status = "admin_review"
    else:
        status = "reject"

    return score, status, details


@app.post("/validate", response_model=ValidationResult)
def validate(req: ValidationRequest):
    ok, reason = check_url(req.url)
    if not ok:
        logger.warning(f"URL validation rejected: url={req.url} reason={reason}")
        raise HTTPException(status_code=400, detail=f"URL check failed: {reason}")

    with httpx.Client(timeout=10.0) as client:
        resp = client.get(req.url)
        title = ""
        description = ""
        body = resp.text.lower()
        # naive: use substring hints
        if "<title>" in body:
            start = body.find("<title>") + 7
            end = body.find("</title>", start)
            title = body[start:end] if end > start else ""
        # naive description
        if "<meta name=\"description\"" in body:
            desc_start = body.find("<meta name=\"description\"")
            desc_content = body[desc_start:desc_start+300]
            if "content=\"" in desc_content:
                c = desc_content.split("content=\"")[1]
                description = c.split("\"")[0]

    metadata = {"title": title, "description": description}
    score, status, details = compute_score(req, metadata)
    logger.info(f"Validated: url={req.url} score={score} status={status}")

    return ValidationResult(url=req.url, score=score, status=status, details=details)
