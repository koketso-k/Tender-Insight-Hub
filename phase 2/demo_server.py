#!/usr/bin/env python3
"""
Tender Insight Hub - Demo Server with Enhanced Output
This version shows detailed execution output for demonstration
"""

import http.server
import socketserver
import json
import urllib.parse
import hashlib
import secrets
from datetime import datetime
import threading
import time
import os

# Simple in-memory storage
users_db = {}
tokens_db = {}

# Simple password hashing
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password

# Simple token generation
def create_token(user_email: str) -> str:
    token = secrets.token_urlsafe(32)
    tokens_db[token] = {
        "email": user_email,
        "created_at": datetime.now()
    }
    return token

def verify_token(token: str) -> str:
    if token in tokens_db:
        return tokens_db[token]["email"]
    return None

class APIHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        """Enhanced logging with timestamps"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {format % args}")

    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] CORS preflight request handled")

    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "message": "Tender Insight Hub API - Demo Version",
                "status": "running",
                "timestamp": datetime.now().isoformat(),
                "endpoints": {
                    "register": "/api/auth/register",
                    "login": "/api/auth/login",
                    "me": "/api/auth/me",
                    "create_team": "/api/teams/create"
                }
            }
            self.wfile.write(json.dumps(response).encode())
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ API Root accessed - Status: 200")
            
        elif self.path == '/api/auth/me':
            # Get current user info
            auth_header = self.headers.get('Authorization', '')
            if not auth_header.startswith('Bearer '):
                self.send_error(401, "Token required")
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Unauthorized access attempt to /api/auth/me")
                return
                
            token = auth_header[7:]  # Remove 'Bearer ' prefix
            user_email = verify_token(token)
            
            if not user_email or user_email not in users_db:
                self.send_error(401, "Invalid token")
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Invalid token for user info request")
                return
                
            user = users_db[user_email]
            response = {
                "id": user["id"],
                "email": user["email"],
                "full_name": user["full_name"],
                "role": user["role"],
                "created_at": user["created_at"].isoformat()
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ User info retrieved for: {user['email']}")
            
        else:
            self.send_error(404, "Not Found")
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ 404 - Path not found: {self.path}")

    def do_POST(self):
        """Handle POST requests"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Invalid JSON received")
            return

        if self.path == '/api/auth/register':
            # Register new user
            email = data.get('email')
            full_name = data.get('full_name')
            password = data.get('password')
            role = data.get('role', 'collaborator')
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 📝 Registration attempt for: {email}")
            
            if not email or not full_name or not password:
                self.send_error(400, "Missing required fields")
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Registration failed - Missing fields")
                return
                
            if email in users_db:
                self.send_error(400, "Email already registered")
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Registration failed - Email already exists: {email}")
                return
                
            user_id = len(users_db) + 1
            hashed_password = hash_password(password)
            
            users_db[email] = {
                "id": user_id,
                "email": email,
                "full_name": full_name,
                "role": role,
                "hashed_password": hashed_password,
                "created_at": datetime.now()
            }
            
            response = {
                "id": user_id,
                "email": email,
                "full_name": full_name,
                "role": role,
                "created_at": datetime.now().isoformat()
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ User registered successfully: {full_name} ({email}) - Role: {role}")
            
        elif self.path == '/api/auth/login':
            # Login user
            email = data.get('email')
            password = data.get('password')
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔐 Login attempt for: {email}")
            
            if not email or not password:
                self.send_error(400, "Missing email or password")
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Login failed - Missing credentials")
                return
                
            if email not in users_db:
                self.send_error(401, "Invalid email or password")
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Login failed - User not found: {email}")
                return
                
            user = users_db[email]
            if not verify_password(password, user["hashed_password"]):
                self.send_error(401, "Invalid email or password")
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Login failed - Invalid password for: {email}")
                return
                
            token = create_token(email)
            response = {
                "access_token": token,
                "token_type": "bearer"
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Login successful: {user['full_name']} ({email}) - Token generated")
            
        elif self.path == '/api/teams/create':
            # Create team
            auth_header = self.headers.get('Authorization', '')
            if not auth_header.startswith('Bearer '):
                self.send_error(401, "Token required")
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Team creation failed - No token provided")
                return
                
            token = auth_header[7:]
            user_email = verify_token(token)
            
            if not user_email or user_email not in users_db:
                self.send_error(401, "Invalid token")
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Team creation failed - Invalid token")
                return
                
            user = users_db[user_email]
            team_name = data.get('name')
            description = data.get('description', '')
            plan = data.get('plan', 'free')
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 👥 Team creation attempt by: {user['full_name']} - Team: {team_name}")
            
            if not team_name:
                self.send_error(400, "Team name required")
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Team creation failed - No team name provided")
                return
                
            team_id = len(users_db) + 1000  # Simple ID generation
            
            response = {
                "id": team_id,
                "name": team_name,
                "description": description,
                "plan": plan,
                "created_at": datetime.now().isoformat(),
                "created_by": user["full_name"]
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Team created successfully: {team_name} by {user['full_name']} - Plan: {plan}")
            
        else:
            self.send_error(404, "Not Found")
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ 404 - API endpoint not found: {self.path}")

def start_backend_server():
    """Start the backend server with enhanced logging"""
    PORT = 8000
    try:
        with socketserver.TCPServer(("", PORT), APIHandler) as httpd:
            print(f"🚀 Backend server started on http://localhost:{PORT}")
            print(f"📡 API endpoints ready:")
            print(f"   🔧 Register: POST /api/auth/register")
            print(f"   🔐 Login: POST /api/auth/login")
            print(f"   👤 User Info: GET /api/auth/me")
            print(f"   👥 Create Team: POST /api/teams/create")
            print(f"📊 Waiting for requests...")
            print("=" * 60)
            httpd.serve_forever()
    except Exception as e:
        print(f"❌ Backend server error: {e}")

def start_frontend_server():
    """Start the frontend server with enhanced logging"""
    PORT = 3000
    try:
        # Change to frontend directory
        original_dir = os.getcwd()
        frontend_dir = os.path.join(original_dir, 'frontend')
        
        if os.path.exists(frontend_dir):
            os.chdir(frontend_dir)
            print(f"📁 Changed to frontend directory: {frontend_dir}")
        else:
            print(f"⚠️  Frontend directory not found: {frontend_dir}")
        
        with socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
            print(f"🌐 Frontend server started on http://localhost:{PORT}")
            print(f"📱 Open your browser and go to: http://localhost:{PORT}")
            print(f"📊 Serving files from: {os.getcwd()}")
            print("=" * 60)
            httpd.serve_forever()
    except Exception as e:
        print(f"❌ Frontend server error: {e}")
    finally:
        # Change back to original directory
        os.chdir(original_dir)

if __name__ == "__main__":
    print("🚀 Tender Insight Hub - Demo Server Starting...")
    print("=" * 60)
    print(f"⏰ Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Start backend server in a separate thread
    print("🔄 Starting backend server...")
    backend_thread = threading.Thread(target=start_backend_server)
    backend_thread.daemon = True
    backend_thread.start()
    
    # Wait a moment for backend to start
    print("⏳ Waiting for backend to initialize...")
    time.sleep(3)
    
    # Start frontend server
    print("🔄 Starting frontend server...")
    start_frontend_server()
