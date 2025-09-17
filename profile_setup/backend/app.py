"""
SED Tender Insight Hub - Profile Setup & Scoring API
Backend service for managing user profiles with CIDB and BEE scoring
"""

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, date
from decimal import Decimal
import json
import hashlib
import jwt
from functools import wraps
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///sed_tender_hub.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

# Database Models
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    company_name = db.Column(db.String(255))
    company_registration_number = db.Column(db.String(50))
    phone_number = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationship
    profile = db.relationship('UserProfile', backref='user', uselist=False, cascade='all, delete-orphan')

class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # CIDB Information
    cidb_grade = db.Column(db.Integer, db.CheckConstraint('cidb_grade BETWEEN 1 AND 9'))
    cidb_registration_number = db.Column(db.String(50))
    cidb_expiry_date = db.Column(db.Date)
    cidb_work_categories = db.Column(db.JSON)
    
    # BEE Information
    bee_level = db.Column(db.Integer, db.CheckConstraint('bee_level BETWEEN 1 AND 8'))
    bee_certificate_number = db.Column(db.String(100))
    bee_expiry_date = db.Column(db.Date)
    bee_ownership_percentage = db.Column(db.Numeric(5, 2), db.CheckConstraint('bee_ownership_percentage >= 0 AND bee_ownership_percentage <= 100'))
    bee_management_control_percentage = db.Column(db.Numeric(5, 2), db.CheckConstraint('bee_management_control_percentage >= 0 AND bee_management_control_percentage <= 100'))
    bee_skills_development_percentage = db.Column(db.Numeric(5, 2), db.CheckConstraint('bee_skills_development_percentage >= 0 AND bee_skills_development_percentage <= 100'))
    bee_enterprise_development_percentage = db.Column(db.Numeric(5, 2), db.CheckConstraint('bee_enterprise_development_percentage >= 0 AND bee_enterprise_development_percentage <= 100'))
    bee_socio_economic_development_percentage = db.Column(db.Numeric(5, 2), db.CheckConstraint('bee_socio_economic_development_percentage >= 0 AND bee_socio_economic_development_percentage <= 100'))
    
    # Additional scoring factors
    years_in_business = db.Column(db.Integer, default=0)
    annual_turnover = db.Column(db.Numeric(15, 2), default=0)
    number_of_employees = db.Column(db.Integer, default=0)
    previous_tender_wins = db.Column(db.Integer, default=0)
    previous_tender_applications = db.Column(db.Integer, default=0)
    
    # Calculated scores
    readiness_score = db.Column(db.Integer, default=0)
    profile_completion_percentage = db.Column(db.Integer, default=0)
    last_score_calculation = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CIDBWorkCategory(db.Model):
    __tablename__ = 'cidb_work_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    category_code = db.Column(db.String(10), unique=True, nullable=False)
    category_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)

