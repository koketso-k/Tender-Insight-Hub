# Setup Guide – Tender Insight Hub

## 1. Introduction  
This guide walks you through setting up the Tender Insight Hub project locally for development and testing. It covers prerequisites, installation, configuration, and running the system components.

## 2. Prerequisites

Before starting, ensure your development environment meets the following:

- **Python 3.10+** (recommend Python 3.11)  
- **Node.js 18+** and **npm/yarn** (for frontend)  
- **PostgreSQL 15+** (or compatible version)  
- **MongoDB 6.0+** or **Redis 7+**  
- **Git 2.30+** for version control  
- **Docker & Docker Compose** (optional but recommended for containerized environment)  
- A code editor like **VS Code** with Python and Markdown extensions  


## 3. Clone the Repository

```bash
git clone https://github.com/tender-insight-hub/tender-insight-hub.git
cd tender-insight-hub

**4. Backend Setup
4.1 Create Virtual Environment
python -m venv venv
Activate it:
.\venv\Scripts\Activate.ps1

4.2 Install Dependencies
pip install -r requirements.txt

4.3 Environment Variables
Create a .env file at the project root with the following variables:

DATABASE_URL=postgresql://<user>:<password>@localhost:5432/tenderhub
NOSQL_URI=mongodb://localhost:27017
SECRET_KEY=your-secure-random-string
JWT_ALGORITHM=HS256

4.4 Database Setup
Make sure PostgreSQL and MongoDB/Redis are running.

Run migrations:
alembic upgrade head

Seed the database if applicable:
python scripts/seed_data.py

4.5 Start Backend Server
uvicorn app.main:app --reload

5. Frontend Setup
Navigate to the frontend directory:
cd frontend

Install dependencies:
npm install

Start development server:
npm run dev

6. Using Docker (Optional)
Docker Compose can spin up backend, frontend, PostgreSQL, and MongoDB/Redis together.
docker-compose up --build

7. Troubleshooting Tips
Python version errors: Check Python version with python --version.
Database connection failures: Verify services are running and .env variables are correct.
Port conflicts: Make sure ports 8000, 3000, 5432, and 27017 are free.
Dependency issues: Try reinstalling with pip install --upgrade -r requirements.txt.

8. Additional Resources
FastAPI Documentation
PostgreSQL Official Site
MongoDB Manual
React Documentation
Docker Documentation

End of Setup Guide.
