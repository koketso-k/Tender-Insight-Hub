"""
User Profile Models for SED Tender Insight Hub
Handles CIDB and BEE compliance data for South African tender scoring
"""

from datetime import datetime, date
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from enum import Enum
import uuid

class CIDBGrade(int, Enum):
    """CIDB Grade enumeration (1-9, where 1 is highest)"""
    GRADE_1 = 1
    GRADE_2 = 2
    GRADE_3 = 3
    GRADE_4 = 4
    GRADE_5 = 5
    GRADE_6 = 6
    GRADE_7 = 7
    GRADE_8 = 8
    GRADE_9 = 9

class BEELevel(int, Enum):
    """BEE Level enumeration (1-8, where 1 is highest)"""
    LEVEL_1 = 1
    LEVEL_2 = 2
    LEVEL_3 = 3
    LEVEL_4 = 4
    LEVEL_5 = 5
    LEVEL_6 = 6
    LEVEL_7 = 7
    LEVEL_8 = 8

class ComplianceStatus(str, Enum):
    """Compliance status enumeration"""
    ACTIVE = "Active"
    SUSPENDED = "Suspended"
    EXPIRED = "Expired"
    VALID = "Valid"
    PENDING = "Pending"

class ReadinessLevel(str, Enum):
    """Tender readiness level"""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

class UserBase(BaseModel):
    """Base user model"""
    email: str = Field(..., description="User email address")
    company_name: str = Field(..., description="Company name")
    contact_person: str = Field(..., description="Contact person name")
    phone: Optional[str] = Field(None, description="Contact phone number")

class UserCreate(UserBase):
    """User creation model"""
    password: str = Field(..., min_length=8, description="User password")

class UserResponse(UserBase):
    """User response model"""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserProfileBase(BaseModel):
    """Base user profile model for CIDB and BEE compliance"""
    
    # CIDB Compliance
    cidb_grade: Optional[CIDBGrade] = Field(None, description="CIDB grade (1-9)")
    cidb_category: Optional[str] = Field(None, description="CIDB category")
    cidb_registration_number: Optional[str] = Field(None, description="CIDB registration number")
    cidb_expiry_date: Optional[date] = Field(None, description="CIDB expiry date")
    cidb_status: ComplianceStatus = Field(ComplianceStatus.ACTIVE, description="CIDB status")
    
    # BEE Compliance
    bee_level: Optional[BEELevel] = Field(None, description="BEE level (1-8)")
    bee_score: Optional[int] = Field(None, ge=0, le=100, description="BEE score (0-100)")
    bee_certificate_number: Optional[str] = Field(None, description="BEE certificate number")
    bee_certificate_issuer: Optional[str] = Field(None, description="BEE certificate issuer")
    bee_expiry_date: Optional[date] = Field(None, description="BEE expiry date")
    bee_status: ComplianceStatus = Field(ComplianceStatus.VALID, description="BEE status")
    
    # Additional Compliance
    tax_clearance_status: bool = Field(False, description="Tax clearance status")
    tax_clearance_expiry: Optional[date] = Field(None, description="Tax clearance expiry date")
    vat_registration_number: Optional[str] = Field(None, description="VAT registration number")
    company_registration_number: Optional[str] = Field(None, description="Company registration number")

    @validator('cidb_grade')
    def validate_cidb_grade(cls, v):
        if v is not None and not (1 <= v <= 9):
            raise ValueError('CIDB grade must be between 1 and 9')
        return v

    @validator('bee_level')
    def validate_bee_level(cls, v):
        if v is not None and not (1 <= v <= 8):
            raise ValueError('BEE level must be between 1 and 8')
        return v

    @validator('bee_score')
    def validate_bee_score(cls, v):
        if v is not None and not (0 <= v <= 100):
            raise ValueError('BEE score must be between 0 and 100')
        return v

class UserProfileCreate(UserProfileBase):
    """User profile creation model"""
    pass

class UserProfileUpdate(BaseModel):
    """User profile update model - all fields optional"""
    
    # CIDB Compliance
    cidb_grade: Optional[CIDBGrade] = None
    cidb_category: Optional[str] = None
    cidb_registration_number: Optional[str] = None
    cidb_expiry_date: Optional[date] = None
    cidb_status: Optional[ComplianceStatus] = None
    
    # BEE Compliance
    bee_level: Optional[BEELevel] = None
    bee_score: Optional[int] = Field(None, ge=0, le=100)
    bee_certificate_number: Optional[str] = None
    bee_certificate_issuer: Optional[str] = None
    bee_expiry_date: Optional[date] = None
    bee_status: Optional[ComplianceStatus] = None
    
    # Additional Compliance
    tax_clearance_status: Optional[bool] = None
    tax_clearance_expiry: Optional[date] = None
    vat_registration_number: Optional[str] = None
    company_registration_number: Optional[str] = None

class UserProfileResponse(UserProfileBase):
    """User profile response model"""
    id: uuid.UUID
    user_id: uuid.UUID
    last_scored_at: Optional[datetime] = None
    scoring_version: str = "1.0"
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ScoringCriteria(BaseModel):
    """Scoring criteria model"""
    id: uuid.UUID
    tender_type: str
    criteria_name: str
    criteria_type: str
    weight: float
    min_value: Optional[int] = None
    max_value: Optional[int] = None
    is_active: bool = True

class UserScoringResult(BaseModel):
    """User scoring result model"""
    user_id: uuid.UUID
    profile_id: uuid.UUID
    tender_type: str
    overall_score: float
    cidb_score: Optional[float] = None
    bee_score: Optional[float] = None
    tax_score: Optional[float] = None
    readiness_level: ReadinessLevel
    calculated_at: datetime

class ProfileScoringRequest(BaseModel):
    """Request model for calculating profile scores"""
    tender_type: str = Field(..., description="Type of tender (Construction, Services, Goods)")
    user_id: Optional[uuid.UUID] = Field(None, description="Specific user ID (optional)")

class ProfileScoringResponse(BaseModel):
    """Response model for profile scoring"""
    user_id: uuid.UUID
    profile_id: uuid.UUID
    tender_type: str
    overall_score: float
    breakdown: Dict[str, Any]
    readiness_level: ReadinessLevel
    recommendations: list[str] = []
