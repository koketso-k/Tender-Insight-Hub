from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from models import UserRole, TeamPlan

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole = UserRole.COLLABORATOR

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Team schemas
class TeamBase(BaseModel):
    name: str
    description: Optional[str] = None
    plan: TeamPlan = TeamPlan.FREE

class TeamCreate(TeamBase):
    pass

class TeamResponse(TeamBase):
    id: int
    created_at: datetime
    created_by: str
    
    class Config:
        from_attributes = True

# Token schema
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None

# Company Profile schemas
class CompanyProfileBase(BaseModel):
    industry_sector: Optional[str] = None
    services_provided: Optional[str] = None
    certifications: Optional[str] = None
    geographic_coverage: Optional[str] = None
    years_of_experience: Optional[int] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None

class CompanyProfileCreate(CompanyProfileBase):
    team_id: int

class CompanyProfileResponse(CompanyProfileBase):
    id: int
    team_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
