#!/usr/bin/env python3
"""
Simple test to check if servers are running
"""

import socket
import json

def test_port(host, port):
    """Test if a port is open"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def test_backend_api():
    """Test backend API with basic socket connection"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect(('localhost', 8000))
        
        # Send HTTP request
        request = "GET / HTTP/1.1\r\nHost: localhost:8000\r\n\r\n"
        sock.send(request.encode())
        
        # Receive response
        response = sock.recv(1024).decode()
        sock.close()
        
        if "HTTP/1.1" in response and "200" in response:
            return True, "Backend API is responding"
        else:
            return False, f"Backend API error: {response[:100]}"
    except Exception as e:
        return False, f"Backend API error: {e}"

if __name__ == "__main__":
    print("🚀 Testing Tender Insight Hub Servers...")
    print("=" * 50)
    
    # Test ports
    backend_port_open = test_port('localhost', 8000)
    frontend_port_open = test_port('localhost', 3000)
    
    print(f"Backend Port 8000: {'✅ Open' if backend_port_open else '❌ Closed'}")
    print(f"Frontend Port 3000: {'✅ Open' if frontend_port_open else '❌ Closed'}")
    
    # Test backend API
    if backend_port_open:
        api_ok, api_msg = test_backend_api()
        print(f"Backend API: {'✅ Working' if api_ok else '❌ Error'}")
        if not api_ok:
            print(f"  Error: {api_msg}")
    else:
        print("Backend API: ❌ Port not open")
    
    print("=" * 50)
    
    if backend_port_open and frontend_port_open:
        print("🎉 Both servers appear to be running!")
        print("🌐 Frontend: http://localhost:3000")
        print("🔧 Backend: http://localhost:8000")
        print("📚 API Docs: http://localhost:8000/docs")
        print("\nYou can now:")
        print("1. Open http://localhost:3000 in your browser")
        print("2. Register a new user account")
        print("3. Login and explore the dashboard")
    else:
        print("⚠️  Some servers are not running.")
        print("Please check that both servers are started.")