class ScoringCriteria(db.Model):
    __tablename__ = 'scoring_criteria'
    
    id = db.Column(db.Integer, primary_key=True)
    criteria_name = db.Column(db.String(100), nullable=False)
    criteria_type = db.Column(db.Enum('CIDB', 'BEE', 'EXPERIENCE', 'FINANCIAL', 'OTHER'), nullable=False)
    weight_percentage = db.Column(db.Numeric(5, 2), nullable=False)
    max_score = db.Column(db.Integer, default=100)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Authentication decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.filter_by(id=data['user_id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

# Utility functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_token(user_id):
    return jwt.encode({'user_id': user_id}, app.config['SECRET_KEY'], algorithm='HS256')

def calculate_profile_completion(profile):
    """Calculate profile completion percentage"""
    total_fields = 15  # Total number of profile fields
    filled_fields = 0
    
    fields_to_check = [
        profile.cidb_grade, profile.cidb_registration_number, profile.cidb_expiry_date,
        profile.bee_level, profile.bee_certificate_number, profile.bee_expiry_date,
        profile.bee_ownership_percentage, profile.bee_management_control_percentage,
        profile.bee_skills_development_percentage, profile.bee_enterprise_development_percentage,
        profile.bee_socio_economic_development_percentage, profile.years_in_business,
        profile.annual_turnover, profile.number_of_employees, profile.cidb_work_categories
    ]
    
    for field in fields_to_check:
        if field is not None and field != 0 and field != []:
            filled_fields += 1
    
    return int((filled_fields / total_fields) * 100)

def calculate_readiness_score(profile):
    """Calculate overall readiness score based on various factors"""
    if not profile:
        return 0
    
    # Get scoring criteria weights
    criteria = ScoringCriteria.query.filter_by(is_active=True).all()
    total_score = 0
    total_weight = 0
    
    for criterion in criteria:
        weight = float(criterion.weight_percentage)
        score = 0
        
        if criterion.criteria_type == 'CIDB' and profile.cidb_grade:
            # CIDB grade scoring (1-9 scale, higher is better)
            score = (profile.cidb_grade / 9) * 100
        
        elif criterion.criteria_type == 'BEE' and profile.bee_level:
            # BEE level scoring (1-8 scale, lower is better)
            score = ((9 - profile.bee_level) / 8) * 100
        
        elif criterion.criteria_type == 'EXPERIENCE' and profile.years_in_business:
            # Years in business scoring (capped at 20 years for 100%)
            score = min((profile.years_in_business / 20) * 100, 100)
        
        elif criterion.criteria_type == 'FINANCIAL' and profile.annual_turnover:
            # Annual turnover scoring (logarithmic scale)
            if profile.annual_turnover > 0:
                score = min((float(profile.annual_turnover) / 10000000) * 100, 100)  # 10M for 100%
        
        elif criterion.criteria_type == 'OTHER' and criterion.criteria_name == 'Profile Completeness':
            score = profile.profile_completion_percentage
        
        elif criterion.criteria_type == 'OTHER' and criterion.criteria_name == 'Company Size':
            # Company size scoring
            if profile.number_of_employees:
                score = min((profile.number_of_employees / 100) * 100, 100)
        
        total_score += score * weight
        total_weight += weight
    
    return int(total_score / total_weight) if total_weight > 0 else 0

# API Routes

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['email', 'password', 'first_name', 'last_name']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    # Check if user already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'User already exists'}), 409
    
    # Create new user
    user = User(
        email=data['email'],
        password_hash=hash_password(data['password']),
        first_name=data['first_name'],
        last_name=data['last_name'],
        company_name=data.get('company_name'),
        company_registration_number=data.get('company_registration_number'),
        phone_number=data.get('phone_number')
    )
    
    db.session.add(user)
    db.session.commit()
    
    # Create initial profile
    profile = UserProfile(user_id=user.id)
    db.session.add(profile)
    db.session.commit()
    
    token = generate_token(user.id)
    
    return jsonify({
        'message': 'User registered successfully',
        'token': token,
        'user': {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'company_name': user.company_name
        }
    }), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or user.password_hash != hash_password(data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    token = generate_token(user.id)
    
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'company_name': user.company_name
        }
    })

@app.route('/api/profiles', methods=['GET'])
@token_required
def get_profile(current_user):
    """Get user profile"""
    profile = UserProfile.query.filter_by(user_id=current_user.id).first()
    
    if not profile:
        return jsonify({'error': 'Profile not found'}), 404
    
    return jsonify({
        'profile': {
            'id': profile.id,
            'user_id': profile.user_id,
            'cidb_grade': profile.cidb_grade,
            'cidb_registration_number': profile.cidb_registration_number,
            'cidb_expiry_date': profile.cidb_expiry_date.isoformat() if profile.cidb_expiry_date else None,
            'cidb_work_categories': profile.cidb_work_categories,
            'bee_level': profile.bee_level,
            'bee_certificate_number': profile.bee_certificate_number,
            'bee_expiry_date': profile.bee_expiry_date.isoformat() if profile.bee_expiry_date else None,
            'bee_ownership_percentage': float(profile.bee_ownership_percentage) if profile.bee_ownership_percentage else None,
            'bee_management_control_percentage': float(profile.bee_management_control_percentage) if profile.bee_management_control_percentage else None,
            'bee_skills_development_percentage': float(profile.bee_skills_development_percentage) if profile.bee_skills_development_percentage else None,
            'bee_enterprise_development_percentage': float(profile.bee_enterprise_development_percentage) if profile.bee_enterprise_development_percentage else None,
            'bee_socio_economic_development_percentage': float(profile.bee_socio_economic_development_percentage) if profile.bee_socio_economic_development_percentage else None,
            'years_in_business': profile.years_in_business,
            'annual_turnover': float(profile.annual_turnover) if profile.annual_turnover else None,
            'number_of_employees': profile.number_of_employees,
            'previous_tender_wins': profile.previous_tender_wins,
            'previous_tender_applications': profile.previous_tender_applications,
            'readiness_score': profile.readiness_score,
            'profile_completion_percentage': profile.profile_completion_percentage,
            'last_score_calculation': profile.last_score_calculation.isoformat() if profile.last_score_calculation else None,
            'created_at': profile.created_at.isoformat(),
            'updated_at': profile.updated_at.isoformat()
        }
    })

