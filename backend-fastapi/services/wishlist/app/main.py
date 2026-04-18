from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Request, Depends
from pydantic import BaseModel
import json
import logging
from shared.config.settings import get_settings
from shared.db.session import get_db_session
from shared.service.wishlist_service import WishlistService
from shared.repository.category import CategoryRepository
from shared.repository.favourite import FavouriteRepository
from shared.repository.saved_listing import SavedListingRepository
from shared.repository.feedback import FeedbackRepository
from shared.repository.match import MatchRepository
from shared.user import get_current_user, get_optional_user, require_role
from shared.log_config import setup_logging, add_logging_middleware

setup_logging("wishlist")
logger = logging.getLogger(__name__)
settings = get_settings()

app = FastAPI()
add_logging_middleware(app)

# Lazy Kafka / Celery — optional for local dev
_producer = None
_celery = None

def _get_producer():
    global _producer
    if _producer is not None:
        return _producer
    try:
        from kafka import KafkaProducer
        _producer = KafkaProducer(
            bootstrap_servers=settings.messaging.kafka_bootstrap_servers,
            retries=5,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        )
    except Exception as e:
        logger.warning(f"Kafka unavailable: {e}", exc_info=True)
    return _producer

def _get_celery():
    global _celery
    if _celery is not None:
        return _celery
    try:
        from celery import Celery
        _celery = Celery(broker=settings.messaging.celery_broker_url)
    except Exception as e:
        logger.warning(f"Celery unavailable: {e}", exc_info=True)
    return _celery

def _publish_event(topic, data):
    p = _get_producer()
    if p:
        try:
            p.send(topic, data)
        except Exception as e:
            logger.warning(f"Kafka send failed: {e}", exc_info=True)

def _dispatch_task(name, args):
    c = _get_celery()
    if c:
        try:
            c.send_task(name, args=args)
        except Exception as e:
            logger.warning(f"Celery dispatch failed: {e}", exc_info=True)

# ---- Pydantic models ----

class WishlistCreate(BaseModel):
    title: str
    display_title: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    subcategory_id: Optional[int] = None
    filters_json: Optional[dict] = None
    notes: Optional[str] = None
    expiry_date: Optional[datetime] = None
    status: str = "active"
    priority: str = "medium"
    field_values: Optional[list] = None
    preferred_marketplace_ids: Optional[list] = None

class FavouriteAction(BaseModel):
    wishlist_id: Optional[int] = None

class DismissAction(BaseModel):
    wishlist_id: Optional[int] = None
    reason: Optional[str] = None

class SavedListingCreate(BaseModel):
    title: Optional[str] = None
    url: str
    price: Optional[str] = None
    price_numeric: Optional[float] = None
    location: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None
    source: Optional[str] = None

class FeedbackCreate(BaseModel):
    rating: int
    message: Optional[str] = None

# ---- Category / City / MarketplaceSource (public) ----

@app.get("/categories")
def get_categories(db=Depends(get_db_session)):
    repo = CategoryRepository(db)
    categories = repo.get_all_categories()
    result = []
    for cat in categories:
        subcats = []
        for sub in cat.subcategories:
            fields = [
                {
                    "id": f.id,
                    "name": f.name,
                    "label": f.label,
                    "field_type": f.field_type,
                    "is_required": f.is_required,
                    "placeholder": f.placeholder,
                    "options": f.options,
                    "depends_on": f.depends_on,
                    "options_by_parent": f.options_by_parent,
                    "min_value": float(f.min_value) if f.min_value else None,
                    "max_value": float(f.max_value) if f.max_value else None,
                    "step": float(f.step) if f.step else None,
                    "unit": f.unit,
                }
                for f in (sub.field_definitions or [])
            ]
            subcats.append({
                "id": sub.id,
                "name": sub.name,
                "slug": sub.slug,
                "fields": fields,
            })
        result.append({
            "id": cat.id,
            "name": cat.name,
            "slug": cat.slug,
            "icon": cat.icon,
            "subcategories": subcats,
        })
    return result

