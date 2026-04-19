# WISHI Deal-Platform

AI-powered listing aggregator marketplace MVP with buyer wishlists, seller listings, and automatic matching.

## How to Run
### Terminal 1 — Backend:
``` python scripts/run_local.py ```

### Terminal 2 — Frontend:
cd frontend-nextjs
npm run dev


## 🚀 Quick Start

### Option 1: Local Development (Recommended - No Docker Required)

```bash
# 1. Setup Python environment
python -m venv venv
venv\Scripts\activate  # Windows

# 2. Install dependencies
pip install -r requirements.txt
pip install -r backend-fastapi/requirements.txt

# 3. Setup environment variables
cp .env.example .env
# Edit .env with your database and OAuth credentials (optional for basic testing)

# 4. Start API Gateway
set PYTHONPATH=%CD%\backend-fastapi
uvicorn backend-fastapi.gateway.app.main:app --host 0.0.0.0 --port 8000 --reload
```

**✅ API will be available at http://localhost:8000**

### Option 2: Docker (Requires Docker Desktop Running)

```bash
# Ensure Docker Desktop is running first!
docker-compose up --build
```

Access:
- **Frontend**: http://localhost (via Nginx)
- **API Gateway**: http://localhost:8000
- **Monitoring**: http://localhost:9090 (Prometheus), http://localhost:3001 (Grafana admin/admin), http://localhost:3100 (Loki)

### Option 3: Frontend Only

```bash
cd frontend-nextjs
npm install
npm run dev
```

Access at http://localhost:3000

## 📁 Project Structure

```
wishi/
├── frontend-nextjs/          # Next.js storefront & buyer dashboard
├── backend-fastapi/          # FastAPI microservices
│   ├── gateway/              # API Gateway (port 8000)
│   ├── services/             # Individual microservices
│   │   ├── auth/            # Authentication (port 8001)
│   │   ├── wishlist/        # Wishlist management (port 8002)
│   │   ├── seller/          # Seller insights (port 8003)
│   │   ├── matching/        # Match orchestration (port 8004)
│   │   ├── cluster/         # Wishlist clustering (port 8005)
│   │   ├── match-engine/    # Search query generation (port 8006)
│   │   ├── validation/      # URL validation & scoring (port 8007)
│   │   ├── notification/    # Email notifications (port 8008)
│   │   ├── admin/           # Admin review dashboard (port 8009)
│   │   └── worker/          # Async task processing
│   └── shared/              # Shared utilities & models
├── extension/                # Chrome extension for sellers
├── docker/                   # Docker configurations
├── migrations/               # Database migrations
├── nginx.conf                # Reverse proxy config
├── prometheus.yml            # Monitoring config
├── docker-compose.yml        # Service orchestration
├── requirements.txt          # Python dependencies
└── WISHI_Postman_Collection.json  # API testing collection
```

## 🛠 Prerequisites

- **Python 3.9+** (for backend development)
- **Node.js 18+** (for frontend development)
- **Docker Desktop** (for full stack deployment)
- **PostgreSQL** (local or Docker)
- **Redis** (local or Docker)
- **Kafka** (local or Docker)

## 🔧 Environment Setup

### 1. Clone and Setup

```bash
git clone <repository-url>
cd wishi
```

### 2. Environment Variables

Copy and configure environment files:

```bash
cp .env.example .env
```

Required variables:
```env
# Database
DB_NAME=wishi
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost  # local run
DB_PORT=5432

# JWT
SECRET_KEY=your-secret-key-change-in-prod

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Gateway service routing (local defaults)
AUTH_SERVICE_URL=http://localhost:8001
WISHLIST_SERVICE_URL=http://localhost:8002
SELLER_SERVICE_URL=http://localhost:8003
MATCHING_SERVICE_URL=http://localhost:8004
CLUSTER_SERVICE_URL=http://localhost:8005
MATCH_ENGINE_SERVICE_URL=http://localhost:8006
VALIDATION_SERVICE_URL=http://localhost:8007
NOTIFICATION_SERVICE_URL=http://localhost:8008
ADMIN_SERVICE_URL=http://localhost:8009
```

Tip: for Docker Compose use `DB_HOST=postgres`.

### 3. Database Setup

```bash
# Using Docker
docker run -d --name postgres-wishi -p 5432:5432 -e POSTGRES_DB=wishi -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password postgres:13

# Or install PostgreSQL locally and create database
createdb wishi
```

### 4. Run Migrations

```bash
alembic upgrade head
```

## 🚀 Running the Application

### Full Stack with Docker

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Backend Only (Development)

```bash
# Activate virtual environment
venv\Scripts\activate

# Set Python path
set PYTHONPATH=%CD%\backend-fastapi

# Start gateway
uvicorn backend-fastapi.gateway.app.main:app --host 0.0.0.0 --port 8000 --reload

# In another terminal, start individual services (if needed)
# Note: Gateway proxies to services, so only gateway needed for basic testing
```

### Frontend Only (Development)

```bash
cd frontend-nextjs
npm install
npm run dev
```

### Extension Development

