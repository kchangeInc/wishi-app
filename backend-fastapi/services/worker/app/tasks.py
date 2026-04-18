# services/worker/app/tasks.py

import logging
import httpx
import psycopg2
from celery import Celery
from datetime import datetime, timedelta
from shared.db.connection import get_db_connection
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
    }
}
celery.conf.timezone = "UTC"


def _get_connection():
    """Get a fresh DB connection for each task."""
    return get_db_connection()

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
    conn = _get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, url, cluster_id, score, status FROM matches WHERE status IN ('auto_publish','admin_review', 'new') ORDER BY last_validated_at NULLS FIRST LIMIT 50")
            rows = cur.fetchall()

        for row in rows:
            match_id, url, cluster_id, score, status = row

            if status == 'admin_review':
                try:
                    with httpx.Client(timeout=10.0) as client:
                        validation_payload = {
                            "url": url,
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
                            score_new = vdata.get("score", score)
                            status_new = vdata.get("status", status)
                            with conn.cursor() as cur:
                                cur.execute(
                                    "UPDATE matches SET score=%s, status=%s, last_validated_at=NOW() WHERE id=%s",
                                    (score_new, status_new, match_id)
                                )
                                conn.commit()
                            if status_new == "auto_publish":
                                notify_cluster(cluster_id, f"Match validated and auto-published: {url}")
                except Exception as e:
                    logger.error(f"Validation pipeline error for match {match_id}: {e}", exc_info=True)
    finally:
        conn.close()


def notify_cluster(cluster_id: int, message: str):
    try:
        with httpx.Client(timeout=10.0) as client:
            # fetch cluster buyers from cluster service (placeholder) and notify
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
