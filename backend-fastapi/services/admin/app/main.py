from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
import logging
from shared.db.dependencies import get_repos
from shared.repository.factory import RepositoryFactory
from shared.log_config import setup_logging, add_logging_middleware

setup_logging("admin")
logger = logging.getLogger(__name__)

app = FastAPI()
add_logging_middleware(app)


class MatchReviewRequest(BaseModel):
    match_id: int
    action: str
    reason: Optional[str] = None

class MatchReviewResponse(BaseModel):
    match_id: int
    status: str


@app.post("/review", response_model=MatchReviewResponse)
def review(request: MatchReviewRequest, repos: RepositoryFactory = Depends(get_repos)):
    if request.action not in ["approve", "reject"]:
        raise HTTPException(status_code=400, detail="action must be approve or reject")

    logger.info(f"Match review: match_id={request.match_id} action={request.action}")
    new_status = "published" if request.action == "approve" else "rejected"

    repo = repos.match()
    match = repo.update_match(request.match_id, status=new_status)
    if not match:
        logger.warning(f"Match not found for review: match_id={request.match_id}")
        raise HTTPException(status_code=404, detail="match not found")

    return MatchReviewResponse(match_id=request.match_id, status=new_status)


@app.get("/dashboard/pending", response_class=HTMLResponse)
def pending_dashboard(repos: RepositoryFactory = Depends(get_repos)):
    repo = repos.match()
    matches = repo.get_by_status("admin_review")

    items = "".join([
        f"<tr><td>{m.id}</td><td>{m.cluster_id}</td><td><a href='{m.url}' target='_blank'>{m.url}</a></td><td>{m.source}</td><td>{m.score}</td><td>{m.status}</td><td>{m.created_at}</td></tr>"
        for m in matches
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


@app.get("/health")
def health():
    return {"status": "admin ok"}
