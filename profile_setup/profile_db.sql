-- Profile Setup & Scoring Inputs Database Schema
-- For SED Tender Insight Hub - CIDB and BEE Compliance

-- Users table with profile and scoring fields
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    contact_person VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User profiles table for CIDB and BEE compliance data
CREATE TABLE user_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- CIDB (Construction Industry Development Board) Compliance
    cidb_grade INTEGER CHECK (cidb_grade >= 1 AND cidb_grade <= 9), -- CIDB grades 1-9
    cidb_category VARCHAR(50), -- e.g., 'General Building', 'Civil Engineering', 'Electrical Engineering'
    cidb_registration_number VARCHAR(50),
    cidb_expiry_date DATE,
    cidb_status VARCHAR(20) DEFAULT 'Active', -- Active, Suspended, Expired
    
    -- BEE (Broad-Based Black Economic Empowerment) Compliance
    bee_level INTEGER CHECK (bee_level >= 1 AND bee_level <= 8), -- BEE levels 1-8 (1 being highest)
    bee_score INTEGER CHECK (bee_score >= 0 AND bee_score <= 100), -- Overall BEE score
    bee_certificate_number VARCHAR(50),
    bee_certificate_issuer VARCHAR(100),
    bee_expiry_date DATE,
    bee_status VARCHAR(20) DEFAULT 'Valid', -- Valid, Expired, Pending
    
    -- Additional compliance fields
    tax_clearance_status BOOLEAN DEFAULT FALSE,
    tax_clearance_expiry DATE,
    vat_registration_number VARCHAR(20),
    company_registration_number VARCHAR(20),
    
    -- Scoring metadata
    last_scored_at TIMESTAMP,
    scoring_version VARCHAR(10) DEFAULT '1.0',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Scoring criteria table for different tender types
CREATE TABLE scoring_criteria (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tender_type VARCHAR(100) NOT NULL, -- e.g., 'Construction', 'Services', 'Goods'
    criteria_name VARCHAR(100) NOT NULL,
    criteria_type VARCHAR(50) NOT NULL, -- 'CIDB', 'BEE', 'Tax', 'General'
    weight DECIMAL(5,2) NOT NULL, -- Weight in percentage (0-100)
    min_value INTEGER,
    max_value INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User scoring history for analytics
CREATE TABLE user_scoring_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    profile_id UUID NOT NULL REFERENCES user_profiles(id) ON DELETE CASCADE,
    tender_type VARCHAR(100) NOT NULL,
    overall_score DECIMAL(5,2) NOT NULL,
    cidb_score DECIMAL(5,2),
    bee_score DECIMAL(5,2),
    tax_score DECIMAL(5,2),
    readiness_level VARCHAR(20), -- 'High', 'Medium', 'Low'
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX idx_user_profiles_cidb_grade ON user_profiles(cidb_grade);
CREATE INDEX idx_user_profiles_bee_level ON user_profiles(bee_level);
CREATE INDEX idx_scoring_history_user_id ON user_scoring_history(user_id);
CREATE INDEX idx_scoring_history_calculated_at ON user_scoring_history(calculated_at);

-- Insert default scoring criteria
INSERT INTO scoring_criteria (tender_type, criteria_name, criteria_type, weight, min_value, max_value) VALUES
('Construction', 'CIDB Grade', 'CIDB', 40.00, 1, 9),
('Construction', 'BEE Level', 'BEE', 30.00, 1, 8),
('Construction', 'Tax Clearance', 'Tax', 20.00, 0, 1),
('Construction', 'Company Registration', 'General', 10.00, 0, 1),
('Services', 'BEE Level', 'BEE', 50.00, 1, 8),
('Services', 'Tax Clearance', 'Tax', 30.00, 0, 1),
('Services', 'Company Registration', 'General', 20.00, 0, 1),
('Goods', 'BEE Level', 'BEE', 60.00, 1, 8),
('Goods', 'Tax Clearance', 'Tax', 25.00, 0, 1),
('Goods', 'Company Registration', 'General', 15.00, 0, 1);
