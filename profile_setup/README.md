# SED Tender Insight Hub - Profile Setup & Scoring System

A comprehensive profile management system for South African tender compliance, featuring CIDB (Construction Industry Development Board) and BEE (Broad-Based Black Economic Empowerment) scoring capabilities.

## Features

### 🏗️ CIDB Integration
- **CIDB Grade Management**: Support for grades 1-9 with corresponding value ranges
- **Work Categories**: Multiple work category selection (General Building, Civil Engineering, etc.)
- **Registration Tracking**: CIDB registration number and expiry date management
- **Automated Scoring**: CIDB grade contributes to overall readiness score

### 🤝 BEE Compliance
- **BEE Level Management**: Support for levels 1-8 with point ranges
- **Scorecard Elements**: Complete BEE scorecard tracking including:
  - Ownership percentage
  - Management control percentage
  - Skills development percentage
  - Enterprise development percentage
  - Socio-economic development percentage
- **Certificate Management**: BEE certificate number and expiry tracking

### 📊 Advanced Scoring System
- **Multi-factor Scoring**: Combines CIDB, BEE, experience, and financial factors
- **Weighted Calculations**: Configurable weights for different scoring criteria
- **Real-time Updates**: Automatic score recalculation on profile changes
- **Readiness Assessment**: 0-100 readiness score for tender applications

### 🏢 Company Profile Management
- **Basic Information**: Company name, registration number, contact details
- **Business Metrics**: Years in business, annual turnover, employee count
- **Performance Tracking**: Previous tender wins and applications
- **Success Rate Calculation**: Automatic calculation of tender success rate

## System Architecture

### Backend (Flask API)
- **RESTful API**: Complete CRUD operations for profiles
- **Authentication**: JWT-based authentication system
- **Database**: MySQL with comprehensive schema for all profile data
- **Validation**: Server-side validation for all input data
- **Scoring Engine**: Automated calculation of readiness scores

### Frontend (HTML/CSS/JavaScript)
- **Responsive Design**: Bootstrap-based modern UI
- **Tabbed Interface**: Organized sections for different profile aspects
- **Real-time Validation**: Client-side form validation
- **Progress Tracking**: Visual progress indicators and completion percentages
- **Export Functionality**: Profile data export capabilities

## Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL 5.7+
- Modern web browser

### Backend Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Database Setup**
   ```bash
   # Create MySQL database
   mysql -u root -p
   CREATE DATABASE sed_tender_hub;
   
   # Import schema
   mysql -u root -p sed_tender_hub < database_schema.sql
   ```

3. **Environment Configuration**
   ```bash
   export DATABASE_URL="mysql://username:password@localhost/sed_tender_hub"
   export SECRET_KEY="your-secret-key-here"
   ```

4. **Run Backend Server**
   ```bash
   python backend/app.py
   ```

### Frontend Setup

1. **Serve Frontend Files**
   ```bash
   # Using Python's built-in server
   cd frontend
   python -m http.server 8080
   
   # Or using any web server (Apache, Nginx, etc.)
   ```

2. **Access Application**
   - Open browser to `http://localhost:8080`
   - Backend API should be running on `http://localhost:5000`

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login

### Profile Management
- `GET /api/profiles` - Get user profile
- `PUT /api/profiles` - Update user profile
- `POST /api/profiles/score` - Recalculate readiness score

### Reference Data
- `GET /api/cidb/categories` - Get CIDB work categories
- `GET /api/scoring/criteria` - Get scoring criteria

## Database Schema

### Core Tables
- **users**: Basic user information
- **user_profiles**: Detailed profile and scoring data
- **cidb_work_categories**: CIDB work category reference
- **scoring_criteria**: Configurable scoring criteria
- **user_profile_history**: Profile change tracking

### Key Features
- **Foreign Key Constraints**: Data integrity enforcement
- **Check Constraints**: Value range validation
- **JSON Fields**: Flexible data storage for work categories
- **Audit Trail**: Complete change history tracking

## Scoring Algorithm

The readiness score is calculated using weighted criteria:

1. **CIDB Grade (25%)**: Higher grades = higher score
2. **BEE Level (20%)**: Lower levels = higher score (1 is best)
3. **Years in Business (15%)**: More experience = higher score
4. **Annual Turnover (15%)**: Higher turnover = higher score
5. **Tender Success Rate (10%)**: More wins = higher score
6. **Profile Completeness (10%)**: More complete = higher score
7. **Company Size (5%)**: More employees = higher score

## Usage Guide

### 1. User Registration
- Register with email, password, and basic company information
- System automatically creates initial profile

### 2. Profile Setup
- **CIDB Tab**: Enter CIDB grade, registration details, and work categories
- **BEE Tab**: Enter BEE level, certificate details, and scorecard elements
- **Company Tab**: Complete company information and business metrics
- **Experience Tab**: Add tender history and performance data

### 3. Score Monitoring
- View real-time readiness score on dashboard
- Monitor profile completion percentage
- Recalculate scores after major updates

### 4. Data Export
- Export complete profile data as JSON
- Use for external analysis or backup

## Customization

### Scoring Weights
Modify scoring criteria in the `scoring_criteria` table:
```sql
UPDATE scoring_criteria 
SET weight_percentage = 30.00 
WHERE criteria_name = 'CIDB Grade';
```

### Additional Fields
Add new profile fields by:
1. Updating database schema
2. Modifying backend models
3. Updating frontend forms
4. Adjusting scoring algorithm

## Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: SHA-256 password hashing
- **Input Validation**: Both client and server-side validation
- **SQL Injection Protection**: SQLAlchemy ORM protection
- **CORS Configuration**: Controlled cross-origin access

## Future Enhancements

- **Document Upload**: Support for certificate file uploads
- **Notification System**: Email alerts for expiring certificates
- **Advanced Analytics**: Detailed scoring breakdowns and trends
- **Integration APIs**: Connect with external CIDB/BEE databases
- **Mobile App**: Native mobile application
- **Multi-language Support**: Support for multiple languages

## Support

For technical support or feature requests, please contact the development team.

## License

This project is proprietary software developed for SED Tender Insight Hub.

