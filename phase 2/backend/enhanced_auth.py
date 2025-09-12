"""
Enhanced JWT Authentication & Role-Based Access Control (RBAC)
This module provides comprehensive JWT authentication with advanced RBAC features
"""

import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import os
from enum import Enum

from database import get_db
from models import User, UserRole, Team, TeamMember
from schemas import TokenData

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-this-in-production-12345")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

class Permission(str, Enum):
    """Define specific permissions for RBAC"""
    # User Management
    CREATE_USER = "create_user"
    READ_USER = "read_user"
    UPDATE_USER = "update_user"
    DELETE_USER = "delete_user"
    
    # Team Management
    CREATE_TEAM = "create_team"
    READ_TEAM = "read_team"
    UPDATE_TEAM = "update_team"
    DELETE_TEAM = "delete_team"
    MANAGE_TEAM_MEMBERS = "manage_team_members"
    
    # Tender Management
    SEARCH_TENDERS = "search_tenders"
    VIEW_TENDER_DETAILS = "view_tender_details"
    SAVE_TENDERS = "save_tenders"
    MANAGE_TENDER_STATUS = "manage_tender_status"
    
    # AI Features
    USE_AI_SUMMARIZATION = "use_ai_summarization"
    USE_READINESS_SCORING = "use_readiness_scoring"
    EXPORT_REPORTS = "export_reports"
    
    # Analytics
    VIEW_ANALYTICS = "view_analytics"
    MANAGE_ANALYTICS = "manage_analytics"
    
    # Admin Features
    MANAGE_SYSTEM = "manage_system"
    VIEW_ALL_TEAMS = "view_all_teams"
    MANAGE_ALL_USERS = "manage_all_users"

# Role-Permission mapping
ROLE_PERMISSIONS = {
    UserRole.ADMIN: [
        # Full access to everything
        Permission.CREATE_USER, Permission.READ_USER, Permission.UPDATE_USER, Permission.DELETE_USER,
        Permission.CREATE_TEAM, Permission.READ_TEAM, Permission.UPDATE_TEAM, Permission.DELETE_TEAM,
        Permission.MANAGE_TEAM_MEMBERS, Permission.SEARCH_TENDERS, Permission.VIEW_TENDER_DETAILS,
        Permission.SAVE_TENDERS, Permission.MANAGE_TENDER_STATUS, Permission.USE_AI_SUMMARIZATION,
        Permission.USE_READINESS_SCORING, Permission.EXPORT_REPORTS, Permission.VIEW_ANALYTICS,
        Permission.MANAGE_ANALYTICS, Permission.MANAGE_SYSTEM, Permission.VIEW_ALL_TEAMS,
        Permission.MANAGE_ALL_USERS
    ],
    UserRole.SME: [
        # Subject Matter Expert permissions
        Permission.READ_USER, Permission.UPDATE_USER, Permission.CREATE_TEAM, Permission.READ_TEAM,
        Permission.UPDATE_TEAM, Permission.MANAGE_TEAM_MEMBERS, Permission.SEARCH_TENDERS,
        Permission.VIEW_TENDER_DETAILS, Permission.SAVE_TENDERS, Permission.MANAGE_TENDER_STATUS,
        Permission.USE_AI_SUMMARIZATION, Permission.USE_READINESS_SCORING, Permission.EXPORT_REPORTS,
        Permission.VIEW_ANALYTICS
    ],
    UserRole.COLLABORATOR: [
        # Basic collaborator permissions
        Permission.READ_USER, Permission.READ_TEAM, Permission.SEARCH_TENDERS,
        Permission.VIEW_TENDER_DETAILS, Permission.SAVE_TENDERS
    ]
}

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token with enhanced payload"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Add additional token metadata
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    })
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    """Create a JWT refresh token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    })
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, token_type: str = "access") -> TokenData:
    """Verify and decode a JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Verify token type
        if payload.get("type") != token_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token type. Expected {token_type}"
            )
        
        email: str = payload.get("sub")
        role: str = payload.get("role")
        user_id: int = payload.get("user_id")
        
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        token_data = TokenData(email=email, role=role, user_id=user_id)
        return token_data
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get the current authenticated user with enhanced validation"""
    token = verify_token(credentials.credentials)
    
    user = db.query(User).filter(User.email == token.email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get the current active user (can be extended for user status checks)"""
    # Add any additional user status checks here
    return current_user

def require_permission(permission: Permission):
    """Decorator to require specific permission"""
    def permission_checker(current_user: User = Depends(get_current_user)):
        user_role = current_user.role
        user_permissions = ROLE_PERMISSIONS.get(user_role, [])
        
        if permission not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required: {permission.value}"
            )
        return current_user
    return permission_checker

def require_role(required_role: UserRole):
    """Decorator to require specific role"""
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required role: {required_role.value}"
            )
        return current_user
    return role_checker

def get_user_permissions(user: User) -> List[Permission]:
    """Get all permissions for a user based on their role"""
    return ROLE_PERMISSIONS.get(user.role, [])

def check_permission(user: User, permission: Permission) -> bool:
    """Check if user has specific permission"""
    user_permissions = get_user_permissions(user)
    return permission in user_permissions

def get_user_teams(user: User, db: Session) -> List[Team]:
    """Get all teams where user is a member"""
    teams = db.query(Team).join(TeamMember).filter(
        TeamMember.user_id == user.id
    ).all()
    return teams

def is_team_admin(user: User, team_id: int, db: Session) -> bool:
    """Check if user is admin of specific team"""
    membership = db.query(TeamMember).filter(
        TeamMember.user_id == user.id,
        TeamMember.team_id == team_id,
        TeamMember.role == UserRole.ADMIN
    ).first()
    return membership is not None

def is_team_member(user: User, team_id: int, db: Session) -> bool:
    """Check if user is member of specific team"""
    membership = db.query(TeamMember).filter(
        TeamMember.user_id == user.id,
        TeamMember.team_id == team_id
    ).first()
    return membership is not None

def get_user_team_role(user: User, team_id: int, db: Session) -> Optional[UserRole]:
    """Get user's role in specific team"""
    membership = db.query(TeamMember).filter(
        TeamMember.user_id == user.id,
        TeamMember.team_id == team_id
    ).first()
    return membership.role if membership else None

class TokenResponse:
    """Enhanced token response with refresh token"""
    def __init__(self, access_token: str, refresh_token: str, token_type: str = "bearer"):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_type = token_type

def create_token_pair(user: User) -> TokenResponse:
    """Create both access and refresh tokens for user"""
    token_data = {
        "sub": user.email,
        "role": user.role.value,
        "user_id": user.id,
        "full_name": user.full_name
    }
    
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    return TokenResponse(access_token, refresh_token)

