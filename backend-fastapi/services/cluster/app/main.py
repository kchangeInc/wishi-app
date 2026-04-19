from fastapi import FastAPI, HTTPException, Request, Depends
from pydantic import BaseModel
import logging
from datetime import datetime
from shared.db.dependencies import get_repos
from shared.repository.factory import RepositoryFactory
from shared.user import get_optional_user
from shared.log_config import setup_logging, add_logging_middleware

setup_logging("cluster")
logger = logging.getLogger(__name__)

app = FastAPI()
add_logging_middleware(app)


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


def normalize_filters(req: ClusterRequest):
    key = f"{req.title}_{req.price}_{req.location}".replace(" ", "_").lower()
    return key


@app.post("/clusters", response_model=ClusterResponse)
def upsert_cluster(payload: ClusterRequest, request: Request, repos: RepositoryFactory = Depends(get_repos)):
    user = get_optional_user(request)
    normalized = normalize_filters(payload)
    repo = repos.cluster()
    cluster = repo.get_or_create(normalized, user_id=user["user_id"] if user else None)
    logger.info(f"Cluster upserted: id={cluster.id} buyer_count={cluster.buyer_count}")
    return ClusterResponse(
        id=cluster.id,
        normalized_filters=cluster.normalized_filters,
        buyer_count=cluster.buyer_count,
        created_at=cluster.created_at,
    )


@app.get("/clusters/{cluster_id}", response_model=ClusterResponse)
def get_cluster(cluster_id: int, repos: RepositoryFactory = Depends(get_repos)):
    repo = repos.cluster()
    cluster = repo.get_not_deleted(cluster_id)
    if not cluster:
        raise HTTPException(status_code=404, detail="Cluster not found")
    return ClusterResponse(
        id=cluster.id,
        normalized_filters=cluster.normalized_filters,
        buyer_count=cluster.buyer_count,
        created_at=cluster.created_at,
    )


@app.get("/health")
def health():
    return {"status": "cluster ok"}
