"""
SED Tender Insight Hub - Configuration
Centralized configuration management
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration class"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'mysql://root:password@localhost/sed_tender_hub')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ALGORITHM = 'HS256'
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    
    # CORS Configuration
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:8080,http://127.0.0.1:8080').split(',')
    
    # Scoring Configuration
    DEFAULT_SCORING_WEIGHTS = {
        'CIDB_GRADE': 25.0,
        'BEE_LEVEL': 20.0,
        'YEARS_IN_BUSINESS': 15.0,
        'ANNUAL_TURNOVER': 15.0,
        'TENDER_SUCCESS_RATE': 10.0,
        'PROFILE_COMPLETENESS': 10.0,
        'COMPANY_SIZE': 5.0
    }
    
    # CIDB Configuration
    CIDB_GRADES = {
        1: {'min_value': 0, 'max_value': 200000, 'description': 'R0 - R200,000'},
        2: {'min_value': 200000, 'max_value': 500000, 'description': 'R200,000 - R500,000'},
        3: {'min_value': 500000, 'max_value': 1000000, 'description': 'R500,000 - R1,000,000'},
        4: {'min_value': 1000000, 'max_value': 3000000, 'description': 'R1,000,000 - R3,000,000'},
        5: {'min_value': 3000000, 'max_value': 8000000, 'description': 'R3,000,000 - R8,000,000'},
        6: {'min_value': 8000000, 'max_value': 15000000, 'description': 'R8,000,000 - R15,000,000'},
        7: {'min_value': 15000000, 'max_value': 40000000, 'description': 'R15,000,000 - R40,000,000'},
        8: {'min_value': 40000000, 'max_value': 80000000, 'description': 'R40,000,000 - R80,000,000'},
        9: {'min_value': 80000000, 'max_value': float('inf'), 'description': 'R80,000,000+'}
    }
    
    # BEE Configuration
    BEE_LEVELS = {
        1: {'min_points': 100, 'description': '100+ points'},
        2: {'min_points': 95, 'max_points': 99, 'description': '95-99 points'},
        3: {'min_points': 90, 'max_points': 94, 'description': '90-94 points'},
        4: {'min_points': 80, 'max_points': 89, 'description': '80-89 points'},
        5: {'min_points': 75, 'max_points': 79, 'description': '75-79 points'},
        6: {'min_points': 70, 'max_points': 74, 'description': '70-74 points'},
        7: {'min_points': 55, 'max_points': 69, 'description': '55-69 points'},
        8: {'min_points': 40, 'max_points': 54, 'description': '40-54 points'}
    }
    
    # Work Categories
    WORK_CATEGORIES = {
        'GB': 'General Building',
        'CE': 'Civil Engineering',
        'ME': 'Mechanical Engineering',
        'EE': 'Electrical Engineering',
        'RE': 'Refrigeration and Air Conditioning',
        'EL': 'Elevator Installation',
        'RO': 'Roads and Storm Water Drainage',
        'WA': 'Water and Sanitation',
        'EN': 'Environmental',
        'OT': 'Other'
    }
    
    # Validation Rules
    VALIDATION_RULES = {
        'cidb_grade': {'min': 1, 'max': 9, 'type': 'integer'},
        'bee_level': {'min': 1, 'max': 8, 'type': 'integer'},
        'bee_percentage': {'min': 0, 'max': 100, 'type': 'decimal'},
        'years_in_business': {'min': 0, 'max': 100, 'type': 'integer'},
        'annual_turnover': {'min': 0, 'type': 'decimal'},
        'number_of_employees': {'min': 0, 'max': 10000, 'type': 'integer'},
        'tender_wins': {'min': 0, 'type': 'integer'},
        'tender_applications': {'min': 0, 'type': 'integer'}
    }

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_ECHO = False
    
    # Override with production values
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable must be set in production")

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on environment"""
    env = os.environ.get('FLASK_ENV', 'default')
    return config.get(env, config['default'])

