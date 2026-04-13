from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import logging
import psycopg2
from datetime import datetime
from shared.db.connection import get_db_connection
from shared.user import get_optional_user
from shared.log_config import setup_logging, add_logging_middleware

setup_logging("cluster")
logger = logging.getLogger(__name__)

app = FastAPI()
add_logging_middleware(app)

conn = get_db_connection()

class ClusterRequest(BaseModel):
    title: str
    location: str
    price: int
    category: str
    subcategory: str
    user_id: int

class ClusterResponse(BaseModel):
    id: int
    normalized_filters: str
    buyer_count: int
    created_at: datetime


def _ensure_table():
    # Tables are now managed by Alembic migrations
    pass


@app.on_event("startup")
async def startup():
    _ensure_table()


def normalize_filters(req: ClusterRequest):
    key = f"{req.title}_{req.price}_{req.location}".replace(" ", "_").lower()
    return key


@app.post("/clusters", response_model=ClusterResponse)
def upsert_cluster(payload: ClusterRequest, request: Request):
    user = get_optional_user(request)
    normalized = normalize_filters(payload)

    with conn.cursor() as cur:
        cur.execute("SELECT id, buyer_count, created_at FROM clusters WHERE normalized_filters = %s", (normalized,))
        row = cur.fetchone()
        if row:
            cluster_id, buyer_count, created_at = row
            buyer_count += 1
            cur.execute(
                "UPDATE clusters SET buyer_count = %s, updated_at = NOW(), updated_by = %s WHERE id = %s",
                (buyer_count, user["user_id"] if user else None, cluster_id)
            )
            conn.commit()
            logger.info(f"Cluster updated: id={cluster_id} buyer_count={buyer_count}")
            return ClusterResponse(id=cluster_id, normalized_filters=normalized, buyer_count=buyer_count, created_at=created_at)

        cur.execute(
            "INSERT INTO clusters(normalized_filters, buyer_count, created_by, updated_by, created_at, updated_at) VALUES (%s, 1, %s, %s, NOW(), NOW()) RETURNING id, created_at",
            (normalized, user["user_id"] if user else None, user["user_id"] if user else None)
        )
        cluster_id, created_at = cur.fetchone()
        conn.commit()
        logger.info(f"Cluster created: id={cluster_id} filters={normalized}")

    return ClusterResponse(id=cluster_id, normalized_filters=normalized, buyer_count=1, created_at=created_at)


@app.get("/clusters/{cluster_id}", response_model=ClusterResponse)
def get_cluster(cluster_id: int):
    with conn.cursor() as cur:
        cur.execute("SELECT id, normalized_filters, buyer_count, created_at FROM clusters WHERE id = %s", (cluster_id,))
        row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Cluster not found")
    return ClusterResponse(id=row[0], normalized_filters=row[1], buyer_count=row[2], created_at=row[3])
