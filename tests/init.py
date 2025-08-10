Tender Insight Hub - Test Suite
===============================

Comprehensive test suite for the Tender Insight Hub SaaS platform.
Tests cover all core functionality including:
- Authentication & Authorization
- Tender CRUD operations
- AI summarization features
- Readiness scoring algorithms
- Public API endpoints
- Multi-tenant architecture
- SaaS plan enforcement

__version__ = "1.0.0"
__author__ = "NSED742 Development Team"

# Test configuration constants
TEST_DB_URL = "postgresql://test:test@localhost:5432/tender_hub_test"
TEST_MONGO_URL = "mongodb://localhost:27017/tender_hub_test"
TEST_REDIS_URL = "redis://localhost:6379/1"

# Test data constants
SAMPLE_TENDER_ID = "test_tender_123"
SAMPLE_USER_EMAIL = "test@example.com"
SAMPLE_TEAM_ID = "team_test_123"
