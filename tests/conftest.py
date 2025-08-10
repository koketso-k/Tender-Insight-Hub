Pytest configuration and shared fixtures for Tender Insight Hub tests.

import pytest
import asyncio
from typing import AsyncGenerator, Generator
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient
import redis
from unittest.mock import Mock, AsyncMock

from app.main import app
from app.database import get_db, Base
from app.config import settings
from app.models.users import User, Team
from app.models.tenders import Tender
from app.auth.jwt_handler import create_access_token
from tests import TEST_DB_URL, TEST_MONGO_URL, TEST_REDIS_URL


# Database test engine
test_engine = create_async_engine(
    TEST_DB_URL,
    echo=True,
    future=True
)

TestSessionLocal = sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create a clean database session for each test."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with TestSessionLocal() as session:
        yield session
    
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
def client(db_session: AsyncSession) -> TestClient:
    """Create a test client with database dependency override."""
    def override_get_db():
        return db_session
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def mongo_client():
    """Create a test MongoDB client."""
    client = MongoClient(TEST_MONGO_URL)
    db = client.tender_hub_test
    yield db
    client.drop_database("tender_hub_test")
    client.close()


@pytest.fixture(scope="function")
def redis_client():
    """Create a test Redis client."""
    r = redis.Redis.from_url(TEST_REDIS_URL)
    r.flushdb()
    yield r
    r.flushdb()
    r.close()


@pytest.fixture
async def sample_team(db_session: AsyncSession) -> Team:
    """Create a sample team for testing."""
    team = Team(
        name="Test SME Company",
        saas_plan="basic",
        max_users=3
    )
    db_session.add(team)
    await db_session.commit()
    await db_session.refresh(team)
    return team


@pytest.fixture
async def sample_user(db_session: AsyncSession, sample_team: Team) -> User:
    """Create a sample user for testing."""
    user = User(
        email="test@example.com",
        hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "secret"
        team_id=sample_team.id,
        role="admin",
        is_active=True
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
async def sample_tender(db_session: AsyncSession) -> Tender:
    """Create a sample tender for testing."""
    tender = Tender(
        title="IT Security Services",
        description="Procurement of cybersecurity consulting services",
        buyer="Department of Defence",
        province="Gauteng",
        deadline="2024-12-31T23:59:59",
        budget_min=100000.0,
        budget_max=500000.0,
        sector="Information Technology",
        status="open"
    )
    db_session.add(tender)
    await db_session.commit()
    await db_session.refresh(tender)
    return tender


@pytest.fixture
def auth_headers(sample_user: User) -> dict:
    """Create authentication headers for API requests."""
    token = create_access_token(data={"sub": sample_user.email})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def mock_ai_summarizer():
    """Mock AI summarization service."""
    mock = Mock()
    mock.summarize.return_value = {
        "summary": "Test tender for IT security services. Deadline: 2024-12-31. Budget: R100k-500k. Requires CIDB Level 3+ certification.",
        "key_requirements": ["CIDB Level 3+", "Security clearance", "5+ years experience"],
        "deadline": "2024-12-31",
        "budget_range": "R100,000 - R500,000"
    }
    return mock


@pytest.fixture
def mock_readiness_scorer():
    """Mock readiness scoring service."""
    mock = Mock()
    mock.calculate_score.return_value = {
        "score": 85,
        "breakdown": {
            "sector_match": 30,
            "certification_match": 25,
            "geographic_match": 20,
            "experience_match": 10
        },
        "checklist": [
            {"criterion": "CIDB Level 3+", "matched": True},
            {"criterion": "Security clearance", "matched": False},
            {"criterion": "Geographic coverage", "matched": True}
        ],
        "recommendation": "Strong match - recommend proceeding with application"
    }
    return mock


@pytest.fixture
def sample_pdf_content():
    """Sample PDF content for document processing tests."""
    return b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Contents 4 0 R\n>>\nendobj\n4 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 12 Tf\n100 700 Td\n(Test tender document) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000204 00000 n \ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n297\n%%EOF"


@pytest.fixture
def sample_company_profile():
    """Sample company profile data for testing."""
    return {
        "sector": "Information Technology",
        "services": ["Cybersecurity", "Network Infrastructure", "Cloud Services"],
        "certifications": {
            "cidb": "Level 3",
            "bbbee": "Level 2",
            "iso27001": True
        },
        "coverage_areas": ["Gauteng", "Western Cape"],
        "experience_years": 8,
        "contact_info": {
            "address": "123 Business Park, Sandton, Johannesburg",
            "phone": "+27 11 123 4567",
            "website": "https://testsme.co.za"
        },
        "previous_contracts": 15,
        "annual_turnover": 2500000
    }


@pytest.fixture
def sample_tender_document():
    """Sample tender document metadata for testing."""
    return {
        "tender_id": "TND-2024-001",
        "title": "Cybersecurity Consulting Services",
        "description": "The Department of Defence requires comprehensive cybersecurity consulting services...",
        "buyer": "Department of Defence",
        "province": "Gauteng",
        "deadline": "2024-12-31T23:59:59",
        "budget_min": 100000.0,
        "budget_max": 500000.0,
        "requirements": [
            "CIDB Level 3 or higher",
            "Security clearance required",
            "Minimum 5 years experience",
            "ISO 27001 certification preferred"
        ],
        "documents": [
            {"name": "RFP_Security_Services.pdf", "size": 2048576},
            {"name": "Technical_Specifications.pdf", "size": 1024768}
        ]
    }


# Async test utilities
@pytest.fixture
def anyio_backend():
    """Configure anyio backend for async tests."""
    return "asyncio"


# Mock external API responses
@pytest.fixture
def mock_ocds_api_response():
    """Mock OCDS eTenders API response."""
    return {
        "releases": [
            {
                "id": "ZA-GOVT-2024-001",
                "title": "IT Infrastructure Upgrade",
                "description": "Upgrade of government IT infrastructure",
                "buyer": {"name": "Department of Communications"},
                "tender": {
                    "status": "active",
                    "datePublished": "2024-01-15T00:00:00Z",
                    "submissionMethod": ["written"],
                    "tenderPeriod": {
                        "endDate": "2024-03-15T23:59:59Z"
                    },
                    "value": {
                        "amount": 2500000,
                        "currency": "ZAR"
                    }
                }
            }
        ]
    }


# Performance test fixtures
@pytest.fixture
def load_test_data():
    """Generate test data for load testing."""
    return {
        "users": 100,
        "teams": 20,
        "tenders": 1000,
        "concurrent_requests": 50
    }


# Security test fixtures
@pytest.fixture
def malicious_payloads():
    """Common security test payloads."""
    return {
        "sql_injection": ["'; DROP TABLE users; --", "1' OR '1'='1"],
        "xss": ["<script>alert('xss')</script>", "javascript:alert('xss')"],
        "path_traversal": ["../../../etc/passwd", "..\\..\\..\\windows\\system32"],
        "large_payload": "A" * 10000
    }


# AI model test fixtures
@pytest.fixture
def mock_huggingface_pipeline():
    """Mock HuggingFace transformers pipeline."""
    mock = Mock()
    mock.return_value = [{
        "summary_text": "Mock AI summary of the tender document. Key requirements include certification and experience."
    }]
    return mock


# API rate limiting test fixtures
@pytest.fixture
def rate_limit_headers():
    """Headers for rate limiting tests."""
    return {
        "X-RateLimit-Limit": "100",
        "X-RateLimit-Remaining": "99",
        "X-RateLimit-Reset": "1640995200"
    }
