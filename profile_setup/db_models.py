"""
Database Models for SED Tender Insight Hub
SQLAlchemy models for user profiles and scoring system
"""

from sqlalchemy import Column, String, Integer, Boolean, Date, DateTime, Float, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    company_name = Column(String(255), nullable=False)
    contact_person = Column(String(255), nullable=False)
    phone = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    scoring_history = relationship("UserScoringHistory", back_populates="user")

class UserProfile(Base):
    """User profile model for CIDB and BEE compliance"""
    __tablename__ = "user_profiles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # CIDB Compliance
    cidb_grade = Column(Integer, CheckConstraint("cidb_grade >= 1 AND cidb_grade <= 9"))
    cidb_category = Column(String(50))
    cidb_registration_number = Column(String(50))
    cidb_expiry_date = Column(Date)
    cidb_status = Column(String(20), default="Active")
    
    # BEE Compliance
    bee_level = Column(Integer, CheckConstraint("bee_level >= 1 AND bee_level <= 8"))
    bee_score = Column(Integer, CheckConstraint("bee_score >= 0 AND bee_score <= 100"))
    bee_certificate_number = Column(String(50))
    bee_certificate_issuer = Column(String(100))
    bee_expiry_date = Column(Date)
    bee_status = Column(String(20), default="Valid")
    
    # Additional Compliance
    tax_clearance_status = Column(Boolean, default=False)
    tax_clearance_expiry = Column(Date)
    vat_registration_number = Column(String(20))
    company_registration_number = Column(String(20))
    
    # Scoring metadata
    last_scored_at = Column(DateTime(timezone=True))
    scoring_version = Column(String(10), default="1.0")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="profile")
    scoring_history = relationship("UserScoringHistory", back_populates="profile")

class ScoringCriteria(Base):
    """Scoring criteria model"""
    __tablename__ = "scoring_criteria"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tender_type = Column(String(100), nullable=False)
    criteria_name = Column(String(100), nullable=False)
    criteria_type = Column(String(50), nullable=False)
    weight = Column(Float, nullable=False)
    min_value = Column(Integer)
    max_value = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class UserScoringHistory(Base):
    """User scoring history model"""
    __tablename__ = "user_scoring_history"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("user_profiles.id", ondelete="CASCADE"), nullable=False)
    tender_type = Column(String(100), nullable=False)
    overall_score = Column(Float, nullable=False)
    cidb_score = Column(Float)
    bee_score = Column(Float)
    tax_score = Column(Float)
    readiness_level = Column(String(20))
    calculated_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="scoring_history")
    profile = relationship("UserProfile", back_populates="scoring_history")
