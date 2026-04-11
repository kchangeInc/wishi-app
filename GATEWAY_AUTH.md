# Gateway Token Validation & User Info Passing

## Overview
The gateway now implements **token validation** and passes **user information** to all authenticated endpoints.

## Implementation

### 1. Gateway Authentication (`gateway/app/main.py`)
- **Token Validation**: Validates JWT tokens from Authorization header
- **Public Endpoints**: Certain endpoints can skip authentication
- **User Info Extraction**: Extracts user_id and email from token
- **Header Passing**: Adds `X-User-ID` and `X-User-Email` headers to authenticated requests

### 2. Public Endpoints (Skip Authentication)

These endpoints **do NOT require** authentication:

#### Auth Service
- `POST /auth/login/google` - Google OAuth login
- `GET /auth/callback` - OAuth callback
- `POST /auth/token` - Token refresh/exchange
- `GET /auth/health` - Health check

#### Match Engine Service
- `GET /match/templates` - Get query templates
- `GET /match/health` - Health check

#### Validation Service
- `GET /validation/health` - Health check

#### Notification Service
- `GET /notification/health` - Health check

### 3. Protected Endpoints (Require Authentication)

All other endpoints require a valid JWT token:

#### Wishlist Service ✅
- `POST /wishlist/wishlists` - Create wishlist
- `GET /wishlist/wishlists` - List wishlists
- `GET /wishlist/wishlists/{id}` - Get wishlist
- `PUT /wishlist/wishlists/{id}` - Update wishlist
- `DELETE /wishlist/wishlists/{id}` - Delete wishlist

#### Cluster Service ✅
- `POST /cluster/clusters` - Create/upsert cluster
- `GET /cluster/clusters/{id}` - Get cluster

#### Admin Service ✅
- `POST /admin/matches/{id}/review` - Review matches
- `GET /admin/dashboard` - Admin dashboard

#### Seller Service ✅
- `GET /seller/insights` - Seller insights

#### Matching Service
- Event-driven (internal), no HTTP endpoints requiring auth

---

## User Information Passing

### Request Flow
```
Client
  ↓ (Authorization: Bearer {token})
Gateway
  ↓ (validates token)
  ↓ (adds X-User-ID, X-User-Email headers)
Service Endpoints
  ↓ (receive user_id & email)
  ↓ (tracks created_by, updated_by)
Database
```

### Header Structure
```
Headers sent to protected endpoints:
- X-User-ID: 123
- X-User-Email: user@example.com
```

### Services Using User Info

#### Wishlist Service
- Automatically sets `user_id` from header when creating wishlists
- Tracks `created_by` (creator user_id)
- Tracks `updated_by` (last modifier user_id)
- `user_only=true` query param to filter wishlists by current user

#### Cluster Service
- Tracks `created_by` and `updated_by`
- Optional user tracking (user can be NULL for internal service calls)

#### Admin Service
- Can access user info for audit logging

---

## Configuration

### Required Environment Variables
```bash
SECRET_KEY=your-secret-key-change-in-prod
DB_NAME=wishi
DB_USER=user
DB_PASSWORD=password
DB_HOST=postgres
```

### Example Usage

#### 1. Login (Public - No Token Required)
```bash
POST /auth/login/google
Response: redirect to Google OAuth
```

#### 2. OAuth Callback (Public)
```bash
GET /auth/callback?code=...
Response: 
{
  "access_token": "...",
  "refresh_token": "...",
  "expires_in": 1800
}
```

#### 3. Create Wishlist (Protected - Token Required)
```bash
POST /wishlist/wishlists
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "title": "Used Car",
  "description": "Toyota Camry 2020",
  "category": "automobile",
  "filters_json": {"year": 2020, "price": 800000}
}

Response:
{
  "id": 1,
  "title": "Used Car",
  "user_id": 123,
  "created_by": 123,
  "created_at": "2026-03-29T10:00:00"
}
```

#### 4. List User's Wishlists (Protected)
```bash
GET /wishlist/wishlists?user_only=true
Authorization: Bearer {access_token}
```

#### 5. Refresh Token (Public)
```bash
POST /auth/token
Content-Type: application/json

{
  "grant_type": "refresh_token",
  "refresh_token": "..."
}
```

---

## Audit Trail

All protected endpoints now track:
- **created_by**: User ID who created the record
- **updated_by**: User ID who last modified the record
- **created_at**: Timestamp of creation
- **updated_at**: Timestamp of last modification
- **version**: Version number for optimistic locking

---

## Summary

✅ **Token Validation**: Implemented in gateway middleware
✅ **User Info Extraction**: From JWT payload
✅ **User Info Passing**: Via X-User-ID and X-User-Email headers
✅ **Audit Tracking**: created_by and updated_by fields
✅ **Public Endpoints**: Authentication-free endpoints for login/health checks
✅ **Protected Endpoints**: All data mutation endpoints require authentication

**Endpoints that can be skipped**: Login, OAuth callback, token refresh, health checks
