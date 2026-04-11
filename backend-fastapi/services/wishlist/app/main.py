from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Request, Depends
from pydantic import BaseModel
from kafka import KafkaProducer
import json
from celery import Celery
from shared.db.session import get_db_session
from shared.service.wishlist_service import WishlistService
from shared.user import get_current_user, get_optional_user

app = FastAPI()

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    retries=5,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

celery = Celery(broker="redis://redis:6379/0")

class WishlistCreate(BaseModel):
    title: str
    display_title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    filters_json: Optional[dict] = None
    user_email: Optional[str] = None
    user_id: Optional[int] = None
    expiry_date: Optional[datetime] = None
    status: str = "active"
    priority: str = "medium"

class WishlistResponse(WishlistCreate):
    id: int
    is_active: bool = True
    is_deleted: bool = False
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    version: int = 1


def _ensure_table():
    # Tables are now managed by Alembic migrations
    pass


@app.on_event("startup")
def startup_event():
    _ensure_table()


@app.post("/wishlists", response_model=WishlistResponse)
def create_wishlist(
    payload: WishlistCreate,
    request: Request,
    db = Depends(get_db_session)
):
    user = get_current_user(request)
    service = WishlistService(db)
    
    result = service.create_wishlist(
        title=payload.title,
        user_id=user["user_id"],
        user_email=user["email"],
        display_title=payload.display_title,
        description=payload.description,
        category=payload.category,
        subcategory=payload.subcategory,
        filters_json=payload.filters_json,
        expiry_date=payload.expiry_date,
        status=payload.status,
        priority=payload.priority
    )
    
    # Send async events
    celery.send_task("match_wishlist", args=[result["id"]])
    producer.send("wishlist-events", {
        "wishlist_id": result["id"],
        "action": "CREATED",
        "user_id": user["user_id"]
    })
    
    return result


@app.get("/wishlists", response_model=List[WishlistResponse])
def get_all_wishlists(
    request: Request,
    user_only: bool = False,
    skip: int = 0,
    limit: int = 100,
    db = Depends(get_db_session)
):
    user = get_optional_user(request)
    service = WishlistService(db)
    
    if user_only and user:
        wishlists = service.get_user_wishlists(user["user_id"], skip, limit)
    else:
        wishlists = service.get_all_wishlists(skip, limit)
    
    return wishlists


@app.get("/wishlists/{wishlist_id}", response_model=WishlistResponse)
def get_wishlist(
    wishlist_id: int,
    db = Depends(get_db_session)
):
    service = WishlistService(db)
    wishlist = service.get_wishlist(wishlist_id)
    
    if not wishlist:
        raise HTTPException(status_code=404, detail="Wishlist not found")
    
    return wishlist


@app.delete("/wishlists/{wishlist_id}")
def delete_wishlist(
    wishlist_id: int,
    request: Request,
    db = Depends(get_db_session)
):
    user = get_current_user(request)
    service = WishlistService(db)
    
    if not service.delete_wishlist(wishlist_id, user["user_id"]):
        raise HTTPException(status_code=404, detail="Wishlist not found")
    
    producer.send("wishlist-events", {
        "wishlist_id": wishlist_id,
        "action": "DELETED",
        "user_id": user["user_id"]
    })
    
    return {"status": "deleted", "wishlist_id": wishlist_id}


@app.put("/wishlists/{wishlist_id}", response_model=WishlistResponse)
def update_wishlist(
    wishlist_id: int,
    payload: WishlistCreate,
    request: Request,
    db = Depends(get_db_session)
):
    user = get_current_user(request)
    service = WishlistService(db)
    
    result = service.update_wishlist(
        wishlist_id=wishlist_id,
        user_id=user["user_id"],
        title=payload.title,
        display_title=payload.display_title,
        description=payload.description,
        category=payload.category,
        subcategory=payload.subcategory,
        filters_json=payload.filters_json,
        status=payload.status,
        priority=payload.priority
    )
    
    if not result:
        raise HTTPException(status_code=404, detail="Wishlist not found")
    
    producer.send("wishlist-events", {
        "wishlist_id": wishlist_id,
        "action": "UPDATED",
        "user_id": user["user_id"]
    })
    
    return result


