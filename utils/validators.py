import re
from typing import Optional

def validate_email(email: str) -> bool:
    """
    Validates email format.
    """
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None


def validate_keyword_search(keyword: str) -> bool:
    """
    Validates a keyword search string. 
    Only allows alphanumeric characters, spaces, and basic punctuation.
    """
    if not keyword or len(keyword.strip()) == 0:
        return False
    # Allow letters, digits, spaces, dash, underscore, apostrophe, and comma
    pattern = r"^[\w\s\-_',]+$"
    return re.match(pattern, keyword.strip()) is not None


def validate_budget_range(min_budget: Optional[float], max_budget: Optional[float]) -> bool:
    """
    Validates if a budget range makes sense.
    """
    if min_budget is None and max_budget is None:
        return True
    
    if min_budget is not None and min_budget < 0:
        return False
    
    if max_budget is not None and max_budget < 0:
        return False
    
    if min_budget is not None and max_budget is not None:
        return min_budget <= max_budget
    
    return True


def validate_province(province: str, valid_provinces: list) -> bool:
    """
    Checks if province is in list of valid provinces.
    """
    return province in valid_provinces


def validate_company_profile(profile: dict) -> bool:
    """
    Basic validation for company profile fields.
    
    Expects keys: industry_sector, services, certifications, geographic_coverage,
    years_experience (int), contact_email
    
    Returns True if valid, False otherwise.
    """
    required_keys = [
        "industry_sector",
        "services_provided",
        "certifications",
        "geographic_coverage",
        "years_of_experience",
        "contact_email"
    ]
    
    for key in required_keys:
        if key not in profile or not profile[key]:
            return False
    
    # Example further validation on email and years_of_experience
    if not validate_email(profile["contact_email"]):
        return False
    
    try:
        years = int(profile["years_of_experience"])
        if years < 0:
            return False
    except (ValueError, TypeError):
        return False
    
    return True
