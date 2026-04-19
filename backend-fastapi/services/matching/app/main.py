import json
import threading
import logging
from datetime import datetime

import httpx
from fastapi import FastAPI, BackgroundTasks
from kafka import KafkaConsumer
from shared.repository.factory import create_repos
from shared.log_config import add_logging_middleware, build_trace_headers, setup_logging
from app.matcher import find_matches

setup_logging("matching")
logger = logging.getLogger(__name__)

app = FastAPI()
add_logging_middleware(app)


@app.on_event("startup")
def startup():
    thread = threading.Thread(target=kafka_wishlist_consumer, daemon=True)
    thread.start()


def kafka_wishlist_consumer():
    consumer = KafkaConsumer(
        'wishlist-events',
        bootstrap_servers='kafka:9092',
        group_id='matching-group',
        auto_offset_reset='earliest',
        enable_auto_commit=True
    )
    for msg in consumer:
        try:
            data = json.loads(msg.value.decode('utf-8'))
            logger.info(f"Processing Kafka event: {data}")
            wishlist_id = data.get('wishlist_id')
            if wishlist_id:
                process_wishlist(wishlist_id)
        except Exception as e:
            logger.error(f"Error processing Kafka event: {e}", exc_info=True)


def process_wishlist(wishlist_id: int):
    # 1) Fetch wishlist data from wishlist service
    try:
        with httpx.Client(timeout=10.0) as client:
            wish_resp = client.get(
                f"http://wishlist-service:8002/wishlists/{wishlist_id}",
                headers=build_trace_headers(),
            )
            wish_resp.raise_for_status()
            wish = wish_resp.json()
    except Exception as e:
        logger.error(f"Failed to fetch wishlist {wishlist_id}: {e}", exc_info=True)
        return

    product = wish.get("title", "")
    category = wish.get("category", "")
    subcategory = wish.get("subcategory", "")
    filters = wish.get("filters_json", {}) or {}
    location = filters.get("location", "") if isinstance(filters, dict) else ""
    price = filters.get("price", 0) if isinstance(filters, dict) else 0
    year = filters.get("year", datetime.now().year)

    # 2) Cluster upsert
    cluster_payload = {
        "title": product,
        "location": location or "",
        "price": int(price) if price else 0,
        "category": category,
        "subcategory": subcategory,
        "user_id": 0
    }
    try:
        with httpx.Client(timeout=10.0) as client:
            cluster_resp = client.post(
                "http://cluster-service:8005/clusters",
                json=cluster_payload,
                headers=build_trace_headers(),
            )
            cluster_resp.raise_for_status()
            cluster = cluster_resp.json()
            cluster_id = cluster["id"]
    except Exception as e:
        logger.error(f"Cluster upsert failed for wishlist {wishlist_id}: {e}", exc_info=True)
        return

    # 3) Query generation by match-engine
    try:
        with httpx.Client(timeout=10.0) as client:
            query_resp = client.post("http://match-engine-service:8006/search", json={
                "product": product,
                "year": year,
                "city": location,
                "price": price
            }, headers=build_trace_headers())
            query_resp.raise_for_status()
            queries = query_resp.json().get("queries", [])
    except Exception as e:
        logger.warning(f"Match engine query failed: {e}", exc_info=True)
        queries = []

    # 4) Find matches — search + fetch pages + extract SEO metadata + score
    try:
        candidates = find_matches(wish, max_fetch=20, min_score=30)
    except Exception as e:
        logger.error(f"Matching failed for wishlist {wishlist_id}: {e}", exc_info=True)
        candidates = []

    for candidate in candidates[:30]:
        # Use pre-computed score if available (from scrapers/serper), otherwise validate via service
        if candidate.get("score"):
            score = candidate["score"]
            status = "auto_publish" if score >= 60 else "admin_review"
        else:
            score_data = validate_candidate(candidate, product, location, price)
            score = score_data["score"]
            status = score_data["status"]

        store_match(
            cluster_id=cluster_id,
            url=candidate["url"],
            source=candidate.get("source", "unknown"),
            score=score,
            status=status,
            wishlist_id=wishlist_id,
            title=candidate.get("title"),
            description=candidate.get("description"),
            price=candidate.get("price"),
            formatted_price=candidate.get("formatted_price"),
        )
        if status == "auto_publish":
            send_notification(cluster_id, f"New {product} found in {location}", [wish.get("user_email")])


def validate_candidate(candidate: dict, product, location, price):
    try:
        with httpx.Client(timeout=10.0) as client:
            payload = {
                "url": candidate["url"],
                "product": product,
                "brand": product.split()[0] if isinstance(product, str) and len(product.split()) > 0 else "",
                "model": product.split()[-1] if isinstance(product, str) else "",
                "location": location,
                "price": float(price) if price else 0.0
            }
            resp = client.post(
                "http://validation-service:8007/validate",
                json=payload,
                headers=build_trace_headers(),
            )
            if resp.status_code == 200:
                return resp.json()
    except Exception as e:
        logger.warning(f"Validation call failed for {candidate['url']}: {e}", exc_info=True)

    return {"score": 0, "status": "reject", "details": {"error": "validation_failed"}}


def store_match(cluster_id, url, source, score, status, wishlist_id=None,
                title=None, description=None, price=None, formatted_price=None):
    with create_repos() as repos:
        repo = repos.match()
        # Deduplicate by URL
        if repo.get_by_url(url):
            return
        repo.create_match(
            cluster_id=cluster_id,
            url=url,
            source=source,
            score=score,
            status=status,
            wishlist_id=wishlist_id,
            title=title,
            description=description,
            price=float(price) if price else None,
            formatted_price=formatted_price,
        )


def send_notification(cluster_id, message, recipients):
    try:
        with httpx.Client(timeout=10.0) as client:
            client.post(
                "http://notification-service:8008/notify",
                json={
                    "cluster_id": cluster_id,
                    "message": message,
                    "recipients": recipients or []
                },
                headers=build_trace_headers(),
            )
    except Exception as e:
        logger.error(f"Notification send failed for cluster {cluster_id}: {e}", exc_info=True)


@app.get("/health")
def health():
    return {"status": "matching ok"}


@app.post("/process_wishlist/{wishlist_id}")
def trigger_process_wishlist(wishlist_id: int, background_tasks: BackgroundTasks):
    """Endpoint called by the worker service to trigger wishlist processing."""
    background_tasks.add_task(process_wishlist, wishlist_id)
    return {"status": "processing", "wishlist_id": wishlist_id}
