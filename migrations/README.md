# Database Migrations

This project uses Alembic for version-based database schema management.

## Setup

1. Install Alembic: `pip install alembic`
2. Copy `.env.example` to `.env` and fill in your values.

## Usage

### Create a new migration
```bash
alembic revision -m "Add new table"
```

### Apply migrations
```bash
alembic upgrade head
```

### Check current status
```bash
alembic current
```

### Downgrade
```bash
alembic downgrade -1
```

## Migrations Directory

- `migrations/versions/` contains all migration scripts.
- Each migration has `upgrade()` and `downgrade()` functions.

## Environment Variables

All database connections use environment variables:
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`

See `.env.example` for details.