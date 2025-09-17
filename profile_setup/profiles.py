"""
Profile Management API Endpoints
Handles CRUD operations for user profiles with CIDB and BEE compliance data
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
import logging

from database import get_db
from models.user_profile import (
    UserProfileCreate,
    UserProfileUpdate,
    UserProfileResponse,
    ProfileScoringRequest,
    ProfileScoringResponse,
    UserScoringResult
)
from services.scoring_service import ScoringService
from auth import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/profiles", tags=["profiles"])

@router.post("/", response_model=UserProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_user_profile(
    profile_data: UserProfileCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new user profile with CIDB and BEE compliance data
    
    Args:
        profile_data: Profile data including CIDB and BEE information
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Created user profile
    """
    try:
        # Check if user already has a profile
        existing_profile = db.query(UserProfile).filter(
            UserProfile.user_id == current_user["id"]
        ).first()
        
        if existing_profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already has a profile. Use PUT to update existing profile."
            )
        
        # Create new profile
        profile = UserProfile(
            user_id=current_user["id"],
            **profile_data.dict()
        )
        
        db.add(profile)
        db.commit()
        db.refresh(profile)
        
        logger.info(f"Created profile for user {current_user['id']}")
        return profile
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create profile"
        )

@router.get("/me", response_model=UserProfileResponse)
async def get_my_profile(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's profile
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        User's profile data
    """
    try:
        profile = db.query(UserProfile).filter(
            UserProfile.user_id == current_user["id"]
        ).first()
        
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found"
            )
        
        return profile
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve profile"
        )

@router.put("/me", response_model=UserProfileResponse)
async def update_my_profile(
    profile_update: UserProfileUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update current user's profile
    
    Args:
        profile_update: Profile update data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Updated user profile
    """
    try:
        profile = db.query(UserProfile).filter(
            UserProfile.user_id == current_user["id"]
        ).first()
        
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found"
            )
        
        # Update only provided fields
        update_data = profile_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(profile, field, value)
        
        profile.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(profile)
        
        logger.info(f"Updated profile for user {current_user['id']}")
        return profile
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile"
        )

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_my_profile(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete current user's profile
    
    Args:
        current_user: Current authenticated user
        db: Database session
    """
    try:
        profile = db.query(UserProfile).filter(
            UserProfile.user_id == current_user["id"]
        ).first()
        
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found"
            )
        
        db.delete(profile)
        db.commit()
        
        logger.info(f"Deleted profile for user {current_user['id']}")
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete profile"
        )

@router.post("/score", response_model=ProfileScoringResponse)
async def calculate_profile_score(
    scoring_request: ProfileScoringRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Calculate profile score for a specific tender type
    
    Args:
        scoring_request: Scoring request with tender type
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Profile scoring results with recommendations
    """
    try:
        # Get user profile
        profile = db.query(UserProfile).filter(
            UserProfile.user_id == current_user["id"]
        ).first()
        
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found. Please create a profile first."
            )
        
        # Calculate score using scoring service
        scoring_service = ScoringService()
        scoring_result = scoring_service.calculate_profile_score(
            profile, scoring_request.tender_type
        )
        
        # Get recommendations
        recommendations = scoring_service.get_scoring_recommendations(
            profile, scoring_request.tender_type
        )
        
        # Save scoring history
        scoring_history = UserScoringHistory(
            user_id=scoring_result.user_id,
            profile_id=scoring_result.profile_id,
            tender_type=scoring_result.tender_type,
            overall_score=scoring_result.overall_score,
            cidb_score=scoring_result.cidb_score,
            bee_score=scoring_result.bee_score,
            tax_score=scoring_result.tax_score,
            readiness_level=scoring_result.readiness_level.value
        )
        
        db.add(scoring_history)
        db.commit()
        
        # Prepare response
        breakdown = {
            "cidb_score": scoring_result.cidb_score,
            "bee_score": scoring_result.bee_score,
            "tax_score": scoring_result.tax_score,
            "overall_score": scoring_result.overall_score
        }
        
        return ProfileScoringResponse(
            user_id=scoring_result.user_id,
            profile_id=scoring_result.profile_id,
            tender_type=scoring_result.tender_type,
            overall_score=scoring_result.overall_score,
            breakdown=breakdown,
            readiness_level=scoring_result.readiness_level,
            recommendations=recommendations
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error calculating profile score: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to calculate profile score"
        )

@router.get("/score/history", response_model=List[UserScoringResult])
async def get_scoring_history(
    tender_type: Optional[str] = None,
    limit: int = 10,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's scoring history
    
    Args:
        tender_type: Filter by tender type (optional)
        limit: Maximum number of results to return
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        List of scoring history records
    """
    try:
        query = db.query(UserScoringHistory).filter(
            UserScoringHistory.user_id == current_user["id"]
        )
        
        if tender_type:
            query = query.filter(UserScoringHistory.tender_type == tender_type)
        
        history = query.order_by(
            UserScoringHistory.calculated_at.desc()
        ).limit(limit).all()
        
        return history
        
    except Exception as e:
        logger.error(f"Error retrieving scoring history: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve scoring history"
        )

@router.get("/compliance/status")
async def get_compliance_status(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current compliance status for all certifications
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Compliance status summary
    """
    try:
        profile = db.query(UserProfile).filter(
            UserProfile.user_id == current_user["id"]
        ).first()
        
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found"
            )
        
        from datetime import date
        today = date.today()
        
        compliance_status = {
            "cidb": {
                "has_certification": profile.cidb_grade is not None,
                "grade": profile.cidb_grade.value if profile.cidb_grade else None,
                "status": profile.cidb_status,
                "expiry_date": profile.cidb_expiry_date,
                "is_expired": profile.cidb_expiry_date < today if profile.cidb_expiry_date else False,
                "days_until_expiry": (profile.cidb_expiry_date - today).days if profile.cidb_expiry_date else None
            },
            "bee": {
                "has_certification": profile.bee_level is not None,
                "level": profile.bee_level.value if profile.bee_level else None,
                "score": profile.bee_score,
                "status": profile.bee_status,
                "expiry_date": profile.bee_expiry_date,
                "is_expired": profile.bee_expiry_date < today if profile.bee_expiry_date else False,
                "days_until_expiry": (profile.bee_expiry_date - today).days if profile.bee_expiry_date else None
            },
            "tax_clearance": {
                "has_clearance": profile.tax_clearance_status,
                "expiry_date": profile.tax_clearance_expiry,
                "is_expired": profile.tax_clearance_expiry < today if profile.tax_clearance_expiry else False,
                "days_until_expiry": (profile.tax_clearance_expiry - today).days if profile.tax_clearance_expiry else None
            }
        }
        
        return compliance_status
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving compliance status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve compliance status"
        )
