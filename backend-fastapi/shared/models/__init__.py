# shared/models/__init__.py
"""Database models using SQLAlchemy ORM"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey, Numeric, Index
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(255))
    display_name = Column(String(255))
    google_id = Column(String(255), unique=True)
    role = Column(String(50), default="buyer")
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    last_login_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.id"))
    updated_by = Column(Integer, ForeignKey("users.id"))
    version = Column(Integer, default=1)
    
    __table_args__ = (
        Index("idx_users_email", "email"),
        Index("idx_users_google_id", "google_id"),
    )


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String(512), unique=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    revoked = Column(Boolean, default=False)
    revoked_at = Column(DateTime)
    revoked_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Wishlist(Base):
    __tablename__ = "wishlist"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    display_title = Column(String(255))
    description = Column(Text)
    category = Column(String(100))
    subcategory = Column(String(100))
    filters_json = Column(JSON)
    user_email = Column(String(255))
    user_id = Column(Integer, ForeignKey("users.id"))
    expiry_date = Column(DateTime)
    status = Column(String(50), default="active")
    priority = Column(String(50), default="medium")
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.id"))
    updated_by = Column(Integer, ForeignKey("users.id"))
    version = Column(Integer, default=1)
    
    __table_args__ = (
        Index("idx_wishlist_user_id", "user_id"),
    )


class Cluster(Base):
    __tablename__ = "clusters"
    
    id = Column(Integer, primary_key=True)
    normalized_filters = Column(String(512), unique=True, nullable=False)
    display_name = Column(String(255))
    description = Column(Text)
    buyer_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    last_matched_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.id"))
    updated_by = Column(Integer, ForeignKey("users.id"))
    version = Column(Integer, default=1)
    
    __table_args__ = (
        Index("idx_clusters_normalized_filters", "normalized_filters"),
    )


class Match(Base):
    __tablename__ = "matches"
    
    id = Column(Integer, primary_key=True)
    cluster_id = Column(Integer, ForeignKey("clusters.id"))
    url = Column(Text, nullable=False)
    source = Column(String(100))
    title = Column(String(255))
    description = Column(Text)
    price = Column(Numeric(10, 2))
    location = Column(String(255))
    image_url = Column(Text)
    score = Column(Integer)
    status = Column(String(50), default="pending")
    validation_attempts = Column(Integer, default=0)
    last_validation_error = Column(Text)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_validated_at = Column(DateTime)
    created_by = Column(Integer, ForeignKey("users.id"))
    updated_by = Column(Integer, ForeignKey("users.id"))
    version = Column(Integer, default=1)
    
    __table_args__ = (
        Index("idx_matches_cluster_id", "cluster_id"),
        Index("idx_matches_status", "status"),
    )


class Click(Base):
    __tablename__ = "clicks"
    
    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey("matches.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    ip_address = Column(String(45))
    user_agent = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index("idx_clicks_match_id", "match_id"),
        Index("idx_clicks_user_id", "user_id"),
    )


class AuditLog(Base):
    __tablename__ = "audit_log"
    
    id = Column(Integer, primary_key=True)
    table_name = Column(String(100), nullable=False)
    record_id = Column(Integer, nullable=False)
    action = Column(String(50), nullable=False)  # INSERT, UPDATE, DELETE
    old_values = Column(JSON)
    new_values = Column(JSON)
    user_id = Column(Integer, ForeignKey("users.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String(45))
    
    __table_args__ = (
        Index("idx_audit_log_table_record", "table_name", "record_id"),
    )