@app.route('/api/profiles', methods=['PUT'])
@token_required
def update_profile(current_user):
    """Update user profile"""
    data = request.get_json()
    
    profile = UserProfile.query.filter_by(user_id=current_user.id).first()
    
    if not profile:
        return jsonify({'error': 'Profile not found'}), 404
    
    # Update profile fields
    if 'cidb_grade' in data:
        profile.cidb_grade = data['cidb_grade']
    if 'cidb_registration_number' in data:
        profile.cidb_registration_number = data['cidb_registration_number']
    if 'cidb_expiry_date' in data:
        profile.cidb_expiry_date = datetime.strptime(data['cidb_expiry_date'], '%Y-%m-%d').date() if data['cidb_expiry_date'] else None
    if 'cidb_work_categories' in data:
        profile.cidb_work_categories = data['cidb_work_categories']
    
    if 'bee_level' in data:
        profile.bee_level = data['bee_level']
    if 'bee_certificate_number' in data:
        profile.bee_certificate_number = data['bee_certificate_number']
    if 'bee_expiry_date' in data:
        profile.bee_expiry_date = datetime.strptime(data['bee_expiry_date'], '%Y-%m-%d').date() if data['bee_expiry_date'] else None
    if 'bee_ownership_percentage' in data:
        profile.bee_ownership_percentage = Decimal(str(data['bee_ownership_percentage'])) if data['bee_ownership_percentage'] else None
    if 'bee_management_control_percentage' in data:
        profile.bee_management_control_percentage = Decimal(str(data['bee_management_control_percentage'])) if data['bee_management_control_percentage'] else None
    if 'bee_skills_development_percentage' in data:
        profile.bee_skills_development_percentage = Decimal(str(data['bee_skills_development_percentage'])) if data['bee_skills_development_percentage'] else None
    if 'bee_enterprise_development_percentage' in data:
        profile.bee_enterprise_development_percentage = Decimal(str(data['bee_enterprise_development_percentage'])) if data['bee_enterprise_development_percentage'] else None
    if 'bee_socio_economic_development_percentage' in data:
        profile.bee_socio_economic_development_percentage = Decimal(str(data['bee_socio_economic_development_percentage'])) if data['bee_socio_economic_development_percentage'] else None
    
    if 'years_in_business' in data:
        profile.years_in_business = data['years_in_business']
    if 'annual_turnover' in data:
        profile.annual_turnover = Decimal(str(data['annual_turnover'])) if data['annual_turnover'] else None
    if 'number_of_employees' in data:
        profile.number_of_employees = data['number_of_employees']
    if 'previous_tender_wins' in data:
        profile.previous_tender_wins = data['previous_tender_wins']
    if 'previous_tender_applications' in data:
        profile.previous_tender_applications = data['previous_tender_applications']
    
    # Recalculate scores
    profile.profile_completion_percentage = calculate_profile_completion(profile)
    profile.readiness_score = calculate_readiness_score(profile)
    profile.last_score_calculation = datetime.utcnow()
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Profile updated successfully',
            'profile': {
                'readiness_score': profile.readiness_score,
                'profile_completion_percentage': profile.profile_completion_percentage,
                'last_score_calculation': profile.last_score_calculation.isoformat()
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/api/profiles/score', methods=['POST'])
@token_required
def recalculate_score(current_user):
    """Recalculate readiness score"""
    profile = UserProfile.query.filter_by(user_id=current_user.id).first()
    
    if not profile:
        return jsonify({'error': 'Profile not found'}), 404
    
    # Recalculate scores
    profile.profile_completion_percentage = calculate_profile_completion(profile)
    profile.readiness_score = calculate_readiness_score(profile)
    profile.last_score_calculation = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'readiness_score': profile.readiness_score,
        'profile_completion_percentage': profile.profile_completion_percentage,
        'last_score_calculation': profile.last_score_calculation.isoformat()
    })

@app.route('/api/cidb/categories', methods=['GET'])
def get_cidb_categories():
    """Get CIDB work categories"""
    categories = CIDBWorkCategory.query.filter_by(is_active=True).all()
    
    return jsonify({
        'categories': [{
            'id': cat.id,
            'category_code': cat.category_code,
            'category_name': cat.category_name,
            'description': cat.description
        } for cat in categories]
    })

@app.route('/api/scoring/criteria', methods=['GET'])
def get_scoring_criteria():
    """Get scoring criteria"""
    criteria = ScoringCriteria.query.filter_by(is_active=True).all()
    
    return jsonify({
        'criteria': [{
            'id': c.id,
            'criteria_name': c.criteria_name,
            'criteria_type': c.criteria_type,
            'weight_percentage': float(c.weight_percentage),
            'max_score': c.max_score,
            'description': c.description
        } for c in criteria]
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
