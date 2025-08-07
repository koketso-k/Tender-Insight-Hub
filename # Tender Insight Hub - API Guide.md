# Tender Insight Hub - API Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Authentication](#authentication)
3. [Rate Limiting & Usage](#rate-limiting--usage)
4. [Core Endpoints](#core-endpoints)
5. [Search & Discovery](#search--discovery)
6. [Document Analysis](#document-analysis)
7. [Company Management](#company-management)
8. [Workspace Operations](#workspace-operations)
9. [Premium Features](#premium-features)
10. [Webhooks](#webhooks)
11. [Error Handling](#error-handling)
12. [SDK Examples](#sdk-examples)

---

## Getting Started

### Base URL
```
Production: https://api.tenderinsighthub.co.za/v1
Staging: https://api-staging.tenderinsighthub.co.za/v1
```

### API Versioning
The API uses URL versioning. Current version is `v1`. All endpoints are prefixed with `/v1/`.

### Content Type
All API requests and responses use JSON format:
```
Content-Type: application/json
Accept: application/json
```

### Quick Start Example
```bash
# Get your API key from the dashboard
curl -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     https://api.tenderinsighthub.co.za/v1/tenders/search?q=construction
```

---

## Authentication

### API Key Authentication
All API requests require authentication via API key in the Authorization header:

```http
Authorization: Bearer YOUR_API_KEY
```

### Obtaining API Keys
1. Log into your Tender Insight Hub dashboard
2. Navigate to **Settings > API Access**
3. Click **"Generate New API Key"**
4. Copy and securely store your key
5. Set key permissions and expiration (optional)

### Key Management
```bash
# Test your API key
curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://api.tenderinsighthub.co.za/v1/auth/verify

# Response
{
  "valid": true,
  "team_id": "team_12345",
  "permissions": ["read:tenders", "write:profiles"],
  "expires_at": "2025-12-31T23:59:59Z"
}
```

### Multi-Tenant Isolation
API keys are automatically scoped to your team. All operations are isolated to your team's data.

---

## Rate Limiting & Usage

### Rate Limits
- **Free Tier**: 100 requests/hour
- **Pro Tier**: 1,000 requests/hour  
- **Enterprise Tier**: 10,000 requests/hour

### Rate Limit Headers
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
X-RateLimit-Window: 3600
```

### Handling Rate Limits
```python
import requests
import time

def api_request_with_retry(url, headers, max_retries=3):
    for attempt in range(max_retries):
        response = requests.get(url, headers=headers)
        
        if response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 60))
            time.sleep(retry_after)
            continue
            
        return response
    
    raise Exception("Max retries exceeded")
```

---

## Core Endpoints

### Health Check
Check API availability and response time:

```bash
GET /health
```

```json
{
  "status": "healthy",
  "timestamp": "2025-08-01T10:30:00Z",
  "version": "1.0.0",
  "response_time_ms": 45
}
```

### Team Information
Get current team details:

```bash
GET /team
```

```json
{
  "team_id": "team_12345",
  "name": "ABC Construction Ltd",
  "plan": "pro",
  "created_at": "2025-01-15T09:00:00Z",
  "member_count": 5,
  "api_usage": {
    "current_period": 245,
    "limit": 1000,
    "reset_at": "2025-08-02T00:00:00Z"
  }
}
```

---

## Search & Discovery

### Basic Tender Search
Search for tenders using keywords and filters:

```bash
GET /tenders/search?q=construction&province=gauteng&limit=10
```

**Parameters:**
- `q` (string): Search query keywords
- `province` (string): Province filter
- `buyer` (string): Buyer organization filter
- `budget_min` (integer): Minimum budget
- `budget_max` (integer): Maximum budget
- `deadline_days` (integer): Closing within X days
- `limit` (integer): Results per page (max 100)
- `offset` (integer): Pagination offset

**Response:**
```json
{
  "results": [
    {
      "tender_id": "TND-2025-001234",
      "title": "Road Construction Project - N1 Highway",
      "description": "Construction and maintenance of highway infrastructure...",
      "buyer": {
        "name": "Gauteng Department of Roads and Transport",
        "contact": "procurement@gdrt.gov.za"
      },
      "budget": {
        "estimated_value": 15000000,
        "currency": "ZAR"
      },
      "dates": {
        "published": "2025-07-15T00:00:00Z",
        "briefing": "2025-08-05T14:00:00Z",
        "closing": "2025-08-20T17:00:00Z"
      },
      "location": {
        "province": "Gauteng",
        "municipality": "City of Johannesburg"
      },
      "readiness_score": 85,
      "status": "open"
    }
  ],
  "pagination": {
    "total": 156,
    "limit": 10,
    "offset": 0,
    "has_more": true
  },
  "filters_applied": {
    "q": "construction",
    "province": "gauteng"
  }
}
```

### Advanced Search with Scoring
Get tenders with readiness scores based on your company profile:

```bash
POST /tenders/search/scored
```

```json
{
  "query": "road construction",
  "filters": {
    "province": ["gauteng", "western_cape"],
    "budget_range": {
      "min": 1000000,
      "max": 50000000
    },
    "deadline_days": 30
  },
  "scoring": {
    "min_score": 60,
    "include_explanation": true
  },
  "pagination": {
    "limit": 20,
    "offset": 0
  }
}
```

**Response includes detailed scoring:**
```json
{
  "results": [
    {
      "tender_id": "TND-2025-001234",
      "title": "Road Construction Project",
      "readiness_score": 85,
      "score_breakdown": {
        "technical_fit": 90,
        "experience_match": 85,
        "compliance_status": 80,
        "capacity_assessment": 85
      },
      "recommendations": [
        "Strong technical alignment with your road construction experience",
        "Budget size matches your typical project range",
        "Consider partnering for specialized equipment requirements"
      ]
    }
  ]
}
```

### Saved Searches
Create and manage saved search queries:

```bash
# Create saved search
POST /searches
{
  "name": "Road Construction - Gauteng",
  "query": "road construction",
  "filters": {
    "province": "gauteng",
    "budget_min": 5000000
  },
  "notifications": true
}

# Get saved searches
GET /searches

# Execute saved search
GET /searches/{search_id}/execute
```

---

## Document Analysis

### Upload and Analyze Documents
Upload tender documents for AI analysis:

```bash
POST /documents/analyze
Content-Type: multipart/form-data
```

**Python Example:**
```python
import requests

url = "https://api.tenderinsighthub.co.za/v1/documents/analyze"
headers = {"Authorization": "Bearer YOUR_API_KEY"}

files = {
    'document': ('tender_spec.pdf', open('tender_spec.pdf', 'rb'), 'application/pdf')
}
data = {
    'tender_id': 'TND-2025-001234',
    'generate_summary': True,
    'extract_requirements': True
}

response = requests.post(url, headers=headers, files=files, data=data)
```

**Response:**
```json
{
  "document_id": "doc_67890",
  "analysis": {
    "summary": {
      "text": "This tender involves the construction of a 15km highway section including bridges, drainage systems, and safety barriers. The project requires CIDB Grade 7 certification and previous experience with similar highway projects. Key deliverables include detailed engineering drawings, quality assurance plans, and environmental compliance certificates.",
      "confidence": 0.92,
      "key_points": [
        "15km highway construction",
        "CIDB Grade 7 required",
        "Environmental compliance mandatory",
        "24-month project duration"
      ]
    },
    "requirements": [
      {
        "category": "certification",
        "requirement": "CIDB Grade 7 CE certification",
        "mandatory": true
      },
      {
        "category": "experience",
        "requirement": "Minimum 3 similar highway projects",
        "mandatory": true
      }
    ],
    "extracted_data": {
      "project_value": 25000000,
      "duration_months": 24,
      "start_date": "2025-10-01",
      "key_dates": [
        {
          "event": "Site handover",
          "date": "2025-10-15"
        }
      ]
    }
  },
  "processing_time_ms": 3420
}
```

### Document Status and Results
Check analysis status for large documents:

```bash
# Check processing status
GET /documents/{document_id}/status

{
  "document_id": "doc_67890",
  "status": "completed",
  "progress": 100,
  "estimated_completion": null,
  "results_available": true
}

# Get analysis results
GET /documents/{document_id}/analysis
```

### Batch Document Processing
Process multiple documents simultaneously:

```bash
POST /documents/batch-analyze
```

```json
{
  "documents": [
    {
      "name": "technical_specs.pdf",
      "url": "https://example.com/doc1.pdf"
    },
    {
      "name": "commercial_terms.pdf", 
      "url": "https://example.com/doc2.pdf"
    }
  ],
  "tender_id": "TND-2025-001234",
  "callback_url": "https://your-app.com/webhook/analysis-complete"
}
```

---

## Company Management

### Company Profile Operations
Manage your company profile programmatically:

```bash
# Get current profile
GET /company/profile

# Update profile
PUT /company/profile
{
  "basic_info": {
    "name": "ABC Construction Ltd",
    "registration_number": "2020/123456/07",
    "tax_number": "4001234567",
    "contact": {
      "email": "info@abcconstruction.co.za",
      "phone": "+27118884444",
      "address": {
        "street": "123 Builder Street",
        "city": "Johannesburg",
        "province": "Gauteng",
        "postal_code": "2000"
      }
    }
  },
  "business_details": {
    "primary_sector": "construction",
    "secondary_sectors": ["civil_engineering", "project_management"],
    "services": [
      "Road construction",
      "Bridge construction", 
      "Highway maintenance"
    ],
    "capabilities": [
      "Heavy machinery operation",
      "Environmental compliance",
      "Safety management"
    ]
  },
  "certifications": [
    {
      "name": "CIDB Grade 7 CE",
      "number": "CIDB123456",
      "issued_date": "2023-01-15",
      "expiry_date": "2026-01-15",
      "issuer": "Construction Industry Development Board"
    }
  ],
  "experience": [
    {
      "project_name": "N3 Highway Upgrade",
      "client": "SANRAL",
      "value": 18000000,
      "start_date": "2023-03-01",
      "end_date": "2024-08-30",
      "description": "15km highway upgrade including new bridges"
    }
  ],
  "financial_info": {
    "annual_turnover_range": "10M-50M",
    "working_capital": 5000000,
    "bank_references": ["Standard Bank", "FNB"]
  }
}
```

### Profile Validation
Validate profile completeness for better scoring:

```bash
GET /company/profile/validation

{
  "overall_score": 85,
  "completeness": {
    "basic_info": 100,
    "business_details": 90,
    "certifications": 80,
    "experience": 85,
    "financial_info": 70
  },
  "recommendations": [
    "Add more recent project experience",
    "Upload certificate documents for verification",
    "Include more detailed service descriptions"
  ],
  "missing_fields": [
    "certifications[0].document_url",
    "financial_info.audited_statements"
  ]
}
```

---

## Workspace Operations

### Tender Management
Manage saved tenders in your workspace:

```bash
# Save tender to workspace
POST /workspace/tenders
{
  "tender_id": "TND-2025-001234",
  "status": "interested",
  "priority": "high",
  "notes": "Good fit for our highway experience",
  "assigned_to": "user_456",
  "tags": ["highway", "gauteng", "high-value"]
}

# Get workspace tenders
GET /workspace/tenders?status=interested&limit=20

# Update tender status
PATCH /workspace/tenders/{tender_id}
{
  "status": "submitted",
  "notes": "Bid submitted on 2025-08-01",
  "submission_details": {
    "bid_amount": 24500000,
    "submission_method": "online",
    "reference_number": "BID-2025-ABC-001"
  }
}
```

### Team Collaboration
Manage team activities and assignments:

```bash
# Get team activity
GET /workspace/activity?days=7

{
  "activities": [
    {
      "id": "act_789",
      "user": "John Smith",
      "action": "saved_tender",
      "tender_id": "TND-2025-001234",
      "timestamp": "2025-08-01T14:30:00Z",
      "details": "Added to interested list with high priority"
    }
  ]
}

# Assign tender to team member
POST /workspace/assignments
{
  "tender_id": "TND-2025-001234",
  "assigned_to": "user_456",
  "due_date": "2025-08-15T17:00:00Z",
  "task": "Prepare technical proposal",
  "notes": "Focus on highway experience and CIDB compliance"
}
```

### Workspace Analytics
Get insights into workspace usage:

```bash
GET /workspace/analytics?period=30days

{
  "summary": {
    "tenders_saved": 45,
    "tenders_submitted": 8,
    "avg_readiness_score": 72,
    "team_activity_score": 85
  },
  "status_breakdown": {
    "interested": 18,
    "pending": 12,
    "not_eligible": 7,
    "submitted": 8
  },
  "top_sectors": [
    {"sector": "construction", "count": 23},
    {"sector": "civil_engineering", "count": 15}
  ]
}
```

---

## Premium Features

### Advanced Analytics
Access detailed market insights (Pro/Enterprise only):

```bash
# Government spending analysis
GET /analytics/spending?buyer=gdrt&period=12months

{
  "total_spend": 2500000000,
  "tender_count": 156,
  "average_value": 16025641,
  "spending_by_month": [
    {"month": "2024-08", "amount": 180000000, "tenders": 12},
    {"month": "2024-09", "amount": 220000000, "tenders": 15}
  ],
  "top_categories": [
    {"category": "road_construction", "amount": 800000000},
    {"category": "building_construction", "amount": 650000000}
  ]
}

# Market competition analysis
GET /analytics/competition?sector=construction&province=gauteng

{
  "market_overview": {
    "total_tenders": 89,
    "avg_bidders": 8.3,
    "competition_level": "high"
  },
  "success_rates": {
    "your_rate": 18.5,
    "market_average": 12.1,
    "top_quartile": 25.0
  },
  "winning_companies": [
    {"name": "XYZ Construction", "wins": 12, "success_rate": 24.0},
    {"name": "ABC Builders", "wins": 8, "success_rate": 20.0}
  ]
}
```

### Report Generation
Generate and download reports:

```bash
# Generate custom report
POST /reports/generate
{
  "type": "monthly_summary",
  "period": {
    "start": "2025-07-01",
    "end": "2025-07-31"
  },
  "sections": [
    "tender_activity",
    "readiness_scores",
    "team_performance",
    "market_insights"
  ],
  "format": "pdf",
  "delivery": {
    "email": "manager@abcconstruction.co.za",
    "callback_url": "https://your-app.com/webhook/report-ready"
  }
}

# Check report status
GET /reports/{report_id}/status

# Download completed report
GET /reports/{report_id}/download
```

### Automated Alerts
Set up intelligent notifications:

```bash
# Create alert rule
POST /alerts/rules
{
  "name": "High-value road construction",
  "conditions": {
    "keywords": ["road construction", "highway"],
    "budget_min": 10000000,
    "readiness_score_min": 70,
    "provinces": ["gauteng", "western_cape"]
  },
  "actions": {
    "email": true,
    "webhook": "https://your-app.com/webhook/new-tender",
    "auto_save": true
  }
}

# Get triggered alerts
GET /alerts/history?days=7
```

---

## Webhooks

### Setting Up Webhooks
Configure webhooks to receive real-time notifications:

```bash
# Register webhook endpoint
POST /webhooks
{
  "url": "https://your-app.com/webhook/tender-insights",
  "events": [
    "tender.new",
    "tender.updated", 
    "analysis.completed",
    "score.updated"
  ],
  "secret": "your-webhook-secret"
}
```

### Webhook Events
**Available Events:**
- `tender.new`: New tender matching your criteria
- `tender.updated`: Changes to saved tenders
- `analysis.completed`: Document analysis finished
- `score.updated`: Readiness score recalculated
- `deadline.approaching`: Tender deadline within threshold

**Example Payload:**
```json
{
  "event": "tender.new",
  "timestamp": "2025-08-01T15:30:00Z",
  "data": {
    "tender_id": "TND-2025-001234",
    "title": "Highway Maintenance Contract",
    "readiness_score": 82,
    "closing_date": "2025-08-25T17:00:00Z",
    "match_reasons": [
      "Keywords: highway, maintenance",
      "Location: Gauteng (preferred)",
      "Budget: Within your typical range"
    ]
  }
}
```

### Webhook Verification
Verify webhook authenticity using HMAC:

```python
import hmac
import hashlib

def verify_webhook(payload, signature, secret):
    expected = hmac.new(
        secret.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(f"sha256={expected}", signature)

# Usage
is_valid = verify_webhook(
    payload=request.body,
    signature=request.headers['X-Signature'],
    secret="your-webhook-secret"
)
```

---

## Error Handling

### HTTP Status Codes
- `200` - Success
- `201` - Created successfully
- `400` - Bad request (validation error)
- `401` - Unauthorized (invalid API key)
- `403` - Forbidden (insufficient permissions)
- `404` - Resource not found
- `429` - Rate limit exceeded
- `500` - Internal server error

### Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": [
      {
        "field": "budget_min",
        "message": "Must be a positive integer"
      }
    ],
    "request_id": "req_abc123",
    "timestamp": "2025-08-01T15:30:00Z"
  }
}
```

### Common Error Codes
- `INVALID_API_KEY`: API key is invalid or expired
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `VALIDATION_ERROR`: Request parameters are invalid
- `RESOURCE_NOT_FOUND`: Requested resource doesn't exist
- `INSUFFICIENT_PERMISSIONS`: API key lacks required permissions
- `PROCESSING_ERROR`: Document analysis failed
- `QUOTA_EXCEEDED`: Plan limits reached

### Retry Logic Example
```python
import requests
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_session_with_retries():
    session = requests.Session()
    
    retry_strategy = Retry(
        total=3,
        status_forcelist=[429, 500, 502, 503, 504],
        backoff_factor=1,
        respect_retry_after_header=True
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session

# Usage
session = create_session_with_retries()
response = session.get(
    "https://api.tenderinsighthub.co.za/v1/tenders/search",
    headers={"Authorization": "Bearer YOUR_API_KEY"},
    timeout=30
)
```

---

## SDK Examples

### Python SDK
```python
from tender_insight import TenderInsightClient

# Initialize client
client = TenderInsightClient(api_key="YOUR_API_KEY")

# Search for tenders
tenders = client.search_tenders(
    query="construction",
    filters={
        "province": "gauteng",
        "budget_min": 1000000
    },
    include_scores=True
)

# Analyze document
analysis = client.analyze_document(
    file_path="tender_spec.pdf",
    tender_id="TND-2025-001234"
)

# Update company profile
client.update_profile({
    "services": ["Road construction", "Bridge building"],
    "certifications": [
        {
            "name": "CIDB Grade 7",
            "expiry_date": "2026-01-15"
        }
    ]
})

# Save tender to workspace
client.save_tender(
    tender_id="TND-2025-001234",
    status="interested",
    notes="Good match for our experience"
)
```

### JavaScript/Node.js SDK
```javascript
const TenderInsight = require('@tender-insight/sdk');

const client = new TenderInsight({
  apiKey: 'YOUR_API_KEY',
  baseUrl: 'https://api.tenderinsighthub.co.za/v1'
});

// Search tenders
const tenders = await client.tenders.search({
  query: 'construction',
  filters: {
    province: 'gauteng',
    budgetMin: 1000000
  }
});

// Analyze document
const analysis = await client.documents.analyze({
  file: fs.createReadStream('tender_spec.pdf'),
  tenderId: 'TND-2025-001234'
});

// Workspace operations
await client.workspace.saveTender({
  tenderId: 'TND-2025-001234',
  status: 'interested',
  priority: 'high'
});
```

### cURL Examples
```bash
# Search with multiple filters
curl -G "https://api.tenderinsighthub.co.za/v1/tenders/search" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d "q=road construction" \
  -d "province=gauteng" \
  -d "budget_min=5000000" \
  -d "deadline_days=30"

# Upload document for analysis
curl -X POST "https://api.tenderinsighthub.co.za/v1/documents/analyze" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "document=@tender_spec.pdf" \
  -F "tender_id=TND-2025-001234" \
  -F "generate_summary=true"

# Update tender status
curl -X PATCH "https://api.tenderinsighthub.co.za/v1/workspace/tenders/TND-2025-001234" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "submitted",
    "notes": "Bid submitted successfully",
    "bid_amount": 24500000
  }'
```

---

## Best Practices

### API Usage Optimization
1. **Batch Operations**: Use batch endpoints when processing multiple items
2. **Caching**: Cache frequently accessed data like company profiles
3. **Pagination**: Always handle pagination for large result sets
4. **Compression**: Enable gzip compression for large responses
5. **Async Processing**: Use webhooks for long-running operations

### Security Best Practices
1. **API Key Management**: Store keys securely, rotate regularly
2. **HTTPS Only**: Always use HTTPS endpoints
3. **Input Validation**: Validate all input parameters
4. **Rate Limiting**: Implement client-side rate limiting
5. **Error Handling**: Don't expose sensitive information in errors

### Performance Tips
1. **Request Optimization**: Only request needed fields using field selectors
2. **Concurrent Requests**: Use appropriate concurrency limits
3. **Timeout Handling**: Set reasonable timeouts for all requests
4. **Connection Pooling**: Reuse HTTP connections when possible
5. **Monitoring**: Track API usage and performance metrics

---

## Support and Resources

### Getting Help
- **Documentation**: https://docs.tenderinsighthub.co.za
- **API Status**: https://status.tenderinsighthub.co.za
- **Developer Support**: api-support@tenderinsighthub.co.za
- **Community Forum**: https://community.tenderinsighthub.co.za

### Tools and Resources
- **API Explorer**: Interactive API testing tool
- **Postman Collection**: Pre-built API requests
- **SDK Documentation**: Language-specific guides
- **Code Examples**: GitHub repository with samples

### Changelog and Updates
- **Release Notes**: Track API changes and new features
- **Breaking Changes**: Advance notice of breaking changes
- **Deprecation Policy**: 6-month notice for deprecated endpoints
- **Migration Guides**: Step-by-step upgrade instructions

---

*This API guide is updated regularly. For the latest version and additional examples, visit our developer documentation at https://docs.tenderinsighthub.co.za*

**Document Version**: 1.0  
**API Version**: v1  
**Last Updated**: August 2025