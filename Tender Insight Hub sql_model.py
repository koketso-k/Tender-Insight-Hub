"""
Tender Insight Hub - SQLAlchemy ORM Models
PostgreSQL schema optimized for multi-tenant SaaS performance.
"""

from datetime import datetime
from typing import Optional, List, Dict
from enum import Enum
from sqlalchemy import (
    Column, Integer, String, Boolean, Float, DateTime, 
    ForeignKey, JSON, Text, ARRAY, UniqueConstraint,
    Index, CheckConstraint, func
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()

# ---- Enums for Type Safety ----
class UserRole(str, Enum):
    GUEST = "guest"
    MEMBER = "team_member"
    ADMIN = "admin"
    ACCOUNT_OWNER = "account_owner"

class TenderStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    CLOSED = "closed"
    AWARDED = "awarded"

# ---- Core Tables ----
class Tenant(Base):
    """SaaS tenant container with subscription data"""
    __tablename__ = "tenants"
    __table_args__ = (
        Index("ix_tenant_created", "created_at"),
        CheckConstraint("subscription_expires > created_at", name="ck_subscription_dates"),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(50), unique=True)
    tier = Column(String(20), default="free")  # free, pro, enterprise
    created_at = Column(DateTime, server_default=func.now())
    subscription_expires = Column(DateTime)
    settings = Column(JSON, default={"locale": "en-ZA"})

    # Relationships
    users = relationship("User", back_populates="tenant")
    profiles = relationship("CompanyProfile", back_populates="tenant")

class User(Base):
    """Authentication and access control"""
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("email", name="uq_user_email"),
        Index("ix_user_tenant", "tenant_id"),
        Index("ix_user_role", "tenant_id", "role"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    role = Column(String(20), default=UserRole.MEMBER, nullable=False)
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)

    # Relationships
    tenant = relationship("Tenant", back_populates="users")
    activities = relationship("UserActivity", back_populates="user")

    # Hybrid properties
    @hybrid_property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

class CompanyProfile(Base):
    """SME qualification data for scoring"""
    __tablename__ = "company_profiles"
    __table_args__ = (
        UniqueConstraint("tenant_id", name="uq_tenant_profile"),
        Index("ix_profile_sectors", "tenant_id", "primary_sector"),
    )

    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    legal_name = Column(String(100))
    trading_name = Column(String(100))
    registration_number = Column(String(30))
    primary_sector = Column(String(50))
    secondary_sectors = Column(ARRAY(String(50)))
    bbbee_level = Column(Integer)
    annual_revenue = Column(Float)
    employee_count = Column(Integer)
    certifications = Column(ARRAY(String(50)))
    last_updated = Column(DateTime, onupdate=func.now())

    # Relationships
    tenant = relationship("Tenant", back_populates="profiles")
    readiness_scores = relationship("ReadinessScore", back_populates="profile")

class Tender(Base):
    """Government tender opportunities"""
    __tablename__ = "tenders"
    __table_args__ = (
        Index("ix_tender_search", "title", "description", postgresql_using="gin"),
        Index("ix_tender_active", "is_active", "deadline"),
    )

    id = Column(Integer, primary_key=True)
    external_id = Column(String(50), unique=True)  # Source system ID
    title = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(100))
    budget = Column(Float)
    currency = Column(String(3), default="ZAR")
    deadline = Column(DateTime)
    published_date = Column(DateTime)
    buyer_name = Column(String(100))
    buyer_category = Column(String(50))
    province = Column(String(50))
    documents_url = Column(String(255))
    is_active = Column(Boolean, default=True, index=True)
    status = Column(String(20), default=TenderStatus.ACTIVE)

    # Relationships
    summaries = relationship("TenderSummary", back_populates="tender")
    tracked_instances = relationship("TrackedTender", back_populates="tender")

class TrackedTender(Base):
    """Team-specific tender tracking"""
    __tablename__ = "tracked_tenders"
    __table_args__ = (
        UniqueConstraint("tenant_id", "tender_id", name="uq_tenant_tender"),
        Index("ix_tracked_status", "tenant_id", "status"),
    )

    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    tender_id = Column(Integer, ForeignKey("tenders.id"), nullable=False)
    status = Column(String(20), default="pending")
    assigned_to = Column(UUID, ForeignKey("users.id"))
    notes = Column(Text)
    last_updated = Column(DateTime, default=func.now())

    # Relationships
    tenant = relationship("Tenant")
    tender = relationship("Tender", back_populates="tracked_instances")
    assignee = relationship("User")

# ---- Audit Tables ----
class UserActivity(Base):
    """Key user actions for auditing"""
    __tablename__ = "user_activities"
    __table_args__ = (
        Index("ix_activity_tenant", "tenant_id", "activity_time"),
    )

    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    activity_type = Column(String(50))
    entity_type = Column(String(50))
    entity_id = Column(Integer)
    activity_time = Column(DateTime, server_default=func.now())
    ip_address = Column(String(45))
    user_agent = Column(String(255))

    # Relationships
    user = relationship("User", back_populates="activities")

# ---- Helper Functions ----
def create_all(engine):
    """Initialize database schema"""
    Base.metadata.create_all(engine)

def drop_all(engine):
    """Drop all tables (for testing)"""
    Base.metadata.drop_all(engine)