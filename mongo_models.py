"""
Tender Insight Hub - SQLAlchemy Models
Defines all PostgreSQL tables with relationships and constraints.
"""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import (
    Column, Integer, String, Boolean, 
    Float, DateTime, ForeignKey, JSON,
    UniqueConstraint, Index
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    """User accounts with JWT authentication"""
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint('email', name='uq_user_email'),
        Index('ix_user_team', 'team_id'),
    )

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100))
    role = Column(String(50), default="team_member")  # team_member, admin, etc.
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)

    # Relationships
    team = relationship("Team", back_populates="members")
    activity_logs = relationship("UserActivityLog", back_populates="user")

class Team(Base):
    """SaaS tenant isolation unit"""
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    saas_plan = Column(String(50), default="free")  # free, pro, enterprise
    created_at = Column(DateTime, default=datetime.utcnow)
    subscription_expires = Column(DateTime)

    # Relationships
    members = relationship("User", back_populates="team")
    profiles = relationship("CompanyProfile", back_populates="team")
    tracked_tenders = relationship("TrackedTender", back_populates="team")

class CompanyProfile(Base):
    """SME profile data for readiness scoring"""
    __tablename__ = "company_profiles"
    __table_args__ = (
        UniqueConstraint('team_id', name='uq_team_profile'),
    )

    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    company_name = Column(String(100))
    registration_number = Column(String(50))
    sectors = Column(JSON)  # List of sectors e.g. ["construction", "it"]
    certifications = Column(JSON)  # e.g. ["ISO9001", "BEE-Level-1"]
    annual_revenue = Column(Float)
    employee_count = Column(Integer)
    past_experience = Column(JSON)  # List of past projects
    last_updated = Column(DateTime, default=datetime.utcnow)

    # Relationships
    team = relationship("Team", back_populates="profiles")
    readiness_scores = relationship("ReadinessScore", back_populates="profile")

class Tender(Base):
    """Public tender data from OCDS API"""
    __tablename__ = "tenders"
    __table_args__ = (
        Index('ix_tender_deadline', 'deadline'),
        Index('ix_tender_buyer', 'buyer'),
    )

    id = Column(Integer, primary_key=True)
    source_id = Column(String(100), unique=True)  # ID from government API
    title = Column(String(255), nullable=False)
    description = Column(String)
    deadline = Column(DateTime)
    budget = Column(Float)
    currency = Column(String(3), default="ZAR")
    province = Column(String(50))
    buyer = Column(String(100))  # Government department
    category = Column(String(100))
    documents_url = Column(String(255))
    published_date = Column(DateTime)
    is_active = Column(Boolean, default=True)

    # Relationships
    tracked_by = relationship("TrackedTender", back_populates="tender")
    summaries = relationship("TenderSummary", back_populates="tender")

class TrackedTender(Base):
    """Tenders saved to team workspaces"""
    __tablename__ = "tracked_tenders"
    __table_args__ = (
        UniqueConstraint('team_id', 'tender_id', name='uq_team_tender'),
    )

    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    tender_id = Column(Integer, ForeignKey("tenders.id"), nullable=False)
    status = Column(String(50), default="pending")  # pending, interested, submitted
    assigned_to = Column(Integer, ForeignKey("users.id"))
    notes = Column(String)
    last_updated = Column(DateTime, default=datetime.utcnow)

    # Relationships
    team = relationship("Team", back_populates="tracked_tenders")
    tender = relationship("Tender", back_populates="tracked_by")
    assignee = relationship("User")

class ReadinessScore(Base):
    """Generated suitability scores for tenders"""
    __tablename__ = "readiness_scores"
    __table_args__ = (
        Index('ix_score_profile', 'profile_id'),
        Index('ix_score_tender', 'tender_id'),
    )

    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("company_profiles.id"), nullable=False)
    tender_id = Column(Integer, ForeignKey("tenders.id"), nullable=False)
    score = Column(Integer)  # 0-100
    strengths = Column(JSON)  # e.g. ["certifications", "experience"]
    weaknesses = Column(JSON)  # e.g. ["revenue_too_low"]
    generated_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    profile = relationship("CompanyProfile", back_populates="readiness_scores")
    tender = relationship("Tender")

class UserActivityLog(Base):
    """Audit trail for user actions"""
    __tablename__ = "user_activity_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String(50))  # e.g. "tender_view", "summary_generate"
    entity_type = Column(String(50))  # "tender", "profile", etc.
    entity_id = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String(45))
    user_agent = Column(String(255))

    # Relationships
    user = relationship("User", back_populates="activity_logs")

# Helper function for Alembic migrations
def get_metadata():
    return Base.metadata
Database Relationships:
    TEAM ||--o{ USER : "1:N"
    TEAM ||--o{ COMPANY_PROFILE : "1:1"
    TEAM ||--o{ TRACKED_TENDER : "1:N"
    USER ||--o{ USER_ACTIVITY_LOG : "1:N"
    COMPANY_PROFILE ||--o{ READINESS_SCORE : "1:N"
    TENDER ||--o{ TRACKED_TENDER : "1:N"
    TENDER ||--o{ READINESS_SCORE : "1:N"
    TENDER ||--o{ TENDER_SUMMARY : "1:1"
    from pydantic import BaseModel

class CompanyProfileCreate(BaseModel):
    company_name: str
    sectors: List[str]
    certifications: Optional[List[str]] = None             