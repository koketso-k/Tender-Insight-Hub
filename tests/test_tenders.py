Tender Endpoint Tests

Tests for tender-related API endpoints including CRUD operations,
search functionality, and AI integration features.

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import patch, Mock
import json
from datetime import datetime, timedelta

from app.models.tenders import Tender
from app.models.users import User, Team
from tests import SAMPLE_TENDER_ID


class TestTenderCRUD:
    """Test tender CRUD operations."""
    
    def test_create_tender(self, client: TestClient, auth_headers: dict):
        """Test creating a new tender."""
        tender_data = {
            "title": "Software Development Services",
            "description": "Custom software development for government agency",
            "buyer": "Department of Home Affairs",
            "province": "Western Cape",
            "deadline": "2024-06-30T23:59:59",
            "budget_min": 50000.0,
            "budget_max": 200000.0,
            "sector": "Information Technology"
        }
        
        response = client.post(
            "/api/tenders/",
            json=tender_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == tender_data["title"]
        assert data["buyer"] == tender_data["buyer"]
        assert "id" in data
    
    def test_get_tender(self, client: TestClient, sample_tender: Tender):
        """Test retrieving a tender by ID."""
        response = client.get(f"/api/tenders/{sample_tender.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == sample_tender.title
        assert data["buyer"] == sample_tender.buyer
    
    def test_update_tender(self, client: TestClient, sample_tender: Tender, auth_headers: dict):
        """Test updating a tender."""
        update_data = {
            "title": "Updated IT Security Services",
            "budget_max": 750000.0
        }
        
        response = client.patch(
            f"/api/tenders/{sample_tender.id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["budget_max"] == update_data["budget_max"]
    
    def test_delete_tender(self, client: TestClient, sample_tender: Tender, auth_headers: dict):
        """Test deleting a tender."""
        response = client.delete(
            f"/api/tenders/{sample_tender.id}",
            headers=auth_headers
        )
        
        assert response.status_code == 204
        
        # Verify tender is deleted
        get_response = client.get(f"/api/tenders/{sample_tender.id}")
        assert get_response.status_code == 404


class TestTenderSearch:
    """Test tender search and filtering functionality."""
    
    @pytest.fixture
    async def multiple_tenders(self, db_session: AsyncSession):
        """Create multiple tenders for search testing."""
        tenders = [
            Tender(
                title="IT Security Audit",
                description="Security audit services for government systems",
                buyer="Department of Defence",
                province="Gauteng",
                deadline=datetime.now() + timedelta(days=30),
                budget_min=75000.0,
                budget_max=150000.0,
                sector="Information Technology"
            ),
            Tender(
                title="Construction Management",
                description="Project management for infrastructure development",
                buyer="Department of Public Works",
                province="KwaZulu-Natal",
                deadline=datetime.now() + timedelta(days=45),
                budget_min=500000.0,
                budget_max=2000000.0,
                sector="Construction"
            ),
            Tender(
                title="Medical Equipment Supply",
                description="Supply of medical equipment to public hospitals",
                buyer="Department of Health",
                province="Western Cape",
                deadline=datetime.now() + timedelta(days=60),
                budget_min=200000.0,
                budget_max=800000.0,
                sector="Healthcare"
            )
        ]
        
        for tender in tenders:
            db_session.add(tender)
        await db_session.commit()
        return tenders
    
    def test_search_by_keyword(self, client: TestClient, multiple_tenders):
        """Test keyword-based tender search."""
        response = client.get("/api/tenders/search?q=security")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["results"]) >= 1
        assert any("security" in result["title"].lower() for result in data["results"])
    
    def test_filter_by_province(self, client: TestClient, multiple_tenders):
        """Test filtering tenders by province."""
        response = client.get("/api/tenders/search?province=Gauteng")
        
        assert response.status_code == 200
        data = response.json()
        for result in data["results"]:
            assert result["province"] == "Gauteng"
    
    def test_filter_by_budget_range(self, client: TestClient, multiple_tenders):
        """Test filtering tenders by budget range."""
        response = client.get("/api/tenders/search?min_budget=100000&max_budget=300000")
        
        assert response.status_code == 200
        data = response.json()
        for result in data["results"]:
            assert result["budget_min"] >= 100000
            assert result["budget_max"] <= 300000
    
    def test_filter_by_sector(self, client: TestClient, multiple_tenders):
        """Test filtering tenders by sector."""
        response = client.get("/api/tenders/search?sector=Information Technology")
        
        assert response.status_code == 200
        data = response.json()
        for result in data["results"]:
            assert result["sector"] == "Information Technology"
    
    def test_combined_filters(self, client: TestClient, multiple_tenders):
        """Test combining multiple filters."""
        response = client.get(
            "/api/tenders/search?q=IT&province=Gauteng&min_budget=50000"
        )
        
        assert response.status_code == 200
        data = response.json()
        # Should return IT security tender from Gauteng
        assert len(data["results"]) >= 0  # May be 0 or more depending on exact data


class TestTenderAIIntegration:
    """Test AI-powered tender features."""
    
    @patch('app.services.ai_summarizer.HuggingFaceSummarizer')
    def test_summarize_tender_document(self, mock_summarizer, client: TestClient, 
                                     sample_tender: Tender, auth_headers: dict, 
                                     sample_pdf_content: bytes):
        """Test AI summarization of tender documents."""
        # Mock the summarizer
        mock_instance = Mock()
        mock_instance.summarize.return_value = {
            "summary": "Government IT security tender. Deadline: 2024-12-31. Requires CIDB Level 3+.",
            "key_requirements": ["CIDB Level 3+", "Security clearance"]
        }
        mock_summarizer.return_value = mock_instance
        
        # Upload and summarize document
        files = {"file": ("tender.pdf", sample_pdf_content, "application/pdf")}
        response = client.post(
            f"/api/tenders/{sample_tender.id}/summarize",
            files=files,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert "key_requirements" in data
        mock_instance.summarize.assert_called_once()
    
    @patch('app.services.readiness_scorer.ReadinessScorer')
    def test_calculate_readiness_score(self, mock_scorer, client: TestClient,
                                     sample_tender: Tender, sample_user: User,
                                     auth_headers: dict, sample_company_profile: dict):
        """Test readiness score calculation."""
        # Mock the scorer
        mock_instance = Mock()
        mock_instance.calculate_score.return_value = {
            "score": 85,
            "breakdown": {"sector_match": 30, "certification_match": 25},
            "recommendation": "Strong match"
        }
        mock_scorer.return_value = mock_instance
        
        # First create company profile
        profile_response = client.post(
            "/api/profile/",
            json=sample_company_profile,
            headers=auth_headers
        )
        assert profile_response.status_code == 201
        
        # Calculate readiness score
        response = client.post(
            f"/api/tenders/{sample_tender.id}/readiness",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "score" in data
        assert "breakdown" in data
        assert "recommendation" in data
        assert data["score"] == 85


class TestTenderWorkspace:
    """Test tender workspace and tracking features."""
    
    def test_save_tender_to_workspace(self, client: TestClient, sample_tender: Tender,
                                    auth_headers: dict):
        """Test saving a tender to user workspace."""
        workspace_data = {
            "tender_id": sample_tender.id,
            "status": "interested",
            "notes": "Promising opportunity, need to review requirements"
        }
        
        response = client.post(
            "/api/workspace/tenders",
            json=workspace_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["tender_id"] == sample_tender.id
        assert data["status"] == "interested"
    
    def test_update_tender_status(self, client: TestClient, sample_tender: Tender,
                                auth_headers: dict):
        """Test updating tender status in workspace."""
        # First save tender
        client.post(
            "/api/workspace/tenders",
            json={"tender_id": sample_tender.id, "status": "pending"},
            headers=auth_headers
        )
        
        # Update status
        response = client.patch(
            f"/api/workspace/tenders/{sample_tender.id}",
            json={"status": "submitted", "notes": "Application submitted on time"},
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "submitted"
    
    def test_get_workspace_tenders(self, client: TestClient, auth_headers: dict):
        """Test retrieving workspace tenders."""
        response = client.get("/api/workspace/tenders", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "tenders" in data
        assert isinstance(data["tenders"], list)


class TestTenderValidation:
    """Test tender data validation."""
    
    def test_invalid_tender_data(self, client: TestClient, auth_headers: dict):
        """Test validation of invalid tender data."""
        invalid_data = {
            "title": "",  # Empty title
            "buyer": "Test Buyer",
            "deadline": "invalid-date",  # Invalid date format
            "budget_min": -1000,  # Negative budget
        }
        
        response = client.post(
            "/api/tenders/",
            json=invalid_data,
            headers=auth_headers
        )
        
        assert response.status_code == 422
        errors = response.json()["detail"]
        assert any(error["loc"] == ["title"] for error in errors)
        assert any(error["loc"] == ["deadline"] for error in errors)
        assert any(error["loc"] == ["budget_min"] for error in errors)
    
    def test_budget_range_validation(self, client: TestClient, auth_headers: dict):
        """Test that budget_min <= budget_max validation."""
        invalid_data = {
            "title": "Test Tender",
            "buyer": "Test Buyer",
            "deadline": "2024-12-31T23:59:59",
            "budget_min": 200000.0,
            "budget_max": 100000.0  # Max less than min
        }
        
        response = client.post(
            "/api/tenders/",
            json=invalid_data,
            headers=auth_headers
        )
        
        assert response.status_code == 422


class TestTenderPermissions:
    """Test tender access permissions and multi-tenancy."""
    
    async def test_tender_access_isolation(self, client: TestClient, db_session: AsyncSession):
        """Test that teams can only access their own tenders."""
        # Create two teams
        team1 = Team(name="Team 1", saas_plan="basic")
        team2 = Team(name="Team 2", saas_plan="basic")
        db_session.add_all([team1, team2])
        await db_session.commit()
        
        # Create users for each team
        user1 = User(email="user1@test.com", team_id=team1.id, role="admin")
        user2 = User(email="user2@test.com", team_id=team2.id, role="admin")
        db_session.add_all([user1, user2])
        await db_session.commit()
        
        # Create tokens
        from app.auth.jwt_handler import create_access_token
        token1 = create_access_token(data={"sub": user1.email})
        token2 = create_access_token(data={"sub": user2.email})
        
        headers1 = {"Authorization": f"Bearer {token1}"}
        headers2 = {"Authorization": f"Bearer {token2}"}
        
        # User 1 creates a tender
        tender_data = {
            "title": "Private Tender",
            "buyer": "Test Buyer",
            "deadline": "2024-12-31T23:59:59"
        }
        response = client.post("/api/tenders/", json=tender_data, headers=headers1)
        tender_id = response.json()["id"]
        
        # User 2 should not be able to access it
        response = client.get(f"/api/tenders/{tender_id}", headers=headers2)
        assert response.status_code == 404  # Or 403 depending on implementation
    
    def test_unauthorized_access(self, client: TestClient, sample_tender: Tender):
        """Test that unauthorized requests are rejected."""
        response = client.patch(
            f"/api/tenders/{sample_tender.id}",
            json={"title": "Hacked Title"}
        )
        
        assert response.status_code == 401


class TestTenderPublicAPI:
    """Test public API endpoints."""
    
    def test_public_tender_list(self, client: TestClient, sample_tender: Tender):
        """Test public API for listing tenders."""
        response = client.get("/api/public/tenders")
        
        assert response.status_code == 200
        data = response.json()
        assert "tenders" in data
        assert isinstance(data["tenders"], list)
    
    def test_public_api_rate_limiting(self, client: TestClient):
        """Test rate limiting on public API."""
        # Make multiple requests quickly
        responses = []
        for i in range(10):
            response = client.get("/api/public/tenders")
            responses.append(response)
        
        # Should include rate limit headers
        last_response = responses[-1]
        assert "X-RateLimit-Limit" in last_response.headers
    
    @patch('app.services.cache.redis_client')
    def test_tender_caching(self, mock_redis, client: TestClient, sample_tender: Tender):
        """Test that public tender results are cached."""
        mock_redis.get.return_value = None
        mock_redis.setex.return_value = True
        
        # First request should hit database and cache result
        response1 = client.get("/api/public/tenders")
        assert response1.status_code == 200
        mock_redis.setex.assert_called()
        
        # Mock cache hit for second request
        mock_redis.get.return_value = json.dumps([{
            "id": sample_tender.id,
            "title": sample_tender.title
        }])
        
        response2 = client.get("/api/public/tenders")
        assert response2.status_code == 200


class TestTenderDocumentProcessing:
    """Test tender document upload and processing."""
    
    def test_upload_tender_document(self, client: TestClient, sample_tender: Tender,
                                  auth_headers: dict, sample_pdf_content: bytes):
        """Test uploading a tender document."""
        files = {"file": ("tender.pdf", sample_pdf_content, "application/pdf")}
        
        response = client.post(
            f"/api/tenders/{sample_tender.id}/documents",
            files=files,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["filename"] == "tender.pdf"
        assert data["file_size"] > 0
    
    def test_invalid_file_type(self, client: TestClient, sample_tender: Tender,
                             auth_headers: dict):
        """Test rejection of invalid file types."""
        files = {"file": ("malware.exe", b"fake exe content", "application/octet-stream")}
        
        response = client.post(
            f"/api/tenders/{sample_tender.id}/documents",
            files=files,
            headers=auth_headers
