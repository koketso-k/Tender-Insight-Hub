"""
Scoring Service for SED Tender Insight Hub
Handles automated scoring based on CIDB and BEE compliance data
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime, date
from models.user_profile import (
    UserProfileResponse, 
    ScoringCriteria, 
    UserScoringResult, 
    ReadinessLevel,
    CIDBGrade,
    BEELevel
)
import logging

logger = logging.getLogger(__name__)

class ScoringService:
    """Service for calculating user profile scores based on compliance data"""
    
    def __init__(self):
        self.scoring_criteria = self._load_default_criteria()
    
    def _load_default_criteria(self) -> Dict[str, List[ScoringCriteria]]:
        """Load default scoring criteria for different tender types"""
        return {
            "Construction": [
                ScoringCriteria(
                    id="cidb-criteria",
                    tender_type="Construction",
                    criteria_name="CIDB Grade",
                    criteria_type="CIDB",
                    weight=40.0,
                    min_value=1,
                    max_value=9
                ),
                ScoringCriteria(
                    id="bee-criteria",
                    tender_type="Construction",
                    criteria_name="BEE Level",
                    criteria_type="BEE",
                    weight=30.0,
                    min_value=1,
                    max_value=8
                ),
                ScoringCriteria(
                    id="tax-criteria",
                    tender_type="Construction",
                    criteria_name="Tax Clearance",
                    criteria_type="Tax",
                    weight=20.0,
                    min_value=0,
                    max_value=1
                ),
                ScoringCriteria(
                    id="registration-criteria",
                    tender_type="Construction",
                    criteria_name="Company Registration",
                    criteria_type="General",
                    weight=10.0,
                    min_value=0,
                    max_value=1
                )
            ],
            "Services": [
                ScoringCriteria(
                    id="bee-services-criteria",
                    tender_type="Services",
                    criteria_name="BEE Level",
                    criteria_type="BEE",
                    weight=50.0,
                    min_value=1,
                    max_value=8
                ),
                ScoringCriteria(
                    id="tax-services-criteria",
                    tender_type="Services",
                    criteria_name="Tax Clearance",
                    criteria_type="Tax",
                    weight=30.0,
                    min_value=0,
                    max_value=1
                ),
                ScoringCriteria(
                    id="registration-services-criteria",
                    tender_type="Services",
                    criteria_name="Company Registration",
                    criteria_type="General",
                    weight=20.0,
                    min_value=0,
                    max_value=1
                )
            ],
            "Goods": [
                ScoringCriteria(
                    id="bee-goods-criteria",
                    tender_type="Goods",
                    criteria_name="BEE Level",
                    criteria_type="BEE",
                    weight=60.0,
                    min_value=1,
                    max_value=8
                ),
                ScoringCriteria(
                    id="tax-goods-criteria",
                    tender_type="Goods",
                    criteria_name="Tax Clearance",
                    criteria_type="Tax",
                    weight=25.0,
                    min_value=0,
                    max_value=1
                ),
                ScoringCriteria(
                    id="registration-goods-criteria",
                    tender_type="Goods",
                    criteria_name="Company Registration",
                    criteria_type="General",
                    weight=15.0,
                    min_value=0,
                    max_value=1
                )
            ]
        }
    
    def calculate_profile_score(self, profile: UserProfileResponse, tender_type: str) -> UserScoringResult:
        """
        Calculate overall profile score based on compliance data and tender type
        
        Args:
            profile: User profile with compliance data
            tender_type: Type of tender (Construction, Services, Goods)
            
        Returns:
            UserScoringResult with calculated scores and readiness level
        """
        try:
            criteria = self.scoring_criteria.get(tender_type, [])
            if not criteria:
                raise ValueError(f"No scoring criteria found for tender type: {tender_type}")
            
            scores = {}
            total_weighted_score = 0.0
            total_weight = 0.0
            
            for criterion in criteria:
                score = self._calculate_criterion_score(profile, criterion)
                if score is not None:
                    weighted_score = score * (criterion.weight / 100.0)
                    total_weighted_score += weighted_score
                    total_weight += criterion.weight
                    scores[criterion.criteria_name] = {
                        'score': score,
                        'weight': criterion.weight,
                        'weighted_score': weighted_score
                    }
            
            # Calculate overall score as percentage
            overall_score = (total_weighted_score / total_weight * 100) if total_weight > 0 else 0
            
            # Determine readiness level
            readiness_level = self._determine_readiness_level(overall_score, tender_type)
            
            return UserScoringResult(
                user_id=profile.user_id,
                profile_id=profile.id,
                tender_type=tender_type,
                overall_score=round(overall_score, 2),
                cidb_score=scores.get('CIDB Grade', {}).get('score'),
                bee_score=scores.get('BEE Level', {}).get('score'),
                tax_score=scores.get('Tax Clearance', {}).get('score'),
                readiness_level=readiness_level,
                calculated_at=datetime.utcnow()
            )
            
        except Exception as e:
            logger.error(f"Error calculating profile score: {str(e)}")
            raise
    
    def _calculate_criterion_score(self, profile: UserProfileResponse, criterion: ScoringCriteria) -> Optional[float]:
        """Calculate score for a specific criterion"""
        try:
            if criterion.criteria_type == "CIDB":
                return self._calculate_cidb_score(profile, criterion)
            elif criterion.criteria_type == "BEE":
                return self._calculate_bee_score(profile, criterion)
            elif criterion.criteria_type == "Tax":
                return self._calculate_tax_score(profile, criterion)
            elif criterion.criteria_type == "General":
                return self._calculate_general_score(profile, criterion)
            else:
                logger.warning(f"Unknown criteria type: {criterion.criteria_type}")
                return None
        except Exception as e:
            logger.error(f"Error calculating {criterion.criteria_name} score: {str(e)}")
            return None
    
    def _calculate_cidb_score(self, profile: UserProfileResponse, criterion: ScoringCriteria) -> Optional[float]:
        """Calculate CIDB score (higher grade = higher score)"""
        if not profile.cidb_grade or profile.cidb_status != "Active":
            return 0.0
        
        # Check if CIDB is expired
        if profile.cidb_expiry_date and profile.cidb_expiry_date < date.today():
            return 0.0
        
        # Convert grade to score (1-9 scale, where 1 is best)
        # Score = (10 - grade) / 9 * 100
        grade_value = profile.cidb_grade.value
        score = ((10 - grade_value) / 9) * 100
        return min(100.0, max(0.0, score))
    
    def _calculate_bee_score(self, profile: UserProfileResponse, criterion: ScoringCriteria) -> Optional[float]:
        """Calculate BEE score (lower level = higher score)"""
        if not profile.bee_level or profile.bee_status != "Valid":
            return 0.0
        
        # Check if BEE is expired
        if profile.bee_expiry_date and profile.bee_expiry_date < date.today():
            return 0.0
        
        # Convert level to score (1-8 scale, where 1 is best)
        # Score = (9 - level) / 8 * 100
        level_value = profile.bee_level.value
        score = ((9 - level_value) / 8) * 100
        return min(100.0, max(0.0, score))
    
    def _calculate_tax_score(self, profile: UserProfileResponse, criterion: ScoringCriteria) -> Optional[float]:
        """Calculate tax clearance score"""
        if not profile.tax_clearance_status:
            return 0.0
        
        # Check if tax clearance is expired
        if profile.tax_clearance_expiry and profile.tax_clearance_expiry < date.today():
            return 0.0
        
        return 100.0
    
    def _calculate_general_score(self, profile: UserProfileResponse, criterion: ScoringCriteria) -> Optional[float]:
        """Calculate general compliance score (company registration, etc.)"""
        if criterion.criteria_name == "Company Registration":
            return 100.0 if profile.company_registration_number else 0.0
        
        return 0.0
    
    def _determine_readiness_level(self, overall_score: float, tender_type: str) -> ReadinessLevel:
        """Determine readiness level based on overall score and tender type"""
        # Different thresholds for different tender types
        thresholds = {
            "Construction": {"high": 80, "medium": 60},
            "Services": {"high": 75, "medium": 55},
            "Goods": {"high": 70, "medium": 50}
        }
        
        tender_thresholds = thresholds.get(tender_type, {"high": 75, "medium": 55})
        
        if overall_score >= tender_thresholds["high"]:
            return ReadinessLevel.HIGH
        elif overall_score >= tender_thresholds["medium"]:
            return ReadinessLevel.MEDIUM
        else:
            return ReadinessLevel.LOW
    
    def get_scoring_recommendations(self, profile: UserProfileResponse, tender_type: str) -> List[str]:
        """Generate recommendations for improving profile score"""
        recommendations = []
        
        # CIDB recommendations
        if not profile.cidb_grade:
            recommendations.append("Register for CIDB grading to improve construction tender eligibility")
        elif profile.cidb_grade.value > 5:
            recommendations.append("Consider upgrading CIDB grade for better tender competitiveness")
        
        if profile.cidb_expiry_date and profile.cidb_expiry_date < date.today():
            recommendations.append("Renew expired CIDB registration immediately")
        
        # BEE recommendations
        if not profile.bee_level:
            recommendations.append("Obtain BEE certification to improve tender scoring")
        elif profile.bee_level.value > 4:
            recommendations.append("Work on improving BEE level for better tender competitiveness")
        
        if profile.bee_expiry_date and profile.bee_expiry_date < date.today():
            recommendations.append("Renew expired BEE certificate immediately")
        
        # Tax clearance recommendations
        if not profile.tax_clearance_status:
            recommendations.append("Obtain tax clearance certificate for tender eligibility")
        
        if profile.tax_clearance_expiry and profile.tax_clearance_expiry < date.today():
            recommendations.append("Renew expired tax clearance certificate")
        
        # General recommendations
        if not profile.company_registration_number:
            recommendations.append("Ensure company is properly registered")
        
        return recommendations
