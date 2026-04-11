# ORM MIGRATION GUIDE

## Quick Start: Converting Wishlist Service

### Before (Raw SQL in Endpoint)
```python
@app.post("/wishlists", response_model=WishlistResponse)
def create_wishlist(payload: WishlistCreate, request: Request):
    user = get_current_user(request)
    
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO wishlist(...)
            VALUES (...)
            RETURNING id, created_at, ...
        """, (title, ..., user["user_id"]))
        wid, created_at, updated_at = cur.fetchone()
        conn.commit()
    
    return {"id": wid, "created_at": created_at, ...}
```

### After (ORM + Service Layer)
```python
from fastapi import Depends
from shared.db.session import get_db_session
from shared.service.wishlist_service import WishlistService

@app.post("/wishlists", response_model=WishlistResponse)
def create_wishlist(payload: WishlistCreate, request: Request, 
                   db = Depends(get_db_session)):
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
    
    return result
```

## Step-by-Step Migration

### Step 1: Update imports
**OLD:**
```python
import psycopg2
conn = psycopg2.connect(...)
```

**NEW:**
```python
from fastapi import Depends
from shared.db.session import get_db_session
from shared.service.wishlist_service import WishlistService
```

### Step 2: Remove connection initialization
Remove:
```python
import os
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME", "wishi"),
    ...
)
```

### Step 3: Update endpoint signatures
Add `db` parameter with dependency injection:
```python
def get_wishlist(wishlist_id: int, db = Depends(get_db_session)):
    service = WishlistService(db)
    return service.get_wishlist(wishlist_id)
```

### Step 4: Replace all SQL calls
Replace:
```python
with conn.cursor() as cur:
    cur.execute("SELECT ... WHERE id = %s", (id,))
    row = cur.fetchone()
```

With:
```python
service = WishlistService(db)
result = service.get_wishlist(id)
```

## Available Service Methods

### WishlistService Methods

```python
# Create
service.create_wishlist(title, user_id, user_email, ...)

# Read
service.get_wishlist(wishlist_id)
service.get_all_wishlists(skip=0, limit=100)
service.get_user_wishlists(user_id)
service.get_wishlist_by_category(category)
service.get_active_wishlists()

# Update
service.update_wishlist(wishlist_id, user_id, title=..., description=...)

# Delete
service.delete_wishlist(wishlist_id, user_id)
```

## Complete Refactored Endpoint Examples

### Example 1: List Wishlists
```python
@app.get("/wishlists")
def list_wishlists(
    request: Request,
    user_only: bool = False,
    skip: int = 0,
    limit: int = 100,
    db = Depends(get_db_session)
):
    user = get_optional_user(request)
    service = WishlistService(db)
    
    if user_only and user:
        return service.get_user_wishlists(user["user_id"], skip, limit)
    else:
        return service.get_all_wishlists(skip, limit)
```

### Example 2: Update Wishlist
```python
@app.put("/wishlists/{wishlist_id}")
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
        description=payload.description,
        category=payload.category,
        filters_json=payload.filters_json
    )
    
    if not result:
        raise HTTPException(status_code=404, detail="Wishlist not found")
    
    return result
```

### Example 3: Delete Wishlist
```python
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
    
    return {"status": "deleted", "wishlist_id": wishlist_id}
```

## Creating New Services

### Create a Cluster Service

```python
# shared/service/cluster_service.py
from sqlalchemy.orm import Session
from shared.repository.cluster import ClusterRepository
from datetime import datetime

class ClusterService:
    def __init__(self, db: Session):
        self.repo = ClusterRepository(db)
    
    def get_or_create(self, normalized_filters: str, user_id: int = None) -> dict:
        cluster = self.repo.get_or_create(normalized_filters, user_id)
        return self._cluster_to_dict(cluster)
    
    def get_cluster(self, cluster_id: int) -> dict:
        cluster = self.repo.get_not_deleted(cluster_id)
        return self._cluster_to_dict(cluster) if cluster else None
    
    @staticmethod
    def _cluster_to_dict(cluster) -> dict:
        if not cluster:
            return None
        return {
            "id": cluster.id,
            "normalized_filters": cluster.normalized_filters,
            "buyer_count": cluster.buyer_count,
            "created_at": cluster.created_at,
            ...
        }
```

## Testing with ORM

### Mock Repository for Tests
```python
from unittest.mock import Mock, MagicMock
from shared.service.wishlist_service import WishlistService

def test_create_wishlist():
    # Mock repository
    mock_repo = Mock()
    mock_repo.create_wishlist.return_value = Mock(
        id=1,
        title="Car",
        user_id=123
    )
    
    # Create service with mocked DB
    service = WishlistService(Mock())
    service.repo = mock_repo
    
    result = service.create_wishlist("Car", 123, "user@example.com")
    
    assert result["id"] == 1
    assert result["title"] == "Car"
    mock_repo.create_wishlist.assert_called_once()
```

## Performance Tips

### 1. Use Pagination
```python
# Good - limit results
wishlists = service.get_all_wishlists(skip=0, limit=100)

# Avoid - load all records
wishlists = service.get_all_wishlists()  # default limit=100
```

### 2. Custom Filter Queries
For complex queries, add methods to repositories:

```python
# In ClusterRepository
def get_top_clusters_by_demand(self, limit=10):
    return self.db.query(Cluster).filter(
        Cluster.is_deleted == False
    ).order_by(Cluster.buyer_count.desc()).limit(limit).all()
```

### 3. Use Raw SQL for Complex Joins
```python
# In repository
from sqlalchemy import text

def complex_match_query(self):
    result = self.db.execute(text("""
        SELECT w.id, w.title, COUNT(m.id) as matches
        FROM wishlist w
        LEFT JOIN matches m ON w.id = m.cluster_id
        WHERE w.is_deleted = FALSE
        GROUP BY w.id
    """))
    return result.fetchall()
```

## Migration Checklist

- [ ] Create ORM models in `shared/models/__init__.py` ✅
- [ ] Create repositories in `shared/repository/` ✅
- [ ] Create service layers in `shared/service/` ✅
- [ ] Update imports in services
- [ ] Replace SQL queries with service methods
- [ ] Test each endpoint
- [ ] Remove raw SQL from endpoints
- [ ] Update error handling
- [ ] Run full test suite

## Common Patterns

### Pattern 1: CRUD Endpoint
```python
@app.get("/items/{item_id}")
def get_item(item_id: int, db = Depends(get_db_session)):
    service = YourService(db)
    item = service.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404)
    return item
```

### Pattern 2: List with Pagination
```python
@app.get("/items")
def list_items(skip: int = 0, limit: int = 100, db = Depends(get_db_session)):
    service = YourService(db)
    return service.get_all_items(skip, limit)
```

### Pattern 3: Create with User Tracking
```python
@app.post("/items")
def create_item(payload: ItemCreate, request: Request, db = Depends(get_db_session)):
    user = get_current_user(request)
    service = YourService(db)
    return service.create_item(
        user_id=user["user_id"],
        **payload.dict()
    )
```

## Next Steps

1. Migrate `wishlist` service endpoints (start here)
2. Migrate `cluster` service endpoints
3. Migrate `matching` service (uses transactions)
4. Migrate `admin` service
5. Update `auth` service to use UserRepository

---

✅ **All ORM models and repositories ready**
📦 **SQLAlchemy installed**
🚀 **Ready to start migrating services**
