from sqlalchemy.orm import Session
from sqlalchemy import and_
from models import User, Team, TeamMember, CompanyProfile
from schemas import UserCreate, TeamCreate
from auth import get_password_hash
from typing import List, Optional

def create_user(db: Session, user_data: UserCreate, hashed_password: str):
    """Create a new user"""
    db_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        role=user_data.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()

def create_team(db: Session, team_data: TeamCreate, created_by: int):
    """Create a new team"""
    db_team = Team(
        name=team_data.name,
        description=team_data.description,
        plan=team_data.plan,
        created_by=created_by
    )
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    
    # Add creator as team member
    team_member = TeamMember(
        team_id=db_team.id,
        user_id=created_by,
        role="admin"  # Creator becomes admin
    )
    db.add(team_member)
    db.commit()
    
    return db_team

def get_team_by_name(db: Session, name: str):
    """Get team by name"""
    return db.query(Team).filter(Team.name == name).first()

def get_team_by_id(db: Session, team_id: int):
    """Get team by ID"""
    return db.query(Team).filter(Team.id == team_id).first()

def get_user_teams(db: Session, user_id: int):
    """Get all teams where user is a member"""
    teams = db.query(Team).join(TeamMember).filter(
        TeamMember.user_id == user_id
    ).all()
    return teams

def add_team_member(db: Session, team_id: int, user_id: int, role: str = "collaborator"):
    """Add a user to a team"""
    team_member = TeamMember(
        team_id=team_id,
        user_id=user_id,
        role=role
    )
    db.add(team_member)
    db.commit()
    return team_member

def get_team_members(db: Session, team_id: int):
    """Get all members of a team"""
    members = db.query(User).join(TeamMember).filter(
        TeamMember.team_id == team_id
    ).all()
    return members

def create_company_profile(db: Session, profile_data, team_id: int):
    """Create a company profile for a team"""
    db_profile = CompanyProfile(
        team_id=team_id,
        industry_sector=profile_data.get("industry_sector"),
        services_provided=profile_data.get("services_provided"),
        certifications=profile_data.get("certifications"),
        geographic_coverage=profile_data.get("geographic_coverage"),
        years_of_experience=profile_data.get("years_of_experience"),
        contact_email=profile_data.get("contact_email"),
        contact_phone=profile_data.get("contact_phone")
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def get_company_profile(db: Session, team_id: int):
    """Get company profile for a team"""
    return db.query(CompanyProfile).filter(CompanyProfile.team_id == team_id).first()
