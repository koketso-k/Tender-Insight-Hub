# 🚀 SED Tender Insight Hub - Complete Running Guide

## 📖 **About This System**

The SED Tender Insight Hub is a comprehensive profile management system designed for South African tender compliance. It features CIDB (Construction Industry Development Board) and BEE (Broad-Based Black Economic Empowerment) scoring capabilities to help businesses assess their readiness for government tenders.

## 📋 **Prerequisites Checklist**

Before starting, ensure you have the following installed and ready:

- [ ] **Python 3.8 or higher** installed on your system
- [ ] **Internet connection** for downloading dependencies
- [ ] **Modern web browser** (Chrome, Firefox, Safari, or Edge)
- [ ] **Command line access** (PowerShell or Command Prompt)
- [ ] **Administrator privileges** (may be required for some installations)

### **Step 1: Verify Python Installation**

Open your command line tool and check if Python is installed:

**For Windows PowerShell:**
```powershell
python --version
```

**For Windows Command Prompt:**
```cmd
python --version
```

**Expected Output:**
```
Python 3.8.x
```
*or any version 3.8 or higher*

**❌ If Python is not installed:**
1. Go to [python.org](https://www.python.org/downloads/)
2. Download Python 3.8 or higher
3. Run the installer
4. **Important:** Check "Add Python to PATH" during installation
5. Restart your command line tool

---

## 📁 **Step 2: Locate and Navigate to Project Directory**

### **2.1 Find Your Project Folder**

The SED Tender Insight Hub system should be located in a folder containing these files:
- `backend/` (folder)
- `frontend/` (folder) 
- `requirements.txt`
- `database_schema.sql`
- `README.md`

**Common locations:**
- Desktop: `C:\Users\[YourUsername]\Desktop\SILAS PROFILE`
- Documents: `C:\Users\[YourUsername]\Documents\SILAS PROFILE`
- Downloads: `C:\Users\[YourUsername]\Downloads\SILAS PROFILE`

### **2.2 Navigate to the Project Directory**

**Open PowerShell or Command Prompt:**

**Option A: Using File Explorer**
1. Open File Explorer
2. Navigate to your project folder
3. Right-click in the folder
4. Select "Open PowerShell window here" or "Open in Terminal"

**Option B: Using Command Line**
```powershell
# Replace with your actual path
cd "C:\Users\YourUsername\Documents\SILAS PROFILE"
```

### **2.3 Verify You're in the Correct Directory**

Run this command to see the project files:
```powershell
dir
```

**Expected Output:**
```
Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----        [date]      [time]                backend
d-----        [date]      [time]                frontend
-a----        [date]      [time]            [size] requirements.txt
-a----        [date]      [time]            [size] database_schema.sql
-a----        [date]      [time]            [size] README.md
```

**✅ If you see these files, you're in the right place!**
**❌ If you don't see these files, navigate to the correct folder**

---

## 📦 **Step 3: Install Required Dependencies**

The system requires several Python packages to function. Install them using pip:

### **3.1 Install Dependencies**

```powershell
pip install -r requirements.txt
```

**Expected Output:**
```
Collecting Flask==2.3.3
  Downloading Flask-2.3.3-py3-none-any.whl (96 kB)
Collecting Flask-SQLAlchemy==3.0.5
  Downloading Flask_SQLAlchemy-3.0.5-py3-none-any.whl (24 kB)
...
Successfully installed Flask-2.3.3 Flask-CORS-4.0.0 Flask-SQLAlchemy-3.0.5 PyJWT-2.8.0 PyMySQL-1.1.0 Werkzeug-2.3.7 greenlet-3.2.4 itsdangerous-2.2.0 python-dotenv-1.0.0 sqlalchemy-2.0.43
```

### **3.2 Verify Installation**

Test that the packages are installed correctly:
```powershell
python -c "import flask; print('Flask installed successfully')"
```

**Expected Output:**
```
Flask installed successfully
```

**❌ If you get an error:**
- Make sure Python is installed correctly
- Try running: `python -m pip install --upgrade pip`
- Then run: `pip install -r requirements.txt` again

---

## 🗄️ **Step 4: Database Setup (Automatic)**

The system uses SQLite database which is automatically created when you first run the backend. No additional setup required!

**What happens automatically:**
- Database file (`sed_tender_hub.db`) is created
- All required tables are set up
- Sample data is loaded
- No manual configuration needed

*Note: The system has been configured to use SQLite instead of MySQL for easier setup and no external database server requirements.*

---

## 🔧 **Step 5: Start the Backend Server**

The backend server provides the API and database functionality for the system.

### **5.1 Open a New Command Line Window**

**Important:** You need to keep this window open while using the system.

**Option A: Using File Explorer**
1. Navigate to your project folder
2. Right-click in the folder
3. Select "Open PowerShell window here" or "Open in Terminal"

**Option B: Using Command Line**
```powershell
# Navigate to your project directory
cd "C:\Users\YourUsername\Documents\SILAS PROFILE"
```

### **5.2 Start the Backend Server**

```powershell
python backend/app.py
```

**Expected Output:**
```
* Serving Flask app 'app'
* Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:5000
* Running on http://10.245.160.57:5000
Press CTRL+C to quit
* Restarting with watchdog (windowsapi)
* Debugger is active!
* Debugger PIN: 294-074-670
```

**✅ Success Indicators:**
- You see "Running on http://127.0.0.1:5000"
- No error messages
- The window stays open and shows activity

**❌ If you see errors:**
- Make sure you're in the correct directory
- Verify Python dependencies are installed
- Check that port 5000 is not in use by another application

**⚠️ Important:** Keep this window open! Closing it will stop the backend server.

---

## 🌐 **Step 6: Start the Frontend Server**

The frontend server provides the web interface for the system.

### **6.1 Open Another New Command Line Window**

**Important:** You need TWO command line windows running simultaneously:
- Window 1: Backend server (from Step 5)
- Window 2: Frontend server (this step)

**Option A: Using File Explorer**
1. Navigate to your project folder
2. Right-click in the folder
3. Select "Open PowerShell window here" or "Open in Terminal"

**Option B: Using Command Line**
```powershell
# Navigate to your project directory
cd "C:\Users\YourUsername\Documents\SILAS PROFILE"
```

### **6.2 Navigate to Frontend Directory**

```powershell
cd frontend
```

### **6.3 Start the Frontend Server**

```powershell
python -m http.server 8080
```

**Expected Output:**
```
Serving HTTP on :: port 8080 (http://[::]:8080/) ...
```

**✅ Success Indicators:**
- You see "Serving HTTP on :: port 8080"
- No error messages
- The window stays open

**❌ If you see errors:**
- Make sure you're in the `frontend` directory
- Check that port 8080 is not in use by another application
- Verify Python is installed correctly

**⚠️ Important:** Keep this window open too! Closing it will stop the frontend server.

---

## 🧪 **Step 7: Verify System is Running**

Before using the system, let's verify that both servers are working correctly.

### **7.1 Test Backend API**

Open a **third** PowerShell window and test the backend:

```powershell
Invoke-WebRequest -Uri "http://localhost:5000/api/cidb/categories" -UseBasicParsing
```

**Expected Output:**
```
StatusCode        : 200
StatusDescription : OK
Content           : {"categories": []}
```

**✅ If you see StatusCode 200, your backend is working!**
**❌ If you get an error, check that the backend server is running in Window 1**

### **7.2 Test Frontend Interface**

Open your web browser and navigate to:
```
http://localhost:8080
```

**Expected Result:** You should see the SED Tender Insight Hub interface with:
- **Header:** "SED Tender Insight Hub" with navigation
- **Profile Overview:** Company information and completion status
- **Readiness Score:** Circular progress indicator showing 0/100
- **Tabbed Interface:** Four tabs (CIDB, BEE, Company, Experience)
- **Action Buttons:** "Recalculate Score" and "Export Profile"

**✅ If you see this interface, your frontend is working!**
**❌ If you see an error or blank page, check that the frontend server is running in Window 2**

### **7.3 Quick System Check**

You should now have:
- **Window 1:** Backend server running (showing Flask messages)
- **Window 2:** Frontend server running (showing HTTP server messages)
- **Browser:** SED Tender Insight Hub interface loaded

**If everything is working, you're ready to use the system!**

---

## 🎯 **Step 8: First-Time User Setup**

Now that the system is running, let's set up your first user account and profile.

### **8.1 Register a New User Account**

1. **Open your web browser** and go to `http://localhost:8080`
2. **You'll see a login prompt** - this is normal for first-time users
3. **Click "Register"** or enter credentials when prompted
4. **Fill in the registration form:**
   - **Email address:** Use a valid email (e.g., yourname@company.com)
   - **Password:** Choose a secure password
   - **First Name:** Your first name
   - **Last Name:** Your last name
   - **Company Name:** Your company name

5. **Click "Register"** to create your account

**✅ Success:** You should be automatically logged in and see the main interface

### **8.2 Complete Your Company Profile**

The system has four main sections to complete. Navigate through the tabs:

#### **🏗️ CIDB Information Tab**
Fill in your Construction Industry Development Board details:
- **CIDB Grade:** Select from dropdown (1-9, where 9 is highest)
- **CIDB Registration Number:** Your official CIDB registration number
- **CIDB Expiry Date:** When your CIDB registration expires
- **Work Categories:** Select all applicable categories:
  - General Building (GB)
  - Civil Engineering (CE)
  - Mechanical Engineering (ME)
  - Electrical Engineering (EE)
  - And others as applicable

#### **🤝 BEE Information Tab**
Complete your Broad-Based Black Economic Empowerment details:
- **BEE Level:** Select from dropdown (1-8, where 1 is best)
- **BEE Certificate Number:** Your official BEE certificate number
- **BEE Expiry Date:** When your BEE certificate expires
- **BEE Scorecard Elements:**
  - Ownership percentage (0-100%)
  - Management Control percentage (0-100%)
  - Skills Development percentage (0-100%)
  - Enterprise Development percentage (0-100%)
  - Socio-Economic Development percentage (0-100%)

#### **🏢 Company Information Tab**
Add your business details:
- **Company Name:** (Pre-filled from registration)
- **Company Registration Number:** Your official company registration
- **Phone Number:** Business contact number
- **Years in Business:** How long your company has been operating
- **Annual Turnover:** Your company's yearly revenue (in ZAR)
- **Number of Employees:** Total staff count

#### **📊 Experience & Performance Tab**
Enter your tender history:
- **Previous Tender Wins:** Number of successful tender applications
- **Previous Tender Applications:** Total number of tender applications
- **Success Rate:** Automatically calculated as (Wins ÷ Applications) × 100

### **8.3 Monitor Your Readiness Score**

As you complete each section:
- **Watch the circular progress indicator** update in real-time
- **Check the profile completion percentage** in the overview
- **See your readiness score** increase as you add more information
- **Use the "Recalculate Score" button** to refresh calculations

**The scoring system considers:**
- CIDB Grade (25% weight)
- BEE Level (20% weight)
- Years in Business (15% weight)
- Annual Turnover (15% weight)
- Tender Success Rate (10% weight)
- Profile Completeness (10% weight)
- Company Size (5% weight)

---

## 🔄 **Step 9: Daily Usage**

### **9.1 Starting the System Each Time**

Every time you want to use the system, you need to start both servers:

#### **Start Backend Server (Window 1):**
1. Open PowerShell or Command Prompt
2. Navigate to your project directory:
   ```powershell
   cd "C:\Users\YourUsername\Documents\SILAS PROFILE"
   ```
3. Start the backend:
   ```powershell
   python backend/app.py
   ```
4. Wait for "Running on http://127.0.0.1:5000" message
5. **Keep this window open**

#### **Start Frontend Server (Window 2):**
1. Open another PowerShell or Command Prompt
2. Navigate to your project directory:
   ```powershell
   cd "C:\Users\YourUsername\Documents\SILAS PROFILE"
   ```
3. Navigate to frontend folder:
   ```powershell
   cd frontend
   ```
4. Start the frontend:
   ```powershell
   python -m http.server 8080
   ```
5. Wait for "Serving HTTP on :: port 8080" message
6. **Keep this window open**

#### **Access the System:**
1. Open your web browser
2. Go to `http://localhost:8080`
3. Log in with your credentials

### **9.2 Stopping the System**

When you're done using the system:

1. **Stop Backend Server:** In Window 1, press `Ctrl+C`
2. **Stop Frontend Server:** In Window 2, press `Ctrl+C`
3. **Close Browser:** Close the browser tab
4. **Close Windows:** Close both command line windows

### **9.3 Quick Start Scripts (Optional)**

You can create batch files to make starting easier:

**Create `start_backend.bat`:**
```batch
@echo off
cd /d "C:\Users\YourUsername\Documents\SILAS PROFILE"
python backend/app.py
pause
```

**Create `start_frontend.bat`:**
```batch
@echo off
cd /d "C:\Users\YourUsername\Documents\SILAS PROFILE\frontend"
python -m http.server 8080
pause
```

Then just double-click these files to start the servers!

---

## 🛠️ **Troubleshooting Guide**

### **❌ "Module not found" errors**
**Solution:**
```powershell
pip install -r requirements.txt
```

### **❌ "Port already in use" errors**
**Solution:**
```powershell
# Find process using port 5000
netstat -ano | findstr :5000
# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F

# Find process using port 8080
netstat -ano | findstr :8080
# Kill the process
taskkill /PID <PID> /F
```

### **❌ Backend won't start**
**Check:**
1. Are you in the correct directory?
2. Did you install requirements?
3. Is another process using port 5000?

**Solution:**
```powershell
cd "C:\Users\thati\OneDrive\Documents\SILAS PROFILE"
python backend/app.py
```

### **❌ Frontend won't start**
**Check:**
1. Are you in the frontend directory?
2. Is another process using port 8080?

**Solution:**
```powershell
cd "C:\Users\thati\OneDrive\Documents\SILAS PROFILE\frontend"
python -m http.server 8080
```

### **❌ "Cannot connect to API" in browser**
**Check:**
1. Is backend running on port 5000?
2. Are there any error messages in backend terminal?

**Test backend:**
```powershell
Invoke-WebRequest -Uri "http://localhost:5000/api/cidb/categories" -UseBasicParsing
```

### **❌ Database errors**
**Solution:** The system uses SQLite which is automatically created. If you see database errors:
1. Delete `sed_tender_hub.db` file (if it exists)
2. Restart the backend server
3. The database will be recreated automatically

---

## 📊 **System Status Indicators**

### **✅ Backend Running Correctly:**
- Terminal shows: "Running on http://127.0.0.1:5000"
- No error messages
- API test returns StatusCode 200

### **✅ Frontend Running Correctly:**
- Terminal shows: "Serving HTTP on :: port 8080"
- Browser loads the interface
- No 404 errors in terminal

### **✅ System Working:**
- Can register/login users
- Can update profile information
- Scores calculate automatically
- Data saves successfully

---

## 🚀 **Quick Start Commands**

### **One-Line Setup (After First Time):**
```powershell
# Terminal 1 - Backend
cd "C:\Users\thati\OneDrive\Documents\SILAS PROFILE" && python backend/app.py

# Terminal 2 - Frontend  
cd "C:\Users\thati\OneDrive\Documents\SILAS PROFILE\frontend" && python -m http.server 8080
```

### **Test Commands:**
```powershell
# Test backend
Invoke-WebRequest -Uri "http://localhost:5000/api/cidb/categories" -UseBasicParsing

# Test frontend
Invoke-WebRequest -Uri "http://localhost:8080" -UseBasicParsing
```

---

## 📱 **Access Points**

- **Main Application:** `http://localhost:8080`
- **Backend API:** `http://localhost:5000`
- **API Documentation:** `http://localhost:5000/api/cidb/categories`

---

## 🎯 **Success Checklist**

- [ ] Backend server running on port 5000
- [ ] Frontend server running on port 8080
- [ ] Browser loads the application
- [ ] Can register a new user
- [ ] Can update profile information
- [ ] Scores calculate automatically
- [ ] Data persists between sessions

---

## 📞 **Getting Additional Help**

### **Self-Diagnosis Steps**

1. **Check System Status:**
   - Are both servers running? (Two command windows active)
   - Can you access `http://localhost:8080` in your browser?
   - Are there any error messages in the terminal windows?

2. **Verify Prerequisites:**
   - Is Python 3.8+ installed? (`python --version`)
   - Are all dependencies installed? (`pip list`)
   - Are you in the correct directory? (`dir` should show backend/ and frontend/)

3. **Test Individual Components:**
   - Backend: `Invoke-WebRequest -Uri "http://localhost:5000/api/cidb/categories" -UseBasicParsing`
   - Frontend: Open `http://localhost:8080` in browser

### **Common Solutions**

- **Restart everything:** Close all windows, restart both servers
- **Check ports:** Make sure 5000 and 8080 are not in use
- **Reinstall dependencies:** `pip install -r requirements.txt`
- **Clear browser cache:** Refresh page or try different browser
- **Run as administrator:** Right-click PowerShell → "Run as administrator"

### **When to Seek Help**

Contact technical support if you experience:
- Persistent "Module not found" errors after reinstalling
- Database corruption or data loss
- System crashes or freezes
- Security or authentication issues
- Performance problems with large datasets

---

## 🎉 **Congratulations!**

Once both servers are running and you can access `http://localhost:8080`, you're ready to use the SED Tender Insight Hub system for managing your tender compliance profiles!

### **Quick Reference Card**

**Start System:**
1. Window 1: `python backend/app.py`
2. Window 2: `cd frontend && python -m http.server 8080`
3. Browser: `http://localhost:8080`

**Stop System:**
1. Press `Ctrl+C` in both windows
2. Close browser tab

**Important Reminders:**
- Keep both terminal windows open while using the system
- Save your work regularly
- Export your profile data for backup
- Update your information as your business grows

**Happy Tender Management!** 🚀

