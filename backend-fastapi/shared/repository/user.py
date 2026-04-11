# shared/repository/user.py
"""User repository - handles user CRUD operations"""

from sqlalchemy.orm import Session
from shared.models import User, RefreshToken
from shared.repository.base import BaseRepository
from typing import Optional
from datetime import datetime, timedelta
import secrets

class UserRepository(BaseRepository[User]):
    """User-specific repository"""
    
    def __init__(self, db: Session):
        super().__init__(User, db)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.db.query(User).filter(
            User.email == email,
            User.is_deleted == False
        ).first()
    
    def get_by_google_id(self, google_id: str) -> Optional[User]:
        """Get user by Google ID"""
        return self.db.query(User).filter(
            User.google_id == google_id,
            User.is_deleted == False
        ).first()
    
    def get_active_user(self, id: int) -> Optional[User]:
        """Get active user by ID"""
        return self.db.query(User).filter(
            User.id == id,
            User.is_deleted == False,
            User.is_active == True
        ).first()
    
    def create_or_update_google_user(self, email: str, google_id: str, name: str = None) -> User:
        """Create new user or update existing Google user"""
        user = self.get_by_google_id(google_id)
        
        if user:
            # Update existing
            user.name = name or user.name
            user.display_name = name or user.display_name
            user.last_login_at = datetime.utcnow()
            user.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(user)
            return user
        
        # Create new
        user = User(
            email=email,
            name=name,
            display_name=name,
            google_id=google_id,
            role="buyer",
            is_active=True,
            last_login_at=datetime.utcnow(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def update_user(self, id: int, **kwargs) -> Optional[User]:
        """Update user"""
        user = self.get_active_user(id)
        if user:
            kwargs['updated_at'] = datetime.utcnow()
            kwargs['version'] = (user.version or 0) + 1
            for key, value in kwargs.items():
                if key not in ['id', 'created_at']:
                    setattr(user, key, value)
            self.db.commit()
            self.db.refresh(user)
        return user
    
    def create_refresh_token(self, user_id: int, expires_days: int = 7) -> str:
        """Create and store refresh token"""
        token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(days=expires_days)
        
        refresh_token = RefreshToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
            created_at=datetime.utcnow()
        )
        self.db.add(refresh_token)
        self.db.commit()
        return token
    
    def validate_refresh_token(self, token: str) -> Optional[int]:
        """Validate refresh token and return user_id"""
        refresh_token = self.db.query(RefreshToken).filter(
            RefreshToken.token == token,
            RefreshToken.revoked == False,
            RefreshToken.expires_at > datetime.utcnow()
        ).first()
        
        return refresh_token.user_id if refresh_token else None
    
    def revoke_refresh_token(self, token: str, user_id: int) -> bool:
        """Revoke refresh token"""
        refresh_token = self.db.query(RefreshToken).filter(
            RefreshToken.token == token
        ).first()
        
        if refresh_token:
            refresh_token.revoked = True
            refresh_token.revoked_at = datetime.utcnow()
            refresh_token.revoked_by = user_id
            self.db.commit()
            return True
        return False
    
    def revoke_all_user_tokens(self, user_id: int) -> int:
        """Revoke all refresh tokens for a user"""
        tokens = self.db.query(RefreshToken).filter(
            RefreshToken.user_id == user_id,
            RefreshToken.revoked == False
        ).all()
        
        count = 0
        for token in tokens:
            token.revoked = True
            token.revoked_at = datetime.utcnow()
            token.revoked_by = user_id
            count += 1
        
        self.db.commit()
        return count
