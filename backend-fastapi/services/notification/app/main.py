from fastapi import FastAPI, HTTPException, Request, Depends
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import logging
from shared.db.session import get_db_session
from shared.repository.notification import NotificationRepository
from shared.repository.notification_setting import NotificationSettingRepository
from shared.user import get_current_user
from shared.log_config import setup_logging, add_logging_middleware

setup_logging("notification")
logger = logging.getLogger(__name__)

app = FastAPI()
add_logging_middleware(app)

# ---- Pydantic models ----

class NotificationSettingUpdate(BaseModel):
    email_matches: Optional[bool] = None
    email_price_drops: Optional[bool] = None
    email_newsletter: Optional[bool] = None
    push_matches: Optional[bool] = None
    push_messages: Optional[bool] = None
    push_promotions: Optional[bool] = None

class NotifyRequest(BaseModel):
    cluster_id: int
    message: str
    recipients: list[str]

# ---- Notification CRUD ----

@app.get("/notifications")
def get_notifications(
    request: Request, type: str = None, is_read: bool = None,
    skip: int = 0, limit: int = 50, db=Depends(get_db_session)
):
    user = get_current_user(request)
    repo = NotificationRepository(db)
    notifications = repo.get_user_notifications(user["user_id"], type=type, is_read=is_read, skip=skip, limit=limit)
    unread_count = repo.get_unread_count(user["user_id"])
    return {
        "notifications": [
            {
                "id": n.id,
                "type": n.type,
                "title": n.title,
                "description": n.description,
                "wishlist_id": n.wishlist_id,
                "match_id": n.match_id,
                "action_url": n.action_url,
                "is_read": n.is_read,
                "read_at": n.read_at.isoformat() if n.read_at else None,
                "created_at": n.created_at.isoformat() if n.created_at else None,
            }
            for n in notifications
        ],
        "unread_count": unread_count,
    }

@app.put("/notifications/{notification_id}/read")
def mark_read(notification_id: int, request: Request, db=Depends(get_db_session)):
    user = get_current_user(request)
    repo = NotificationRepository(db)
    if not repo.mark_read(notification_id, user["user_id"]):
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"status": "read"}

@app.put("/notifications/read-all")
def mark_all_read(request: Request, db=Depends(get_db_session)):
    user = get_current_user(request)
    repo = NotificationRepository(db)
    count = repo.mark_all_read(user["user_id"])
    return {"status": "ok", "marked": count}

@app.delete("/notifications/{notification_id}")
def delete_notification(notification_id: int, request: Request, db=Depends(get_db_session)):
    user = get_current_user(request)
    repo = NotificationRepository(db)
    if not repo.soft_delete(notification_id, user["user_id"]):
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"status": "deleted"}

@app.delete("/notifications")
def clear_all_notifications(request: Request, db=Depends(get_db_session)):
    user = get_current_user(request)
    repo = NotificationRepository(db)
    count = repo.clear_all(user["user_id"])
    return {"status": "cleared", "count": count}

# ---- Notification Settings ----

@app.get("/notification-settings")
def get_notification_settings(request: Request, db=Depends(get_db_session)):
    user = get_current_user(request)
    repo = NotificationSettingRepository(db)
    s = repo.get_or_create(user["user_id"])
    return {
        "email_matches": s.email_matches,
        "email_price_drops": s.email_price_drops,
        "email_newsletter": s.email_newsletter,
        "push_matches": s.push_matches,
        "push_messages": s.push_messages,
        "push_promotions": s.push_promotions,
    }

@app.put("/notification-settings")
def update_notification_settings(body: NotificationSettingUpdate, request: Request, db=Depends(get_db_session)):
    user = get_current_user(request)
    repo = NotificationSettingRepository(db)
    updates = body.dict(exclude_unset=True)
    s = repo.update(user["user_id"], **updates)
    return {
        "email_matches": s.email_matches,
        "email_price_drops": s.email_price_drops,
        "email_newsletter": s.email_newsletter,
        "push_matches": s.push_matches,
        "push_messages": s.push_messages,
        "push_promotions": s.push_promotions,
    }

# ---- Legacy notify endpoint (internal, from worker/matching) ----

@app.post("/notify")
def notify(req: NotifyRequest):
    logger.info(f"Notify request: cluster={req.cluster_id} recipients={len(req.recipients)}")
    return {"status": "ok", "delivered_to": len(req.recipients), "timestamp": datetime.utcnow().isoformat()}

@app.get("/health")
def health():
    return {"status": "notification ok"}
