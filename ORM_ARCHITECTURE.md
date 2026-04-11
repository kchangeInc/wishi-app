# ORM & Repository Pattern Architecture

## Overview
Migrated from raw SQL queries to **SQLAlchemy ORM** with **Repository Pattern** for better code organization, maintainability, and query centralization.

## Directory Structure

```
shared/
├── models/
│   └── __init__.py          # SQLAlchemy ORM models (User, Wishlist, Cluster, Match, etc.)
├── db/
│   ├── session.py           # SQLAlchemy session management
│   ├── connection.py        # Legacy psycopg2 connection
│   └── db.py                # Legacy SQLAlchemy session (deprecated)
├── repository/
│   ├── base.py              # BaseRepository with generic CRUD operations
│   ├── user.py              # UserRepository - user-specific queries
│   ├── wishlist.py          # WishlistRepository - wishlist queries
│   ├── cluster.py           # ClusterRepository - cluster queries
│   ├── match.py             # MatchRepository - match queries
│   └── __init__.py          # Repository exports
└── service/
    ├── wishlist_service.py  # WishlistService - business logic layer
    └── __init__.py          # Service exports
```

## Architecture Layers

### 1. **ORM Models** (`shared/models/`)
- SQLAlchemy ORM models with column definitions
- Automatic table creation support
- Type safety and IDE autocompletion

```python
# Example: Wishlist model
class Wishlist(Base):
    __tablename__ = "wishlist"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_by = Column(Integer, ForeignKey("users.id"))
    # ... more columns
```

### 2. **Repository Pattern** (`shared/repository/`)
- **BaseRepository**: Generic CRUD operations
  - `create()` - Insert record
  - `get_by_id()` - Fetch by ID
  - `get_all()` - List with pagination
  - `update()` - Update record
  - `delete()` - Hard delete
  - `soft_delete()` - Soft delete (mark as deleted)

- **Specific Repositories**: Domain-specific query methods
  - `WishlistRepository`: `get_by_user()`, `get_by_category()`, `get_active_wishlists()`
  - `ClusterRepository`: `get_or_create()`, `get_active_clusters()`
  - `UserRepository`: `get_by_email()`, `create_or_update_google_user()`
  - `MatchRepository`: `get_pending_validation()`, `get_by_cluster()`

### 3. **Service Layer** (`shared/service/`)
- Pure business logic (no SQL queries)
- Uses repositories for data access
- Data transformation and validation
- API response formatting

```python
# Example: WishlistService
class WishlistService:
    def __init__(self, db: Session):
        self.repo = WishlistRepository(db)
    
    def create_wishlist(self, title, user_id, ...):
        wishlist = self.repo.create_wishlist(...)
        return self._wishlist_to_dict(wishlist)
```

### 4. **HTTP Layer** (FastAPI endpoints)
- Receives requests
- Calls service layer
- Returns JSON responses

## Benefits

✅ **No Raw SQL Strings**: All queries in repository classes
✅ **Type Safety**: ORM provides type hints
✅ **Reusability**: Repositories used across services
✅ **Testing**: Easy to mock repositories
✅ **Maintainability**: Single source of truth for each query
✅ **Hybrid Approach**: Can still use raw SQL via `db.execute()`
✅ **Migration Ready**: Alembic integrates seamlessly

## Usage Examples

### Creating a Wishlist (Old vs New)

#### Old Approach (Raw SQL)
```python
with conn.cursor() as cur:
    cur.execute("""
        INSERT INTO wishlist(title, user_id, created_by, ...)
        VALUES (%s, %s, %s, ...)
        RETURNING id, created_at, ...
    """, (title, user_id, user_id, ...))
    row = cur.fetchone()
    conn.commit()
```

#### New Approach (ORM)
```python
service = WishlistService(db_session)
wishlist_dict = service.create_wishlist(
    title=title,
    user_id=user_id,
    display_title=display_title,
    category=category,
    filters_json=filters_json
)
```

### Getting User's Wishlists

#### Old Approach
```python
with conn.cursor() as cur:
    cur.execute("""
        SELECT id, title, ... FROM wishlist
        WHERE user_id = %s AND is_deleted = FALSE
        ORDER BY created_at DESC
    """, (user_id,))
    rows = cur.fetchall()
# Manual row-to-dict conversion
```

#### New Approach
```python
service = WishlistService(db_session)
wishlists = service.get_user_wishlists(user_id)
# Automatically formatted as dicts
```

### Soft Delete

#### Old Approach
```python
with conn.cursor() as cur:
    cur.execute("""
        UPDATE wishlist SET is_deleted = TRUE, updated_by = %s
        WHERE id = %s
    """, (user_id, wishlist_id))
    conn.commit()
```

#### New Approach
```python
service = WishlistService(db_session)
success = service.delete_wishlist(wishlist_id, user_id)
```

## Hybrid Approach (Raw SQL When Needed)

If you need complex queries or optimizations, you can use raw SQL via repository:

```python
from sqlalchemy import text

# In repository
def complex_query(self):
    result = self.db.execute(text("""
        SELECT w.id, w.title, COUNT(m.id) as match_count
        FROM wishlist w
        LEFT JOIN matches m ON w.id = m.wishlist_id
        WHERE w.is_deleted = FALSE
        GROUP BY w.id
    """))
    return result.fetchall()
```

## Environment Configuration

### Database URL
```bash
DATABASE_URL=postgresql://user:password@postgres:5432/wishi
```

### SQL Debugging (Optional)
```bash
SQL_ECHO=true  # Enable SQLAlchemy SQL logging
```

## Migration from Raw SQL

### Step 1: Use Service Layer
```python
# Old
with conn.cursor() as cur:
    cur.execute("SELECT ... FROM wishlist WHERE ...")

# New
service = WishlistService(db_session)
wishlists = service.get_all_wishlists()
```

### Step 2: Update Models
Already created in `shared/models/__init__.py`

### Step 3: Update Endpoints
Use dependency injection to get service:

```python
from fastapi import Depends
from shared.db.session import get_db_session
from shared.service import WishlistService

@app.get("/wishlists")
def list_wishlists(db = Depends(get_db_session)):
    service = WishlistService(db)
    return service.get_all_wishlists()
```

## Summary

| Aspect | Old | New |
|--------|-----|-----|
| Query Location | Scattered in endpoints | Centralized in repositories |
| SQL Pattern | Raw parameterized SQL | SQLAlchemy ORM |
| Type Safety | Limited | Full (Python types + mypy) |
| Testing | Difficult (mock cursors) | Easy (mock repositories) |
| Code Reuse | Manual | Via repositories + services |
| Maintainability | Low (SQL strings) | High (methods with names) |

✅ **Ready for production** - All models and repositories in place
✅ **Gradual migration** - Can update services incrementally
✅ **Hybrid support** - Both ORM and raw SQL available