```bash
cd extension
# Load unpacked extension in Chrome developer mode
```

## 🧪 Testing with Postman

1. **Import Collection**:
   - Open Postman
   - Import `WISHI_Postman_Collection.json`
   - Import `WISHI_Postman_Environment.json`

2. **Select Environment**:
   - Choose "WISHI Local Development"

3. **Test Flow**:
   - Start with Gateway → Health Check
   - Test public endpoints (categories, templates)
   - Authenticate via Google OAuth
   - Test protected endpoints (create wishlist, etc.)

## 📊 Monitoring & Observability

- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3001 (admin/admin)
- **Loki**: http://localhost:3100
- **API Metrics**: http://localhost:8000/metrics
- **Health Checks**: http://localhost:8000/health

### Logging

- Backend services emit structured JSON logs to stdout by default.
- Promtail scrapes backend container logs and pushes them to Loki.
- Grafana is pre-provisioned with both Prometheus and Loki datasources.
- Each log line includes `service`, `trace_id`, `logger`, and exception details when present.

Useful queries in Grafana Explore:

```logql
{service="gateway"}
```

```logql
{trace_id="your-trace-id"}
```

Optional local file fallback for a service:

```bash
ENABLE_FILE_LOGS=true LOG_FORMAT=text uvicorn backend-fastapi.gateway.app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 🔒 Authentication

The platform uses Google OAuth 2.0 with JWT tokens:

1. **Login Flow**:
   - GET `/auth/login/google` → Redirect to Google
   - Google callback → GET `/auth/callback`
   - POST `/auth/token` → Receive access_token

2. **Protected Endpoints**:
   - Include `Authorization: Bearer <access_token>` header
   - Gateway validates tokens and adds user context headers

## 🏗 Architecture

### API Gateway Pattern
- **Gateway** (port 8000): Central entry point with authentication, rate limiting, and routing
- **Rate Limiting**: 100 requests/minute per IP
- **CORS**: Enabled for frontend integration
- **Metrics**: Prometheus integration for monitoring

### Microservices
- **Auth Service**: OAuth authentication and token management
- **Wishlist Service**: CRUD operations for buyer wishlists
- **Matching Service**: Orchestrates the matching pipeline
- **Cluster Service**: Groups similar wishlists
- **Match Engine**: Generates search queries
- **Validation Service**: Scores and validates candidate URLs
- **Admin Service**: Manual review interface
- **Notification Service**: Email notifications
- **Seller Service**: Market insights

### Data Flow
1. User creates wishlist → Kafka event
2. Matching service processes → Calls cluster, match-engine, validation
3. Results stored in database with status (auto_publish/admin_review/reject)
4. Notifications sent to users

## 🔧 Development Commands

```bash
# Run tests
pytest backend-fastapi/tests/

# Run specific service
cd backend-fastapi/services/auth
uvicorn app.main:app --port 8001

# Database migrations
alembic revision --autogenerate -m "migration message"
alembic upgrade head

# Docker management
docker-compose build --no-cache
docker-compose up -d gateway
docker-compose logs -f gateway

# Start all backend services locally (opens separate PowerShell windows)
powershell -ExecutionPolicy Bypass -File scripts/start-backend-local.ps1

# Start all backend services except worker
powershell -ExecutionPolicy Bypass -File scripts/start-backend-local.ps1 -IncludeWorker:$false

# Stop all backend service terminals started by the local launcher
powershell -ExecutionPolicy Bypass -File scripts/stop-backend-local.ps1
```

## 🚀 Deployment

### Production Checklist
- [ ] Update environment variables for production
- [ ] Configure SSL certificates
- [ ] Setup production database
- [ ] Configure monitoring alerts
- [ ] Update OAuth redirect URIs
- [ ] Enable security headers

### Docker Production

```bash
# Build production images
docker-compose -f docker-compose.prod.yml up --build
```

## 📝 API Documentation

- **Interactive API Docs**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc
- **Postman Collection**: `WISHI_Postman_Collection.json`

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Submit pull request

## 📄 License

[Add your license here]

## 🆘 Troubleshooting

### Common Issues

**❌ Docker Daemon Not Running** (Most Common):
```
Error: pywintypes.error: (2, 'CreateFile', 'The system cannot find the file specified.')
```
**✅ Solution**: Use Local Development option instead (see Quick Start Option 1)

**Docker Issues**:
- Ensure Docker Desktop is running
- Check available disk space
- Try `docker system prune`

**Database Connection**:
- Verify PostgreSQL is running
- Check connection string in .env
- Run migrations: `alembic upgrade head`

**Import Errors**:
- Ensure PYTHONPATH is set: `set PYTHONPATH=%CD%\backend-fastapi`
- Activate virtual environment
- Install dependencies: `pip install -r requirements.txt`

**Port Conflicts**:
- Check if ports 8000, 3000, 5432 are available
- Use `netstat -ano | findstr :8000`

**OAuth Issues**:
- Verify Google OAuth credentials
- Update redirect URIs in Google Console
- Check callback URL matches configuration
8. **Database Migrations**: Alembic already integrated.

