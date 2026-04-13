from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging
import psycopg2
from shared.db.connection import get_db_connection
from shared.log_config import setup_logging, add_logging_middleware

setup_logging("admin")
logger = logging.getLogger(__name__)

app = FastAPI()
add_logging_middleware(app)

conn = get_db_connection()

class MatchReviewRequest(BaseModel):
    match_id: int
    action: str
    reason: Optional[str] = None

class MatchReviewResponse(BaseModel):
    match_id: int
    status: str


def _ensure_table():
    # Tables are now managed by Alembic migrations
    pass


@app.on_event("startup")
async def startup():
    _ensure_table()


@app.post("/review", response_model=MatchReviewResponse)
def review(request: MatchReviewRequest):
    if request.action not in ["approve", "reject"]:
        raise HTTPException(status_code=400, detail="action must be approve or reject")

    logger.info(f"Match review: match_id={request.match_id} action={request.action}")
    new_status = "published" if request.action == "approve" else "rejected"

    with conn.cursor() as cur:
        cur.execute("UPDATE matches SET status=%s WHERE id=%s RETURNING id", (new_status, request.match_id))
        row = cur.fetchone()
        conn.commit()

    if not row:
        logger.warning(f"Match not found for review: match_id={request.match_id}")
        raise HTTPException(status_code=404, detail="match not found")

    return MatchReviewResponse(match_id=request.match_id, status=new_status)


@app.get("/dashboard/pending")
def pending_dashboard():
    with conn.cursor() as cur:
        cur.execute("SELECT id, cluster_id, url, source, score, status, created_at FROM matches WHERE status = 'admin_review' ORDER BY created_at DESC")
        rows = cur.fetchall()

    items = "".join([
        f"<tr><td>{r[0]}</td><td>{r[1]}</td><td><a href='{r[2]}' target='_blank'>{r[2]}</a></td><td>{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td><td>{r[6]}</td></tr>"
        for r in rows
    ])

    html = f"""
    <html><head><title>Admin Review Dashboard</title></head><body>
    <h1>Pending admin_review matches</h1>
    <table border='1' cellspacing='0' cellpadding='4'>
      <tr><th>id</th><th>cluster_id</th><th>url</th><th>source</th><th>score</th><th>status</th><th>created_at</th></tr>
      {items}
    </table>
    </body></html>
    """
    return html

