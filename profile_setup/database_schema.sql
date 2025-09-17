-- SED Tender Insight Hub - Profile Setup & Scoring Database Schema
-- This schema supports CIDB and BEE level scoring for South African tender compliance

CREATE DATABASE IF NOT EXISTS sed_tender_hub;
USE sed_tender_hub;

-- Users table with profile and scoring information
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    company_name VARCHAR(255),
    company_registration_number VARCHAR(50),
    phone_number VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- User profiles table for detailed scoring information
CREATE TABLE user_profiles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    
    -- CIDB (Construction Industry Development Board) Information
    cidb_grade INT CHECK (cidb_grade BETWEEN 1 AND 9), -- CIDB grades 1-9
    cidb_registration_number VARCHAR(50),
    cidb_expiry_date DATE,
    cidb_work_categories JSON, -- Store multiple work categories
    
    -- BEE (Broad-Based Black Economic Empowerment) Information
    bee_level INT CHECK (bee_level BETWEEN 1 AND 8), -- BEE levels 1-8
    bee_certificate_number VARCHAR(100),
    bee_expiry_date DATE,
    bee_ownership_percentage DECIMAL(5,2) CHECK (bee_ownership_percentage >= 0 AND bee_ownership_percentage <= 100),
    bee_management_control_percentage DECIMAL(5,2) CHECK (bee_management_control_percentage >= 0 AND bee_management_control_percentage <= 100),
    bee_skills_development_percentage DECIMAL(5,2) CHECK (bee_skills_development_percentage >= 0 AND bee_skills_development_percentage <= 100),
    bee_enterprise_development_percentage DECIMAL(5,2) CHECK (bee_enterprise_development_percentage >= 0 AND bee_enterprise_development_percentage <= 100),
    bee_socio_economic_development_percentage DECIMAL(5,2) CHECK (bee_socio_economic_development_percentage >= 0 AND bee_socio_economic_development_percentage <= 100),
    
    -- Additional scoring factors
    years_in_business INT DEFAULT 0,
    annual_turnover DECIMAL(15,2) DEFAULT 0,
    number_of_employees INT DEFAULT 0,
    previous_tender_wins INT DEFAULT 0,
    previous_tender_applications INT DEFAULT 0,
    
    -- Calculated readiness score (0-100)
    readiness_score INT DEFAULT 0 CHECK (readiness_score >= 0 AND readiness_score <= 100),
    
    -- Profile metadata
    profile_completion_percentage INT DEFAULT 0 CHECK (profile_completion_percentage >= 0 AND profile_completion_percentage <= 100),
    last_score_calculation TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_profile (user_id)
);

-- CIDB work categories reference table
CREATE TABLE cidb_work_categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    category_code VARCHAR(10) UNIQUE NOT NULL,
    category_name VARCHAR(255) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE
);

-- Insert CIDB work categories
INSERT INTO cidb_work_categories (category_code, category_name, description) VALUES
('GB', 'General Building', 'General building construction work'),
('CE', 'Civil Engineering', 'Civil engineering construction work'),
('ME', 'Mechanical Engineering', 'Mechanical engineering construction work'),
('EE', 'Electrical Engineering', 'Electrical engineering construction work'),
('RE', 'Refrigeration and Air Conditioning', 'Refrigeration and air conditioning work'),
('EL', 'Elevator Installation', 'Elevator installation and maintenance'),
('RO', 'Roads and Storm Water Drainage', 'Roads and storm water drainage construction'),
('WA', 'Water and Sanitation', 'Water and sanitation infrastructure work'),
('EN', 'Environmental', 'Environmental construction and remediation work'),
('OT', 'Other', 'Other specialized construction work');

-- Tender scoring criteria table
CREATE TABLE scoring_criteria (
    id INT PRIMARY KEY AUTO_INCREMENT,
    criteria_name VARCHAR(100) NOT NULL,
    criteria_type ENUM('CIDB', 'BEE', 'EXPERIENCE', 'FINANCIAL', 'OTHER') NOT NULL,
    weight_percentage DECIMAL(5,2) NOT NULL CHECK (weight_percentage >= 0 AND weight_percentage <= 100),
    max_score INT NOT NULL DEFAULT 100,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default scoring criteria
INSERT INTO scoring_criteria (criteria_name, criteria_type, weight_percentage, max_score, description) VALUES
('CIDB Grade', 'CIDB', 25.00, 100, 'Construction Industry Development Board grade (1-9)'),
('BEE Level', 'BEE', 20.00, 100, 'Broad-Based Black Economic Empowerment level (1-8)'),
('Years in Business', 'EXPERIENCE', 15.00, 100, 'Number of years the company has been in business'),
('Annual Turnover', 'FINANCIAL', 15.00, 100, 'Company annual turnover'),
('Previous Tender Success Rate', 'EXPERIENCE', 10.00, 100, 'Percentage of successful tender applications'),
('Profile Completeness', 'OTHER', 10.00, 100, 'Completeness of user profile information'),
('Company Size', 'OTHER', 5.00, 100, 'Number of employees');

-- User profile history for tracking changes
CREATE TABLE user_profile_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    profile_id INT NOT NULL,
    field_name VARCHAR(100) NOT NULL,
    old_value TEXT,
    new_value TEXT,
    changed_by INT, -- user_id of who made the change
    change_reason VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (profile_id) REFERENCES user_profiles(id) ON DELETE CASCADE,
    FOREIGN KEY (changed_by) REFERENCES users(id) ON DELETE SET NULL
);

-- Indexes for better performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX idx_user_profiles_cidb_grade ON user_profiles(cidb_grade);
CREATE INDEX idx_user_profiles_bee_level ON user_profiles(bee_level);
CREATE INDEX idx_user_profiles_readiness_score ON user_profiles(readiness_score);
CREATE INDEX idx_user_profile_history_user_id ON user_profile_history(user_id);
CREATE INDEX idx_user_profile_history_created_at ON user_profile_history(created_at);

