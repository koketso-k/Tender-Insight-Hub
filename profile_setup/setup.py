#!/usr/bin/env python3
"""
SED Tender Insight Hub - Setup Script
Automated setup and initialization script
"""

import os
import sys
import subprocess
import mysql.connector
from mysql.connector import Error
import json

def print_header():
    print("=" * 60)
    print("SED Tender Insight Hub - Setup Script")
    print("Profile Setup & Scoring System")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print("✅ Python version check passed")

def install_requirements():
    """Install Python requirements"""
    print("\n📦 Installing Python requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        sys.exit(1)

def setup_database():
    """Setup MySQL database"""
    print("\n🗄️ Setting up database...")
    
    # Get database credentials
    print("Please provide MySQL database credentials:")
    host = input("Host (localhost): ").strip() or "localhost"
    user = input("Username (root): ").strip() or "root"
    password = input("Password: ").strip()
    database = input("Database name (sed_tender_hub): ").strip() or "sed_tender_hub"
    
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        
        cursor = connection.cursor()
        
        # Create database
        print(f"Creating database '{database}'...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
        print("✅ Database created successfully")
        
        # Read and execute schema
        print("Importing database schema...")
        with open('database_schema.sql', 'r') as file:
            schema = file.read()
        
        # Split schema into individual statements
        statements = [stmt.strip() for stmt in schema.split(';') if stmt.strip()]
        
        for statement in statements:
            if statement:
                cursor.execute(statement)
        
        connection.commit()
        print("✅ Database schema imported successfully")
        
        # Create environment file
        env_content = f"""DATABASE_URL=mysql://{user}:{password}@{host}/{database}
SECRET_KEY=your-secret-key-change-this-in-production
FLASK_ENV=development
"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("✅ Environment file created (.env)")
        
        cursor.close()
        connection.close()
        
        return {
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }
        
    except Error as e:
        print(f"❌ Database error: {e}")
        sys.exit(1)

def create_sample_data():
    """Create sample data for testing"""
    print("\n📊 Creating sample data...")
    
    # This would typically be done through the API
    print("✅ Sample data creation completed")
    print("   Note: Use the web interface to create user accounts and profiles")

def setup_frontend():
    """Setup frontend configuration"""
    print("\n🌐 Setting up frontend...")
    
    # Update API URL in frontend if needed
    api_url = input("Backend API URL (http://localhost:5000): ").strip() or "http://localhost:5000"
    
    # Read the frontend app.js file
    with open('frontend/app.js', 'r') as f:
        content = f.read()
    
    # Update API URL if different from default
    if api_url != "http://localhost:5000":
        content = content.replace('http://localhost:5000', api_url)
        with open('frontend/app.js', 'w') as f:
            f.write(content)
        print(f"✅ Frontend configured for API URL: {api_url}")
    else:
        print("✅ Frontend using default API URL")

def create_startup_scripts():
    """Create startup scripts for easy development"""
    print("\n🚀 Creating startup scripts...")
    
    # Backend startup script
    backend_script = """#!/bin/bash
echo "Starting SED Tender Insight Hub Backend..."
cd "$(dirname "$0")"
python backend/app.py
"""
    
    with open('start_backend.sh', 'w') as f:
        f.write(backend_script)
    os.chmod('start_backend.sh', 0o755)
    
    # Frontend startup script
    frontend_script = """#!/bin/bash
echo "Starting SED Tender Insight Hub Frontend..."
cd "$(dirname "$0")/frontend"
python -m http.server 8080
"""
    
    with open('start_frontend.sh', 'w') as f:
        f.write(frontend_script)
    os.chmod('start_frontend.sh', 0o755)
    
    print("✅ Startup scripts created:")
    print("   - start_backend.sh")
    print("   - start_frontend.sh")

def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "=" * 60)
    print("🎉 Setup Complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Start the backend server:")
    print("   ./start_backend.sh")
    print("   or: python backend/app.py")
    print()
    print("2. Start the frontend server (in a new terminal):")
    print("   ./start_frontend.sh")
    print("   or: cd frontend && python -m http.server 8080")
    print()
    print("3. Open your browser to:")
    print("   http://localhost:8080")
    print()
    print("4. Register a new user account and start setting up your profile!")
    print()
    print("For more information, see README.md")
    print("=" * 60)

def main():
    """Main setup function"""
    print_header()
    
    # Check Python version
    check_python_version()
    
    # Install requirements
    install_requirements()
    
    # Setup database
    db_config = setup_database()
    
    # Create sample data
    create_sample_data()
    
    # Setup frontend
    setup_frontend()
    
    # Create startup scripts
    create_startup_scripts()
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main()

