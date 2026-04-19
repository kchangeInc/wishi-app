# services/worker/app/tasks.py

import logging
import time
import httpx
from celery import Celery
from datetime import datetime, timedelta
from shared.repository.factory import create_repos
from shared.log_config import build_trace_headers, setup_logging

setup_logging("worker")
logger = logging.getLogger(__name__)

celery = Celery(
    "worker",
    broker="redis://redis:6379/0"
)

celery.conf.beat_schedule = {
    "validation-pipeline-30-min": {
        "task": "run_validation_pipeline",
        "schedule": 1800.0,
    },
    "daily-serper-refresh": {
        "task": "daily_serper_refresh",
        "schedule": 86400.0,
    },
}
celery.conf.timezone = "UTC"


@celery.task(name="match_wishlist")
def match_wishlist(wishlist_id):
    logger.info(f"Received match_wishlist task: wishlist_id={wishlist_id}")
    try:
        with httpx.Client(timeout=10.0) as client:
            client.post(
                f"http://matching-service:8004/process_wishlist/{wishlist_id}",
                headers=build_trace_headers(),
            )
    except Exception as e:
        logger.error(f"Failed to forward wishlist {wishlist_id} to matching-service: {e}", exc_info=True)


@celery.task(name="run_validation_pipeline")
def run_validation_pipeline():
    logger.info("Starting validation pipeline run")
    with create_repos() as repos:
        match_repo = repos.match()
        matches = match_repo.get_pending_validation(limit=50)

        for m in matches:
            if m.status == 'admin_review':
                try:
                    with httpx.Client(timeout=10.0) as client:
                        validation_payload = {
                            "url": m.url,
                            "product": "",
                            "brand": "",
                            "model": "",
                            "location": "",
                            "price": 0
                        }
                        vresp = client.post(
                            "http://validation-service:8007/validate",
                            json=validation_payload,
                            headers=build_trace_headers(),
                        )
                        if vresp.status_code == 200:
                            vdata = vresp.json()
                            score_new = vdata.get("score", m.score)
                            status_new = vdata.get("status", m.status)
                            match_repo.update_match(m.id, score=score_new, status=status_new)
                            if status_new == "auto_publish":
                                notify_cluster(m.cluster_id, f"Match validated and auto-published: {m.url}")
                except Exception as e:
                    logger.error(f"Validation pipeline error for match {m.id}: {e}", exc_info=True)


def notify_cluster(cluster_id: int, message: str):
    try:
        with httpx.Client(timeout=10.0) as client:
            client.post(
                "http://notification-service:8008/notify",
                json={
                    "cluster_id": cluster_id,
                    "message": message,
                    "recipients": ["admin@wishi.local"]
                },
                headers=build_trace_headers(),
            )
    except Exception as e:
        logger.error(f"Notify cluster {cluster_id} failed: {e}", exc_info=True)


@celery.task(name="daily_serper_refresh")
def daily_serper_refresh():
    """Daily task: search all legal APIs for active wishlists and insert new matches."""
    from services.matching.app.serper import search_and_score_for_wishlist
    from services.matching.app.google_cse import search_and_score_google_cse
    from services.matching.app.flipkart_affiliate import search_and_score_flipkart
    from services.matching.app.amazon_affiliate import search_and_score_amazon

    logger.info("Starting daily search refresh for all active wishlists")

    with create_repos() as repos:
        wishlist_repo = repos.wishlist()
        match_repo = repos.match()

        skip = 0
        batch_size = 100
        total_new = 0
        total_wishlists = 0

        while True:
            wishlists = wishlist_repo.get_active_wishlists(skip=skip, limit=batch_size)
            if not wishlists:
                break

            for wl in wishlists:
                total_wishlists += 1
                try:
                    total_new += _search_refresh_one(
                        wl, match_repo,
                        [search_and_score_for_wishlist, search_and_score_google_cse,
                         search_and_score_flipkart, search_and_score_amazon],
                    )
                except Exception as e:
                    logger.error(f"Search refresh failed for wishlist {wl.id}: {e}", exc_info=True)
                # Rate-limit: 1 second between wishlists
                time.sleep(1)

            if len(wishlists) < batch_size:
                break
            skip += batch_size

    logger.info(f"Daily search refresh complete: {total_wishlists} wishlists, {total_new} new matches")


def _search_refresh_one(wl, match_repo, search_functions) -> int:
    """Search all legal APIs for one wishlist and insert new matches."""
    wish_dict = {
        "title": wl.title,
        "category": "",
        "subcategory": "",
        "filters_json": wl.filters_json or {},
    }

    all_results = []
    for search_fn in search_functions:
        try:
            results = search_fn(wish_dict)
            all_results.extend(results)
        except Exception as e:
            logger.warning(f"{search_fn.__name__} failed for wishlist {wl.id}: {e}")

    # Deduplicate
    seen_urls = set()
    new_count = 0

    for r in all_results:
        url = r.get("url", "")
        if url in seen_urls:
            continue
        seen_urls.add(url)

        if match_repo.get_by_url(url):
            continue

        status = "auto_publish" if r.get("score", 0) >= 60 else "admin_review"

        match_repo.create_match(
            cluster_id=None,
            url=url,
            source=r.get("source", "unknown"),
            score=r.get("score", 0),
            status=status,
            wishlist_id=wl.id,
            title=r.get("title"),
            description=r.get("description"),
            price=float(r["price"]) if r.get("price") else None,
            formatted_price=r.get("formatted_price"),
        )
        new_count += 1

    return new_count