# --------------------------------------------------------
# Dynamic Category / Platform UI metadata endpoints
# --------------------------------------------------------

class MatchCard(BaseModel):
    title: str
    url: str
    price: Optional[str] = None
    location: Optional[str] = None
    condition: Optional[str] = None

class PlatformMatches(BaseModel):
    platform: str
    cards: List[MatchCard]


@app.get("/categories")
def get_category_schema():
    return {
        "automobile": {
            "fields": {
                "city": {"type": "text", "required": True},
                "pincode": {"type": "text", "required": False},
                "year": {"type": "select", "options": list(range(2005, 2026)), "required": True},
                "brand": {"type": "search", "required": True},
                "model": {"type": "dependent_select", "depends_on": "brand", "required": True},
                "price": {"type": "slider", "min": 0, "max": 2000000, "step": 10000, "required": True},
                "fuel_type": {"type": "select", "options": ["Petrol", "Diesel", "Electric", "CNG"], "required": False},
                "owner_type": {"type": "select", "options": ["First", "Second", "Third"], "required": False}
            },
            "platforms": ["OLX", "Spinny", "Cars24", "DriveX"]
        },
        "real_estate": {
            "fields": {
                "city": {"type": "text", "required": True},
                "pincode": {"type": "text", "required": False},
                "property_type": {"type": "select", "options": ["Flat", "House"], "required": True},
                "bhk": {"type": "select", "options": [1,2,3,4], "required": True},
                "listing_type": {"type": "select", "options": ["Rent", "Buy"], "required": True},
                "price": {"type": "number", "required": True},
                "furnishing": {"type": "select", "options": ["Furnished", "Semi-furnished", "Unfurnished"], "required": False},
                "parking": {"type": "boolean", "required": False},
                "lift": {"type": "boolean", "required": False}
            },
            "platforms": ["NoBroker", "MagicBricks", "99acres"]
        },
        "mobile": {
            "fields": {
                "brand": {"type": "text", "required": True},
                "model": {"type": "text", "required": True},
                "storage": {"type": "select", "options": ["64GB","128GB","256GB","512GB"], "required": True},
                "condition": {"type": "select", "options": ["New","Refurbished","Used"], "required": True},
                "price": {"type": "number", "required": True}
            }
        },
        "computer": {
            "fields": {
                "type": {"type": "select", "options": ["Laptop","Desktop"], "required": True},
                "brand": {"type": "text", "required": True},
                "ram": {"type": "text", "required": True},
                "processor": {"type": "text", "required": True},
                "price": {"type": "number", "required": True}
            }
        },
        "electronics": {
            "fields": {
                "type": {"type": "select", "options": ["TV","Fridge","Washing Machine","AC"], "required": True},
                "brand": {"type": "text", "required": True},
                "size_capacity": {"type": "text", "required": True},
                "price": {"type": "number", "required": True}
            }
        }
    }


@app.get("/wishlists/{wishlist_id}/matches", response_model=List[PlatformMatches])
def get_wishlist_matches(wishlist_id: int):
    # Placeholder response; in production, implement search across sources for matches.
    if wishlist_id <= 0:
        raise HTTPException(status_code=404, detail="Wishlist not found")

    return [
        PlatformMatches(
            platform="OLX",
            cards=[
                MatchCard(title="Honda Activa 2023 - Excellent", url="https://olx.example/1", price="₹68,000", location="K.K Nagar"),
                MatchCard(title="Activa 2022", url="https://olx.example/2", price="₹65,000", location="Anna Nagar"),
            ]
        ),
        PlatformMatches(
            platform="Spinny",
            cards=[
                MatchCard(title="Activa 2021", url="https://spinny.example/1", price="₹66,000", location="Velachery"),
            ]
        ),
        PlatformMatches(
            platform="Cars24",
            cards=[
                MatchCard(title="Activa 2023, 10k km", url="https://cars24.example/1", price="₹69,000", location="T Nagar"),
            ]
        )
    ]