@app.get("/cities")
def get_cities(search: str = None, metro_only: bool = False, db=Depends(get_db_session)):
    repo = CategoryRepository(db)
    cities = repo.get_all_cities(search=search, metro_only=metro_only)
    return [{"id": c.id, "name": c.name, "slug": c.slug, "state": c.state, "is_metro": c.is_metro} for c in cities]

@app.get("/marketplace-sources")
def get_marketplace_sources(category_id: int = None, db=Depends(get_db_session)):
    repo = CategoryRepository(db)
    sources = repo.get_marketplace_sources(category_id=category_id)
    return [{"id": s.id, "name": s.name, "slug": s.slug, "url_template": s.url_template, "color": s.color} for s in sources]

# ---- Wishlist CRUD ----

@app.post("/wishlists")
def create_wishlist(payload: WishlistCreate, request: Request, db=Depends(get_db_session)):
    user = get_current_user(request)
    service = WishlistService(db)
    result = service.create_wishlist(
        title=payload.title,
        user_id=user["user_id"],
        user_email=user["email"],
        display_title=payload.display_title,
        description=payload.description,
        category_id=payload.category_id,
        subcategory_id=payload.subcategory_id,
        filters_json=payload.filters_json,
        notes=payload.notes,
        expiry_date=payload.expiry_date,
        status=payload.status,
        priority=payload.priority,
        field_values=payload.field_values,
        preferred_marketplace_ids=payload.preferred_marketplace_ids,
    )
    _dispatch_task("match_wishlist", [result["id"]])
    _publish_event("wishlist-events", {"wishlist_id": result["id"], "action": "CREATED", "user_id": user["user_id"]})
    logger.info(f"Wishlist created: id={result['id']} user_id={user['user_id']}")
    return result

@app.get("/wishlists")
def get_all_wishlists(request: Request, user_only: bool = False, skip: int = 0, limit: int = 100, db=Depends(get_db_session)):
    user = get_optional_user(request)
    service = WishlistService(db)
    if user_only and user:
        return service.get_user_wishlists(user["user_id"], skip, limit)
    return service.get_all_wishlists(skip, limit)

@app.get("/wishlists/{wishlist_id}")
def get_wishlist(wishlist_id: int, db=Depends(get_db_session)):
    service = WishlistService(db)
    wishlist = service.get_wishlist(wishlist_id)
    if not wishlist:
        raise HTTPException(status_code=404, detail="Wishlist not found")
    return wishlist

