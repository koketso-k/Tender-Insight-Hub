# Tender Insight Hub

A cloud-native SaaS platform designed to assist South African SMEs in navigating public procurement opportunities. Built with FastAPI backend and HTML/CSS frontend.

## 🚀 Features

- **JWT-based Authentication & RBAC**: Secure user authentication with role-based access control
- **User Registration & Login**: Complete authentication system
- **Team Management**: Create and manage teams with different pricing tiers
- **Company Profile Management**: Store and manage company information
- **Tender Search & Analysis**: Search and analyze public procurement opportunities
- **AI-powered Document Summarization**: Extract and summarize tender documents
- **Readiness Scoring**: Assess suitability for tenders based on company profile

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM for database operations
- **MySQL**: Primary database for structured data
- **JWT**: JSON Web Tokens for authentication
- **Pydantic**: Data validation and serialization

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with animations
- **JavaScript**: Frontend logic and API communication
- **Font Awesome**: Icons

## 📋 Prerequisites

- Python 3.8+
- MySQL 8.0+
- pip (Python package manager)

## 🔧 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd tender-hub-insight
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Setup

#### Option A: Using MySQL Command Line
```bash
mysql -u root -p < setup_database.sql
```

#### Option B: Using MySQL Workbench
1. Open MySQL Workbench
2. Execute the SQL commands from `setup_database.sql`
3. Create database `tender_hub` and all required tables

### 4. Configure Environment Variables
Create a `.env` file in the backend directory:
```env
SECRET_KEY=your-super-secret-key-change-this-in-production-12345
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/tender_hub
```

### 5. Start the Server
```bash
python run_server.py
```

The API will be available at `http://localhost:8000`

## 🌐 Frontend Setup

### Option A: Simple HTTP Server
```bash
cd frontend
python -m http.server 3000
```

### Option B: Using Node.js (if available)
```bash
cd frontend
npx serve -s . -l 3000
```

The frontend will be available at `http://localhost:3000`

## 📚 API Documentation

Once the server is running, you can access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 Authentication

The system uses JWT-based authentication with the following roles:

- **Admin**: Full access to all features
- **SME (Subject Matter Expert)**: Focused on reviewing and scoring tenders
- **Collaborator**: Limited to viewing/editing shared projects

### Default Admin User
- Email: `admin@tenderhub.com`
- Password: `admin123`

## 🏗️ Project Structure

```
tender-hub-insight/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # Authentication logic
│   ├── crud.py              # Database operations
│   └── config.py            # Configuration settings
├── frontend/
│   ├── index.html           # Login/Register page
│   ├── dashboard.html       # Main dashboard
│   ├── styles.css           # CSS styles
│   ├── script.js            # Login/Register logic
│   └── dashboard.js         # Dashboard logic
├── requirements.txt         # Python dependencies
├── setup_database.sql      # Database schema
├── run_server.py           # Server startup script
└── README.md               # This file
```

## 🔄 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user info

### Teams
- `POST /api/teams/create` - Create new team
- `GET /api/teams/my-teams` - Get user's teams

### Future Endpoints
- `GET /api/enriched-releases` - Get filtered tenders
- `GET /api/analytics/spend-by-buyer` - Government spending analytics
- `POST /api/summary/extract` - Extract document summary
- `POST /api/readiness/check` - Check tender readiness

## 🎨 Frontend Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern UI**: Clean, professional interface with animations
- **Form Validation**: Real-time validation and error handling
- **JWT Token Management**: Automatic token handling and refresh
- **Modal Dialogs**: Interactive forms for team creation and search

## 🚦 Usage

1. **Register**: Create a new account with your details
2. **Login**: Access your dashboard
3. **Create Team**: Set up your organization
4. **Search Tenders**: Find relevant opportunities
5. **Manage Profile**: Update company information

## 🔒 Security Features

- Password hashing with bcrypt
- JWT token authentication
- CORS protection
- Input validation and sanitization
- SQL injection prevention through ORM

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure MySQL is running
   - Check database credentials in config
   - Verify database exists

2. **Port Already in Use**
   - Change port in `run_server.py`
   - Kill existing processes on port 8000

3. **Frontend Not Loading**
   - Check if frontend server is running
   - Verify API URL in JavaScript files

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of a Software Engineering course assignment.

## 👥 Team

This project is developed as part of NSED742 - Software Engineering & Design course.

---

**Note**: This is a development version. For production deployment, ensure proper security configurations, environment variables, and database security measures are in place.