@app.put("/wishlists/{wishlist_id}")
def update_wishlist(wishlist_id: int, payload: WishlistCreate, request: Request, db=Depends(get_db_session)):
    user = get_current_user(request)
    service = WishlistService(db)
    result = service.update_wishlist(
        wishlist_id=wishlist_id,
        user_id=user["user_id"],
        title=payload.title,
        display_title=payload.display_title,
        description=payload.description,
        category_id=payload.category_id,
        subcategory_id=payload.subcategory_id,
        filters_json=payload.filters_json,
        notes=payload.notes,
        status=payload.status,
        priority=payload.priority,
        field_values=payload.field_values,
        preferred_marketplace_ids=payload.preferred_marketplace_ids,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Wishlist not found")
    _publish_event("wishlist-events", {"wishlist_id": wishlist_id, "action": "UPDATED", "user_id": user["user_id"]})
    return result

@app.delete("/wishlists/{wishlist_id}")
def delete_wishlist(wishlist_id: int, request: Request, db=Depends(get_db_session)):
    user = get_current_user(request)
    service = WishlistService(db)
    if not service.delete_wishlist(wishlist_id, user["user_id"]):
        raise HTTPException(status_code=404, detail="Wishlist not found")
    _publish_event("wishlist-events", {"wishlist_id": wishlist_id, "action": "DELETED", "user_id": user["user_id"]})
    logger.info(f"Wishlist deleted: id={wishlist_id} user_id={user['user_id']}")
    return {"status": "deleted", "wishlist_id": wishlist_id}

# ---- Matches for a wishlist ----

@app.get("/wishlists/{wishlist_id}/matches")
def get_wishlist_matches(wishlist_id: int, request: Request, skip: int = 0, limit: int = 50, db=Depends(get_db_session)):
    user = get_optional_user(request)
    match_repo = MatchRepository(db)
    matches = match_repo.get_by_wishlist(wishlist_id, skip, limit)

    fav_ids = set()
    dismissed_ids = set()
    if user:
        fav_repo = FavouriteRepository(db)
        fav_ids = fav_repo.get_favourite_match_ids(user["user_id"], wishlist_id)
        dismissed_ids = fav_repo.get_dismissed_match_ids(user["user_id"], wishlist_id)

    result = []
    for m in matches:
        if m.id in dismissed_ids:
            continue
        result.append({
            "id": m.id,
            "title": m.title,
            "description": m.description,
            "price": float(m.price) if m.price else None,
            "formatted_price": m.formatted_price,
            "location": m.location,
            "url": m.url,
            "source": m.source,
            "image_url": m.image_url,
            "score": m.score,
            "specs": m.specs,
            "seller_tag": m.seller_tag,
            "is_featured": m.is_featured,
            "is_favourite": m.id in fav_ids,
            "posted_at": m.posted_at.isoformat() if m.posted_at else None,
            "created_at": m.created_at.isoformat() if m.created_at else None,
        })
    return result

# ---- Favourites ----

@app.post("/wishlists/{wishlist_id}/matches/{match_id}/favourite")
def add_favourite(wishlist_id: int, match_id: int, request: Request, db=Depends(get_db_session)):
    user = get_current_user(request)
    repo = FavouriteRepository(db)
    repo.add_favourite(user["user_id"], match_id, wishlist_id)
    return {"status": "favourited"}

@app.delete("/wishlists/{wishlist_id}/matches/{match_id}/favourite")
def remove_favourite(wishlist_id: int, match_id: int, request: Request, db=Depends(get_db_session)):
    user = get_current_user(request)
    repo = FavouriteRepository(db)
    repo.remove_favourite(user["user_id"], match_id)
    return {"status": "unfavourited"}

# ---- Dismiss ----

@app.post("/wishlists/{wishlist_id}/matches/{match_id}/dismiss")
def dismiss_match(wishlist_id: int, match_id: int, body: DismissAction, request: Request, db=Depends(get_db_session)):
    user = get_current_user(request)
    repo = FavouriteRepository(db)
    repo.dismiss_match(user["user_id"], match_id, wishlist_id, reason=body.reason)
    return {"status": "dismissed"}

# ---- Saved Listings ----

@app.get("/saved-listings")
def get_saved_listings(request: Request, skip: int = 0, limit: int = 50, db=Depends(get_db_session)):
    user = get_current_user(request)
    repo = SavedListingRepository(db)
    listings = repo.get_user_saved(user["user_id"], skip, limit)
    return [
        {
            "id": l.id,
            "title": l.title,
            "url": l.url,
            "price": l.price,
            "price_numeric": float(l.price_numeric) if l.price_numeric else None,
            "location": l.location,
            "category": l.category,
            "image_url": l.image_url,
            "source": l.source,
            "saved_at": l.saved_at.isoformat() if l.saved_at else None,
        }
        for l in listings
    ]

@app.post("/saved-listings")
def save_listing(body: SavedListingCreate, request: Request, db=Depends(get_db_session)):
    user = get_current_user(request)
    repo = SavedListingRepository(db)
    listing = repo.save_listing(user["user_id"], **body.model_dump())
    return {"id": listing.id, "status": "saved"}

@app.delete("/saved-listings/{listing_id}")
def delete_saved_listing(listing_id: int, request: Request, db=Depends(get_db_session)):
    user = get_current_user(request)
    repo = SavedListingRepository(db)
    if not repo.delete_saved(listing_id, user["user_id"]):
        raise HTTPException(status_code=404, detail="Listing not found")
    return {"status": "deleted"}

# ---- Feedback ----

@app.post("/feedback")
def submit_feedback(body: FeedbackCreate, request: Request, db=Depends(get_db_session)):
    user = get_current_user(request)
    if body.rating < 1 or body.rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be 1-5")
    repo = FeedbackRepository(db)
    fb = repo.create(user["user_id"], body.rating, body.message)
    logger.info(f"Feedback submitted: user_id={user['user_id']} rating={body.rating}")
    return {"id": fb.id, "status": "submitted"}

# ---- Health ----

@app.get("/health")
def health():
    return {"status": "wishlist ok"}
